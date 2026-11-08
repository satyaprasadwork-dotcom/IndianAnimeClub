#!/usr/bin/env python3
"""Lightweight scheduled live checks of AI discovery, bots and public schema.

This tests HTTP reachability and markup. It cannot prove a crawler actually visited
the site, that Google indexed a URL, or that an AI product cites an article.
"""
from urllib.request import urlopen, Request
from urllib.parse import urlparse
from html.parser import HTMLParser
from xml.etree import ElementTree as ET
import json
import re
import sys

BASE = "https://indiananimeclub.com"
errors = []


def get(path):
    req = Request(BASE + path, headers={
        "User-Agent": "IndianAnimeClubDiscoveryAudit/1.0",
        "Cache-Control": "no-cache",
    })
    try:
        with urlopen(req, timeout=25) as response:
            if response.status != 200:
                errors.append(f"{path}: HTTP {response.status}")
            return response.read(2500000).decode("utf-8", "replace")
    except Exception as exc:
        errors.append(f"{path}: HTTP request failed ({type(exc).__name__})")
        return ""


class StructuredData(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts = []
        self.active = False
        self.canonical = None
        self.noindex = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.active = True
            self.texts.append("")
        if tag == "link" and "canonical" in (attrs.get("rel") or "").split():
            self.canonical = attrs.get("href")
        if tag == "meta" and attrs.get("name", "").lower() == "robots":
            self.noindex = "noindex" in attrs.get("content", "").lower()

    def handle_data(self, data):
        if self.active:
            self.texts[-1] += data

    def handle_endtag(self, tag):
        if tag == "script":
            self.active = False

    def nodes(self):
        result = []
        for text in self.texts:
            try:
                data = json.loads(text)
            except ValueError:
                errors.append("Invalid JSON-LD detected on public page")
                continue
            result += data.get("@graph", [data]) if isinstance(data, dict) else []
        return result


robots = get("/robots.txt")
llms = get("/llms.txt")
sitemap = get("/sitemap.xml")
if robots:
    for bot in ("OAI-SearchBot", "GPTBot", "ClaudeBot", "PerplexityBot", "CCBot"):
        if f"User-agent: {bot}" not in robots:
            errors.append(f"robots.txt missing AI bot rule for {bot}")
    if "Disallow: /scripts/" not in robots:
        errors.append("robots.txt missing protection for /scripts/")
if llms and ("# Indian Anime Club" not in llms or "## Selected editorial guides" not in llms):
    errors.append("llms.txt is not the expected editorial discovery guide")
urls = []
if sitemap:
    try:
        urls = [
            item.text.strip() for item in ET.fromstring(sitemap).findall(".//{*}loc")
            if item.text
        ]
    except ET.ParseError:
        errors.append("sitemap.xml is invalid XML")
if len(urls) < 38 or len(urls) != len(set(urls)):
    errors.append(f"Expected at least 38 unique canonical URLs; found {len(urls)}")
for url in urls:
    if not url.startswith(BASE + "/"):
        errors.append(f"Unexpected sitemap URL: {url}")
        continue
    slug = urlparse(url).path
    html = get(slug)
    if not html:
        continue
    parser = StructuredData()
    parser.feed(html)
    nodes = parser.nodes()
    if parser.noindex:
        errors.append(f"Public canonical page has noindex: {url}")
    if parser.canonical != url:
        errors.append(f"Canonical mismatch: {url} -> {parser.canonical}")
    types = [node.get("@type") for node in nodes if isinstance(node, dict)]
    if slug == "/":
        if not {"Organization", "WebSite", "WebPage"} <= set(types):
            errors.append("Homepage is missing Organization, WebSite or WebPage schema")
    elif slug == "/articles/":
        if "CollectionPage" not in types or "BreadcrumbList" not in types:
            errors.append("Archive has missing CollectionPage/BreadcrumbList schema")
    elif slug not in ("/watchlist-planner/", "/about/", "/contact/", "/community-guidelines/",
                      "/editorial-policy/", "/privacy-policy/", "/terms/", "/disclaimer/",
                      "/leadership/"):
        articles = [node for node in nodes if isinstance(node, dict) and node.get("@type") == "BlogPosting"]
        breadcrumbs = [node for node in nodes if isinstance(node, dict) and node.get("@type") == "BreadcrumbList"]
        if len(articles) != 1 or articles[0].get("@id") != url + "#article" or len(breadcrumbs) != 1:
            errors.append(f"Article schema or breadcrumbs missing: {url}")

if errors:
    print("LIVE AI DISCOVERY CHECK FAILED:")
    for item in errors:
        print(" - " + item)
    sys.exit(1)
print(f"LIVE AI DISCOVERY CHECK PASS: {len(urls)} live canonical pages, AI crawler permissions, llms.txt and structured data.")
