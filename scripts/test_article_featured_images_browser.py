#!/usr/bin/env python3
"""Regression test: all article headers contain bounded editorial imagery."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import re
from playwright.sync_api import sync_playwright

root = Path(".").resolve()
articles = sorted(p for p in (root / "articles").glob("*.html") if p.name != "index.html")
assert articles, "No article HTML files found."
for article in articles:
    markup = article.read_text(encoding="utf-8")
    assert len(re.findall(r'<figure class="article-featured-image">', markup)) == 1, article
    assert re.search(r'<figure class="article-featured-image"><img[^>]+>', markup), article

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(root), **kwargs)
    def log_message(self, *args):
        pass

server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
Thread(target=server.serve_forever, daemon=True).start()
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        samples = [articles[0], articles[len(articles)//2], articles[-1]]
        for width in (320, 390, 768, 1280):
            ctx = browser.new_context(viewport={"width": width, "height": 850})
            ctx.route("https://**/*", lambda route: route.abort())
            for article in samples:
                page = ctx.new_page()
                page.goto(f"http://127.0.0.1:{server.server_port}/{article.as_posix()}",
                          wait_until="domcontentloaded", timeout=25000)
                page.wait_for_function("""() => {
                    const image = document.querySelector('.article-featured-image img');
                    return !!image && image.complete && image.naturalWidth > 0;
                }""")
                metrics = page.evaluate("""() => {
                    const figure = document.querySelector('article.article > .article-hero > .article-featured-image');
                    const img = figure.querySelector('img');
                    const content = document.querySelector('.article-reading-layout');
                    const f = figure.getBoundingClientRect();
                    const i = img.getBoundingClientRect();
                    const c = content.getBoundingClientRect();
                    return {
                        figWidth: f.width, figLeft: f.left, figRight: f.right,
                        figBottom: f.bottom, imageWidth: i.width, imageHeight: i.height,
                        contentTop: c.top, position: getComputedStyle(img).position,
                        imgNaturalWidth: img.naturalWidth
                    };
                }""")
                label=f"{article.name} at {width}px: {metrics}"
                assert metrics["figWidth"] <= min(width, 722), label
                assert metrics["imageHeight"] <= 406, label
                assert metrics["figLeft"] >= -1 and metrics["figRight"] <= width+1, label
                assert abs(metrics["imageWidth"]/metrics["imageHeight"]-16/9) < .1, label
                assert metrics["contentTop"] >= metrics["figBottom"]-1, label
                assert metrics["position"] == "static", label
                print(f"PASS {article.stem[:35]} viewport={width}: featured image "
                      f"{metrics['imageWidth']:.0f}x{metrics['imageHeight']:.0f}")
                page.close()
            ctx.close()
        browser.close()
finally:
    server.shutdown()
print(f"Passed: static image markup in {len(articles)} articles and responsive browser geometry.")
