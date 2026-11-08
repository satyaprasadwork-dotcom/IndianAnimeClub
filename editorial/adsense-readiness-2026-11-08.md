# Indian Anime Club — AI discovery and AdSense readiness follow-up
**Assessment date:** 8 November 2026  
**Site:** https://indiananimeclub.com/  
**Repository:** https://github.com/satyaprasadwork-dotcom/IndianAnimeClub

This is a source and live-domain technical assessment. It is **not** a claim of AdSense eligibility, official Google rich-result approval, independent plagiarism clearance, or search-engine indexing.

## Verified technical implementation
- 27 retained article source pages and 38 canonical sitemap URLs (confirmed in the existing audit); four overlapping articles were retired with redirects on 4 November 2026.
- Homepage includes Organization, WebSite and WebPage JSON-LD.
- Article directory includes CollectionPage and BreadcrumbList.
- All 27 retained article sources carry BlogPosting and BreadcrumbList, canonical article URL, founder byline, publication and modification dates, and local featured-image references. Existing source integrity checks continue to run.
- The root llms.txt offers an editorial content map, and robots.txt permits public AI/search bots while excluding the private build scripts directory.
- Added a comprehensive source validator and a lightweight scheduled weekly custom-domain reachability/schema audit. The scheduled check validates HTTP-accessible public content, not actual search indexing.
- Corrected a false failure in the Chromium TOC check: shorter real guides can have seven (or fewer) contents links. It now verifies actual section targets instead of demanding eight headings. The live custom-domain job passed after that fix.
- The latest source audit generates an editorial claim-review report and verifies article body structure, canonical metadata, article dates, source links on the page, image paths, advertising notices, and tag consistency.
- Earlier source review register records 31 reviewed articles (including the four later retired), 72 primary-source-scoped statements, 159 advice/scope statements, 52 editorial qualifications, 13 explicitly hypothetical examples, and 36 additional factual checks. These are review classifications, not an external originality or accuracy certification.
- Weekly third-party source-link checks are configured with reports. Blocked requests (403/429) cannot be classified as broken without human confirmation.

## Remaining independent/account-side work

| Priority | Gate | Necessary evidence/action |
| --- | --- | --- |
| P1 | Google-certified CMP | Confirm in AdSense Privacy & messaging that an appropriate Google-certified IAB TCF CMP is configured for relevant EEA, UK and Swiss traffic. Test the actual consent interface and cookie/tag behaviour from those regions. The privacy policy currently says the site has no built-in analytics preference panel. Do **not** claim compliance from HTML alone. |
| P1 | Independent editorial & rights verification | Conduct a human spot-check of primary sources and factual claims against the current publisher material; document original authorship, commissioned artwork permissions and any third-party screenshots; decide whether guide overlap harms unique user value. The prior 31-page review is a useful internal record, not plagiarism certification. |
| P2 | Official rich-result validation | Run https://search.google.com/test/rich-results and https://validator.schema.org on the homepage, /articles/ and multiple canonical article URLs. Address any official warnings/errors. Automated JSON-LD and canonical tests do not replace these services. |
| P2 | Index coverage | In verified Google Search Console and Bing Webmaster Tools, inspect page indexing counts, exclusion reasons, canonical selections and sitemaps. Use individual URL inspection where needed. Ordinary editorial pages are not eligible for Google's restricted Indexing API. |
| P2 | AI crawler activity | Use Hostinger/CDN access logs to verify requests by identifiable user agents (e.g. OAI-SearchBot, GPTBot, ClaudeBot, PerplexityBot), status codes, WAF rules and whether robots.txt is actually cached. An explicit Allow directive does not mean the bot has visited. |
| P3 | Audience and policy outcome | Check real GA4/GSC engagement, AdSense site status and actual policy messages. Google determines the AdSense result; no tool can guarantee acceptance. |

## Technical caveat about caching
Deploy-time live verification must bypass stale CDN copies of robots.txt and llms.txt. The new scheduled monitor uses ordinary URLs to surface persisted caching problems later. On Hostinger's Apache/LiteSpeed, a no-cache header is configured for those text files; GitHub Pages may apply its own caching rules. A cached old robots.txt can briefly appear on an ordinary request even when a cache-busted version is current.

## Primary guidance consulted
- Google's Article JSON-LD guidance: https://developers.google.com/search/docs/appearance/structured-data/article
- Google's BreadcrumbList guidance: https://developers.google.com/search/docs/appearance/structured-data/breadcrumb
- Google's sitemap guidance: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Google's certified-CMP requirement: https://support.google.com/adsense/answer/13554116
- Google's Indexing API scope: https://developers.google.com/search/apis/indexing-api/v3/using-api

## Recommended order
First confirm live monitoring remains green and address any persistent cached bot-rule responses. Then finish consent-platform setup and independent article/illustration review before requesting another AdSense review. Use Search Console/Bing to diagnose actual index status and the official Rich Results Test for Google-specific structured data eligibility.
