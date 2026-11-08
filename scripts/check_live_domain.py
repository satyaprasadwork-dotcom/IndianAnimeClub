#!/usr/bin/env python3
"""Inspect actual public custom-domain HTML after deploy; GitHub Pages success alone is insufficient."""
from html.parser import HTMLParser
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
import os
import re
from pathlib import Path
from datetime import date
import sys
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

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

# The published CSS, not only the repository or a completed Pages run, must
# include the article-image containment fix. This catches stale CDN builds that
# kept showing giant featured images despite updated source code.
shared_css=get("/site-shell.css",True)
if shared_css and ("ARTICLE FEATURED IMAGE SIZING" not in shared_css or
                   "max-width:960px !important;" not in shared_css):
    errors.append("CUSTOM DOMAIN STALE: Shared stylesheet does not contain the bounded 960px featured-image fix.")
if shared_css and "ARTICLE TOC SCROLL CONTAINMENT" not in shared_css:
    errors.append("CUSTOM DOMAIN STALE: Public shared stylesheet lacks the article TOC scroll fix.")
article_css=get("/css/article.css",True)
if article_css and "width:min(100%,960px)" not in article_css:
    errors.append("CUSTOM DOMAIN STALE: Primary article stylesheet does not contain the bounded featured-image fallback.")
sample_article=get("/anime-between-lectures-and-chai-breaks-inside-indias-college-fan-culture/",True)
if sample_article:
    article_ref=re.search(r'href="(/site-shell\.css\?v=[^"]+)"',sample_article)
    if not article_ref:
        errors.append("CUSTOM DOMAIN STALE: Published article is missing its versioned shared stylesheet.")
    else:
        if "v=20261104-header" in article_ref.group(1):
            errors.append("CUSTOM DOMAIN STALE: Article HTML refers to the previous shared CSS version.")
        loaded_css=get(article_ref.group(1))
        if loaded_css and "ARTICLE TOC SCROLL CONTAINMENT" not in loaded_css:
            errors.append("CUSTOM DOMAIN STALE: Article's actual versioned CSS lacks the TOC fix.")
if sample_article and ('<figure class="article-featured-image" style=' not in sample_article or
                       'max-width:960px!important' not in sample_article):
    errors.append("CUSTOM DOMAIN STALE: Article does not contain the inline featured-image width cap.")

homepage=get("/",True)
if homepage and ('id="featured-reading"' not in homepage or 'href="/watchlist-planner/"' not in homepage):
    errors.append("CUSTOM DOMAIN STALE: Homepage is missing the editorial section or linked planner.")
archive=get("/articles/",True)
if archive and ('data-filter="rankings"' in archive or 'data-filter="recommendations"' in archive):
    errors.append("CUSTOM DOMAIN STALE: Archive still exposes empty Rankings/Recommendations filters.")
if archive and '<p class="eyebrow" style="color:#07182b!important">Stories, analysis &amp; guides</p>' not in archive:
    errors.append("CUSTOM DOMAIN STALE: Archive is missing the dark navy Stories, analysis & guides heading.")
if archive:
    css_ref=re.search(r'href="(/site-shell\.css\?v=[^"]+)"',archive)
    if not css_ref:
        errors.append("CUSTOM DOMAIN STALE: Archive is missing its versioned shared stylesheet reference.")
    else:
        if "v=9ff0c1af6f08" in css_ref.group(1):
            errors.append("CUSTOM DOMAIN STALE: Archive still references the old shared CSS cache key.")
        loaded_css=get(css_ref.group(1))
        if loaded_css and "ARTICLE TOC SCROLL CONTAINMENT" not in loaded_css:
            errors.append("CUSTOM DOMAIN STALE: Archive's actual versioned CSS lacks the TOC fix.")
if archive and "history.pushState" not in archive:
    errors.append("CUSTOM DOMAIN STALE: Archive lacks shareable pagination script.")
planner=get("/watchlist-planner/",True)
if planner and 'id="iac-watch-form"' not in planner:
    errors.append("CUSTOM DOMAIN STALE: The original watchlist tool is absent.")
sitemap=get("/sitemap.xml",True)
if sitemap:
    try:
        urls=[el.text.strip() for el in ET.fromstring(sitemap).findall(".//{*}loc") if el.text]
        if BASE+"/watchlist-planner/" not in urls or len(urls)<38:
            errors.append(f"Custom-domain sitemap does not contain all expected public routes ({len(urls)} found).")
    except ET.ParseError as exc:errors.append(f"Custom-domain sitemap XML invalid: {exc}")
# Confirm the public domain, not just GitHub, serves AI discovery instructions.
llms=get("/llms.txt",True)
if llms and ("# Indian Anime Club" not in llms or "## Selected editorial guides" not in llms):
    errors.append("CUSTOM DOMAIN STALE: /llms.txt does not contain the new AI discovery guide.")
robots=get("/robots.txt",True)
if robots:
    required_agents=("OAI-SearchBot", "GPTBot", "ChatGPT-User", "ClaudeBot",
                     "PerplexityBot", "Google-Extended", "Applebot-Extended", "CCBot")
    for agent in required_agents:
        if f"User-agent: {agent}" not in robots:
            errors.append(f"CUSTOM DOMAIN STALE: /robots.txt missing permission for {agent}.")
if homepage and '"@id":"https://indiananimeclub.com/#website"' not in homepage:
    errors.append("CUSTOM DOMAIN STALE: Homepage lacks the linked WebSite structured data.")
if archive and '"@type":"CollectionPage"' not in archive:
    errors.append("CUSTOM DOMAIN STALE: Archive lacks CollectionPage structured data.")
if sample_article and ('"@type":"BlogPosting"' not in sample_article or
                       'id="iac-article-breadcrumb"' not in sample_article):
    errors.append("CUSTOM DOMAIN STALE: Article lacks BlogPosting or breadcrumb structured data.")

ads=get("/ads.txt",True)
if ads and "pub-7937216909291905" not in ads:
    errors.append("Public ads.txt does not contain the expected authorised publisher ID.")
# Verify actual HTML tag parity for every canonical URL, not only GitHub source files.
# Limited concurrency avoids aggressive traffic while surfacing stale cache/deploys.
def verify_tracking_url(url):
    if not url.startswith(BASE + "/"):
        return f"Unknown sitemap domain: {url}"
    html=get(url[len(BASE):],True)
    if not html:
        return f"Could not retrieve public canonical page: {url}"
    found_emails={email.lower() for email in re.findall(
        r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",html)}
    unexpected=found_emails-{"satyaprasadwork@gmail.com"}
    if unexpected:
        return f"{url}: unexpected public email(s): {sorted(unexpected)}"
    head=html.split("</head>",1)[0]
    if '<article class="article">' in html:
        article_slug=url[len(BASE):].strip("/")
        local=Path(__file__).resolve().parents[1]/"articles"/f"{article_slug}.html"
        if not local.is_file():
            return f"{url}: live article missing matching source file"
        expected_match=re.search(r'"dateModified":"(\d{4}-\d{2}-\d{2})"',local.read_text(encoding="utf-8"))
        if not expected_match:
            return f"{url}: local Article dateModified is missing"
        expected_iso=expected_match.group(1)
        stamp=date.fromisoformat(expected_iso)
        human=f"Updated {stamp.day} {stamp.strftime('%B %Y')}"
        if f'"dateModified":"{expected_iso}"' not in html or human not in html:
            return f"{url}: stale article updated date; expected {expected_iso} and {human}."
    if '<article class="article">' in html:
        featured=re.search(r'<figure\b[^>]*class="article-featured-image"[^>]*>', html)
        if not featured or 'max-width:960px!important' not in featured.group(0):
            return f"{url}: article featured image lacks its inline 960px max-width."
    checks={
        "GA4 script":"https://www.googletagmanager.com/gtag/js?id=G-M4738D1ZND",
        "GA4 initialization":"gtag('config','G-M4738D1ZND')",
        "AdSense script":"https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7937216909291905",
        "Microsoft Clarity loader":"https://www.clarity.ms/tag/",
        "Clarity initialization":'"ywqdm8xkj7"',
        "Canonical tracking block":"IAC_TRACKING_START",
        "Canonical tracking end":"IAC_TRACKING_END"
    }
    for name,needle in checks.items():
        if head.count(needle)!=1:
            return f"{url}: {name} expected once, found {head.count(needle)}"
    return None

if sitemap and 'urls' in locals() and urls:
    with ThreadPoolExecutor(max_workers=4) as pool:
        for failure in pool.map(verify_tracking_url,urls):
            if failure:errors.append(failure)

if errors:
    print("LIVE CUSTOM-DOMAIN VERIFICATION FAILED:")
    for e in errors:print(" - "+e)
    print("Check whether Hostinger serves an older artifact, the GitHub Pages custom-domain/DNS configuration, or CDN cache. Do not assume successful GitHub Pages deployment updated the public domain.")
    sys.exit(1)
print(f"Public custom domain passed all {len(urls)} canonical page tracking checks, editorial navigation, planner, sitemap and ads.txt.")
print("This is not an AdSense policy approval, independent content audit, or proof of regional CMP compliance.")
