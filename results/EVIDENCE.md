# Pilot evidence

Feasibility samples only. Human validation is pending.

Each source link resolves a README at a recorded commit. IDs match the blank review sheets.

## R01: ZephonMakale/Zeph-Insty (2021-01)

A web application that clones Instagram functionality, displaying posts and user profiles. Built as a Django app intended for deployment on Heroku.

[Historical README](https://github.com/ZephonMakale/Zeph-Insty/blob/6138c5cc2944065967587bf8ae718f5a53f3004e/README.md) · commit `6138c5cc2944065967587bf8ae718f5a53f3004e`

Created: 2021-01-15T12:13:55Z; cutoff: 2021-02-14T12:13:55Z; commit timestamp: 2021-01-20T06:53:43Z.

Supporting model-input quotes:

> displays posts and profiles of different users

> Instagram Clone

Request SHA256: `d1e5a655ac0c36d3355d076954360fec1f11b7222ca2a4c3b77d19ed55ede351`. README SHA256: `7a27d7eef20bf5b635c5d1c955bb69a689b5194eb840865100b1d46ab6ba0d0c`.

**AI source-audit note (not human validation): supported.** Purpose, posts/profiles, Django and Heroku are explicit in the README. Incidental deployment detail remains despite the prompt preference.

## R02: gache-ru/Instagram-clone (2021-01)

A social photo-sharing web application where users sign up, upload images, view other users' pictures, like and comment on posts, follow other users, edit their profile with a bio and picture, and log in/out.

[Historical README](https://github.com/gache-ru/Instagram-clone/blob/4e44514f697f0627863ccfce339f9bf795dd1da0/README.md) · commit `4e44514f697f0627863ccfce339f9bf795dd1da0`

Created: 2021-01-15T12:29:06Z; cutoff: 2021-02-14T12:29:06Z; commit timestamp: 2021-01-20T11:33:48Z.

Supporting model-input quotes:

> users to sign up, upload images,view other user's pictures,like them, comment on them and also follow the other users

> On the account link, click on the  update profile

> Click on the comment and like icon and add a comment and like

Request SHA256: `2fcbc9f99e75bc046efb81ef879817bdd3b4ff1faec78dd0b86dd778fcc086cd`. README SHA256: `a68cccd9c8aa7d4ee6370cc003992856469d92f0fdfe68e61b23432f78ad77cb`.

**AI source-audit note (not human validation): supported.** Photo upload, browsing, likes, comments, follows, profile edits and login/logout are explicit in the description and behavior table.

## R03: nicklasfrahm/distributed-charging (2021-01)

A proof-of-concept distributed charging infrastructure consisting of station and manager components communicating via an MQTT broker.

[Historical README](https://github.com/nicklasfrahm/distributed-charging/blob/39990abd88f1b09736f8f7315a3dae9b346aeaa6/README.md) · commit `39990abd88f1b09736f8f7315a3dae9b346aeaa6`

Created: 2021-01-15T12:55:06Z; cutoff: 2021-02-14T12:55:06Z; commit timestamp: 2021-01-16T13:18:31Z.

Supporting model-input quotes:

> A proof of concept for a distributed charging infrastructure.

> The application consists of three components:

Request SHA256: `26c3001a038ba9551ae33d6afe9346cab106b1925b57acfd7f1a000fe6bb6b88`. README SHA256: `d19c03094507764ee1290e2ee387ac8a73b0648f62100b695bf577d736ca3415`.

**AI source-audit note (not human validation): supported.** Distributed charging, station/manager components and an MQTT broker are explicit in the architecture section.

## R04: ebhardjan/MacOSKeyLayouts (2021-01)

Provides Mac OS keyboard layout files (.keylayout) implementing the PC ISO Swiss German layout, so users can type with that layout on macOS. Includes an install script to add them system-wide via System Preferences.

[Historical README](https://github.com/ebhardjan/MacOSKeyLayouts/blob/a565366903df03d6b44fb4df855a3b67c397c42c/README.md) · commit `a565366903df03d6b44fb4df855a3b67c397c42c`

Created: 2021-01-15T12:01:13Z; cutoff: 2021-02-14T12:01:13Z; commit timestamp: 2021-01-15T12:31:16Z.

Supporting model-input quotes:

> Mac OS .keylayout files for PC ISO Swiss German

> sudo ./install.sh

Request SHA256: `e2657714a0e54edc840fd7aaf39a90eba9cff826bf9a8ebb41486d9c3519958a`. README SHA256: `d6de89991e0a7a7830fdb07a9dd7fe996d5b51d35da7ebbc45d9214c1caa0298`.

**AI source-audit note (not human validation): supported.** PC ISO Swiss German key layouts and the install procedure are explicit. Filter review needed: this may be configuration rather than software under the planned exclusion rule.

## R05: jacobbaek/grafana-backup-cli (2021-01)

A CLI tool that backs up Grafana dashboards by collecting their JSON files via the Grafana API and committing/pushing them to a Git server, so dashboard definitions are version-controlled.

[Historical README](https://github.com/jacobbaek/grafana-backup-cli/blob/52c61288714ac120c3a319185f9ba99c25dd81c5/README.md) · commit `52c61288714ac120c3a319185f9ba99c25dd81c5`

Created: 2021-01-15T12:10:06Z; cutoff: 2021-02-14T12:10:06Z; commit timestamp: 2021-01-16T08:47:07Z.

Supporting model-input quotes:

> collect dashboard json files from grafana using API

> commit and push with specific message into git server

Request SHA256: `453d2f471957dc22c82a3ab75f9c0deb9147b8b52d5dd38dccba0b5403c3dfc5`. README SHA256: `85c7081c952f363e386e2f598e579110519901cad5b23f098df04929b133f305`.

**AI source-audit note (not human validation): supported.** Dashboard JSON collection, Grafana API use and git commit/push are explicit; the Go component is marked WIP.

## R06: diegoesqui/csv_processor (2023-01)

A tool that merges multiple CSV files exported from Boursorama Wicount360 into a single CSV and Excel file, with optional automatic item replacements defined in a replacements.xlsx file.

[Historical README](https://github.com/diegoesqui/csv_processor/blob/f748b771ba4bfdb5a4906e80955d170249c1edd7/README.md) · commit `f748b771ba4bfdb5a4906e80955d170249c1edd7`

Created: 2023-01-15T12:08:24Z; cutoff: 2023-02-14T12:08:24Z; commit timestamp: 2023-01-15T17:58:17Z.

Supporting model-input quotes:

> merge multiple csv files extracted from Boursorama Wicount360 into a single CSV and Excel file

> Use the replacements.xlsx file to create rules to replace some items automatically.

Request SHA256: `0d1d7113c24247665c312d5a1518706635706e911324f74cadf046344236f562`. README SHA256: `e9f8cf650c0fd2e73209689ac0229df90f90ab6c373b5988c3d4eb81f3c5c2ad`.

**AI source-audit note (not human validation): supported.** CSV/Excel merging and replacement rules are explicit in the short README.

## R07: AdamBurgess38/Simple-To-Do-List (2023-01)

A simple to-do list application consisting of a Go backend server and a web front-end client. The README provides commands to run both components but does not describe further functionality or intended users.

[Historical README](https://github.com/AdamBurgess38/Simple-To-Do-List/blob/31b4d0e58b0adb3487beb5f77d9029fb9ea05a91/README.md) · commit `31b4d0e58b0adb3487beb5f77d9029fb9ea05a91`

Created: 2023-01-15T12:16:33Z; cutoff: 2023-02-14T12:16:33Z; commit timestamp: 2023-01-15T12:21:54Z.

Supporting model-input quotes:

> Simple-To-Do-List

> To run golang server

> To run the front end

Request SHA256: `56a7f3e62534fd11312c7b9af8f232cc486c4030d97417f20316e7e745ea4d38`. README SHA256: `5fa8e893a0085f1f197a2ea24d8da401ed37862476912ee405dd8c080ea6fabf`.

**AI source-audit note (not human validation): supported.** The title identifies a to-do list; the run instructions identify Go server and client. Summary correctly acknowledges limited functional evidence.

## R08: sakindia123/typescript-redux-weather-app (2023-01)

A weather application built with React, TypeScript, and react-redux. The README provides run instructions but does not describe specific features beyond being a weather app.

[Historical README](https://github.com/sakindia123/typescript-redux-weather-app/blob/b777d8d7c74c685ec15af68cd42a8fd0e2b64141/README.md) · commit `b777d8d7c74c685ec15af68cd42a8fd0e2b64141`

Created: 2023-01-15T12:11:01Z; cutoff: 2023-02-14T12:11:01Z; commit timestamp: 2023-01-15T12:13:22Z.

Supporting model-input quotes:

> This is a weather application written with React and Typescript using react-redux.

Request SHA256: `53510a350913712399ca804489d02612b36314764830207241d5089684c5acf2`. README SHA256: `f73d5b11827be09e59c1e1f132a1b5b10146ed6b41c3dc9af5935d0ac3deb80e`.

**AI source-audit note (not human validation): supported.** The README explicitly identifies a weather application and its frameworks. Summary correctly acknowledges limited feature detail.

## R09: ARYAN6307/Simple-Calculator-C- (2023-01)

A simple command-line calculator that reads two numeric values and an operator (*, /, +, -, ^) and performs the corresponding calculation using a switch statement.

[Historical README](https://github.com/ARYAN6307/Simple-Calculator-C-/blob/3b853208b26674d149776946e8ef47f088183b5b/README.md) · commit `3b853208b26674d149776946e8ef47f088183b5b`

Created: 2023-01-15T12:48:14Z; cutoff: 2023-02-14T12:48:14Z; commit timestamp: 2023-01-15T13:02:06Z.

Supporting model-input quotes:

> valueOne, valueTwo and the operator (choice of *,/,+,-,^)

> A switch statement is then used in order to run the right calculation for the given operator

Request SHA256: `5a144f760b06fe5a23a7fbad3e38e3cba078b936d95094a38f95d40e885482d2`. README SHA256: `f5a77e5b3eb13ccb742fceba8ef7e1ace2a9fea0f5a753fb97c3bdcab7b55e7f`.

**AI source-audit note (not human validation): uncertain.** The numerical inputs/operators and switch behavior are explicit. The command-line platform is inferred from scanf rather than stated directly.

## R10: Eslam030/Login-Application (2023-01)

A desktop login application built with the Qt framework that lets users register and log in, storing account data in files. After logging in, users can edit their saved information synchronously and change passwords, with prevention of reusing old passwords.

[Historical README](https://github.com/Eslam030/Login-Application/blob/22f8a9ad56a62b6c0863e3ff274b2b29b18bee2c/README.md) · commit `22f8a9ad56a62b6c0863e3ff274b2b29b18bee2c`

Created: 2023-01-15T12:47:37Z; cutoff: 2023-02-14T12:47:37Z; commit timestamp: 2023-01-15T13:09:09Z.

Supporting model-input quotes:

> It make a login and register and works very simple and good

> When logged in You have a text box You can change info and it is save synchronously

> You can change your password and you can't use one of the old passwords of yours on the database

Request SHA256: `247eeecad63300a6df84454eb54c2d658b63a48294d8573af568e5f2b2f1f7a4`. README SHA256: `2d1271d2ea3c79ec22c28eeafc134ced4932e61a10fb69519bded706c9db31da`.

**AI source-audit note (not human validation): uncertain.** Login, registration, file storage, edits and password history are explicit. The desktop platform is inferred from Qt and UI description.

## R11: mohamedfawas/rmshop (2025-01)

An e-commerce system built as microservices, comprising an admin service, an auth service handling authentication and JWT, a user service, and an API gateway exposing REST endpoints for all services.

[Historical README](https://github.com/mohamedfawas/rmshop/blob/08c18bafdff48c8f3ec999564755c29ff224f016/readme.md) · commit `08c18bafdff48c8f3ec999564755c29ff224f016`

Created: 2025-01-15T12:45:50Z; cutoff: 2025-02-14T12:45:50Z; commit timestamp: 2025-01-17T10:37:38Z.

Supporting model-input quotes:

> A microservices-based e-commerce project

> Auth Service: Manages authentication and JWT

> API Gateway: REST API gateway for all services

Request SHA256: `c59a3ec7b3fcee71a055ad146b65448a8179fe52c56c66634f53526c3250813e`. README SHA256: `a9970f0cd7cdccff1c51689056cf4e34dabe49f909b4c3ad164b8e44a4784b14`.

**AI source-audit note (not human validation): supported.** E-commerce purpose, four services, JWT authentication and REST gateway are explicit.

## R12: mrnmsfrog/eliza (2025-01)

Eliza is a framework for building AI agents that connect to platforms like Discord, Twitter, and Telegram, support multiple models, manage retrievable memory and documents, and let users create custom actions and clients for chatbots, autonomous agents, and other use cases.

[Historical README](https://github.com/mrnmsfrog/eliza/blob/66931af0699193da97f9c0e2e049a0b5a26c6cbb/README.md) · commit `66931af0699193da97f9c0e2e049a0b5a26c6cbb`

Created: 2025-01-15T12:04:14Z; cutoff: 2025-02-14T12:04:14Z; commit timestamp: 2025-01-15T12:10:56Z.

Supporting model-input quotes:

> 🔗 Support for every model (Llama, Grok, OpenAI, Anthropic, Gemini, etc.)

> 📚 Easily ingest and interact with your documents

> 🚀 Highly extensible - create your own actions and clients

Request SHA256: `3281f572df6abe6ae823b63649a948543baf680238921e8b419c21e499ca434b`. README SHA256: `ad66102d35caa7ac9a56da80fd999f52cf2672cd9053dc20ff68b2c560a1b43c`.

**AI source-audit note (not human validation): supported.** Connectors, models, documents, memory, custom actions and use cases are explicit. Filter review needed: an API non-fork can still copy an upstream project; independent project choice is unverified.

## R13: fauzymadani/Nordic-StartPage (2025-01)

A Nordic-themed custom start page for web browsers, used via third-party new-tab extensions. It offers a simple, elegant startpage design as an unofficial port of the Nordic theme.

[Historical README](https://github.com/fauzymadani/Nordic-StartPage/blob/f50c76468ec0ffe4d66ac7ff6c2ac35fa48b210a/README.md) · commit `f50c76468ec0ffe4d66ac7ff6c2ac35fa48b210a`

Created: 2025-01-15T12:58:43Z; cutoff: 2025-02-14T12:58:43Z; commit timestamp: 2025-01-15T13:05:35Z.

Supporting model-input quotes:

> another unofficial nordic theme port for startpage for any web browser

> use with with third party extension for custom startpage newtab

Request SHA256: `f861a2df7a10d011b899b5a86fb223e32040f705d36b21bc6e5179d2d524d3e6`. README SHA256: `78e29e479735d80aa48c7b5a0b14282738df846af4386776bb4f26e93b0d857f`.

**AI source-audit note (not human validation): supported.** The Nordic theme, browser start page, third-party new-tab extension use and simple design are explicit.

## R14: Luke-Nicklin/rpsls (2025-01)

A web game where users play rock, paper, scissors, lizard, spock against the computer. It shows each player's move with images, displays the result, keeps a running scoreboard of wins, losses and ties, and explains the rules.

[Historical README](https://github.com/Luke-Nicklin/rpsls/blob/9caa1373d667add96495ee9c4b7e8a1aa98c906d/README.md) · commit `9caa1373d667add96495ee9c4b7e8a1aa98c906d`

Created: 2025-01-15T12:52:52Z; cutoff: 2025-02-14T12:52:52Z; commit timestamp: 2025-02-01T12:08:50Z.

Supporting model-input quotes:

> The site's primary users are those looking to enjoy a quick game at the click of a button.

> A running scoreboard showing number of wins, losses and ties

> The rules section shows the winning scenarios for each move.

Request SHA256: `867ed893f63d4ebfef71d62a1a615aa8c22db55078991cadaf8b859065a383e7`. README SHA256: `47b543ee17ade6fc21d9e90346437bf89587443d3c2422c801ddfb82a2657c39`.

**AI source-audit note (not human validation): supported.** Game purpose, choices, images, scoreboard, outcomes and rules are explicit in the feature descriptions.

## R15: aryxntyagi/project-login-database-php-main (2025-01)

A basic web application providing user authentication: registration, login, and logout, backed by a MySQL database via PHP. Users register or log in, are redirected to a homepage with a welcome message and logout button, and sessions are destroyed on logout.

[Historical README](https://github.com/aryxntyagi/project-login-database-php-main/blob/9877d7da8d489fe61226bfb920fcaa9a90a463ce/README.md) · commit `9877d7da8d489fe61226bfb920fcaa9a90a463ce`

Created: 2025-01-15T12:19:08Z; cutoff: 2025-02-14T12:19:08Z; commit timestamp: 2025-01-15T12:19:11Z.

Supporting model-input quotes:

> provides user authentication functionalities such as login, registration, and logout

> Interacts with the database to store new user information securely

> Destroys the user session and redirects them to the login page

Request SHA256: `2f8ffb0a00da10388660064350be2e5ed06ac4be84d74c2d8f2e093b7c00a1f1`. README SHA256: `afc630ba7b401f4322d9f2e587c5aac4acbe8eea724fff2152d92462b7f90bec`.

**AI source-audit note (not human validation): supported.** Registration/login/logout, PHP/MySQL, homepage welcome and session destruction are explicit in the file/usage descriptions.
