"""Collect 200 unfiltered repository IDs per month; no clones or model calls."""

import argparse
import calendar
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
import csv
from datetime import datetime, timedelta, timezone
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import random
import sqlite3
import subprocess
import time

import requests

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
SEED = "eecs448-archive-v2"
MONTHS = [f"{year}-{month:02}" for year in range(2021, 2026) for month in range(1, 13)]


class StopRun(Exception):
    """Stop without changing the sample or silently skipping failed requests."""


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def sample_hours(month):
    year, number = map(int, month.split("-"))
    rng = random.Random(SEED + month)
    offset = rng.randrange(calendar.monthrange(year, number)[1] * 24)
    start = datetime(year, number, 1, tzinfo=timezone.utc)
    return [(start + timedelta(hours=offset)).strftime("%Y-%m-%d-%H")]


def connect():
    DATA.mkdir(exist_ok=True)
    db = sqlite3.connect(DATA / "collection.sqlite")
    db.row_factory = sqlite3.Row
    # Existing decision and cost-ledger columns are preserved, but never used to select IDs.
    db.executescript("""
        CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS hours (hour TEXT PRIMARY KEY, month TEXT, events INTEGER, creations INTEGER);
        CREATE TABLE IF NOT EXISTS repos (
            id INTEGER PRIMARY KEY, name TEXT, month TEXT, created TEXT, hour TEXT, rank TEXT,
            status TEXT DEFAULT 'pending', reason TEXT, commit_sha TEXT, readme_sha TEXT,
            label TEXT, quote TEXT, explanation TEXT);
        CREATE TABLE IF NOT EXISTS api_windows (start TEXT PRIMARY KEY, month TEXT);
    """)
    old = db.execute("SELECT value FROM settings WHERE key='seed'").fetchone()
    if old and old[0] != SEED:
        raise StopRun("Saved sampling seed differs")
    with db:
        db.execute("INSERT OR IGNORE INTO settings VALUES ('seed',?)", (SEED,))
    return db


@contextmanager
def run_lock():
    DATA.mkdir(exist_ok=True)
    with (DATA / ".lock").open("a+b") as handle:
        handle.seek(0)
        handle.write(b"0")
        handle.flush()
        handle.seek(0)
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield


def github_token():
    env = dict(os.environ)
    if (ROOT / ".env").exists():
        for line in (ROOT / ".env").read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                key, value = line.split("=", 1)
                env.setdefault(key.strip(), value.strip().strip("\"'"))
    token = env.get("GITHUB_TOKEN") or env.get("GH_TOKEN")
    if not token:
        command = ["wsl.exe", "bash", "-lc", "gh auth token"] if os.name == "nt" else ["gh", "auth", "token"]
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            token = result.stdout.strip()
    if not token:
        raise StopRun("Set GITHUB_TOKEN or sign into gh")
    return token


def read_archive(hour):
    rows = {}
    events = creations = 0
    date, clock_hour = hour.rsplit("-", 1)
    with requests.get(f"https://data.gharchive.org/{date}-{int(clock_hour)}.json.gz", timeout=(15, 90)) as response:
        if response.status_code == 404:
            return hour, None, None, []
        response.raise_for_status()
        with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as stream:
            for line in stream:
                events += 1
                if b'"CreateEvent"' not in line:
                    continue
                event = json.loads(line)
                if event["type"] != "CreateEvent" or event.get("payload", {}).get("ref_type") != "repository":
                    continue
                creations += 1
                repo = event["repo"]
                rid = repo["id"]
                created = event["created_at"]
                row = (rid, repo["name"], hour[:7], created, hour, digest(SEED + ":" + str(rid)))
                if rid not in rows or created < rows[rid][3]:
                    rows[rid] = row
    return hour, events, creations, list(rows.values())


def archive_hour(hour):
    for attempt in range(3):
        try:
            return read_archive(hour)
        except (requests.RequestException, EOFError):
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


def save_rows(db, rows):
    db.executemany("INSERT OR IGNORE INTO repos(id,name,month,created,hour,rank) VALUES (?,?,?,?,?,?)", rows)


def discover(db, workers):
    completed = {row[0] for row in db.execute("SELECT hour FROM hours")}
    jobs = [sample_hours(month)[0] for month in MONTHS if sample_hours(month)[0] not in completed]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        tasks = [pool.submit(archive_hour, hour) for hour in jobs]
        for task in as_completed(tasks):
            hour, events, creations, rows = task.result()
            with db:
                save_rows(db, rows)
                db.execute("INSERT INTO hours VALUES (?,?,?,?)", (hour, hour[:7], events, creations))
            print(f"{hour}: {len(rows)} IDs", flush=True)


def minute_windows(month):
    year, number = map(int, month.split("-"))
    start = datetime(year, number, 1, tzinfo=timezone.utc)
    offsets = list(range(calendar.monthrange(year, number)[1] * 24 * 60))
    random.Random(SEED + month + ":minutes").shuffle(offsets)
    for offset in offsets:
        yield start + timedelta(minutes=offset)


def search_window(start, end, token):
    """Fetch an entire small creation window; split before GitHub's 1,000-result cap."""
    headers = {"Authorization": "Bearer " + token, "Accept": "application/vnd.github+json"}
    query = f"created:{start:%Y-%m-%dT%H:%M:%SZ}..{end:%Y-%m-%dT%H:%M:%SZ} fork:true"
    rows = []
    page = 1
    while True:
        response = requests.get("https://api.github.com/search/repositories",
                                params={"q": query, "per_page": 100, "page": page, "sort": "updated", "order": "asc"},
                                headers=headers, timeout=40)
        if response.status_code in (403, 429):
            raise StopRun("GitHub quota reached; rerun to resume")
        response.raise_for_status()
        body = response.json()
        if body.get("incomplete_results"):
            raise StopRun("Incomplete GitHub response; no window saved")
        total = body["total_count"]
        if total > 1000:
            if end <= start:
                raise StopRun("Too many repositories in one second")
            middle = start + timedelta(seconds=int((end - start).total_seconds()) // 2)
            return search_window(start, middle, token) + search_window(middle + timedelta(seconds=1), end, token)
        for repo in body["items"]:
            created = datetime.fromisoformat(repo["created_at"].replace("Z", "+00:00"))
            if not start <= created <= end:
                raise StopRun("GitHub returned a creation time outside the requested window")
            rid = repo["id"]
            rows.append((rid, repo["full_name"], start.strftime("%Y-%m"), repo["created_at"], None, digest(SEED + ":" + str(rid))))
        if page * 100 >= total:
            if len({row[0] for row in rows}) != total:
                raise StopRun("Results changed while paging; no window saved")
            return rows
        page += 1


def complete_candidates(db, target, workers):
    token = None
    while True:
        counts = dict(db.execute("SELECT month,count(*) FROM repos GROUP BY month"))
        missing = [month for month in MONTHS if counts.get(month, 0) < target]
        if not missing:
            return
        if token is None:
            token = github_token()
        seen = {row[0] for row in db.execute("SELECT start FROM api_windows")}
        jobs = {}
        with ThreadPoolExecutor(max_workers=min(workers, 2)) as pool:
            for month in missing:
                start = next((x for x in minute_windows(month) if x.isoformat() not in seen), None)
                if start is None:
                    raise StopRun(f"No unexamined windows remain for {month}")
                jobs[pool.submit(search_window, start, start + timedelta(seconds=59), token)] = start
            for task in as_completed(jobs):
                start = jobs[task]
                rows = task.result()
                with db:
                    save_rows(db, rows)
                    db.execute("INSERT INTO api_windows VALUES (?,?)", (start.isoformat(), start.strftime("%Y-%m")))
                print(f"{start:%Y-%m}: added {len(rows)} IDs", flush=True)


def export(db, target):
    totals = []
    temporary = DATA / "repositories.csv.tmp"
    with temporary.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["month", "id", "name", "url"])
        for month in MONTHS:
            # No eligibility, availability, language, commit-count or model-label filter.
            rows = db.execute("SELECT id,name FROM repos WHERE month=? ORDER BY rank,id LIMIT ?", (month, target)).fetchall()
            writer.writerows((month, row["id"], row["name"], "https://github.com/" + row["name"]) for row in rows)
            pool = db.execute("SELECT count(*) FROM repos WHERE month=?", (month,)).fetchone()[0]
            totals.append((month, len(rows), target, pool))
    temporary.replace(DATA / "repositories.csv")
    temporary = DATA / "months.csv.tmp"
    with temporary.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["month", "collected", "target", "candidate_pool"])
        writer.writerows(totals)
    temporary.replace(DATA / "months.csv")
    print(json.dumps({"ids": sum(row[1] for row in totals), "complete_months": sum(row[1] == target for row in totals), "months": len(MONTHS)}), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["collect", "export"])
    parser.add_argument("--target", type=int, default=200)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if args.target < 1 or not 1 <= args.workers <= 8:
        parser.error("target must be positive; workers must be between 1 and 8")
    with run_lock():
        db = connect()
        try:
            if args.command == "collect":
                discover(db, args.workers)
                complete_candidates(db, args.target, args.workers)
        except (StopRun, requests.RequestException, EOFError) as error:
            print("Stopped:", error, flush=True)
            raise SystemExit(1)
        finally:
            export(db, args.target)
            db.close()


if __name__ == "__main__":
    main()
