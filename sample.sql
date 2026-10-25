-- BigQuery Standard SQL. PREPARATION ONLY: this query has not been executed.
-- Select a single monthly table and supply @seed (STRING), @candidate_limit (INT64).
-- Run a dry run first and set maximum_bytes_billed in the job configuration.
-- Export the ordered candidates; take the next candidate after every rejection.
WITH creations AS (
  SELECT
    repo.id AS repository_id,
    ARRAY_AGG(STRUCT(repo.name AS name, id AS event_id, created_at)
              ORDER BY created_at, id LIMIT 1)[OFFSET(0)] AS first_event
  FROM `githubarchive.month.202101`
  WHERE type = 'CreateEvent'
    AND JSON_VALUE(payload, '$.ref_type') = 'repository'
  GROUP BY repository_id
)
SELECT repository_id, first_event.*,
       TO_HEX(SHA256(CONCAT(@seed, ':', CAST(repository_id AS STRING)))) AS sample_key
FROM creations
ORDER BY sample_key, repository_id
LIMIT @candidate_limit;
