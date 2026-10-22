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

import re
import shutil
import sys
from datetime import date, datetime
from email.utils import format_datetime
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


def build():
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    shutil.copytree(STATIC, OUTPUT / "static")

    env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=select_autoescape(["html"]))
    base = SITE["base_path"]
    env.globals.update(site=SITE, year=date.today().year, url=lambda p: base + p)
    env.filters["nicedate"] = lambda d: f"{d.day} {d.strftime('%B %Y')}"

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
    page_tpl = env.get_template("page.html")
    for p in pages:
        if p["slug"] == "about":
            continue
        write(f"{p['slug']}/index.html", page_tpl.render(page=p, current=f"/{p['slug']}/"))

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
