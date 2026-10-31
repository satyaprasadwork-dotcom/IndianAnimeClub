#!/usr/bin/env python3
"""Make header/footer identical across all published HTML before clean-route generation.

Single source of truth is partials/header.html and partials/footer.html.
The shared markup is inserted server-side during the build, so it displays
immediately instead of being replaced by client-side JavaScript after loading.
The article body, homepage hero and page-specific content are never rewritten.
"""
from pathlib import Path
from hashlib import sha256
import re

ROOT = Path(".")
HEADER = (ROOT / "partials/header.html").read_text(encoding="utf-8").strip()
FOOTER = (ROOT / "partials/footer.html").read_text(encoding="utf-8").strip()
HEADER_RE = re.compile(
    r"""<nav\b(?=[^>]*\baria-label\s*=\s*["']Main navigation["'])[^>]*>[\s\S]*?</nav\s*>""",
    re.I,
)
FOOTER_RE = re.compile(r"<footer\b[^>]*>[\s\S]*?</footer\s*>", re.I)
CSS_RE = re.compile(r"""<link\b(?=[^>]*\bhref=["']/site-shell\.css(?:\?[^"']*)?["'])[^>]*>""", re.I)
SHELL_RE = re.compile(r"""<script\b[^>]*\bsrc=["']/site-shell\.js(?:\?[^"']*)?["'][^>]*>\s*</script\s*>""", re.I)
FONTS = 'https://fonts.googleapis.com/css2?family=Dela+Gothic+One&amp;family=Space+Grotesk:wght@400;500;700&amp;display=swap'
def versioned(asset):
    return '/' + asset + '?v=' + sha256((ROOT / asset).read_bytes()).hexdigest()[:12]

def source_files():
    files = list(ROOT.glob("*.html"))
    files += list((ROOT / "articles").glob("*.html"))
    files += list(ROOT.glob("*/index.html"))
    return sorted(set(p for p in files if p.is_file()))

for path in source_files():
    html = path.read_text(encoding="utf-8")
    # Repair a known legacy article typo: <header class="article-hero">">
    # This is text outside the HTML element and otherwise renders above the title.
    html = re.sub(
        r"""(<header\b(?=[^>]*\bclass=["'][^"']*\barticle-hero\b[^"']*["'])[^>]*>)\s*["']>""",
        r"\1",
        html,
        flags=re.I,
    )
    matches = list(HEADER_RE.finditer(html))
    if len(matches) > 1:
        raise SystemExit(f"{path}: multiple main-navigation headers; refusing to alter page body")
    if matches:
        html = HEADER_RE.sub(lambda _m: HEADER, html, count=1)
    else:
        if not re.search(r"<body\b", html, re.I):
            raise SystemExit(f"{path}: missing document body")
        html = re.sub(r"<body\b[^>]*>", lambda m: m.group(0) + "\n" + HEADER, html, count=1, flags=re.I)

    matches = list(FOOTER_RE.finditer(html))
    if len(matches) > 1:
        raise SystemExit(f"{path}: multiple footers; review before publishing")
    if matches:
        html = FOOTER_RE.sub(lambda _m: FOOTER, html, count=1)
    else:
        if not re.search(r"</body\s*>", html, re.I):
            raise SystemExit(f"{path}: missing closing body")
        html = re.sub(r"</body\s*>", lambda _m: FOOTER + "\n</body>", html, count=1, flags=re.I)

    # Load shared CSS before paint, rather than injecting it after page load.
    if not CSS_RE.search(html):
        html = re.sub(r"</head\s*>",
                      '<link rel="stylesheet" href="/site-shell.css">\n</head>',
                      html, count=1, flags=re.I)
    # Menu behaviour + analytics fallback. Does NOT replace any header/footer DOM.
    if not SHELL_RE.search(html):
        html = re.sub(r"</body\s*>",
                      '<script src="/site-shell.js" defer></script>\n</body>',
                      html, count=1, flags=re.I)
    # All hosts must receive the same fonts and fresh assets, even when serving
    # committed HTML directly rather than the generated GitHub Pages artifact.
    if 'fonts.googleapis.com/css2?family=Dela+Gothic+One' not in html:
        html = html.replace('</head>', '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
                            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
                            '<link rel="stylesheet" href="' + FONTS + '">\n</head>')
    html = re.sub(r'''<link\b(?=[^>]*href=["']/css/navigation\.css(?:\?[^"']*)?["'])[^>]*>\s*''', '', html, flags=re.I)
    html = html.replace('</head>', '<link rel="stylesheet" href="' + versioned('css/navigation.css') + '">\n</head>')
    for asset in ('site-shell.css', 'site-shell.js'):
        html = re.sub(r'''((?:href|src)=["'])/''' + re.escape(asset) + r'''(?:\?[^"']*)?(["'])''',
                      lambda m: m[1] + versioned(asset) + m[2], html)
    html = re.sub(r'''<link\b(?=[^>]*\brel=["'](?:shortcut\s+)?icon["'])[^>]*>\s*''', '', html, flags=re.I)
    html = html.replace('</head>', '<link rel="icon" type="image/png" sizes="48x48" href="' + versioned('favicon-48.png') + '">\n'
                        '<link rel="icon" type="image/svg+xml" href="' + versioned('favicon.svg') + '">\n'
                        '<link rel="shortcut icon" href="' + versioned('favicon.ico') + '">\n</head>')
    path.write_text(html, encoding="utf-8")

print(f"Synced shared visible logo, navigation and dark-blue footer on {len(source_files())} HTML sources.")
