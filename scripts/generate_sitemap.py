#!/usr/bin/env python3
"""Generate sitemap.xml from canonical URLs in the static site's HTML sources."""
from html.parser import HTMLParser
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree, register_namespace

DOMAIN = "https://indiananimeclub.com"
ROOT = Path(".")
OUTPUT = ROOT / "sitemap.xml"
EXCLUDED_DIRS = {".git", ".github", "node_modules", ".venv", "__pycache__"}

class CanonicalParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.canonical = None

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "link":
            return
        attrs = dict(attrs)
        if "canonical" in attrs.get("rel", "").lower().split():
            href = (attrs.get("href") or "").strip()
            if href.startswith(DOMAIN + "/") or href == DOMAIN:
                self.canonical = href

def source_pages():
    # Public top-level HTML pages, plus article sources and the article listing.
    candidates = list(ROOT.glob("*.html")) + list((ROOT / "articles").glob("*.html"))
    return sorted(p for p in candidates if p.is_file())

urls = set()
for path in source_pages():
    parser = CanonicalParser()
    try:
        parser.feed(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as exc:
        raise SystemExit(f"Cannot read {path}: {exc}")
    if parser.canonical:
        urls.add(parser.canonical.rstrip("/") + "/" if parser.canonical != DOMAIN else DOMAIN + "/")

if not urls:
    raise SystemExit("No canonical URLs found; refusing to overwrite sitemap.xml.")

# Keep the homepage first, then sort the remaining canonical URLs deterministically.
homepage = DOMAIN + "/"
ordered = ([homepage] if homepage in urls else []) + sorted(url for url in urls if url != homepage)
register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
root = Element("{http://www.sitemaps.org/schemas/sitemap/0.9}urlset")
for url in ordered:
    entry = SubElement(root, "{http://www.sitemaps.org/schemas/sitemap/0.9}url")
    SubElement(entry, "{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text = url

ElementTree(root).write(OUTPUT, encoding="UTF-8", xml_declaration=True)
print(f"Generated {OUTPUT} with {len(ordered)} canonical URLs.")
