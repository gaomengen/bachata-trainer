# journal/: the learning journal

## Purpose

The operator's bachata learning journal: what he learns in classes, at socials, from videos and in practice,
written up from voice notes. It is the raw material for the articles. It is public
on GitHub by his choice (2026-10-07) but is not part of the website: `.vercelignore` excludes `journal/`.

## Files

- `JOURNAL.md` (~700 lines): dated entries, newest at the top, each headed `## YYYY-MM-DD · Title`. Each entry
  has **Source** (class, social, YouTube, practice, conversation), **What I learned**, **Why it works**,
  **Try next**. The format is described at the top of the file.
- `KNOWLEDGE.md`: the organised master notes by topic (Leading & following, Body & technique, Steps &
  patterns, Practice & learning, Musicality, Bachata styles, Styling, Social dancing & floor craft, Teaching
  ideas, Open questions, Article ideas). Each point ends with the date of the entry it came from.
- `VOCABULARY.md`: every move he knows, by name, with a one-line cue and a status (from "with video" up to
  "social-ready", defined at the top of the file), grouped by style (sensual, Dominican / traditional).

## Rules

- Input is voice-transcribed. Clean up the wording, keep the meaning, invent nothing.
- A new entry goes at the top of `JOURNAL.md`, under the format header, with today's date.
- File each lesson into `KNOWLEDGE.md` under the right topic, with the entry date. When something refines or
  contradicts an existing point, update that point instead of adding a duplicate.
- A new move goes into `VOCABULARY.md`; a status change edits the existing line.
- Unresolved questions go under "Open questions" and lessons worth writing up under "Article ideas" in
  `KNOWLEDGE.md`, each with its date. What to do with an answered question is not written down **[check]**.
- Other people (teachers, partners, dancers at socials) stay anonymous.
- Plain language, no em dashes (none in these files on 2026-11-27), matching the existing entries.

## Gotchas

- Journal edits are content commits: the repo is public, so anything written here is published on GitHub as
  soon as it is pushed.
- Several entries can share a date (2026-10-21 has two). Keep them as separate headings, newest on top.
- Articles are not generated from these files; they are written by hand into `articles/src/content.py`.

## Tests

None. Check that the new entry renders as expected in a Markdown preview and that every `KNOWLEDGE.md`
addition carries a date that exists in `JOURNAL.md`.
