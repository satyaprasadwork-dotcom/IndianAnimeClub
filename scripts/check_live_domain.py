#!/usr/bin/env python3
"""Inspect actual public custom-domain HTML after deploy; GitHub Pages success alone is insufficient."""
from html.parser import HTMLParser
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
import os
import sys
import time
import xml.etree.ElementTree as ET

BASE="https://indiananimeclub.com"
NONCE=os.environ.get("GITHUB_RUN_ID") or str(int(time.time()))
errors=[]
def get(path,add_nonce=False):
    suffix=("&" if "?" in path else "?")+"iac_audit="+NONCE if add_nonce else ""
    url=BASE+path+suffix
    try:
        request=Request(url,headers={"User-Agent":"IndianAnimeClubLiveReleaseAudit/1.0",
                                    "Cache-Control":"no-cache","Pragma":"no-cache"})
        with urlopen(request,timeout=22) as response:
            body=response.read(2_000_000).decode("utf-8","replace")
            if response.status!=200:
                errors.append(f"{url} returned HTTP {response.status}")
            return body
    except (HTTPError,URLError,TimeoutError,OSError) as exc:
        errors.append(f"{url} unavailable: {exc}")
        return ""

homepage=get("/",True)
if homepage and ('id="featured-reading"' not in homepage or 'href="/watchlist-planner/"' not in homepage):
    errors.append("CUSTOM DOMAIN STALE: Homepage is missing the editorial section or linked planner.")
archive=get("/articles/",True)
if archive and ('data-filter="rankings"' in archive or 'data-filter="recommendations"' in archive):
    errors.append("CUSTOM DOMAIN STALE: Archive still exposes empty Rankings/Recommendations filters.")
if archive and "history.pushState" not in archive:
    errors.append("CUSTOM DOMAIN STALE: Archive lacks shareable pagination script.")
planner=get("/watchlist-planner/",True)
if planner and 'id="iac-watch-form"' not in planner:
    errors.append("CUSTOM DOMAIN STALE: The original watchlist tool is absent.")
sitemap=get("/sitemap.xml",True)
if sitemap:
    try:
        urls=[el.text.strip() for el in ET.fromstring(sitemap).findall(".//{*}loc") if el.text]
        if BASE+"/watchlist-planner/" not in urls or len(urls)<42:
            errors.append(f"Custom-domain sitemap does not contain all expected public routes ({len(urls)} found).")
    except ET.ParseError as exc:errors.append(f"Custom-domain sitemap XML invalid: {exc}")
ads=get("/ads.txt",True)
if ads and "pub-7937216909291905" not in ads:
    errors.append("Public ads.txt does not contain the expected authorised publisher ID.")
if errors:
    print("LIVE CUSTOM-DOMAIN VERIFICATION FAILED:")
    for e in errors:print(" - "+e)
    print("Check whether Hostinger serves an older artifact, the GitHub Pages custom-domain/DNS configuration, or CDN cache. Do not assume successful GitHub Pages deployment updated the public domain.")
    sys.exit(1)
print("Public custom domain passed editorial, archive, planner, sitemap and ads.txt release checks.")
print("This is not an AdSense policy approval, independent content audit, or proof of regional CMP compliance.")
