#!/usr/bin/env python3
"""Editorial claim inventory for every published article.

A source URL is only a *candidate*, never automatic proof of a claim.
This script inventories all sentence-level factual candidates and cross-article
repetition for editor review. It must not mark unverified claims as true.
"""
from collections import defaultdict
from html import unescape
from pathlib import Path
import json
import re
from article_content import review_fingerprint, body_word_count

ROOT=Path(".")
OUT=ROOT/"reports"
OUT.mkdir(exist_ok=True)
PAGES=sorted(p for p in (ROOT/"articles").glob("*.html") if p.name!="index.html")
ledger_path=ROOT/'editorial'/'review-2026-11-01.json'
ledger=json.loads(ledger_path.read_text()) if ledger_path.exists() else {'articles': [], 'sources': {}}
reviews={row['slug']:row for row in ledger['articles']}
RISK={
 "legal / rights":r"\b(copyright|law|legal|licen[sc](?:e|ing)|permission|fair.deal|rights.holder|infringement|consumer.protection)\b",
 "provider / availability":r"\b(Netflix|Crunchyroll|Prime Video|streaming|catalogue|region|subscription|dub|subtitle|platform)\b",
 "money / statistics":r"(?:₹|\b\d+(?:[.,]\d+)?%|\b\d{4}\b|\bmarket size\b|\bprice\b|\bcost\b|\bfees\b|\bgrowth\b|\bhiring\b)",
 "public policy / events":r"\b(government|policy|regulat|state policy|university|college rule|organiser|venue|public screening|event date)\b",
}
def plain(s):
 return " ".join(unescape(re.sub(r"<[^>]*>"," ",s)).split())
def normalized(s):
 return " ".join(re.findall(r"[a-z0-9]+",s.lower()))
rows=[]
paragraph_index=defaultdict(list)
for page in PAGES:
 raw=page.read_text(encoding="utf-8")
 art=re.search(r'<article\b[^>]*class="[^"]*article[^"]*"[^>]*>(.*?)</article>',raw,re.I|re.S)
 if not art:
  raise SystemExit(f"{page}: article body missing")
 body=art.group(1)
 review=reviews.get(page.stem,{})
 current=review.get('review_sha256')==review_fingerprint(raw)
 decisions={item['statement']:item for item in review.get('statement_reviews',[])} if current else {}
 block=re.search(r'<section\b[^>]*class="sources"[^>]*>(.*?)</section>',body,re.I|re.S)
 urls=sorted(set(re.findall(r'<a\b[^>]*href=["\'](https?://[^"\']+)["\']',block.group(1),re.I))) if block else []
 content=re.sub(r'<section\b[^>]*class="sources"[^>]*>.*?</section>'," ",body,flags=re.I|re.S)
 paragraphs=[plain(x) for x in re.findall(r'<p\b[^>]*>(.*?)</p>',content,re.I|re.S)]
 paragraphs=[p for p in paragraphs if len(p.split())>=12]
 candidate_claims=[]
 for paragraph in paragraphs:
  key=normalized(paragraph)
  if len(key.split())>=24:
   paragraph_index[key].append(page.stem)
  for sentence in re.split(r'(?<=[.!?])\s+(?=[A-Z₹0-9“"])',paragraph):
   sentence=sentence.strip()
   if len(sentence.split())<9:continue
   tags=[label for label,pat in RISK.items() if re.search(pat,sentence,re.I)]
   if tags:
    decision=decisions.get(sentence,{})
    candidate_claims.append({
     "statement":sentence,"categories":tags,
     "status":decision.get('disposition','REQUIRES_EDITORIAL_CLAIM_TO_PRIMARY_SOURCE_CHECK'),
     "checked_primary_sources":[ledger['sources'][key] for key in decision.get('sources',[])],
     "candidate_article_references":urls,
     "note":decision.get('note','A listed URL is not proof this particular sentence is accurate.')
    })
 rows.append({"slug":page.stem,"paragraphs":len(paragraphs),
              "body_words":body_word_count(raw),
              "article_source_references":urls,
              "fact_sensitive_sentences":candidate_claims,
              "editorial_status":"REVIEW_RECORDED_AND_CURRENT" if current else "REQUIRES_EDITORIAL_REVIEW",
              "additional_factual_checks":review.get('additional_factual_checks',[]) if current else [],
              "claim_checks":review.get('claim_checks',[]) if current else []})
duplicated=[{"articles":sorted(set(v)),"text":k[:260]} for k,v in paragraph_index.items() if len(set(v))>1]
duplicated.sort(key=lambda x:(-len(x["articles"]),x["text"]))
pending=sum(c['status'].startswith('REQUIRES_') for row in rows for c in row['fact_sensitive_sentences'])
report={"method":"Keyword inventory joined to explicit editorial dispositions only when the reviewed body/source fingerprint still matches. Source-scope checks, advice, interpretation and hypothetical examples are separate. This script does not itself fact-check or certify originality.","article_count":len(rows),"pending_candidate_reviews":pending,"articles":rows,"repeated_paragraphs":duplicated}
(OUT/"claim-review.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
lines=["# Indian Anime Club editorial review register","","Generated from the current source HTML and the dated editorial record in `editorial/review-2026-11-01.json`. Keyword matches are not automatically factual claims. The record distinguishes primary-source scope checks, advice, qualified analysis and explicit hypothetical examples. Additional factual passages outside the keyword inventory were also reviewed. This is not a certificate of originality or approval by an advertising platform.","",
       f"Articles inspected: **{len(rows)}**. Exact cross-article repeated paragraphs: **{len(duplicated)}**.","",
       f"Candidate statements without a current recorded disposition: **{pending}**.","",
       "| Article | Source links in body | Keyword candidates | Editorial result |",
       "| --- | ---: | ---: | --- |"]
for row in rows:
 lines.append(f'| `{row["slug"]}` | {len(row["article_source_references"])} | {len(row["fact_sensitive_sentences"])} | {row["editorial_status"]} |')
lines.extend(["","## How to close a claim","1. Identify the primary document or official service page that actually supports the sentence, not merely the article topic.","2. Confirm the jurisdiction, specific anime title/season and publication date, and note uncertainty when a claim depends on these.","3. Rewrite or remove assertions without support. Do not invent audience research, testing, personal experiences, or source endorsements.","4. Document source details in the relevant article rather than using a generic reference list.","","## Repeated paragraph alerts"])
if duplicated:
 for item in duplicated[:60]:lines.append(f'- {", ".join(item["articles"])}: {item["text"][:150]}')
else:lines.append("No exact normalized paragraph reuse between different article source files was detected (similar ideas or template phrasing may still overlap).")
(OUT/"editorial-review.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
print(f"Inventory: {len(rows)} articles, {sum(len(r['fact_sensitive_sentences']) for r in rows)} candidate statements, {len(duplicated)} exact cross-article paragraph repeats.")
print(f"Current editorial record: {sum(r['editorial_status']=='REVIEW_RECORDED_AND_CURRENT' for r in rows)} articles; {pending} keyword candidates need a new disposition.")
for item in duplicated:
 print("REPEATED ARTICLE PARAGRAPH:", " | ".join(item["articles"]), "::", item["text"][:210])
