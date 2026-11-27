# articles/: the article pages and their builder

## Purpose

The `/articles` section of the site: nine first-person articles written from the learning journal, plus an
index page. The HTML here is generated; the source of truth is `articles/src/content.py`, turned into pages by
`articles/src/build.py`. `articles/src/` is not deployed (`.vercelignore`), so only the built HTML and
`article.css` reach the site.

## Files

- `src/content.py`: `ARTICLES`, a list of dicts with `slug`, `title`, `dek` (one-line summary, also the meta
  description), `date` (ISO), `tag` (kicker such as "Technique" or "Leading") and `body` (raw HTML: `<p>`,
  `<h2>`, `<ol>`, `<strong>`).
- `src/build.py`: writes `<slug>.html` for each article and `index.html`. `ORDER` sets the reading order on the
  index and the two "Keep reading" links (the next two in `ORDER`, wrapping round). Title, dek and tag are
  HTML-escaped; `body` is inserted as is.
- `<slug>.html` (9) and `index.html`: generated output, committed.
- `article.css`: the stylesheet for all article pages (`/articles/article.css`).

## Rules

- Edit `src/content.py`, never the generated HTML; then rebuild from the repo root:
  `python3 articles/src/build.py articles`. A rebuild of unchanged content reproduces the committed files
  byte for byte (checked 2026-11-27), so any diff is your change.
- A new article needs a dict in `ARTICLES` and its slug in `ORDER`. A slug missing from either makes the build
  fail (`KeyError` or the length `assert`).
- Voice: the operator's first person, as a learner rather than a teacher; plain words; no em dashes (none in
  `content.py` on 2026-11-27); other people stay anonymous. Content comes from the journal; invent nothing.
- Article ideas are collected under "Article ideas" in `journal/KNOWLEDGE.md`.
- The site stays free: no ads, sign-ups or affiliate links in articles.

## Gotchas

- `src/__pycache__/content.cpython-38.pyc` is committed. Running the build with Python 3.8 rewrites it and
  dirties the tree; use `PYTHONDONTWRITEBYTECODE=1` or leave that file out of commits.
- `body` is not escaped: a stray `<` or `&` in prose breaks the page. Use `&amp;` / `&lt;` in `content.py`.
- Pages carry canonical and Open Graph tags but no JSON-LD, and the repo has no `sitemap.xml` (2026-11-27).
- Links are root-relative (`/articles/article.css`, `/steps`), so preview by serving the repo root
  (`npx serve .`), not by opening the file directly.
- `nice()` formats dates with `%-d`, which works on macOS and Linux but not on Windows.

## Tests

None. After a rebuild, `git diff articles/` should show only the intended change; open the changed page and
`/articles` in a browser and follow both "Keep reading" links.
