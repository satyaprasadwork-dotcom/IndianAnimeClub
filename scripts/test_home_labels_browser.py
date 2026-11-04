#!/usr/bin/env python3
"""Check orange entry labels fit their existing cards at mobile/desktop widths."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright

root=Path(".").resolve()
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,directory=str(root),**kwargs)
    def log_message(self,*args):
        pass

server=ThreadingHTTPServer(("127.0.0.1",0),Handler)
Thread(target=server.serve_forever,daemon=True).start()
try:
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        for width in (320,390,640,768,987,1280):
            ctx=browser.new_context(viewport={"width":width,"height":820})
            ctx.route("https://**/*",lambda r:r.abort())
            page=ctx.new_page()
            page.goto(f"http://127.0.0.1:{server.server_port}/",wait_until="domcontentloaded")
            rows=page.locator("#events .ev")
            assert rows.count()==4, f"Expected four starting-point cards, got {rows.count()}"
            labels=rows.locator(".date .date-label")
            assert labels.count()==4, f"Missing bounded date labels at {width}px"
            for index in range(4):
                data=rows.nth(index).evaluate("""row=>{
                    const label=row.querySelector('.date-label');
                    const tile=label.closest('.date'), description=row.querySelector('.date + div');
                    const box=tile.getBoundingClientRect(), text=label.getBoundingClientRect();
                    const copy=description.getBoundingClientRect();
                    const s=getComputedStyle(label);
                    return {
                      text:label.textContent, labelWidth:label.clientWidth,
                      naturalScrollWidth:label.scrollWidth,
                      tileRight:box.right, contentLeft:copy.left,
                      labelLeft:text.left, labelRight:text.right,
                      tileLeft:box.left, overflow:s.overflowWrap, fontSize:parseFloat(s.fontSize)
                    };
                }""")
                assert data["naturalScrollWidth"] <= data["labelWidth"] + 1, (
                    f"Label content overflows its own box at {width}px: {data}")
                assert data["labelLeft"] >= data["tileLeft"] - 3, (
                    f"Label protrudes on left at {width}px: {data}")
                assert data["labelRight"] <= data["tileRight"] + 3, (
                    f"Label protrudes on right at {width}px: {data}")
                assert data["tileRight"] <= data["contentLeft"] + 8, (
                    f"Orange badge overlaps description at {width}px: {data}")
                assert data["fontSize"] >= 10, (
                    f"Label would be too small at {width}px: {data}")
            print(f"PASS orange labels fit at viewport {width}px")
            page.close()
            ctx.close()
        browser.close()
finally:
    server.shutdown()
