#!/usr/bin/env python3
"""Regression: the article guide never paints shorter than its contents."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright
import re

ROOT = Path(".").resolve()
FILES = sorted((ROOT / "articles").glob("*.html"))
FILES = [p for p in FILES if p.name != "index.html"]
assert len(FILES) == 27, f"Expected 27 retained article templates, got {len(FILES)}"
for file in FILES:
    markup = file.read_text(encoding="utf-8")
    assert markup.count('class="article-sidebar"') == 1, file
    assert markup.count('class="article-toc"') == 1, file
    fragment = re.search(r'<nav class="article-toc"[^>]*>(.*?)</nav>', markup, re.S)
    assert fragment, file
    assert len(re.findall(r'<li>\s*<a href="#', fragment.group(1))) >= 3, file

class QuietHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)
    def log_message(self, *args):
        pass

server = ThreadingHTTPServer(("127.0.0.1", 0), QuietHandler)
Thread(target=server.serve_forever, daemon=True).start()
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        sample = [FILES[0], max(FILES, key=lambda p: p.read_text(encoding="utf-8").count('<li><a href="#')), FILES[-1]]
        sample = list(dict.fromkeys(sample))
        for width in (390, 768, 1024, 1440):
            ctx = browser.new_context(viewport={"width": width, "height": 850})
            ctx.route("https://**/*", lambda route: route.abort())
            for article in sample:
                page = ctx.new_page()
                url = f"http://127.0.0.1:{server.server_port}/articles/{article.name}"
                response = page.goto(url, wait_until="domcontentloaded", timeout=25000)
                assert response and response.status == 200, (url, response.status if response else None)
                locator = page.locator("aside.article-sidebar > nav.article-toc")
                locator.wait_for(state="attached", timeout=10000)
                metrics = locator.evaluate("""toc => {
                  const aside=toc.parentElement, links=[...toc.querySelectorAll('ol li a')];
                  const frame=toc.getBoundingClientRect(), s=getComputedStyle(toc), outer=getComputedStyle(aside);
                  return {links:links.length, height:frame.height, width:frame.width,
                          scrollHeight:toc.scrollHeight, clientHeight:toc.clientHeight,
                          scrollWidth:toc.scrollWidth, clientWidth:toc.clientWidth,
                          navOverflowY:s.overflowY, asideOverflowY:outer.overflowY,
                          background:s.backgroundColor, asideScrollHeight:aside.scrollHeight,
                          asideClientHeight:aside.clientHeight,
                          lastBottom:links.at(-1).getBoundingClientRect().bottom,
                          frameBottom:frame.bottom};
                }""")
                label=f"{article.name} at {width}px: {metrics}"
                assert metrics["links"] >= 3, label
                assert metrics["background"] == "rgb(237, 247, 250)", label
                assert metrics["scrollWidth"] <= metrics["clientWidth"] + 2, label
                if width > 760:
                    assert metrics["navOverflowY"] == "auto", label
                    assert metrics["asideOverflowY"] == "visible", label
                    assert metrics["height"] <= 740, label
                    locator.evaluate("(el) => { el.scrollTop = el.scrollHeight; }")
                    page.wait_for_timeout(80)
                    after = locator.evaluate("""toc => {
                        const r=toc.getBoundingClientRect(), l=toc.querySelector('ol li:last-child a').getBoundingClientRect();
                        return {lastTop:l.top, lastBottom:l.bottom, panelTop:r.top, panelBottom:r.bottom,
                                scrollTop:toc.scrollTop, scrollLimit:toc.scrollHeight-toc.clientHeight};
                    }""")
                    assert after["lastTop"] >= after["panelTop"] - 2, (label, after)
                    assert after["lastBottom"] <= after["panelBottom"] + 2, (label, after)
                    assert after["scrollTop"] >= max(0, after["scrollLimit"]-2), (label, after)
                else:
                    assert metrics["navOverflowY"] == "visible", label
                    assert metrics["scrollHeight"] <= metrics["clientHeight"]+2, label
                    assert metrics["lastBottom"] <= metrics["frameBottom"]+2, label
                print(f"PASS {width}px {article.stem[:38]}: nav {metrics['height']:.0f}px, links={metrics['links']}", flush=True)
                page.close()
            ctx.close()
        browser.close()
finally:
    server.shutdown()
print(f"Article TOC: all {len(FILES)} templates checked, responsive scroll geometry passed.")
