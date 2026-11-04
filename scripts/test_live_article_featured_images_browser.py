#!/usr/bin/env python3
"""Verify actual rendered featured-image geometry on the public custom domain."""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "https://indiananimeclub.com"
NONCE = os.environ.get("GITHUB_RUN_ID", "local")
PATHS = [
    "/anime-between-lectures-and-chai-breaks-inside-indias-college-fan-culture/",
    "/why-anime-underdogs-resonate-with-indian-audiences-effort-family-expectations-and-ambition/",
    "/your-first-cosplay-on-a-budget-planning-a-costume-with-materials-available-in-india/",
]
Path("reports").mkdir(exist_ok=True)

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    try:
        for viewport in (390, 1440):
            ctx = browser.new_context(viewport={"width": viewport, "height": 900})
            # Third-party scripts are irrelevant to image sizing; prevent their
            # network delays without blocking our own images or stylesheets.
            ctx.route("**/*", lambda route: route.continue_()
                      if route.request.url.startswith(BASE + "/")
                      else route.abort())
            for index, path in enumerate(PATHS):
                page = ctx.new_page()
                url = BASE + path + "?iac_image_test=" + NONCE
                response = page.goto(url, wait_until="domcontentloaded", timeout=30000)
                assert response and response.status == 200, (
                    f"{url} returned {response.status if response else 'no response'}")
                try:
                    page.locator("figure.article-featured-image img").wait_for(
                        state="attached", timeout=10000)
                except Exception:
                    print("DOM summary:", page.locator("body").inner_html()[:1800])
                    raise
                page.wait_for_timeout(300)
                dims = page.evaluate("""() => {
                    const f = document.querySelector('figure.article-featured-image');
                    const i = f.querySelector('img');
                    const fr = f.getBoundingClientRect();
                    const ir = i.getBoundingClientRect();
                    const viewportWidth = document.documentElement.clientWidth;
                    const fs = getComputedStyle(f);
                    const istyle = getComputedStyle(i);
                    return {
                        viewportWidth,
                        figureWidth:fr.width, figureLeft:fr.left, figureRight:fr.right,
                        imageWidth:ir.width, imageHeight:ir.height,
                        figureMaxWidth:fs.maxWidth, imageMaxHeight:istyle.maxHeight,
                        position:istyle.position, inlineStyle:f.getAttribute('style'),
                        source:i.currentSrc, parent:f.parentElement?.className,
                        styleSheets:[...document.styleSheets].map(x=>x.href).filter(Boolean)
                    };
                }""")
                print(f"LIVE {viewport}px {path}: {dims}", flush=True)
                page.screenshot(path=f"reports/live-feature-{viewport}-{index}.png")
                assert dims["figureWidth"] > 0 and dims["imageWidth"] > 0, dims
                assert dims["figureWidth"] <= min(962, viewport + 2), dims
                assert dims["imageHeight"] <= 542, dims
                assert dims["figureLeft"] >= -1 and dims["figureRight"] <= viewport + 1, dims
                assert abs((dims["figureLeft"] + dims["figureWidth"]/2) - viewport/2) <= 35, dims
                assert dims["position"] == "static", dims
                assert "max-width:960px!important" in (dims["inlineStyle"] or ""), dims
                page.close()
            ctx.close()
    finally:
        browser.close()
print("LIVE ARTICLE FEATURED IMAGES: PASS")
