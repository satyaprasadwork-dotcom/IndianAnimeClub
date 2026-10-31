#!/usr/bin/env python3
"""Export topic-specific source SVGs to high-resolution 1200x675 PNG previews.
Keep inline article SVG artwork as is; social previews and Article image metadata
point to the raster version, which has broader sharing-preview support.
"""
from pathlib import Path
import re
import cairosvg

DOMAIN = "https://indiananimeclub.com"
out = Path("images/articles")
count = 0
for image in sorted(out.glob("*.svg")):
    target = image.with_suffix(".png")
    cairosvg.svg2png(url=str(image), write_to=str(target),
                     output_width=1200, output_height=675)
    count += 1

for path in list(Path("articles").glob("*.html")) + list(Path(".").glob("*/index.html")):
    if path.name == "index.html" and path.parent.name == "articles":
        continue
    slug = path.stem if path.parent.name == "articles" else path.parent.name
    if not (out / (slug + ".png")).is_file():
        continue
    html = path.read_text(encoding="utf-8")
    before = DOMAIN + "/images/articles/" + slug + ".svg"
    after = DOMAIN + "/images/articles/" + slug + ".png"
    html = html.replace(before, after)
    if 'property="og:image:width"' not in html:
        html = re.sub(r"</head\s*>",
                      '<meta property="og:image:type" content="image/png">'
                      '<meta property="og:image:width" content="1200">'
                      '<meta property="og:image:height" content="675"></head>',
                      html, count=1, flags=re.I)
    path.write_text(html, encoding="utf-8")
print(f"Generated {count} original-artwork PNG social previews at 1200x675.")
