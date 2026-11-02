#!/usr/bin/env python3
"""Regression test for visible editorial sources and shareable article pagination."""
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright
import re

ROOT=Path(".").resolve()
class Silent(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,directory=str(ROOT),**kwargs)
    def log_message(self,*args):pass

class SourceLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag=="a":
            href=dict(attrs).get("href","")
            if href.startswith(("http://","https://")):self.links.append(href)

server=ThreadingHTTPServer(("127.0.0.1",0),Silent)
Thread(target=server.serve_forever,daemon=True).start()
base=f"http://127.0.0.1:{server.server_port}"
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={"width":390,"height":850})
        page.route("https://**/*",lambda route:route.abort())
        page.goto(base+"/articles/",wait_until="domcontentloaded")
        def visible():
            return page.locator("#article-grid > .card:visible").count()
        assert visible()==15,("initial archive",visible())
        assert page.locator("[data-filter='rankings']").count()==0
        assert page.locator("[data-filter='recommendations']").count()==0
        page.locator("#pagination a",has_text="2").click()
        assert visible()==15
        assert "page=2" in page.url
        page.locator("#pagination a",has_text="3").click()
        assert visible()==1,("last page",visible())
        assert "page=3" in page.url
        page.go_back(wait_until="domcontentloaded")
        assert visible()==15
        page.get_by_role("button",name="Characters",exact=True).click()
        assert visible()==3 and "category=character-studies" in page.url
        page.reload(wait_until="domcontentloaded")
        assert visible()==3,("filtered URL not shareable",visible())
        page.goto(base+"/articles/",wait_until="domcontentloaded")
        assert visible()==15
        for slug in (
            "anime-between-lectures-and-chai-breaks-inside-indias-college-fan-culture",
            "where-to-watch-anime-legally-in-india-a-practical-guide-to-platforms-languages-and-availability",
            "this-anime-scene-changed-how-fans-look-at-life",
        ):
            raw=(ROOT/"articles"/(slug+".html")).read_text(encoding="utf-8")
            section=re.search(r'<section\b[^>]*class="sources"[^>]*>(.*?)</section>',raw,re.I|re.S)
            assert section,("missing committed source section",slug)
            parser=SourceLinks()
            parser.feed(section.group(1))
            expected=parser.links
            page.goto(base+"/articles/"+slug+".html",wait_until="networkidle")
            actual=page.locator("article.article .sources a[href]").evaluate_all(
                "(els)=>els.map(el=>el.getAttribute('href')).filter(url=>url.startsWith('http'))"
            )
            assert actual==expected,(slug,expected,actual)
        browser.close()
finally:server.shutdown()
print("Archive URLs and reviewed editorial source lists remain intact in Chromium.")
