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
    image_tags = re.findall(r'<figure\b[^>]*class="article-featured-image"[^>]*>\s*<img\b[^>]*>', markup)
    assert len(image_tags) == 1, f"{article}: expected one featured image, found {len(image_tags)}"
    image_tag = re.search(r'<figure\b[^>]*class="article-featured-image"[^>]*>\s*<img\b[^>]*>', markup)
    assert image_tag and 'max-width:640px!important' in image_tag.group(0), article
    source = re.search(r'src="([^"]+\.svg)"', image_tag.group(0))
    assert source and source.group(1).startswith("/images/articles/"), article
    asset = root / source.group(1).lstrip("/")
    assert asset.is_file() and asset.stat().st_size > 200, f"{article}: missing featured image {asset}"


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
                response = page.goto(f"http://127.0.0.1:{server.server_port}/{article.relative_to(root).as_posix()}",
                                     wait_until="domcontentloaded", timeout=25000)
                assert response and response.status == 200, (
                    f"{article}: expected HTTP 200, got {response.status if response else 'no response'}")
                # Geometry can be measured before an SVG has decoded; intrinsic
                # naturalWidth is not a reliable readiness signal for these SVGs.
                # Every referenced source image is checked on disk above.
                try:
                    page.locator('figure.article-featured-image img').wait_for(state="attached", timeout=8000)
                except Exception:
                    print(f"DOM DIAGNOSTIC {article.name}: {page.url}")
                    print(page.locator('body').inner_html()[:2000])
                    raise
                metrics = page.evaluate("""() => {
                    const figure = document.querySelector('figure.article-featured-image');
                    const img = figure.querySelector('img');
                    const content = document.querySelector('.article-reading-layout');
                    const f = figure.getBoundingClientRect();
                    const i = img.getBoundingClientRect();
                    const c = content.getBoundingClientRect();
                    return {
                        figWidth: f.width, figLeft: f.left, figRight: f.right,
                        figBottom: f.bottom, imageWidth: i.width, imageHeight: i.height,
                        contentTop: c.top, position: getComputedStyle(img).position,
                        imgNaturalWidth: img.naturalWidth,
                        figureParent:figure.parentElement?.className,
                        inlineStyle:figure.getAttribute('style'),
                        computedWidth:getComputedStyle(figure).width,
                        loadedCss:[...document.styleSheets].map(s=>s.href).filter(Boolean)
                    };
                }""")
                label=f"{article.name} at {width}px: {metrics}"
                assert metrics["figWidth"] <= min(width, 642), label
                assert metrics["imageHeight"] <= 362, label
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
