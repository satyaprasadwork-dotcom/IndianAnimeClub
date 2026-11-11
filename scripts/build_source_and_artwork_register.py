#!/usr/bin/env python3
"""Enumerate all article citations and artwork for manual review; does not certify URLs or rights."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import csv
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports"
OUT.mkdir(exist_ok=True)
pages = sorted(p for p in (ROOT / "articles").glob("*.html") if p.name != "index.html")
artworks = sorted((ROOT / "images" / "articles").glob("*.svg"))
urls = {}

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = set()
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href","")
            if href.startswith(("https://","http://")):
                self.links.add(href)

for page in pages:
    html = page.read_text(encoding="utf-8")
    match = re.search(r'<section class="sources"[^>]*>(.*?)</section>', html, re.S)
    if not match:
        raise SystemExit(f"Missing editorial source section: {page}")
    parse = Links()
    parse.feed(match.group(1))
    for link in parse.links:
        urls.setdefault(link,set()).add(page.stem)

with (OUT / "source-verification-register.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["url","article_slugs","automated_result","human_source_scope","checked_date","notes"])
    for url, slugs in sorted(urls.items()):
        w.writerow([url,"; ".join(sorted(slugs)),"NOT_CHECKED_IN_THIS_REGISTER","PENDING","","Review actual URL, claim scope, locale and status; bot 403/429 is not broken-link proof."])
with (OUT / "artwork-rights-register.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["asset_path","creator","rights_basis","evidence_reference","rights_status"])
    for image in artworks:
        w.writerow([image.relative_to(ROOT).as_posix(),"UNKNOWN","NOT_ESTABLISHED","","PENDING_PROVENANCE"])
print(f"Enumerated {len(urls)} unique citations, {len(artworks)} artwork files, {len(pages)} retained article pages. All require independent review.")
