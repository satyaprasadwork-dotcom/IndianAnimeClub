#!/usr/bin/env python3
"""Validate datePublished/dateModified agree with visible article header dates."""
from datetime import date
from pathlib import Path
import json
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
files=sorted((ROOT/"articles").glob("*.html"))
files=[f for f in files if f.name!="index.html"]
errors=[]
if len(files)<27:
    errors.append(f"Only {len(files)} published articles found; expected at least 27.")
for file in files:
    raw=file.read_text(encoding="utf-8")
    match=re.search(r'<script type="application/ld\+json">(\{.*?\})</script>',raw,re.S)
    if not match:
        errors.append(f"{file.name}: Article JSON-LD missing")
        continue
    try:
        schema=json.loads(match.group(1))
        published=date.fromisoformat(schema["datePublished"])
        modified=date.fromisoformat(schema["dateModified"])
    except (ValueError,KeyError,TypeError,json.JSONDecodeError) as exc:
        errors.append(f"{file.name}: Invalid article date metadata: {exc}")
        continue
    display=re.search(
        r'<span class="date">Published\s+(\d{1,2}\s+[A-Za-z]+\s+\d{4})\s*·\s*Updated\s+(\d{1,2}\s+[A-Za-z]+\s+\d{4})</span>',
        raw)
    if not display:
        errors.append(f"{file.name}: Visible publication/updated dates missing")
        continue
    expected_published=f"{published.day} {published.strftime('%B %Y')}"
    expected_modified=f"{modified.day} {modified.strftime('%B %Y')}"
    if (display.group(1),display.group(2))!=(expected_published,expected_modified):
        errors.append(f"{file.name}: Visible dates disagree with structured data")
    if modified<published:
        errors.append(f"{file.name}: Updated date precedes publication")
    if modified>date.today():
        errors.append(f"{file.name}: Updated date is in the future")
if errors:
    print("ARTICLE DATE AUDIT FAILED:")
    for error in errors:print(" - "+error)
    sys.exit(1)
print(f"Article date audit passed for all {len(files)} published articles.")
