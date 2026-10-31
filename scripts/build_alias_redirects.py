#!/usr/bin/env python3
"""Generate browser-friendly redirect aliases only in the deployed Pages artifact.
The source HTML is kept intact for editorial review and source SEO checks.
Apache/LiteSpeed deployments use .htaccess for real 301 redirects.
"""
from html import escape
from pathlib import Path
import re

DOMAIN = "https://indiananimeclub.com"
paths = list(Path(".").glob("*.html")) + list(Path("articles").glob("*.html"))
changed = []
for path in paths:
    if path.name == "index.html":
        continue
    raw = path.read_text(encoding="utf-8")
    match = re.search(r'<link\b[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', raw, re.I)
    if not match:
        continue
    canonical = match.group(1)
    if not canonical.startswith(DOMAIN + "/") or not canonical.endswith("/"):
        continue
    target = canonical[len(DOMAIN):]
    # Do not redirect if the clean canonical route was not successfully generated.
    clean_target = Path(target.strip("/")) / "index.html"
    if not clean_target.is_file():
        raise SystemExit(f"Cannot redirect {path}: clean target missing: {clean_target}")
    path.write_text(
        '<!doctype html><html lang="en-IN"><head><meta charset="utf-8">'
        '<meta name="robots" content="noindex,follow">'
        '<link rel="canonical" href="' + escape(canonical, quote=True) + '">'
        '<meta http-equiv="refresh" content="0;url=' + escape(target, quote=True) + '">'
        '<title>Page moved | Indian Anime Club</title></head>'
        '<body><p>This page moved to <a href="' + escape(target, quote=True) +
        '">its new address</a>.</p></body></html>\n',
        encoding="utf-8")
    changed.append(str(path))
print("Clean route redirects:", len(changed))
