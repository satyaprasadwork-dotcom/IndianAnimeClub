#!/usr/bin/env python3
"""Smoke-test mobile reader navigation on local source files; does not certify live consent."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SLUG = "where-to-watch-anime-legally-in-india-a-practical-guide-to-platforms-languages-and-availability"

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)
    def translate_path(self, path):
        candidate = urlsplit(path).path.strip("/")
        if candidate and "/" not in candidate:
            article = ROOT / "articles" / (candidate + ".html")
            if article.is_file():
                return str(article)
        return super().translate_path(path)
    def log_message(self, *_args):
        pass

server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
Thread(target=server.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{server.server_port}"
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        for width in (320, 390, 768):
            ctx = browser.new_context(viewport={"width":width,"height":820}, is_mobile=True, has_touch=True)
            ctx.route("https://**/*", lambda route: route.abort())
            page = ctx.new_page()
            response = page.goto(base + "/", wait_until="domcontentloaded")
            assert response and response.status == 200
            page.locator(f'a.iac-editorial-media[href="/{SLUG}/"]').first.click()
            page.wait_for_url(f"**/{SLUG}/", timeout=10000)
            assert page.locator("article.article h1").is_visible()
            source = page.locator('.sources a[href^="https://"]').first
            assert source.count() == 1
            href = source.get_attribute("href")
            assert href.startswith("https://")
            if source.get_attribute("target") == "_blank":
                assert "noopener" in (source.get_attribute("rel") or "").split()
            related = page.locator("section.related a[href^='/']").first
            related.wait_for(timeout=10000)
            target = related.get_attribute("href")
            assert target != f"/{SLUG}/", "Related reading loops to the same page"
            related.click()
            page.wait_for_url(f"**{target}", timeout=10000)
            assert page.locator("article.article h1").is_visible()
            page.locator("footer.iac-footer a[href='/privacy-policy/']").first.click()
            page.wait_for_url("**/privacy-policy/", timeout=10000)
            assert page.locator("main h1").is_visible()
            page.goto(base + "/" + SLUG + "/", wait_until="domcontentloaded")
            table = page.locator("section.editorial-evidence div[style*='overflow-x:auto'] table").first
            assert table.count() == 1
            assert table.evaluate("(el) => ['auto','scroll'].includes(getComputedStyle(el.parentElement).overflowX)")
            print(f"Local navigation and evidence-table smoke test passed at {width}px")
            ctx.close()
        browser.close()
finally:
    server.shutdown()
