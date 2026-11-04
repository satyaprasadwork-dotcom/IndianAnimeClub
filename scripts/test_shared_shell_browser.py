#!/usr/bin/env python3
"""Browser-check identical header and footer on desktop and mobile."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT=Path(".").resolve()
REPORTS=ROOT/"reports"
REPORTS.mkdir(exist_ok=True)

class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,directory=str(ROOT),**kwargs)
    def log_message(self,*args):
        pass

server=ThreadingHTTPServer(("127.0.0.1",0),Handler)
Thread(target=server.serve_forever,daemon=True).start()
base=f"http://127.0.0.1:{server.server_port}"
paths=[
  "/",
  "/about/",
  "/contact/",
  "/community-guidelines/",
  "/editorial-policy/",
  "/privacy-policy/",
  "/terms/",
  "/disclaimer/",
  "/leadership/",
  "/articles/",
  "/articles/beyond-power-levels-how-to-analyse-anime-writing-worldbuilding-and-character-growth.html",
]
# Every article can bring its own legacy CSS. Check all of them, including flat
# information-page sources used directly by Apache/LiteSpeed hosting.
paths += ['/' + p.as_posix() for p in sorted(Path('articles').glob('*.html')) if p.name != 'index.html']
paths += ['/' + p.name for p in sorted(Path('.').glob('*.html')) if p.name != 'index.html']
paths = list(dict.fromkeys(paths))
try:
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        for width in (320,390,768,820,900,1024,1280):
            label = 'mobile' if width <= 900 else 'desktop'
            viewport = {"width":width,"height":850}
            ctx=browser.new_context(viewport=viewport,is_mobile=label=="mobile",has_touch=label=="mobile")
            ctx.route("https://**/*",lambda r:r.abort())
            reference_header=None
            reference_footer=None
            for i,path in enumerate(paths):
                page=ctx.new_page()
                page.goto(base+path,wait_until="domcontentloaded",timeout=25000)
                page.wait_for_function(
                    "() => {const img=document.querySelector('nav.legacy-site-nav .iac-brand-mark');return !!img && img.complete && img.naturalWidth>0;}"
                )
                header=page.locator("nav.legacy-site-nav[aria-label='Main navigation']")
                footer=page.locator("footer.iac-footer")
                if header.count()!=1 or footer.count()!=1:
                    raise AssertionError(f"{path}: missing or duplicate header/footer")
                h=header.evaluate("(el)=>el.outerHTML")
                f=footer.evaluate("(el)=>el.outerHTML")
                if reference_header is None:
                    reference_header=h
                    reference_footer=f
                elif h!=reference_header or f!=reference_footer:
                    raise AssertionError(f"{path}: shared header/footer differs from homepage")
                img=header.locator("img.iac-brand-mark")
                display=img.evaluate("(el) => ({display:getComputedStyle(el).display,visibility:getComputedStyle(el).visibility,width:el.getBoundingClientRect().width})")
                if display["display"]=="none" or display["visibility"]=="hidden" or display["width"]<30:
                    raise AssertionError(f"{path}: logo hidden or too small: {display}")
                color=footer.evaluate("(el)=>getComputedStyle(el).backgroundColor")
                if color!="rgb(6, 24, 44)":
                    raise AssertionError(f"{path}: inconsistent footer color {color}")
                # Compare the visible header as well as the HTML structure.
                appearance=header.evaluate("""el=>{
                  const box=el.getBoundingClientRect();
                  const mark=el.querySelector('.iac-brand-mark').getBoundingClientRect();
                  const link=el.querySelector('#site-links a');
                  return {
                    background:getComputedStyle(el).backgroundColor,
                    border:getComputedStyle(el).borderBottomColor,
                    height:Math.round(box.height),
                    logoWidth:Math.round(mark.width),
                    menuItemColor:getComputedStyle(link).color,
                    label:el.querySelector('.iac-brand').getAttribute('aria-label'),
                    elements:[...el.querySelectorAll('.wrap,.iac-brand,.ln,#site-links,#site-links a,.btn,#menu')].map(node=>{
                      const s=getComputedStyle(node),r=node.getBoundingClientRect();
                      return {font:s.fontFamily,size:s.fontSize,weight:s.fontWeight,line:s.lineHeight,
                        padding:s.padding,margin:s.margin,display:s.display,gap:s.gap,
                        x:Math.round(r.x),y:Math.round(r.y),width:Math.round(r.width),height:Math.round(r.height)};
                    })
                  };
                }""")
                if appearance["background"]!="rgba(255, 243, 224, 0.97)":
                    raise AssertionError(f"{path}: incorrect header background {appearance}")
                if appearance["border"]!="rgb(255, 90, 31)":
                    raise AssertionError(f"{path}: incorrect header border {appearance}")
                if appearance["logoWidth"]<38:
                    raise AssertionError(f"{path}: header logo too narrow {appearance}")
                if i==0:
                    reference_appearance=appearance
                elif appearance!=reference_appearance:
                    raise AssertionError(f"{path}: header styling differs from homepage: {appearance} != {reference_appearance}")
                if path.startswith("/articles/") and path.endswith(".html"):
                    bad=page.locator("article.article > header.article-hero").evaluate(
                        "(el)=>el.firstChild?.nodeType===3 ? el.firstChild.textContent.trim() : ''")
                    if bad in ['">', '>"', '>']:
                        raise AssertionError("Orphan quote/bracket still appears above article")
                if label=="mobile":
                    menu=header.locator("button#menu")
                    menu.click()
                    if menu.get_attribute("aria-expanded")!="true" or "open" not in header.get_attribute("class"):
                        raise AssertionError(f"{path}: mobile menu did not open")
                    links=header.locator('#site-links')
                    if not links.is_visible():
                        raise AssertionError(f"{path}: open menu links are hidden")
                    menu.press('Escape')
                    if menu.get_attribute("aria-expanded")!="false" or "open" in header.get_attribute("class"):
                        raise AssertionError(f"{path}: mobile menu did not close")
                if i in (0,1,5,10):
                    shot = {0:'home',1:'about',5:'privacy',10:'article'}[i]
                    page.screenshot(path=str(REPORTS/f"shared-shell-{width}-{shot}.png"),full_page=False)
                controls=header.locator('.iac-brand,.btn,#menu').evaluate_all("""nodes=>nodes.filter(n=>getComputedStyle(n).display!=='none').map(n=>{const b=n.getBoundingClientRect();return {left:b.left,right:b.right}})""")
                controls.sort(key=lambda b:b['left'])
                if any(a['right'] > b['left'] + 1 for a,b in zip(controls,controls[1:])):
                    raise AssertionError(f"{path} at {width}px: header controls overlap")
                page.close()
            ctx.close()
        browser.close()
finally:
    server.shutdown()
print(f"Shared header typography, geometry, controls and footer pass on {len(paths)} routes at seven mobile, tablet and desktop widths.")
