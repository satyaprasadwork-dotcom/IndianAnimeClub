#!/usr/bin/env python3
"""Check the real custom-domain article TOC and archive heading in Chromium."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os

BASE="https://indiananimeclub.com"
NONCE=os.environ.get("GITHUB_RUN_ID","local")
ARTICLES=[
    "/how-to-start-an-anime-club-at-your-college-a-practical-plan-for-indian-student-communities/",
    "/what-makes-an-anime-community-last-lessons-in-belonging-participation-and-local-leadership/",
    "/hindi-tamil-telugu-or-japanese-audio-how-language-changes-the-indian-anime-experience/",
]
Path("reports").mkdir(exist_ok=True)
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True)
    try:
        for width in (390,1440):
            context=browser.new_context(viewport={"width":width,"height":850})
            context.route("**/*",lambda route:route.continue_()
                          if route.request.url.startswith(BASE+"/") else route.abort())
            archive=context.new_page()
            archive.goto(f"{BASE}/articles/?verify_toc={NONCE}",wait_until="domcontentloaded",timeout=30000)
            eyebrow=archive.locator("main#main header.hero > p.eyebrow")
            eyebrow.wait_for(state="visible")
            color=eyebrow.evaluate("(el)=>getComputedStyle(el).color")
            assert color=="rgb(7, 24, 43)",f"Live archive heading colour is {color}, not navy."
            archive.close()
            for number,path in enumerate(ARTICLES):
                page=context.new_page()
                url=BASE+path+"?verify_toc="+NONCE
                response=page.goto(url,wait_until="domcontentloaded",timeout=30000)
                assert response and response.status==200,(url,response.status if response else "no response")
                nav=page.locator("aside.article-sidebar > nav.article-toc")
                nav.wait_for(state="attached",timeout=10000)
                before=nav.evaluate("""toc=>{
                    const r=toc.getBoundingClientRect(), s=getComputedStyle(toc), aside=getComputedStyle(toc.parentElement);
                    return {height:r.height,width:r.width,background:s.backgroundColor,
                      overflow:s.overflowY,asideOverflow:aside.overflowY,
                      scrollHeight:toc.scrollHeight,clientHeight:toc.clientHeight,
                      scrollWidth:toc.scrollWidth,clientWidth:toc.clientWidth,
                      links:toc.querySelectorAll('ol li a').length};
                }""")
                print(f"LIVE TOC {width}px {path}: {before}",flush=True)
                assert before["links"]>=8, (path,before)
                assert before["background"]=="rgb(237, 247, 250)",(path,before)
                assert before["scrollWidth"] <= before["clientWidth"]+2,(path,before)
                if width>760:
                    assert before["overflow"]=="auto",(path,before)
                    assert before["asideOverflow"]=="visible",(path,before)
                    assert before["height"]<=740,(path,before)
                    nav.evaluate("(toc)=>{toc.scrollTop=toc.scrollHeight;}")
                    page.wait_for_timeout(100)
                    after=nav.evaluate("""toc=>{
                      const frame=toc.getBoundingClientRect(),last=toc.querySelector('ol li:last-child a').getBoundingClientRect();
                      return {bottom:frame.bottom,lastBottom:last.bottom,lastTop:last.top,top:frame.top,
                              scrolled:toc.scrollTop,remaining:toc.scrollHeight-toc.clientHeight};
                    }""")
                    assert after["lastTop"]>=after["top"]-2,(path,after)
                    assert after["lastBottom"]<=after["bottom"]+2,(path,after)
                    assert after["scrolled"]>=max(0,after["remaining"]-2),(path,after)
                else:
                    assert before["overflow"]=="visible",(path,before)
                    assert before["scrollHeight"]<=before["clientHeight"]+2,(path,before)
                page.screenshot(path=f"reports/live-toc-{width}-{number}.png")
                page.close()
            context.close()
    finally:
        browser.close()
print("LIVE TOC AND ARCHIVE HEADING: PASS")
