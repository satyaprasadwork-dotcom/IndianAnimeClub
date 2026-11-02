#!/usr/bin/env python3
"""Run the original, no-account watchlist planner in desktop and mobile Chromium."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright

root=Path(".").resolve()
class Silent(SimpleHTTPRequestHandler):
    def __init__(self,*a,**k):super().__init__(*a,directory=str(root),**k)
    def log_message(self,*a):pass
server=ThreadingHTTPServer(("127.0.0.1",0),Silent)
Thread(target=server.serve_forever,daemon=True).start()
try:
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        for width in (390,1280):
            context=browser.new_context(viewport={"width":width,"height":850})
            context.route("https://**/*",lambda route:route.abort())
            page=context.new_page()
            page.goto(f"http://127.0.0.1:{server.server_port}/watchlist-planner/",wait_until="domcontentloaded")
            page.wait_for_function("document.querySelector('#iac-total-episodes').textContent === '12'")
            assert "288 of 300" in page.locator("#iac-time-result").inner_text()
            assert page.locator("#iac-result-list li").count()==1
            page.locator("#iac-weekly-hours").fill("1")
            page.get_by_role("button",name="Calculate my week").click()
            assert page.locator("#iac-total-episodes").inner_text()=="2"
            page.locator("#iac-budget-limit").fill("100")
            page.locator("#iac-budget-spend").fill("150")
            page.get_by_role("button",name="Calculate my week").click()
            assert "over your ceiling" in page.locator("#iac-money-result").inner_text()
            page.get_by_role("button",name="+ Add another anime").click()
            assert page.locator(".iac-series-row").count()==2
            page.locator(".iac-series-row").nth(0).locator(".iac-series-episodes").fill("0")
            page.locator(".iac-series-row").nth(1).locator(".iac-series-title").fill("Next show")
            page.get_by_role("button",name="Calculate my week").click()
            assert page.locator("#iac-total-episodes").inner_text()=="2"
            assert "Next show" in page.locator("#iac-result-list").inner_text()
            dimensions=page.evaluate("({scroll:document.documentElement.scrollWidth,inner:innerWidth})")
            assert dimensions["scroll"]<=dimensions["inner"]+2,(width,dimensions)
            page.close();context.close()
        browser.close()
finally:server.shutdown()
print("Original watchlist planner calculations, budget warning and responsive layout pass in Chromium.")
