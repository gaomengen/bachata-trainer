import html, os, sys, datetime
sys.path.insert(0, os.path.dirname(__file__))
from content import ARTICLES

OUT = sys.argv[1]
SITE = "https://bachatamusicalidad.com"
ORDER = ["what-is-your-weight", "dont-skip-the-tap", "count-the-and",
         "lead-the-box-from-count-1", "the-leaders-job", "syncopation-reserve",
         "reading-a-bachata-song", "from-class-to-social", "learning-from-videos"]
by = {a["slug"]: a for a in ARTICLES}
arts = [by[s] for s in ORDER]
assert len(arts) == len(ARTICLES)

ICON = ("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'>"
        "<rect width='64' height='64' rx='14' fill='%230e0b14'/>"
        "<rect x='11' y='38' width='6' height='14' rx='3' fill='%235eb1ff'/>"
        "<rect x='23' y='31' width='6' height='21' rx='3' fill='%23ffb454'/>"
        "<rect x='35' y='24' width='6' height='28' rx='3' fill='%23ff5d8f'/>"
        "<rect x='47' y='16' width='6' height='36' rx='3' fill='%23b98cff'/></svg>")

def nice(d):
    return datetime.date.fromisoformat(d).strftime("%B %-d, %Y")

def head(title, desc, path):
    t = html.escape(title); d = html.escape(desc)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{SITE}{path}">
<link rel="icon" href="{ICON}">
<meta name="theme-color" content="#0e0b14">
<meta property="og:type" content="article">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/articles/article.css">
</head>
<body>
<nav class="top"><a href="/">Bachata Musicalidad</a><span>·</span><a href="/articles">Articles</a><span>·</span><a href="/steps">Steps &amp; Styles</a></nav>
"""

for i, a in enumerate(arts):
    path = f"/articles/{a['slug']}"
    nxt = [arts[(i + k) % len(arts)] for k in (1, 2)]
    more = "\n".join(
        f'    <li><a href="/articles/{n["slug"]}">{html.escape(n["title"])}</a><span>{html.escape(n["dek"])}</span></li>'
        for n in nxt)
    page = head(a["title"] + " · Bachata Musicalidad", a["dek"], path) + f"""<main class="wrap">
<article>
  <p class="kicker">{html.escape(a['tag'])}</p>
  <h1>{html.escape(a['title'])}</h1>
  <p class="dek">{html.escape(a['dek'])}</p>
  <p class="meta">From my bachata learning journal · {nice(a['date'])}</p>
{a['body'].strip()}
</article>
<aside class="more">
  <h2>Keep reading</h2>
  <ul>
{more}
  </ul>
  <a class="all" href="/articles">All articles →</a>
</aside>
</main>
</body>
</html>
"""
    open(os.path.join(OUT, a["slug"] + ".html"), "w").write(page)

items = "\n".join(f"""  <li>
    <a href="/articles/{a['slug']}">
      <span class="kicker">{html.escape(a['tag'])}</span>
      <b>{html.escape(a['title'])}</b>
      <span class="d">{html.escape(a['dek'])}</span>
    </a>
  </li>""" for a in arts)
index = head("Articles · Bachata Musicalidad",
             "What I'm learning about bachata, written up for other dancers: technique, leading, musicality and practice.",
             "/articles") + f"""<main class="wrap">
<header class="intro">
  <h1>Articles</h1>
  <p class="dek">I'm learning bachata and keeping a journal of everything I pick up in classes,
    at socials and from videos. These are the lessons from it that I think will help other
    dancers too. I'm a learner, not a teacher, so take them as notes from someone a few
    steps ahead of you, and check anything important with an instructor you trust.</p>
</header>
<ul class="list">
{items}
</ul>
<p class="back"><a href="/">← back to the Rhythm Trainer</a></p>
</main>
</body>
</html>
"""
open(os.path.join(OUT, "index.html"), "w").write(index)
print("built", len(arts), "articles")
