#!/usr/bin/env python3
"""Include newly published source articles in the existing approved archive grid.
Keeps the current hand-designed cards unchanged; adds only missing articles.
Runs on CI and deploy, so publication does not require manual archive markup.
"""
from pathlib import Path
from html import escape, unescape
import json
import re

ROOT = Path(".")
archive = ROOT / "articles" / "index.html"
text = archive.read_text(encoding="utf-8")
marker = re.search(r"<!-- ARTICLE ORDER:[\s\S]*?-->", text)
if marker is None:
    raise SystemExit("Archive insertion marker not found; keep approved markup unchanged.")

def strip_tags(value):
    return re.sub(r"<[^>]*>", "", value)

def get_value(pattern, text, fallback=""):
    hit = re.search(pattern, text, re.I | re.S)
    return unescape(strip_tags(hit.group(1)).strip()) if hit else fallback

existing_slugs = set(re.findall(r"/images/articles/([a-z0-9-]+)\.svg", text))
new_cards = []
for path in sorted((ROOT / "articles").glob("*.html")):
    if path.name == "index.html" or path.stem in existing_slugs:
        continue
    raw = path.read_text(encoding="utf-8")
    title = get_value(r"<h1\b[^>]*>([\s\S]*?)</h1>", raw)
    description = get_value(r'<meta\b[^>]*name="description"[^>]*content="([^"]+)"', raw)
    if not description:
        description = get_value(r'<p\s+class="dek"[^>]*>([\s\S]*?)</p>', raw)
    slug = path.stem
    image = ROOT / "images" / "articles" / (slug + ".svg")
    if not title or not description or not image.is_file():
        raise SystemExit(f"{path}: cannot add card without title, description and original featured image.")
    schema_match = re.search(r'<script\s+type="application/ld\+json">([\s\S]*?)</script>', raw, re.I)
    schema = json.loads(schema_match.group(1)) if schema_match else {}
    category = schema.get("articleSection", "anime analysis")
    if not isinstance(category, str):
        category = "anime analysis"
    category = category.strip().lower()
    allowed = {"anime analysis", "anime & life", "anime trends", "character studies", "rankings",
               "recommendations", "anime guides", "anime industry", "community"}
    if category not in allowed:
        category = "anime analysis"
    url = "https://indiananimeclub.com/" + slug + "/"
    esc_title = escape(title, quote=True)
    card = (
        '<article class="card" data-category="' + escape(category, quote=True) +
        '" data-title="' + escape(title.lower(), quote=True) + '">'
        '<img class="article-card-image" src="/images/articles/' + slug +
        '.svg" alt="" width="1200" height="675" loading="lazy" decoding="async">'
        '<span class="tag">' + escape(category.title()) + '</span>'
        '<h2><a href="' + url + '">' + esc_title + '</a></h2>'
        '<p>' + escape(description) + '</p>'
        '<a class="read" href="' + url + '" aria-label="Read ' + esc_title +
        '">Read article <span aria-hidden="true">↗</span></a></article>\n'
    )
    date = str(schema.get("datePublished", "0000-00-00"))
    new_cards.append((date, slug, card))
if new_cards:
    new_cards.sort(key=lambda x: (x[0], x[1]), reverse=True)
    text = text[:marker.end()] + "\n" + "".join(x[2] for x in new_cards) + text[marker.end():]
    archive.write_text(text, encoding="utf-8")
print(f"Archive synced: {len(new_cards)} missing article card(s) added.")
