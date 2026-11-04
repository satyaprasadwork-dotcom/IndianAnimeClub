#!/usr/bin/env python3
"""Prevent any public/contact email except the approved Indian Anime Club inbox."""
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
ALLOWED="satyaprasadwork@gmail.com"
SUFFIXES={".html",".js",".css",".json",".md",".xml",".txt",".py",".yml",".yaml"}
errors=[]
scanned=0
matches=0
for file in sorted(ROOT.rglob("*")):
    if not file.is_file() or file.suffix.lower() not in SUFFIXES:
        continue
    if any(part in {".git","node_modules","reports","__pycache__"} for part in file.relative_to(ROOT).parts):
        continue
    scanned+=1
    content=file.read_text(encoding="utf-8",errors="replace")
    for match in re.finditer(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",content):
        matches+=1
        address=match.group().lower()
        if address!=ALLOWED:
            errors.append(f"{file.relative_to(ROOT)}: unexpected email {address}")
required=["contact.html","contact/index.html","partials/footer.html","index.html","articles/index.html"]
for filename in required:
    if ALLOWED not in (ROOT/filename).read_text(encoding="utf-8"):
        errors.append(f"{filename} is missing approved contact email")
if errors:
    print("EMAIL CONSISTENCY AUDIT FAILED:")
    for e in errors:print(" - "+e)
    sys.exit(1)
print(f"Email audit passed: {scanned} text files scanned, {matches} email mentions, sole address {ALLOWED}.")
