#!/usr/bin/env python3
"""Lightweight pre-deploy checks for Indian Anime Club's static site."""
from pathlib import Path
from html.parser import HTMLParser
import json
import re
import sys
import xml.etree.ElementTree as ET
from article_content import article_fragment, body_word_count, review_fingerprint

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
if not article_files:
    errors.append("No article source files found.")

seen_canonicals = set()
body_counts = []
ledger_path = ROOT / 'editorial' / 'review-2026-11-01.json'
review_entries = {}
if ledger_path.is_file():
    review_entries = {entry['slug']: entry for entry in json.loads(ledger_path.read_text())['articles']}
for path in article_files:
    raw = path.read_text(encoding="utf-8")
    parser = read_page(path)
    slug = path.stem
    canonical = parser.links[0] if parser.links else ""
    title = "".join(parser.title_text).strip()
    description = meta_value(parser, name="description")
    og_image = meta_value(parser, prop="og:image")
    twitter_card = meta_value(parser, name="twitter:card")
    built = __import__("os").environ.get("IAC_DEPLOY_BUILD") == "1"
    expected_image = f"{DOMAIN}/images/articles/{slug}.{'png' if built else 'svg'}"
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
    if built and not (ROOT / "images" / "articles" / f"{slug}.png").is_file():
        errors.append(f"{path}: PNG social image was not built.")
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
        candidates = candidate.get("@graph", []) if isinstance(candidate, dict) else []
        if not candidates and isinstance(candidate, dict):
            candidates = [candidate]
        for node in candidates:
            if isinstance(node, dict) and node.get("@type") == "Article":
                article_schema = node
                break
        if article_schema:
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
    # Fail fast if a second sources heading or a known wrong legislation link reappears.
    article_body = article_fragment(raw)
    if len(re.findall(r'Sources &amp; further reading', article_body)) != 1:
        errors.append(f"{path}: Sources & further reading must occur exactly once.")
    if "copyright.gov.in/Copyright_Act_1957/chapter_i.html" in raw:
        errors.append(f"{path}: Copyright Act chapter I is not a valid source for infringement exceptions.")
    if not re.search(r'<section\b[^>]*class=["\'][^"\']*\bsources\b', raw, re.I):
        errors.append(f"{path}: missing Sources & further reading section.")
    if re.search(r"<h2[^>]*>\s*Start with the context\s*</h2>", raw, re.I):
        errors.append(f"{path}: generic template heading remains in article body.")
    if re.search(r'<div\b[^>]*class=["\'][^"\']*\bquick-answer\b', raw, re.I):
        warnings.append(f"{path}: check that the brief summary adds information beyond the introduction.")

    # Editorial-quality guardrails. Word count is an internal review signal,
    # not a Google ranking rule or a substitute for usefulness.
    source_match = re.search(r'<section\b[^>]*class=["\'][^"\']*\bsources\b[^"\']*["\'][^>]*>([\s\S]*?)</section>', raw, re.I)
    if source_match:
        source_links = re.findall(r'<a\b[^>]*href=["\'](https?://[^"\']+)["\']', source_match.group(1), re.I)
        if len(set(source_links)) < 2:
            warnings.append(f"{path}: Sources & further reading should contain at least two distinct external references.")
    word_count = body_word_count(raw)
    body_counts.append(word_count)
    # This is the publisher's requirement, not a search-engine ranking rule.
    if word_count <= 1000:
        errors.append(f"{path}: {word_count} article-body words; this project requires more than 1,000, excluding navigation, summaries, references and footer.")
    entry = review_entries.get(slug)
    if not entry or entry.get('review_sha256') != review_fingerprint(raw):
        errors.append(f"{path}: editorial review is missing or stale after a body/source change.")
    toc = re.search(r'<nav\b[^>]*class="article-toc"[^>]*>(.*?)</nav>', article_body, re.S)
    if not toc:
        errors.append(f"{path}: article sidebar table of contents missing.")
    else:
        targets = re.findall(r'href="#([^"]+)"', toc.group(1))
        count = re.search(r'class="toc-count">(\d+) sections', toc.group(1))
        if not count or int(count.group(1)) != len(targets):
            errors.append(f"{path}: table-of-contents count does not match its links.")
        ids = re.findall(r'\bid="([^"]+)"', article_body)
        for target in targets:
            if ids.count(target) != 1:
                errors.append(f"{path}: table of contents points to missing/duplicate anchor #{target}.")
    heading_titles = [
        re.sub(r'<[^>]+>', '', m.group(1)).replace('&amp;', '&').strip().lower()
        for m in re.finditer(r'<h2\b[^>]*>([\s\S]*?)</h2>', raw, re.I)
    ]
    ignored_headings = {"in this article", "on this page", "key takeaways", "sources & further reading", "keep reading"}
    content_headings = [h for h in heading_titles if h and h not in ignored_headings]
    seen_headings = set()
    for heading in content_headings:
        if heading in seen_headings:
            warnings.append(f"{path}: duplicate section heading {heading!r}; editor review is required.")
        seen_headings.add(heading)
    for i, left in enumerate(content_headings):
        left_words = set(re.findall(r'[a-z0-9]+', left))
        if len(left_words) < 3:
            continue
        for right in content_headings[i + 1:]:
            right_words = set(re.findall(r'[a-z0-9]+', right))
            if len(right_words) < 3:
                continue
            overlap = len(left_words & right_words) / max(1, len(left_words | right_words))
            if overlap >= 0.6:
                warnings.append(f"{path}: review potentially overlapping headings {left!r} and {right!r}.")


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
for term in ("google", "cookies", "ads settings"):
    if term not in privacy:
        errors.append(f"Privacy policy may be missing the required advertising disclosure term: {term}.")
if not any(term in privacy for term in ("personalized advertising", "personalised advertising", "personalised ads")):
    errors.append("Privacy policy may be missing its advertising-personalisation disclosure.")

cards = (ROOT / "articles" / "index.html").read_text(encoding="utf-8")
archive_card_count = len(re.findall(r'<article class="card"', cards, re.I))
if archive_card_count != len(article_files):
    errors.append(f"Article listing contains {archive_card_count} cards; expected {len(article_files)}.")
if len(re.findall(r'class="article-card-image"', cards, re.I)) != len(article_files):
    errors.append(f"Article listing should contain {len(article_files)} article thumbnails.")
if "const perPage=15" not in cards and "const perPage = 15" not in cards:
    errors.append("Article listing pagination is not configured for 15 cards per page.")

# The article archive is a public landing page in its own right, not just a grid.
archive_path = ROOT / "articles" / "index.html"
archive = read_page(archive_path)
archive_title = "".join(archive.title_text).strip()
archive_description = meta_value(archive, name="description")
archive_canonical = archive.links[0] if archive.links else ""
if not archive_title:
    errors.append("Article archive is missing a title.")
if not archive_description or len(archive_description) < 70:
    errors.append("Article archive is missing a useful meta description.")
if archive_canonical != f"{DOMAIN}/articles/":
    errors.append(f"Article archive canonical is incorrect: {archive_canonical!r}.")
if archive.h1 != 1:
    errors.append(f"Article archive must have exactly one H1; found {archive.h1}.")
if meta_value(archive, prop="og:url") != f"{DOMAIN}/articles/":
    errors.append("Article archive og:url does not match its canonical URL.")
if meta_value(archive, name="twitter:card") not in ("summary", "summary_large_image"):
    errors.append("Article archive is missing Twitter/X card metadata.")

def _valid_json(value):
    try:
        json.loads(value)
        return True
    except (json.JSONDecodeError, TypeError):
        return False

if not any(
    isinstance(json.loads(raw_schema), dict)
    and json.loads(raw_schema).get("@type") == "CollectionPage"
    for raw_schema in archive.schemas
    if raw_schema.strip().startswith("{") and _valid_json(raw_schema)
):
    errors.append("Article archive is missing valid CollectionPage structured data.")

# Catch duplicate or malformed sitemap entries before publishing.
try:
    sitemap_values = [node.text.strip() for node in ET.parse(ROOT / "sitemap.xml").getroot().findall(".//{*}loc") if node.text]
    if len(sitemap_values) != len(set(sitemap_values)):
        errors.append("Sitemap contains duplicate URLs.")
    if f"{DOMAIN}/articles/" not in sitemap_values:
        errors.append("Sitemap is missing the canonical article archive URL.")
    for url in sitemap_values:
        if " " in url or not url.startswith(DOMAIN + "/") or url.endswith(".html"):
            errors.append(f"Sitemap URL is not a clean canonical URL: {url}")
except (OSError, ET.ParseError) as exc:
    errors.append(f"Could not validate sitemap URL uniqueness: {exc}")

# Confirm each article card links to a known canonical article and a real local thumbnail.
known_article_urls = {f"{DOMAIN}/{path.stem}/" for path in article_files}
for href in re.findall(r'<h2>\s*<a\s+href=["\']([^"\']+)["\']', cards, re.I):
    if href.rstrip("/") + "/" not in known_article_urls:
        errors.append(f"Article archive links to an unknown article URL: {href}")
for image_src in re.findall(r'<img\b[^>]*class=["\'][^"\']*\barticle-card-image\b[^"\']*["\'][^>]*src=["\']([^"\']+)["\']', cards, re.I):
    local_image = ROOT / image_src.lstrip("/")
    if not local_image.is_file():
        errors.append(f"Article archive thumbnail file is missing: {image_src}")

listed_links = set(re.findall(r"<h2>\s*<a\s+href=['\"]([^'\"]+)['\"]", cards, re.I))
missing_cards = sorted(known_article_urls - {href.rstrip("/") + "/" for href in listed_links})
for url in missing_cards:
    errors.append(f"Article missing from archive: {url}")

# Built-page checks can inspect the real deployment artifacts.
if __import__("os").environ.get("IAC_DEPLOY_BUILD") == "1":
    shell = ROOT / "site-shell.js"
    if not shell.is_file() or "G-M4738D1ZND" not in shell.read_text(encoding="utf-8"):
        errors.append("Shared GA4 loader missing.")
    for url in sitemap_urls:
        route = url[len(DOMAIN):].strip("/")
        page = ROOT / route / "index.html" if route else ROOT / "index.html"
        if not page.is_file():
            errors.append(f"{url}: clean route not generated.")
            continue
        html = page.read_text(encoding="utf-8")
        if '/favicon.svg' not in html or '/favicon-48.png' not in html:
            errors.append(f"{page}: shared favicon not installed.")
        if 'site-shell.js' not in html:
            errors.append(f"{page}: shared shell/analytics not installed.")
        if not re.search(r"<main\b", html, re.I):
            errors.append(f"{page}: missing main landmark.")

# Generated public routes must contain all three consistent tracking integrations.
if __import__("os").environ.get("IAC_DEPLOY_BUILD") == "1":
    for url in sitemap_urls:
        route = url[len(DOMAIN):].strip("/")
        page = ROOT / route / "index.html" if route else ROOT / "index.html"
        if not page.is_file(): continue
        head = page.read_text(encoding="utf-8").split("</head>",1)[0]
        for token in ("G-M4738D1ZND","ca-pub-7937216909291905","ywqdm8xkj7"):
            if token not in head:
                errors.append(f"{page}: required tracking id {token} missing")
        for uri in ("https://www.googletagmanager.com/gtag/js?id=",
                    "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=",
                    "https://www.clarity.ms/tag/"):
            if head.count(uri)!=1:
                errors.append(f"{page}: missing or duplicate tracking script {uri}")

# Low-value-content prevention: ensure homepage gives direct, crawlable access
# to genuine published articles rather than only promotional navigation.
homepage_path = ROOT / "index.html"
homepage_html = homepage_path.read_text(encoding="utf-8")
featured_match = re.search(
    r'<section\b[^>]*id="featured-reading"[^>]*>([\s\S]*?)</section>',
    homepage_html, re.I,
)
if not featured_match:
    errors.append("Homepage is missing its editorial article showcase.")
else:
    section_html = featured_match.group(1)
    featured_hrefs = set(re.findall(r'<a\b[^>]*href="(/[^"]+/)"', section_html))
    featured_articles = {DOMAIN + href for href in featured_hrefs if DOMAIN + href in known_article_urls}
    if len(featured_articles) < 6:
        errors.append(f"Homepage should link to at least six published article pages; found {len(featured_articles)}.")
    featured_images = re.findall(r'<img\b[^>]*src="(/images/articles/[^"]+)"', section_html)
    if len(featured_images) < 6:
        errors.append("Homepage editorial showcase is missing article thumbnails.")
    for image_src in featured_images:
        if not (ROOT / image_src.lstrip("/")).is_file():
            errors.append(f"Homepage references missing featured image: {image_src}")
if '<p class="type">We <span id="tw"></span>' in homepage_html:
    errors.append("Homepage hero lacks meaningful non-JavaScript fallback text.")
if "Fans wanted" in homepage_html:
    errors.append("Homepage still advertises hypothetical city chapter cards.")
if homepage_html.count('<section class="worlds" id="events">') != 1:
    errors.append("Homepage discovery section must occur exactly once.")
if homepage_html.count('<main') != 1 or homepage_html.count('</main>') != 1:
    errors.append("Homepage must have one closed main landmark.")
if 'href="/css/home-editorial.css' not in homepage_html or not (ROOT / "css/home-editorial.css").is_file():
    errors.append("Homepage editorial grid stylesheet missing.")

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
print(f"Reviewed article bodies: {min(body_counts)}–{max(body_counts)} words, excluding page furniture and source lists; review fingerprints current.")
