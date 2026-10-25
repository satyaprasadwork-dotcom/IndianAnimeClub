#!/usr/bin/env python3
"""Lightweight pre-deploy checks for Indian Anime Club's static site."""
from pathlib import Path
from html.parser import HTMLParser
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(".")
DOMAIN = "https://indiananimeclub.com"
errors = []
warnings = []

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = False
        self.title_text = []
        self.h1 = 0
        self.meta = []
        self.links = []
        self.images = []
        self.schemas = []
        self.classes = []
        self.in_title = False
        self.in_schema = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "h1":
            self.h1 += 1
        if tag == "meta":
            self.meta.append(attrs)
        if tag == "link" and attrs.get("rel", "").lower() == "canonical":
            self.links.append(attrs.get("href", ""))
        if tag == "img":
            self.images.append(attrs)
        if tag == "script":
            self.in_schema = attrs.get("type") == "application/ld+json"
            if self.in_schema:
                self.schemas.append("")
    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "script":
            self.in_schema = False
    def handle_data(self, data):
        if self.in_title:
            self.title_text.append(data)
        if self.in_schema and self.schemas:
            self.schemas[-1] += data

def read_page(path):
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser

def meta_value(parser, name=None, prop=None):
    for item in parser.meta:
        if name and item.get("name", "").lower() == name.lower():
            return item.get("content", "")
        if prop and item.get("property", "").lower() == prop.lower():
            return item.get("content", "")
    return ""

article_files = sorted(p for p in (ROOT / "articles").glob("*.html") if p.name != "index.html")
if len(article_files) != 31:
    errors.append(f"Expected 31 article source files; found {len(article_files)}.")

seen_canonicals = set()
for path in article_files:
    raw = path.read_text(encoding="utf-8")
    parser = read_page(path)
    slug = path.stem
    canonical = parser.links[0] if parser.links else ""
    title = "".join(parser.title_text).strip()
    description = meta_value(parser, name="description")
    og_image = meta_value(parser, prop="og:image")
    twitter_card = meta_value(parser, name="twitter:card")
    expected_image = f"{DOMAIN}/images/articles/{slug}.svg"
    image_path = ROOT / "images" / "articles" / f"{slug}.svg"

    if not title:
        errors.append(f"{path}: missing title.")
    if not description or len(description) < 60:
        errors.append(f"{path}: missing or unusually short meta description.")
    if parser.h1 != 1:
        errors.append(f"{path}: expected one H1; found {parser.h1}.")
    if canonical != f"{DOMAIN}/{slug}/":
        errors.append(f"{path}: unexpected canonical URL {canonical!r}.")
    if canonical in seen_canonicals:
        errors.append(f"{path}: duplicate article canonical {canonical}.")
    seen_canonicals.add(canonical)
    if not image_path.is_file():
        errors.append(f"{path}: missing featured image file {image_path}.")
    if not any(img.get("src") == f"/images/articles/{slug}.svg" and img.get("alt", "").strip() for img in parser.images):
        errors.append(f"{path}: featured image or descriptive alt text is missing.")
    if og_image != expected_image:
        errors.append(f"{path}: og:image does not match the featured image.")
    if twitter_card != "summary_large_image":
        errors.append(f"{path}: missing large-image social card metadata.")
    article_schema = None
    for raw_schema in parser.schemas:
        try:
            candidate = json.loads(raw_schema)
        except (json.JSONDecodeError, TypeError):
            continue
        if candidate.get("@type") == "Article":
            article_schema = candidate
            break
    if not article_schema:
        errors.append(f"{path}: missing valid Article JSON-LD.")
    else:
        image_data = article_schema.get("image", {})
        image_url = image_data.get("url", "") if isinstance(image_data, dict) else image_data
        if image_url != expected_image:
            errors.append(f"{path}: Article JSON-LD image does not match the featured image.")
        if not article_schema.get("datePublished") or not article_schema.get("dateModified"):
            errors.append(f"{path}: Article JSON-LD is missing publication or modification dates.")
    if not re.search(r'<section\b[^>]*class=["\'][^"\']*\bsources\b', raw, re.I):
        errors.append(f"{path}: missing Sources & further reading section.")
    if re.search(r"<h2[^>]*>\s*Start with the context\s*</h2>", raw, re.I):
        errors.append(f"{path}: generic template heading remains in article body.")
    if re.search(r'<div\b[^>]*class=["\'][^"\']*\bquick-answer\b', raw, re.I):
        warnings.append(f"{path}: check that the brief summary adds information beyond the introduction.")

# Confirm every sitemap URL resolves to a generated HTML file after clean routes are built.
try:
    root = ET.parse(ROOT / "sitemap.xml").getroot()
    sitemap_urls = [node.text.strip() for node in root.findall(".//{*}loc") if node.text]
    for url in sitemap_urls:
        if not url.startswith(DOMAIN + "/"):
            errors.append(f"Sitemap contains a non-canonical domain: {url}")
            continue
        route = url[len(DOMAIN):]
        clean = route.strip("/")
        target = ROOT / clean / "index.html" if clean else ROOT / "index.html"
        if not target.is_file() and clean:
            # Before the deploy workflow creates clean route folders, resolve
            # article routes back to their flat source files.
            source_article = ROOT / "articles" / f"{clean}.html"
            source_page = ROOT / f"{clean}.html"
            if source_article.is_file():
                target = source_article
            elif source_page.is_file():
                target = source_page
        if not target.is_file():
            errors.append(f"Sitemap URL has no source or generated page: {url}")
except (OSError, ET.ParseError) as exc:
    errors.append(f"Could not parse sitemap.xml: {exc}")

ads = (ROOT / "ads.txt").read_text(encoding="utf-8") if (ROOT / "ads.txt").exists() else ""
if "google.com, pub-7937216909291905, DIRECT, f08c47fec0942fa0" not in ads:
    errors.append("ads.txt is missing the expected AdSense publisher record.")

privacy = (ROOT / "privacy-policy.html").read_text(encoding="utf-8").lower() if (ROOT / "privacy-policy.html").exists() else ""
for term in ("google", "cookies", "personalized advertising", "ads settings"):
    if term not in privacy:
        errors.append(f"Privacy policy may be missing the required advertising disclosure term: {term}.")

cards = (ROOT / "articles" / "index.html").read_text(encoding="utf-8")
if len(re.findall(r'<article class="card"', cards, re.I)) != 31:
    errors.append("Article listing does not contain 31 cards.")
if len(re.findall(r'class="article-card-image"', cards, re.I)) != 31:
    errors.append("Article listing does not contain one thumbnail for each of the 31 cards.")
if "const perPage=15" not in cards and "const perPage = 15" not in cards:
    errors.append("Article listing pagination is not configured for 15 cards per page.")

if warnings:
    print("AUDIT WARNINGS:")
    for warning in warnings:
        print(" - " + warning)
if errors:
    print("AUDIT FAILED:")
    for error in errors:
        print(" - " + error)
    sys.exit(1)
print(f"Site audit passed: {len(article_files)} article pages, {len(sitemap_urls)} sitemap URLs, featured images, structured data, ads.txt and privacy disclosures.")
