#!/usr/bin/env python3
"""Make all public source pages use a single canonical, identical tracking block.

The block is embedded in each HTML <head> rather than dynamically injected
from site-shell.js. This script is safe to run repeatedly, also on build output.

This is tag consistency only; certified consent management and jurisdiction-
specific consent behaviour must be handled separately.
"""
from pathlib import Path
import argparse
import re
import sys

ROOT=Path(".")
GA4="G-M4738D1ZND"
ADSENSE="ca-pub-7937216909291905"
CLARITY="ywqdm8xkj7"

START="<!-- IAC_TRACKING_START: Google Analytics, AdSense, Microsoft Clarity -->"
END="<!-- IAC_TRACKING_END -->"
BLOCK=f"""\
{START}
<script async src="https://www.googletagmanager.com/gtag/js?id={GA4}"></script>
<script id="iac-ga4-init">
window.dataLayer=window.dataLayer||[];
function gtag(){{dataLayer.push(arguments);}}
gtag('js',new Date());
gtag('config','{GA4}');
</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE}" crossorigin="anonymous"></script>
<script id="iac-clarity-init">
window.__iacClarityLoaded=true;
(function(c,l,a,r,i,t,y){{
  c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
  t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
  y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
}})(window,document,"clarity","script","{CLARITY}");
</script>
{END}"""

SCRIPT=re.compile(r"<script\b[^>]*>[\s\S]*?</script\s*>",re.I)
BLOCK_RE=re.compile(r"<!--\s*IAC_TRACKING_START[^>]*-->[\s\S]*?<!--\s*IAC_TRACKING_END\s*-->",re.I)
GTAG_INIT=re.compile(r"\bgtag\s*\(\s*['\"](?:js|config)['\"]",re.I)

def is_tracking(script):
    lower=script.lower()
    if any(token in lower for token in (
        "pagead2.googlesyndication.com/pagead/js/adsbygoogle.js",
        "googletagmanager.com/gtag/js",
        "clarity.ms/tag/",
        "__iacclarityloaded",
        'id="iac-ga4-init"', "id='iac-ga4-init'",
        'id="iac-clarity-init"', "id='iac-clarity-init'",
    )):
        return True
    return bool(GTAG_INIT.search(script) and "datalayer" in lower)

def normalize(html):
    match=re.search(r"<head\b[^>]*>([\s\S]*?)</head\s*>",html,re.I)
    if not match or len(re.findall(r"<head\b",html,re.I))!=1:
        raise ValueError("exactly one <head> required")
    inner=match.group(1)
    inner=BLOCK_RE.sub("",inner)
    inner=SCRIPT.sub(lambda m:"" if is_tracking(m.group(0)) else m.group(0),inner)
    inner=re.sub(r"<!--\s*(?:Google tag \(gtag\.js\)|Clarity tracking code[^>]*|IAC tracking[^>]*)\s*-->","",inner,flags=re.I)
    # Canonical insertion at the same position on every page (end of head).
    inner=inner.rstrip()+"\n"+BLOCK+"\n"
    output=html[:match.start(1)]+inner+html[match.end(1):]
    return output

def validate(html,path):
    m=re.search(r"<head\b[^>]*>([\s\S]*?)</head\s*>",html,re.I)
    if not m:
        raise ValueError(f"{path}: missing HTML head")
    h=m.group(1)
    required={
      "AdSense external loader":"pagead2.googlesyndication.com/pagead/js/adsbygoogle.js",
      "Google Analytics external loader":"www.googletagmanager.com/gtag/js",
      "Microsoft Clarity loader":"www.clarity.ms/tag/",
      "GA initialization":'id="iac-ga4-init"',
      "Clarity initialization":'id="iac-clarity-init"',
      "tracking block start":START,
      "tracking block end":END,
    }
    for name,needle in required.items():
        if h.count(needle)!=1 or html.count(needle)!=1:
            raise ValueError(f"{path}: expected exactly one {name}")
    if f"gtag('config','{GA4}')" not in h:
        raise ValueError(f"{path}: wrong GA4 measurement ID")
    if f"client={ADSENSE}" not in h:
        raise ValueError(f"{path}: wrong AdSense publisher ID")
    if f'"{CLARITY}"' not in h:
        raise ValueError(f"{path}: wrong Clarity project ID")
    if h.count('crossorigin="anonymous"')<1:
        raise ValueError(f"{path}: AdSense requires crossorigin attribute")

def pages():
    found=set(ROOT.glob("*.html")) | set((ROOT/"articles").glob("*.html")) | set(ROOT.glob("*/index.html"))
    return sorted(p for p in found if p.is_file())

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--check",action="store_true",help="Fail if any page is not normalized; do not write")
    args=parser.parse_args()
    files=pages()
    if len(files)<40:
        raise SystemExit(f"Unexpected HTML page count: {len(files)}")
    changed=[]
    for path in files:
        source=path.read_text(encoding="utf-8")
        try:
            updated=normalize(source)
            validate(updated,path)
            if normalize(updated)!=updated:
                raise ValueError("normalizer is not idempotent")
        except ValueError as error:
            raise SystemExit(str(error))
        if source!=updated:
            changed.append(str(path))
            if not args.check:
                path.write_text(updated,encoding="utf-8")
    print(f"Tracking inspected on {len(files)} HTML source pages; {len(changed)} differed from canonical tags.")
    if changed and args.check:
        for path in changed:print("Needs normalization:",path)
        return 1
    return 0

if __name__=="__main__":
    sys.exit(main())
