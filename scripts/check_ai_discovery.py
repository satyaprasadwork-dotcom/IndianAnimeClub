#!/usr/bin/env python3
"""Verify AI discovery, canonical relationships, and structured-data invariants.

Static validation only. This does not replace Google's Rich Results Test,
Search Console URL Inspection, or a human editorial/consent review.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import json
import re
import sys
import xml.etree.ElementTree as ET

BASE = "https://indiananimeclub.com"
ROOT = Path(".")
errors = []


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.canonical = None
        self.schemas = []
        self.in_schema = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and "canonical" in (attrs.get("rel") or "").split():
            self.canonical = attrs.get("href")
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.in_schema = True
            self.schemas.append("")

    def handle_data(self, data):
        if self.in_schema and self.schemas:
            self.schemas[-1] += data

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_schema = False


def load(path):
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    nodes = []
    for value in parser.schemas:
        try:
            data = json.loads(value)
        except (ValueError, TypeError) as exc:
            errors.append(f"{path}: invalid JSON-LD ({exc})")
            continue
        if not isinstance(data, dict) or data.get("@context") != "https://schema.org":
            errors.append(f"{path}: JSON-LD must be a Schema.org object")
            continue
        children = data.get("@graph", [data])
        if not isinstance(children, list):
            errors.append(f"{path}: invalid @graph")
            continue
        nodes.extend(child for child in children if isinstance(child, dict))
    return parser.canonical, nodes


def matches(nodes, kind):
    return [node for node in nodes if kind in (
        node.get("@type") if isinstance(node.get("@type"), list)
        else [node.get("@type")]
    )]


def check_breadcrumb(path, nodes, canonical, expected):
    crumbs = matches(nodes, "BreadcrumbList")
    if len(crumbs) != 1:
        errors.append(f"{path}: expected one BreadcrumbList, got {len(crumbs)}")
        return
    entries = crumbs[0].get("itemListElement") or []
    actual = [e.get("item") for e in entries if isinstance(e, dict)]
    positions = [e.get("position") for e in entries if isinstance(e, dict)]
    if actual != expected or positions != list(range(1, len(expected) + 1)):
        errors.append(f"{path}: breadcrumb items/positions don't match site hierarchy")
    if crumbs[0].get("@id") != canonical + "#breadcrumb":
        errors.append(f"{path}: BreadcrumbList @id must match the canonical URL")


sitemap_path = ROOT / "sitemap.xml"
urls = [
    e.text.strip()
    for e in ET.parse(sitemap_path).getroot().findall(".//{*}loc")
    if e.text
]
canonical_set = set(urls)
if len(urls) != len(canonical_set):
    errors.append("sitemap.xml contains duplicate canonical URLs")
if not all(url.startswith(BASE + "/") for url in urls):
    errors.append("sitemap.xml contains an off-domain URL")

article_paths = sorted((ROOT / "articles").glob("*.html"))
article_paths = [path for path in article_paths if path.name != "index.html"]
for path in article_paths:
    canonical, nodes = load(path)
    expected = f"{BASE}/{path.stem}/"
    if canonical != expected or canonical not in canonical_set:
        errors.append(f"{path}: canonical/sitemap mismatch")
    posts = matches(nodes, "BlogPosting")
    if len(posts) != 1:
        errors.append(f"{path}: expected one BlogPosting, got {len(posts)}")
        continue
    post = posts[0]
    if post.get("@id") != expected + "#article":
        errors.append(f"{path}: wrong BlogPosting @id")
    if post.get("mainEntityOfPage", {}).get("@id") != expected:
        errors.append(f"{path}: wrong mainEntityOfPage")
    if post.get("isPartOf", {}).get("@id") != BASE + "/#website":
        errors.append(f"{path}: missing website relationship")
    if post.get("publisher", {}).get("@id") != BASE + "/#organization":
        errors.append(f"{path}: wrong publisher relationship")
    if not post.get("headline") or not post.get("description"):
        errors.append(f"{path}: missing headline/description")
    author = post.get("author") or {}
    if author.get("@type") != "Person" or not author.get("name") or author.get("url") != BASE + "/leadership/":
        errors.append(f"{path}: author lacks a matching profile")
    for key in ("datePublished", "dateModified"):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}(?:T.*)?", post.get(key, "")):
            errors.append(f"{path}: invalid or missing {key}")
    image = post.get("image")
    if not isinstance(image, dict) or not image.get("url", "").startswith(BASE + "/images/articles/"):
        errors.append(f"{path}: missing original featured-image URL")
    elif not (ROOT / image["url"][len(BASE)+1:]).is_file():
        errors.append(f"{path}: referenced featured image is missing")
    check_breadcrumb(path, nodes, expected, [BASE + "/", BASE + "/articles/", expected])

for path in (ROOT / "articles.html", ROOT / "articles/index.html"):
    canonical, nodes = load(path)
    if canonical != BASE + "/articles/":
        errors.append(f"{path}: incorrect canonical")
    if len(matches(nodes, "CollectionPage")) != 1:
        errors.append(f"{path}: missing or duplicate CollectionPage")
    check_breadcrumb(path, nodes, BASE + "/articles/", [BASE + "/", BASE + "/articles/"])

canonical, nodes = load(ROOT / "index.html")
if canonical != BASE + "/":
    errors.append("Homepage canonical is incorrect")
for kind in ("Organization", "WebSite", "WebPage"):
    if len(matches(nodes, kind)) != 1:
        errors.append(f"Homepage missing or duplicate {kind} node")

for path in sorted(ROOT.glob("*.html")) + sorted(ROOT.glob("*/index.html")):
    if path == ROOT / "index.html":
        continue
    canonical, nodes = load(path)
    if canonical and canonical not in canonical_set:
        errors.append(f"{path}: canonical absent from sitemap")

robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
required_agents = (
    "OAI-SearchBot", "GPTBot", "ChatGPT-User", "ClaudeBot",
    "Claude-SearchBot", "Claude-User", "PerplexityBot",
    "Google-Extended", "Applebot-Extended", "CCBot"
)
if "User-agent: *\nAllow: /\nDisallow: /scripts/" not in robots:
    errors.append("robots.txt wildcard allow and script exclusion are missing")
for agent in required_agents:
    if f"User-agent: {agent}" not in robots:
        errors.append(f"robots.txt missing {agent}")
if f"Sitemap: {BASE}/sitemap.xml" not in robots:
    errors.append("robots.txt missing canonical sitemap reference")
if not llms.startswith("# Indian Anime Club\n"):
    errors.append("llms.txt missing publisher heading")
llms_urls = re.findall(r"\]\((https?://[^)\s]+)\)", llms)
if len(llms_urls) < 15:
    errors.append("llms.txt does not provide enough useful canonical links")
for url in llms_urls:
    if url.startswith(BASE + "/") and url not in canonical_set and url != BASE + "/sitemap.xml":
        errors.append(f"llms.txt points to a missing canonical page: {url}")
if "## Selected editorial guides" not in llms:
    errors.append("llms.txt missing curated editorial list")

if errors:
    print("AI DISCOVERY / SCHEMA AUDIT FAILED:")
    for error in errors:
        print(" - " + error)
    sys.exit(1)
print(f"AI DISCOVERY / SCHEMA AUDIT PASS: {len(article_paths)} articles, {len(canonical_set)} canonical URLs, links, robots rules, JSON-LD and breadcrumbs.")
