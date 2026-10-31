#!/usr/bin/env python3
"""Idempotently insert the three canonical analytics/advertising tags into every HTML source.
Applied before clean route generation, so all public pages and articles include the same IDs.
Consent preferences and Google-certified CMP configuration remain separate obligations.
"""
from pathlib import Path
import re

ROOT = Path(".")
GA4 = "G-M4738D1ZND"
PUBLISHER = "ca-pub-7937216909291905"
CLARITY = "ywqdm8xkj7"
GA4_BOOT = """<script id="iac-ga4-init">window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-M4738D1ZND');</script>"""
CLARITY_BOOT = """<script id="iac-clarity-init">
window.__iacClarityLoaded=true;
(function(c,l,a,r,i,t,y){
 c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
 t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
 y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
})(window,document,"clarity","script","ywqdm8xkj7");
</script>"""

def ensure(html):
    if "G-M4738D1ZND" not in html:
        html = re.sub(r"</head\s*>",
          '<script async src="https://www.googletagmanager.com/gtag/js?id='+GA4+'"></script>\n'
          + GA4_BOOT + "\n</head>", html, count=1, flags=re.I)
    if PUBLISHER not in html:
        html = re.sub(r"</head\s*>",
          '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client='
          + PUBLISHER + '" crossorigin="anonymous"></script>\n</head>',
          html, count=1, flags=re.I)
    if CLARITY not in html:
        html = re.sub(r"</head\s*>", CLARITY_BOOT + "\n</head>", html, count=1, flags=re.I)
    return html

sources = list(ROOT.glob("*.html")) + list((ROOT / "articles").glob("*.html")) + list(ROOT.glob("*/index.html"))
seen=set()
for path in sources:
    if path in seen or not path.is_file():
        continue
    seen.add(path)
    raw=path.read_text(encoding="utf-8")
    updated=ensure(raw)
    if updated!=raw: path.write_text(updated, encoding="utf-8")
    head=updated.split("</head>",1)[0]
    if any(key not in head for key in (GA4,PUBLISHER,CLARITY)):
        raise SystemExit(f"{path}: one or more required tracking IDs missing from head")
print(f"Verified analytics, AdSense and Microsoft Clarity on {len(seen)} HTML source pages.")
