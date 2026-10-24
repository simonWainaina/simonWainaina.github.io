"""
Corner Thoughts - a small static site generator.

Turns Markdown files in content/ into a finished website in output/.

    python build.py            # build the site into output/
    python build.py --serve    # build, then preview at http://localhost:8000

Essays live in content/essays/, pages (About, Résumé) in content/pages/.
Each file starts with a few "key: value" lines, a blank line, then Markdown:

    title: Two Birds at Dusk
    date: 2026-09-14
    summary: One line shown on the home page.
    status: draft            (optional - drafts are skipped)

    Your essay text here...
"""

import html
import re
import shutil
import sys
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from email.utils import format_datetime, parsedate_to_datetime
from pathlib import Path
from xml.sax.saxutils import escape

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape

from config import SITE

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"
OUTPUT = ROOT / "output"

WORDS_PER_MINUTE = 230


def parse_file(path):
    """Split a content file into its header fields and Markdown body."""
    text = path.read_text(encoding="utf-8")
    meta, body = {}, text
    head, sep, rest = text.partition("\n\n")
    if sep and all(re.match(r"^[A-Za-z_]+\s*:", line) for line in head.strip().splitlines()):
        for line in head.strip().splitlines():
            key, _, value = line.partition(":")
            meta[key.strip().lower()] = value.strip()
        body = rest

    meta.setdefault("title", path.stem.replace("-", " ").title())
    meta["slug"] = meta.get("slug") or path.stem
    if "date" in meta:
        meta["date"] = datetime.strptime(meta["date"], "%Y-%m-%d").date()
    meta["html"] = markdown.markdown(body, extensions=["extra", "smarty", "sane_lists"])
    words = len(re.findall(r"\w+", body))
    meta["reading_time"] = max(1, round(words / WORDS_PER_MINUTE))
    return meta


def load(folder):
    items = [parse_file(p) for p in sorted((CONTENT / folder).glob("*.md"))]
    return [i for i in items if i.get("status", "").lower() != "draft"]


def write(rel_path, html):
    out = OUTPUT / rel_path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")


def rss(essays):
    """Build feed.xml so readers can follow the site in a feed reader."""
    base = SITE["url"] + SITE["base_path"]
    items = []
    for e in essays[:20]:
        link = f"{base}/essays/{e['slug']}/"
        pub = format_datetime(datetime.combine(e["date"], datetime.min.time()))
        items.append(
            f"<item><title>{escape(e['title'])}</title><link>{link}</link>"
            f"<guid>{link}</guid><pubDate>{pub}</pubDate>"
            f"<description>{escape(e.get('summary', ''))}</description></item>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>'
        f"<title>{escape(SITE['title'])}</title><link>{base}/</link>"
        f"<description>{escape(SITE['tagline'])}</description>"
        + "".join(items)
        + "</channel></rss>\n"
    )


NAIROBI = timezone(timedelta(hours=3))


def fetch_feed(source, url):
    """Read one RSS feed and return its stories as dicts. Returns [] on any failure."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; SimonWainainaSite/1.0)"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            root = ET.fromstring(resp.read())
    except Exception as err:
        print(f"Note: could not load news from {source} ({err.__class__.__name__}).")
        return []

    stories = []
    for item in root.iter("item"):
        title = html.unescape(item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if not title or not link:
            continue
        try:
            when = parsedate_to_datetime(item.findtext("pubDate") or "")
        except (TypeError, ValueError):
            continue
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        summary = (item.findtext("description") or "").split("</p>")[0]  # first paragraph only
        summary = re.sub(r"<[^>]+>", " ", summary)
        summary = re.sub(r"\s+", " ", html.unescape(summary)).strip()
        summary = re.sub(r"^[A-Z][A-Za-z ,]+, \w{3} \d{1,2} [–-] ", "", summary)  # "NAIROBI, Kenya, Oct 24 – "
        stories.append({
            "source": source,
            "title": title,
            "link": re.sub(r"\?(utm|at)_[^#]*", "", link),  # drop tracking tags
            "summary": summary,
            "when": when,
        })
    return stories


def shorten(text, limit=220):
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(",;:") + "…"


def same_story(a, b):
    """True if two headlines share most of their key words (same event, different outlet)."""
    words = lambda t: {w for w in re.findall(r"[a-z0-9]+", t.lower()) if len(w) > 3}
    wa, wb = words(a), words(b)
    return bool(wa and wb) and len(wa & wb) >= 0.5 * min(len(wa), len(wb))


def fetch_news(settings):
    """Latest headlines for each news section, newest first, a few per source."""
    feeds = [(s, f) for s in settings["sections"] for f in s["feeds"]]
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda sf: fetch_feed(*sf[1]), feeds))

    cutoff = datetime.now(timezone.utc) - timedelta(days=settings.get("max_age_days", 3))
    skip = settings.get("skip_links_containing", [])
    per_section = settings.get("per_section", 6)
    per_source = settings.get("per_source", 2)

    sections = []
    for section in settings["sections"]:
        candidates = [st for (s, _), res in zip(feeds, results) if s is section for st in res]
        candidates.sort(key=lambda st: st["when"], reverse=True)
        picked, count = [], {}
        for st in candidates:
            if (st["when"] < cutoff or count.get(st["source"], 0) >= per_source
                    or any(s in st["link"] for s in skip)
                    or any(same_story(st["title"], p["title"]) for p in picked)):
                continue
            count[st["source"]] = count.get(st["source"], 0) + 1
            st["summary"] = shorten(st["summary"])
            st["when"] = st["when"].astimezone(NAIROBI)
            picked.append(st)
            if len(picked) == per_section:
                break
        sections.append({"title": section["title"], "stories": picked})

    if not any(s["stories"] for s in sections):
        return None
    return {"sections": sections, "updated": datetime.now(NAIROBI)}


def build():
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    shutil.copytree(STATIC, OUTPUT / "static")

    env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=select_autoescape(["html"]))
    base = SITE["base_path"]
    env.globals.update(site=SITE, year=date.today().year, url=lambda p: base + p)
    env.globals["build_id"] = datetime.now().strftime("%Y%m%d%H%M")  # makes browsers fetch fresh CSS
    env.filters["nicedate"] = lambda d: f"{d.day} {d.strftime('%B %Y')}"
    env.filters["newsdate"] = lambda d: f"{d.day} {d.strftime('%b')}, {d.strftime('%H:%M')}"

    essays = sorted(load("essays"), key=lambda e: e.get("date", date.min), reverse=True)
    pages = load("pages")

    social = {k: v for k, v in SITE.get("social", {}).items() if v}
    env.globals["social"] = social

    # Profile picture: only shown if the file is actually in static/.
    photo = SITE.get("photo", "")
    env.globals["photo"] = f"{base}/static/{photo}" if photo and (STATIC / photo).is_file() else None
    if photo and not env.globals["photo"]:
        print(f"Note: no profile picture yet - add static/{photo} to show one.")

    # Home page = About page, with recent essays and social links underneath.
    about = next((p for p in pages if p["slug"] == "about"), None)
    write("index.html", env.get_template("home.html").render(
        page=about, recent=essays[:3], current="/"))

    write("essays/index.html", env.get_template("essays.html").render(
        essays=essays, current="/essays/"))

    essay_tpl = env.get_template("essay.html")
    for i, e in enumerate(essays):
        newer = essays[i - 1] if i > 0 else None
        older = essays[i + 1] if i + 1 < len(essays) else None
        page_url = f"{SITE['url']}{base}/essays/{e['slug']}/"
        write(f"essays/{e['slug']}/index.html",
              essay_tpl.render(essay=e, newer=newer, older=older, page_url=page_url, current="/essays/"))

    # Every other page in content/pages/ gets its own address, e.g. /resume/.
    # The news page (see "news" in config.py) also gets today's headlines.
    news_settings = SITE.get("news")
    news_page = news_settings and news_settings.get("page")
    news = fetch_news(news_settings) if any(p["slug"] == news_page for p in pages) else None

    page_tpl = env.get_template("page.html")
    for p in pages:
        if p["slug"] == "about":
            continue
        write(f"{p['slug']}/index.html", page_tpl.render(
            page=p, current=f"/{p['slug']}/", news=news if p["slug"] == news_page else None))

    write("404.html", env.get_template("404.html").render(current=None))
    write("feed.xml", rss(essays))
    (OUTPUT / ".nojekyll").touch()  # tells GitHub Pages to serve files as-is

    print(f"Built {len(essays)} essays and {len(pages)} pages into {OUTPUT}/")


def serve(port=8000):
    import functools
    import http.server

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUTPUT))
    print(f"Previewing at http://localhost:{port}  (Ctrl+C to stop)")
    http.server.ThreadingHTTPServer(("", port), handler).serve_forever()


if __name__ == "__main__":
    build()
    if "--serve" in sys.argv:
        serve()
