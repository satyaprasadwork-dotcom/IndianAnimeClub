# Indian Anime Club — AdSense readiness evidence register
**Reviewed:** 3 November 2026
**Target:** https://indiananimeclub.com/
**Source:** main + the 2026-11-03 remediation PR, once merged

This is an evidence checklist, **not** an approval guarantee or a claim that Google reviewed these changes.

## Verified in source and CI
- 31 published article sources, including one source list per article and a 1,000+ word publisher baseline; the word count is not a Google ranking or approval requirement.
- Runtime JavaScript no longer replaces factual source references with broad topic links. Chromium compares visible links to the editorial HTML.
- Archive filters no longer expose empty Rankings and Recommendations categories. Pagination has shareable `?page=` URLs and preserves back/forward navigation.
- Homepage shows six direct article links and no unconfirmed city chapter cards.
- A local, original watchlist and subscription-budget planner offers useful functionality without inventing catalogue availability or prices. Browser tests verify its arithmetic and layout.
- Four high-priority articles received source-scoped close reading, clearly separated from interpretive claims; review fingerprints and dated check notes were updated.
- Site policies, correction contact, robots, ads.txt, canonical URLs, sitemap, GA4, Microsoft Clarity, and AdSense tags remain present in source/build checks.
- Automated Actions audit validates article structure and links, shared header and footer, generated clean routes and the latest deployment build.

## Still requires independent or account-based verification before pressing Request review

| Gate | Evidence required | Current assessment |
| --- | --- | --- |
| Custom domain serving current build | Compare `indiananimeclub.com` source/version with the deployed GitHub Pages artifact; inspect a fresh uncached browser response, HTTP redirects and DNS/hosting configuration | **Unverified**; search snapshots can be stale |
| Google-certified CMP for relevant EEA/UK/Swiss users | In AdSense > Privacy & messaging confirm appropriate certified TCF CMP/message, publisher settings, and test actual regional consent experience | **Unverified** from repository; a homemade cookie notice is not a substitute |
| Consent behaviour for GA4/Clarity and advertising | Audit relevant jurisdiction requirements, pre-consent requests, vendor disclosures, and actual browser cookies in each region | **Account and browser test required** |
| Editorial uniqueness beyond within-site exact matches | Independent human review of semantic duplication, external source dependence, page usefulness, and new distinctive reader benefits across 31 pages | **Not independently certified** |
| Link and rights verification | Review current external-link report, especially blocked/404 URLs; confirm rights/licensing for every editorial image and any screenshots | **Manual review required** |
| Search Console and Bing | Inspect actual index coverage, exclusions, live tested URL, sitemap acceptance, canonical choices, manual/security actions | **Private account access required** |
| Real audience interest | Read GA4 and Search Console engagement and search performance; do not manufacture sessions, evidence or testimonials | **Not measurable from source code** |
| AdSense approval status | Check site's actual AdSense status after legitimate remediation and request a review yourself | **Previously rejected: low-value content** |

## Primary Google requirements
- [AdSense account/site content-quality issues](https://support.google.com/adsense/answer/81904?hl=en): unique, relevant content that provides a compelling reason to visit.
- [Certified CMP and TCF requirements](https://support.google.com/adsense/answer/13554116?hl=en): relevant EEA, UK and Switzerland traffic.
- [Google CMP setup and privacy messages](https://support.google.com/adsense/answer/7670013?hl=en).

## Editorial next steps
- Continue improving all 31 articles with particular anime episodes, named primary sources, independently produced comparisons, original diagrams where they aid understanding, and interviews only where actually conducted.
- Prioritise generic guide overlap: language tracks vs subs/dubs, streaming vs watchlist budget, community planning vs sustainability.
- Avoid manufacturing field research, film scene observations, numerical results or external reviews.
- Keep original bylines, article URLs and dated editorial records accurate; add a new recorded source check after each substantive body edit.

## Gate to request review
Ask for AdSense review only after the live **custom domain** is serving the current site, important pages and tools work on mobile, sources and artwork have been checked, required consent handling is configured, and the human editorial review is satisfied. The repository test being green does not mean Google will approve.
