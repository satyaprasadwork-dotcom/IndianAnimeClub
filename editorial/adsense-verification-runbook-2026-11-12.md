# Indian Anime Club — AdSense verification runbook
**Prepared:** 12 November 2026. **Tracking issue:** https://github.com/satyaprasadwork-dotcom/IndianAnimeClub/issues/17

**Status:** Code-level editorial improvements committed. This document does **not** establish AdSense approval or CMP, image, interview, indexing, mobile live-browser or human-fact-check compliance.

## Changes now in repository
- Dated public-page evidence for selected Netflix India anime titles, with unverified seasons/audio clearly labelled.
- Real Good Smile Company manufacturer listings compared with Indian seller-level uncertainty.
- Honest hypothetical college-club operating plan (no invented organiser interview) and student-budget scenarios linked to the watchlist planner.
- Related-reading links de-duplicated for three guides.
- New mobile local smoke test that visits homepage → legal streaming guide → source-link metadata → distinct related article → privacy page.
- Source and SVG provenance registers available from the editorial-links GitHub Actions artifact. The committed [artwork checklist](./artwork-rights-2026-11-12.csv) lists every current featured SVG, all PENDING rights evidence.

## External gates before another AdSense review
| Priority | Gate | Exact evidence | Current status |
| --- | --- | --- | --- |
| P1 | Google-certified CMP | AdSense Privacy & messaging published-message screenshot, certified provider/IAB TCF designation, regions EEA/UK/Switzerland, site domain | **NOT VERIFIED** |
| P1 | Consent accept/reject/withdraw | Browser HAR, cookies and storage snapshots, GA4 consent state, Clarity consentv2, AdSense requests for each choice in applicable regions | **NOT VERIFIED** |
| P1 | 12 previously flagged source URLs | Download the latest `editorial-source-link-report` Actions artifact containing `link-check-report.json`, note each actual URL/status, manually follow links, replace unsupported sources | **NOT VERIFIED; exact flagged list not stored in committed files** |
| P1 | 27 human editorial reviews | Named reviewer, checked date, primary source quotation/claim scope, correction and approval per **current** article version | **PENDING** |
| P1 | Rights for 27 featured SVG files and any external media | Creator, original project/license, third-party elements and permitted usage, evidence URL/file, signed review | **PENDING** |
| P1 | Ad placement | Review account-level Auto ads exclusions and inspect homepage, articles, planner, privacy, navigation-only and error/empty screens; capture screenshots | **NOT VERIFIED** |
| P1 | Live mobile reading | Device recordings/screenshots at 320/390/768px, actual source destination reached, menu, images, planner and consent controls | **NOT VERIFIED; local regression coverage added** |
| P1 | AdSense crawler | Hostinger/CDN response logs and WAF checks for Mediapartners-Google, Google-Display-Ads, Googlebot and canonical article URLs | **NOT VERIFIED** |
| P2 | Schema and indexing | Rich Results Test and Schema.org results; GSC canonical and indexing coverage, Bing indexed URL reports | **NOT VERIFIED** |
| P2 | Real account decision | Google AdSense site status and review-message screenshot, along with GA4/GSC audience metrics | **NOT VERIFIED** |

## Intent overlap decisions
- **Legal streaming guide** = title, season, rights and regional availability; **student-budget guide** = time, costs, cancellation and renewal. Cross-link; do not collapse tasks.
- **Hindi/Tamil/Telugu/Japanese audio** = availability and group language access; **subtitles vs dubs** = comprehension, accessibility and translation trade-offs. Retain differentiated guides pending human review.
- **Start a college anime club** = first event, approvals and costs; **make a community last** = moderation, retention and handover. Distinct purposes.
Only merge after a real semantic review identifies pages giving substantially the same answer; redirect retired URLs.

## Minimum evidence-producing sequence
1. Confirm Google-certified IAB TCF CMP and publication inside AdSense.
2. Test consent end-to-end in appropriate regions; account configuration and live tag/network behavior must agree. A homemade banner alone is not a certified CMP.
3. Retrieve the 12 flagged URLs from Actions, check each manually, and resolve unsupported claims/links.
4. Document image provenance and interview permissions; do not fabricate first-hand reporting.
5. Human-review all 27 retained articles with current-page fingerprints, prioritising legal/streaming/merchandise.
6. Run local and actual mobile journeys, crawl/schema/account tests and exclude ads from non-content screens as needed.
7. Re-submit only after the account's stated issues are addressed. Google controls approval.

## Primary policies
- https://support.google.com/adsense/answer/13554116
- https://support.google.com/publisherpolicies/answer/11112688
- https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-consent-api-v2
