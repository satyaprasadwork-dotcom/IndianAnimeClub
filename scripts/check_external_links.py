#!/usr/bin/env python3
"""Non-blocking weekly editorial report on unique external source URLs.
Sites may deny automated requests; 403, 429 and timeouts are NOT broken-link proof.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import json
import sys

IGNORE = {"indiananimeclub.com", "www.indiananimeclub.com", "fonts.googleapis.com",
          "fonts.gstatic.com", "instagram.com", "www.instagram.com",
          "chat.whatsapp.com", "www.facebook.com", "facebook.com"}
class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = set()
    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        url = dict(attrs).get("href", "")
        if url.startswith(("http://", "https://")) and (urlparse(url).hostname or "").lower() not in IGNORE:
            self.urls.add(url)

all_urls = set()
for path in sorted(Path("articles").glob("*.html")):
    if path.name == "index.html":
        continue
    parser = Links()
    parser.feed(path.read_text(encoding="utf-8"))
    all_urls.update(parser.urls)
results = []
for url in sorted(all_urls):
    status = "unverified"
    detail = ""
    for method in ("HEAD", "GET"):
        try:
            req = Request(url, headers={"User-Agent": "IndianAnimeClubEditorialLinkCheck/1.0",
                                        "Accept": "text/html,application/xhtml+xml,*/*"}, method=method)
            with urlopen(req, timeout=9) as response:
                code = response.status
            status = "ok" if 200 <= code < 400 else "review"
            detail = str(code)
            break
        except HTTPError as err:
            detail = str(err.code)
            if err.code in (404, 410):
                status = "possible-broken"
                break
            if err.code in (403, 429):
                status = "blocked-or-rate-limited"
                break
        except (URLError, TimeoutError, OSError) as err:
            detail = type(err).__name__
            if method == "GET":
                status = "unverified"
    results.append({"url": url, "result": status, "detail": detail})
Path("link-check-report.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
for result in results:
    if result["result"] != "ok":
        print(f'{result["result"]}: {result["url"]} ({result["detail"]})')
print(f"Checked {len(results)} unique editorial links. Reports require human review.")
# Do not break site deployments on third-party outages or anti-bot blocking.
