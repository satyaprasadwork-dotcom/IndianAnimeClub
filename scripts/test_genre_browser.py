#!/usr/bin/env python3
"""Real-browser smoke test for the four interactive homepage genre choices."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT=Path(".").resolve()
OUT=ROOT/"reports"
OUT.mkdir(exist_ok=True)
class QuietHandler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,directory=str(ROOT),**kwargs)
    def log_message(self,*args):
        pass

server=ThreadingHTTPServer(("127.0.0.1",0),QuietHandler)
Thread(target=server.serve_forever,daemon=True).start()
url=f"http://127.0.0.1:{server.server_port}/"
palettes={"Shonen":"#ff5a1f","Sci-fi":"#2677ff","Slice of life":"#e76b9b","Isekai":"#8a5cff"}
try:
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(headless=True)
        for viewport,mobile in [({"width":1280,"height":850},False),({"width":390,"height":844},True)]:
            context=browser.new_context(viewport=viewport,is_mobile=mobile,has_touch=mobile)
            # No offsite requests, analytics side effects or external font dependency in tests.
            context.route("https://**/*",lambda route:route.abort())
            page=context.new_page()
            page.goto(url,wait_until="domcontentloaded",timeout=25000)
            page.wait_for_function("document.documentElement.dataset.genreMood === 'shonen'",timeout=15000)
            for name,color in palettes.items():
                btn=page.get_by_role("button",name=name,exact=True)
                btn.click()
                actual=page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--accent').trim()")
                if actual.lower()!=color:
                    raise AssertionError(f"{name}: expected actual theme {color}, got {actual}")
                selected=page.locator(".chips button[aria-pressed='true']")
                if selected.count()!=1 or selected.first.inner_text().strip()!=name:
                    raise AssertionError(f"Incorrect active genre after selecting {name}")
            # Different genre selection must change actual visual styling, not only aria attributes.
            style=page.get_by_role("button",name="Isekai",exact=True).evaluate(
                "(el) => getComputedStyle(el).backgroundColor")
            if style!="rgb(138, 92, 255)":
                raise AssertionError("Selected button still uses the old fixed orange background: "+style)
            page.screenshot(path=str(OUT/("genre-mobile.png" if mobile else "genre-desktop.png")),full_page=False)
            page.close()
            context.close()
        browser.close()
finally:
    server.shutdown()
print("Genre buttons pass real desktop and mobile Chromium tests.")
