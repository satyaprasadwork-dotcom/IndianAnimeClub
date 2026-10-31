#!/usr/bin/env python3
"""Ensure every public source has the exact same visible shared header/footer."""
from pathlib import Path
import re

root=Path(".")
header=(root/"partials/header.html").read_text(encoding="utf-8").strip()
footer=(root/"partials/footer.html").read_text(encoding="utf-8").strip()
pages=sorted(set(list(root.glob("*.html")) + list((root/"articles").glob("*.html")) + list(root.glob("*/index.html"))))
if len(pages)<40:
    raise SystemExit(f"Unexpectedly few site pages: {len(pages)}")
for path in pages:
    html=path.read_text(encoding="utf-8")
    if html.count(header)!=1:
        raise SystemExit(f"{path}: shared header does not match template")
    if html.count(footer)!=1:
        raise SystemExit(f"{path}: shared footer does not match template")
    nav_count = len(re.findall(
        r"""<nav\b(?=[^>]*\baria-label=["']Main navigation["'])[^>]*>""",
        html,
        re.I,
    ))
    if nav_count != 1:
        raise SystemExit(f"{path}: expected one actual main navigation, got {nav_count}")
    if not re.search(r'<img\b[^>]*class="iac-brand-mark"[^>]*src="/favicon\.svg(?:\?[^"]*)?"',html):
        raise SystemExit(f"{path}: visible logo image is missing")
    if not re.search(r'href=["\']/site-shell\.css(?:\?[^"\']*)?["\']',html):
        raise SystemExit(f"{path}: shared stylesheet is missing")
    if 'fonts.googleapis.com/css2?family=Dela+Gothic+One' not in html:
        raise SystemExit(f"{path}: shared navigation fonts are missing")
    if not re.search(r'href=["\']/css/navigation\.css\?v=[a-f0-9]+["\']',html):
        raise SystemExit(f"{path}: versioned navigation styles are missing")
    if not re.search(r'<script[^>]*src="/site-shell\.js(?:\?[^"]*)?"',html):
        raise SystemExit(f"{path}: shared menu script missing")
    if re.search(r'<header\b[^>]*\bclass=["\'][^"\']*\barticle-hero\b[^"\']*["\'][^>]*>\s*["\']>',html):
        raise SystemExit(f"{path}: orphan quote and bracket after article header")
print(f"Shared header, visible logo, footer and clean article tags verified across {len(pages)} source pages.")
