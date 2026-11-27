# bachatamusicalidad.com (bachata-trainer)

## What this is

The operator's **personal** project: a free bachata musicality trainer (Derecho / Majao / Mambo grooves
synthesized with Web Audio, an ear-training game, a 4-week plan, a rhythm reference), a Steps & Styles page, and
nine articles written from his learning journal. Single-file static site, no dependencies. It stays free: no
ads, accounts, paywalls or monetization (operator, 2026-10-01). Only the constitution's red lines and autonomy
rules apply here, not the portfolio's goals or metrics. Not part of the tool-site AEO playbook. Nothing depends
on it.

## Commands

- No build, no tests, no package.json. Preview: open `index.html`, or `npx serve .` (sound needs one tap first).
- Articles: edit `articles/src/content.py`, then `python3 articles/src/build.py articles` (writes
  `articles/*.html` and `articles/index.html`; the slug order is the `ORDER` list in `build.py`).

## Deploy and verify

- Repo `gaomengen/bachata-trainer` (public), branch **`master`**. Vercel project `bachata-trainer` (team
  remotefront, id `prj_QiXor…`; the local `.vercel/project.json` still says its old name `bachata-app`).
- **Pushing does not deploy**: the Vercel project has no git link (2026-11-27), and every deploy so far was the
  operator running `vercel --prod`. Claude may not run that (red line), so a site change ends at a local commit
  and the operator deploys, or connects the repo to Vercel. **[check]** which he wants.
- Verify: `curl -s https://bachatamusicalidad.com/<path>` or open it in a browser; last production deploy
  2026-10-25.

## Map

- `index.html` (~1,500 lines): the whole trainer app, including optional Spotify playback.
- `steps.html`: Steps & Styles. `articles/`: generated pages + `article.css`; `articles/src/`: sources + builder.
- `journal/JOURNAL.md`, `KNOWLEDGE.md`, `VOCABULARY.md`: the learning journal (in git, excluded from the site).
- `LABELING.md` (how to label a song's sections), `SPOTIFY.md` (Spotify integration reference), `DEPLOY.md`
  (original setup notes; its `vercel --prod` path is not for Claude).
- `vercel.json`: `cleanUrls`, and a `www` → apex redirect rule.

## Data and secrets

- No database, no server code, no secrets. Spotify uses PKCE with a client ID the visitor pastes in the app
  (no client secret); the redirect URI is the page's own origin + path and must be registered verbatim.

## Rules for this repo

- `journal/` and `articles/src/` stay out of the deployed site (`.vercelignore`). The journal is public on
  GitHub by the operator's choice (2026-10-07).
- Journal entries: voice-transcribed input; clean up the wording, keep the meaning, invent nothing. Dated entry at
  the top of `JOURNAL.md`; file each lesson into `KNOWLEDGE.md` rather than duplicating.
- Articles: the operator's first-person learner voice, plain, no em dashes; other people stay anonymous.
- Pushing journal entries was standing practice in memory (2026-10-07), but a push still needs the operator's
  yes under the constitution unless he records a decision for it **[check]**.

## Gotchas

- Browsers block audio until a user gesture; the app asks for a tap first.
- Spotify: Premium needed for full tracks; `localhost` is rejected as a redirect URI (use `127.0.0.1`);
  unapproved developer apps are capped at 5 allowlisted users (`SPOTIFY.md`).
- 2026-11-27: `https://www.bachatamusicalidad.com/` answered 200 from cache rather than redirecting to the apex
  **[check]**; pages carry an apex canonical.

## Pointers

- Memory: `~/.claude/projects/-Users-mengengao-code-bachata-trainer/memory/` (journal workflow, style
  preferences, the LA dance month).
