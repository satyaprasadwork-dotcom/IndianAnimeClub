# Editorial review, 1 November 2026

All 31 article bodies were read and revised. The dated JSON record records primary sources, their limits, explicit dispositions for the keyword inventory and additional factual passages the inventory misses. Practical advice, personal interpretation and invented worked examples are distinguished from source-backed assertions. No audience survey, first-hand testing, current subscription quotation, national market forecast or guaranteed legal outcome is invented.

The article bodies contain 1,055 to 1,264 words after excluding titles, descriptions, navigation, takeaway summaries, source lists and footers. This is the publisher's requirement, not a claim about a search-engine word-count rule. Each article has specific takeaways and a concrete worked example or close-reading exercise. The exact normalized cross-article paragraph scan finds no repeated paragraphs; it cannot prove absence of semantic overlap or plagiarism across the web.

Key corrections include the conditional educational-screening exception and separate provider terms, manufacturer-specific authenticity checks, copyright exceptions in asset checklists, role-based community access instead of shared passwords, the dated status of 2022 AVGC recommendations, and the difference between a synopsis and evidence about audience reactions. Language-access and subtitles/dubs articles now have separate practical purposes.

`review-2026-11-01.json` is the editorial record. `scripts/review_articles.py` joins recorded dispositions to the current article only when its body/source fingerprint matches. It does not automatically declare keyword matches true. The JSON includes additional checks for production methods and story premises that the keyword scan did not identify.

Run `python scripts/review_articles.py` for the current inventory and `python scripts/audit_site.py` for the body-length, source, table-of-contents and freshness checks. A substantive body or source change requires reviewing and updating the corresponding entry rather than merely copying its old fingerprint. Do not refresh a fingerprint to bypass a failed review check.

Header and branding validation lives in `scripts/validate_shared_shell.py` and `scripts/test_shared_shell_browser.py`. The browser check compares typography, positions, button geometry, menu behaviour and footer colour across all source routes at 320, 390, 768, 820, 900, 1024 and 1280 pixels. It blocks external requests for deterministic CI; live font loading was separately checked on the deployed homepage and privacy page.

This review does not verify Search Console or Bing indexing, consent-platform configuration inside an advertising account, or an advertising platform's approval decision. Those account-side matters are separate from the completed source and article edits.
