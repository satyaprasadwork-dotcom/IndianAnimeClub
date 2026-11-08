# AI discovery and schema verification

This project's structured data uses canonical URL relationships and truthful
publication metadata. The static validator runs on every push, and the live
validator runs against the custom domain on deployment.

## Checks

- Run \`python3 scripts/generate_sitemap.py\` to refresh canonical URLs.
- Run \`python3 scripts/check_ai_discovery.py\` to validate the public AI
  guide, robots policy, homepage and archive graphs, and every article's
  BlogPosting, author, image, dates and breadcrumbs.
- Run \`python3 scripts/check_live_domain.py\` to check the publicly served
  files and HTML (requires network).
- Review the weekly editorial external-link report.

These are source/HTTP checks, not Google Rich Results Test certification.
For final manual validation, test the homepage, article archive and selected
articles at https://search.google.com/test/rich-results and
https://validator.schema.org/ . Use Search Console URL Inspection for
indexing and Google-selected canonicals. There is no supported general-purpose
Google Indexing API for ordinary anime editorial pages.

## Editorial and compliance

The structured-data audit does not verify editorial originality outside the
site, ownership of artwork, whether users have valid consent choices, or AdSense
account status. Do not treat a successful CI check as proof of AdSense approval.

Search crawlers are *allowed*, not compelled. Crawler activity and ingestion
must be inspected in host/CDN logs and any relevant private search-platform
tools. AI citations and search rankings are not guaranteed.
