(function(){
'use strict';
/* Canonical Indian Anime Club site shell: shared homepage header and footer. */
(()=>{'use strict';
const header='<nav class="legacy-site-nav" aria-label="Main navigation"><div class="wrap"><a class="logo" href="/#top"><b>IAC</b> <span class="ln">Indian Anime Club</span></a><ul id="site-links"><li><a href="/#about">About</a></li><li><a href="/#worlds">Worlds</a></li><li><a href="/#events">Events</a></li><li><a href="/#chapters">Chapters</a></li><li><a href="/articles/">Articles</a></li></ul><a class="btn" href="/#join" style="padding:8px 16px;font-size:14px;box-shadow:4px 4px 0 var(--accent)">Join us</a><button class="menu" id="menu" type="button" aria-label="Toggle navigation" aria-controls="site-links" aria-expanded="false">&#9776;</button></div></nav>';
const footer='<footer class="iac-footer"><div class="iac-footer-inner"><a class="iac-footer-brand" href="/" aria-label="Indian Anime Club home"><span>Indian Anime Club</span></a><p class="iac-footer-tagline">A community, not a sales pitch. Made for India\'s anime community.</p><nav class="iac-footer-social" aria-label="Social and contact links"><a href="https://chat.whatsapp.com/IOR7VBI25dW9ltnofX6Frz" target="_blank" rel="noopener noreferrer">WhatsApp</a><a href="https://instagram.com/indiananime.club" target="_blank" rel="noopener noreferrer">Instagram</a><a href="https://www.facebook.com/people/indiananimeclub/61582607151767/" target="_blank" rel="noopener noreferrer">Facebook</a><a href="mailto:prasad@indiananimeclub.com">Email</a></nav><nav class="iac-footer-site" aria-label="Website information"><a href="/about/">About</a><a href="/contact/">Contact</a><a href="/community-guidelines/">Community guidelines</a><a href="/editorial-policy/">Editorial policy</a><a href="/privacy-policy/">Privacy</a><a href="/terms/">Terms</a><a href="/disclaimer/">Disclaimer</a></nav><p class="iac-footer-copy">© 2026 Indian Anime Club · indiananimeclub.com · Independent fan community, not affiliated with anime studios or rights holders.</p></div></footer>';
if(!document.querySelector('link[data-iac-shell-css]')){const link=document.createElement('link');link.rel='stylesheet';link.href='/site-shell.css';link.dataset.iacShellCss='true';document.head.appendChild(link);}
let nav=document.querySelector('nav[aria-label="Main navigation"]');if(nav)nav.outerHTML=header;else{const main=document.querySelector('main');if(main)main.insertAdjacentHTML('beforebegin',header);}
const oldFooter=document.querySelector('footer');if(oldFooter)oldFooter.outerHTML=footer;else document.body.insertAdjacentHTML('beforeend',footer);
nav=document.querySelector('nav.legacy-site-nav');const btn=nav&&nav.querySelector('#menu');
if(btn&&!btn.dataset.shellBound){btn.dataset.shellBound='true';const close=()=>{nav.classList.remove('open');btn.setAttribute('aria-expanded','false');btn.setAttribute('aria-label','Toggle navigation')};btn.addEventListener('click',()=>{const open=nav.classList.toggle('open');btn.setAttribute('aria-expanded',String(open));btn.setAttribute('aria-label',open?'Close navigation':'Toggle navigation')});nav.querySelectorAll('ul a').forEach(a=>a.addEventListener('click',close));document.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav.classList.contains('open')){close();btn.focus()}});}
})();
const D={
'agents-are-getting-jobs':['cycle','Agent work lifecycle',['Request','Policy check','Approved action','Verify or stop']],
'small-models-on-phone':['compare','Choosing an on-device model',['Privacy and local control','Latency and offline use','Capability and resource limits']],
'three-ai-rule-changes':['pipeline','Turn regulation into product work',['Scope the use','Document evidence','Make transparency visible','Monitor after launch']],
'humanoid-factory-floor':['pipeline','From robot pilot to production',['Select bounded task','Test in real conditions','Measure safety and reliability','Scale with supervision']],
'reasoning-benchmarks':['pipeline','Evaluate reasoning claims',['Define representative tasks','Run controlled tests','Check failures and cost','Validate in real use']],
'ai-pricing-page':['compare','Compare AI pricing models',['Per seat','Per usage or token','Per outcome']],
'regulators-liable':['tree','Trace responsibility',['AI-assisted decision','Provider obligations','Deployer obligations','Human review and appeal']],
'warehouse-robots-help':['pipeline','Warehouse robot workflow',['Sense inventory','Plan route or task','Act in shared space','Confirm delivery']],
'open-weights-licensing':['tree','Check model openness',['Inspect model artifacts','Read the exact license','Verify data and code access','Check use restrictions']],
'data-centers-real-estate':['layers','Data-centre site constraints',['Power availability','Grid and cooling','Land, fibre and permits','Community and water impact']],
'schools-ai-rules':['tree','School AI-use decision',['What is the learning goal?','Is AI use permitted?','Disclose and verify use','Protect student data']],
'drones-last-100-meters':['pipeline','Last-mile drone delivery',['Dispatch and route','Flight and airspace checks','Safe landing and handoff','Confirm receipt']],
'ai-procurement-checklist':['matrix','AI procurement review',['Use case and evidence','Privacy and security','Cost and integration','Owner and exit plan']],
'ai-incident-response':['cycle','AI incident response loop',['Detect and triage','Contain the system','Investigate evidence','Recover and learn']],
'ai-search-citations':['pipeline','From search to supported answer',['Retrieve relevant sources','Check source authority','Ground each claim','Expose citations and limits']],
'rag-vs-fine-tuning':['tree','Choose the intervention',['Missing or changing facts?','Test retrieval (RAG)','Wrong task behaviour?','Evaluate fine-tuning']],
'ai-data-privacy-checklist':['layers','Follow the data lifecycle',['Input and purpose','Provider and processing','Logs, access and retention','Output, deletion and audit']],
'ai-evaluation-before-launch':['cycle','Evaluation is a release gate',['Build representative set','Test and inspect errors','Apply launch thresholds','Monitor and regression-test']],
'ai-customer-support-human-handoff':['pipeline','Human handoff workflow',['Detect risk or uncertainty','Transfer concise context','Human resolves request','Feed outcome into review']],
'ai-coding-assistant-code-review':['cycle','Code assistant review loop',['Generate a proposed change','Run tests and security checks','Human reviews behaviour','Merge or revise']],
'ai-model-drift-monitoring':['trend','Monitor signals, then verify',['Input distribution','Labeled quality sample','Segmented performance','Investigate or roll back']],
'synthetic-data-ai-limitations':['pipeline','Validate synthetic data',['Generate with safeguards','Check coverage and leakage','Test downstream utility','Approve for specific use']],
'ai-hiring-tools-human-review':['tree','Keep hiring decisions accountable',['Define tool influence','Audit outcomes and errors','Human reviews evidence','Enable correction or appeal']],
'small-business-ai-adoption':['matrix','Prioritise a first AI pilot',['High value and low risk','Measure current workflow','Pilot with review','Scale only with evidence']],
'multimodal-ai-what-it-means':['pipeline','Multimodal system pipeline',['Image, audio or text input','Interpret and align signals','Check uncertainty','Verify final output']],
'open-source-open-weights-ai':['layers','Assess access and responsibility',['Weights access','License and rights','Training and code artifacts','Maintenance and security']],
'ai-energy-water-footprint':['layers','Set the footprint boundary',['Training versus inference','Facility energy and electricity','Water withdrawal versus consumption','Location and workload']],
'ai-accessibility-design':['pipeline','Accessible AI user journey',['Access controls','Understand output','Correct or recover','Alternative interaction']],
'ai-agent-security-threat-model':['threat','Agent threat path',['Untrusted input','Model or retrieved context','Tool permissions','External action']],
'ai-generated-content-disclosure':['tree','Decide what to disclose',['What did AI materially create?','Could it change interpretation?','Disclose clearly in context','Verify regardless']]
};
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function diagram(slug){
const d=D[slug];if(!d)return '';
const [type,title,labels]=d;let s='';
const box=(x,y,w,h,label,i)=>'<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="12" fill="'+(i===labels.length-1?'var(--bg)':'var(--card)')+'" stroke="var(--violet)" stroke-width="2"/><text x="'+(x+w/2)+'" y="'+(y+h/2+5)+'" text-anchor="middle" font-size="14" font-weight="650" fill="var(--ink)">'+esc(label.length>34?label.slice(0,32)+'…':label)+'</text>';
if(type==='matrix'){
s='<rect x="105" y="45" width="650" height="270" rx="14" fill="var(--bg)" stroke="var(--violet)" stroke-width="2"/><path d="M430 45V315 M105 180H755" stroke="var(--violet)" stroke-width="2"/>';
labels.slice(0,4).forEach((l,i)=>s+='<text x="'+(i%2?592:267)+'" y="'+(i<2?115:250)+'" text-anchor="middle" font-size="16" font-weight="650" fill="var(--ink)">'+esc(l)+'</text>');
s+='<text x="430" y="350" text-anchor="middle" font-size="12" fill="var(--mut)">Review each dimension; do not treat this as a numeric score</text>';
}else if(type==='trend'){
s='<path d="M85 55V280H785" fill="none" stroke="var(--mut)" stroke-width="2"/><path d="M85 120H785 M85 200H785" fill="none" stroke="var(--mut)" stroke-opacity=".25" stroke-dasharray="5 5"/><polyline points="95,235 190,210 285,230 380,145 475,170 570,105 665,135 775,75" fill="none" stroke="var(--violet)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><text x="435" y="320" text-anchor="middle" font-size="13" fill="var(--mut)">Conceptual illustration only — not measured data</text>';
}else if(type==='cycle'){
const pos=[[65,72],[465,72],[465,215],[65,215]];
s+='<path d="M245 105H465 M650 135V215 M465 245H245 M155 215V135" fill="none" stroke="var(--violet)" stroke-width="3"/>';
labels.slice(0,4).forEach((l,i)=>s+=box(pos[i][0],pos[i][1],180,62,l,i));
}else if(type==='threat'){
const xs=[25,235,445,655];
labels.slice(0,4).forEach((l,i)=>{if(i<3)s+='<path d="M'+(xs[i]+170)+' 145H'+(xs[i+1]-8)+'" stroke="var(--pink)" stroke-width="3"/><path d="M'+(xs[i+1]-18)+' 137l10 8-10 8" fill="none" stroke="var(--pink)" stroke-width="3"/>';s+=box(xs[i],110,170,70,l,i)});
s+='<text x="430" y="235" text-anchor="middle" font-size="13" fill="var(--mut)">Controls: least privilege · validation · approvals · audit logs</text>';
}else if(type==='tree'){
s+='<path d="M430 95V120 M430 120H215V145 M430 120H645V145 M215 205V230H430V255 M645 205V230H430" fill="none" stroke="var(--violet)" stroke-width="2.5"/>';
s+=box(270,35,320,60,labels[0],0);
s+=box(55,145,320,60,labels[1],1);
s+=box(485,145,320,60,labels[2],2);
s+=box(270,255,320,60,labels[3]||'Review and verify',3);
}else if(type==='compare'){
const n=labels.length,w=Math.floor(760/n),gap=12,startX=50;
labels.forEach((l,i)=>{const x=startX+i*(w+gap);s+='<rect x="'+x+'" y="100" width="'+w+'" height="130" rx="14" fill="var(--card)" stroke="var(--violet)" stroke-width="2"/><circle cx="'+(x+w/2)+'" cy="132" r="12" fill="'+(i%2?'var(--pink)':'var(--violet)')+'"/><text x="'+(x+w/2)+'" y="175" text-anchor="middle" font-size="14" font-weight="650" fill="var(--ink)">'+esc(l.length>24?l.slice(0,22)+'…':l)+'</text>'});
s+='<text x="430" y="280" text-anchor="middle" font-size="13" fill="var(--mut)">Compare the trade-offs; no numeric ranking implied</text>';
}else{
labels.forEach((l,i)=>{const y=30+i*75;if(i<labels.length-1)s+='<path d="M430 '+(y+55)+'V'+(y+74)+'m-7 -7 7 7 7 -7" fill="none" stroke="var(--violet)" stroke-width="3"/>';s+=box(100,y,660,55,l,i);s+='<circle cx="130" cy="'+(y+27)+'" r="13" fill="'+(i===labels.length-1?'var(--pink)':'var(--violet)')+'"/><text x="130" y="'+(y+32)+'" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">'+(i+1)+'</text>'});
}
const height=type==='layers'?labels.length*75+35:(type==='cycle'?315:(type==='matrix'||type==='trend'||type==='threat'?365:370));
return '<svg class="topic-diagram-svg" width="100%" height="'+height+'" viewBox="0 0 860 '+height+'" preserveAspectRatio="xMidYMid meet" role="img" aria-label="'+esc(title+': '+labels.join('; '))+'" xmlns="http://www.w3.org/2000/svg"><title>'+esc(title)+'</title>'+s+'</svg>';
}
function enhance(){
const body=document.querySelector('.body');if(!body)return;
const slug=(location.pathname.replace(/\/+$/,'').split('/').pop()||'').replace(/\.html$/i,'').toLowerCase();
const d=D[slug];
let visual=body.querySelector('.visual-explainer');
if(d){
  if(!visual){
    visual=document.createElement('section');visual.className='visual-explainer';
    visual.innerHTML='<p class="eyebrow">Topic diagram</p><h2></h2>';
    const anchor=body.querySelector('.quick-answer')||body.querySelector('.key-takeaways')||body.firstElementChild;
    if(anchor)anchor.insertAdjacentElement('beforebegin',visual);else body.prepend(visual);
  }
  const h=visual.querySelector('h2'),e=visual.querySelector('.eyebrow');
  if(h)h.textContent=d[1];if(e)e.textContent='Topic diagram';
  const svg=diagram(slug);
  if(svg){visual.querySelectorAll('.visual-grid,.topic-diagram-svg').forEach(n=>n.remove());visual.insertAdjacentHTML('beforeend',svg)}
  else if(!visual.querySelector('.visual-grid')){
    const fallback=document.createElement('div');fallback.className='visual-grid';
    d[2].slice(0,3).forEach((label,i)=>{const card=document.createElement('div'),b=document.createElement('b'),span=document.createElement('span');b.textContent=label;span.textContent=['Define the requirement and constraints','Evaluate evidence and trade-offs','Choose controls and review the outcome'][i];card.append(b,span);fallback.appendChild(card)});visual.appendChild(fallback);
  }
}else if(visual && /decision framework|a practical decision path/i.test(visual.textContent||'')){
  visual.remove();
}
body.querySelectorAll('.article-toc,[aria-label="Table of contents"],.table-of-contents,.toc-container').forEach(n=>n.remove());
body.querySelectorAll('h2').forEach(h=>{if(/^in this article$/i.test(h.textContent.trim())&&!h.closest('.visual-explainer,.original-analysis,.sources,.related,.key-takeaways'))h.remove()});
const excluded=/^(key takeaways|sources|sources and further reading|related ninth post reading|keep reading|what this means in practice|in this article|decision framework|topic diagram)$/i;
const seen=new Set();
const heads=Array.from(body.querySelectorAll('h2')).filter(h=>{if(h.closest('.visual-explainer,.original-analysis,.sources,.related,.key-takeaways'))return false;const title=h.textContent.trim();if(!title||excluded.test(title))return false;const key=title.toLowerCase();if(seen.has(key))return false;seen.add(key);return true});
heads.forEach((h,i)=>{if(!h.id||/^section-\d+$/.test(h.id))h.id='article-section-'+(i+1)});
if(heads.length>=3){
  const nav=document.createElement('nav');nav.className='article-toc';nav.setAttribute('aria-label','Table of contents');
  nav.innerHTML='<div class="toc-heading"><span class="toc-kicker">ARTICLE GUIDE</span><h2>In this article</h2><span class="toc-count">'+heads.length+' sections</span></div>';
  const list=document.createElement('ol');heads.forEach(h=>{const li=document.createElement('li'),a=document.createElement('a');a.href='#'+h.id;a.textContent=h.textContent.trim();li.appendChild(a);list.appendChild(li)});nav.appendChild(list);
  const anchor=body.querySelector('.quick-answer')||body.querySelector('.key-takeaways')||body.querySelector(':scope > p')||body.firstElementChild;
  if(anchor)anchor.insertAdjacentElement('afterend',nav);else body.prepend(nav);
}

/* Ninth Post-style end matter: sources first, then related articles. */
const endMatterBySlug={
"this-anime-scene-changed-how-fans-look-at-life":["beyond-power-levels-how-to-analyse-anime-writing-worldbuilding-and-character-growth","when-the-hero-makes-the-wrong-choice-understanding-moral-dilemmas-in-anime-stories"],
"when-anime-became-a-family-debate-how-indian-viewers-explain-their-favourite-shows-at-home":["hindi-tamil-telugu-or-japanese-audio-how-language-changes-the-indian-anime-experience","new-to-anime-in-india-a-beginners-roadmap-based-on-your-interests-not-just-rankings"],
"hindi-tamil-telugu-or-japanese-audio-how-language-changes-the-indian-anime-experience":["where-to-watch-anime-legally-in-india-a-practical-guide-to-platforms-languages-and-availability","subtitles-vs-dubs-how-indian-anime-viewers-can-choose-what-works-for-them"],
"anime-between-lectures-and-chai-breaks-inside-indias-college-fan-culture":["how-to-start-an-anime-club-at-your-college-a-practical-plan-for-indian-student-communities","how-anime-communities-are-taking-shape-across-indian-cities-online-fandom-to-local-meetups"],
"beyond-watching-how-indian-anime-fans-turn-their-favourite-stories-into-art-edits-and-cosplay":["how-to-start-drawing-anime-characters-a-beginners-practice-plan-for-indian-students","your-first-cosplay-on-a-budget-planning-a-costume-with-materials-available-in-india"],
"where-to-watch-anime-legally-in-india-a-practical-guide-to-platforms-languages-and-availability":["anime-watch-orders-explained-how-to-navigate-seasons-films-specials-and-spin-offs","subtitles-vs-dubs-how-indian-anime-viewers-can-choose-what-works-for-them"],
"new-to-anime-in-india-a-beginners-roadmap-based-on-your-interests-not-just-rankings":["where-to-watch-anime-legally-in-india-a-practical-guide-to-platforms-languages-and-availability","building-an-anime-watchlist-on-a-student-budget-a-smarter-guide-for-indian-fans"],
"anime-watch-orders-explained-how-to-navigate-seasons-films-specials-and-spin-offs":["new-to-anime-in-india-a-beginners-roadmap-based-on-your-interests-not-just-rankings","subtitles-vs-dubs-how-indian-anime-viewers-can-choose-what-works-for-them"],
"subtitles-vs-dubs-how-indian-anime-viewers-can-choose-what-works-for-them":["where-to-watch-anime-legally-in-india-a-practical-guide-to-platforms-languages-and-availability","building-an-anime-watchlist-on-a-student-budget-a-smarter-guide-for-indian-fans"],
"building-an-anime-watchlist-on-a-student-budget-a-smarter-guide-for-indian-fans":["where-to-watch-anime-legally-in-india-a-practical-guide-to-platforms-languages-and-availability","new-to-anime-in-india-a-beginners-roadmap-based-on-your-interests-not-just-rankings"],
"why-anime-underdogs-resonate-with-indian-audiences-effort-family-expectations-and-ambition":["the-mentor-the-student-and-the-journey-what-anime-training-arcs-reveal-about-learning","why-the-supporting-cast-matters-how-anime-builds-friendships-beyond-the-main-hero"],
"festivals-food-and-family-exploring-everyday-cultural-details-in-anime-and-indian-life":["when-anime-became-a-family-debate-how-indian-viewers-explain-their-favourite-shows-at-home","beyond-power-levels-how-to-analyse-anime-writing-worldbuilding-and-character-growth"],
"the-mentor-the-student-and-the-journey-what-anime-training-arcs-reveal-about-learning":["why-anime-underdogs-resonate-with-indian-audiences-effort-family-expectations-and-ambition","why-the-supporting-cast-matters-how-anime-builds-friendships-beyond-the-main-hero"],
"why-the-supporting-cast-matters-how-anime-builds-friendships-beyond-the-main-hero":["beyond-power-levels-how-to-analyse-anime-writing-worldbuilding-and-character-growth","when-the-hero-makes-the-wrong-choice-understanding-moral-dilemmas-in-anime-stories"],
"when-the-hero-makes-the-wrong-choice-understanding-moral-dilemmas-in-anime-stories":["this-anime-scene-changed-how-fans-look-at-life","beyond-power-levels-how-to-analyse-anime-writing-worldbuilding-and-character-growth"],
"how-to-start-drawing-anime-characters-a-beginners-practice-plan-for-indian-students":["beyond-watching-how-indian-anime-fans-turn-their-favourite-stories-into-art-edits-and-cosplay","your-first-cosplay-on-a-budget-planning-a-costume-with-materials-available-in-india"],
"your-first-cosplay-on-a-budget-planning-a-costume-with-materials-available-in-india":["how-to-start-drawing-anime-characters-a-beginners-practice-plan-for-indian-students","your-first-anime-convention-in-india-what-to-plan-before-you-go"],
"from-fan-idea-to-finished-edit-a-beginners-guide-to-making-anime-inspired-videos":["fan-art-screenshots-and-copyright-what-indian-anime-creators-should-understand-before-publishing","how-to-start-drawing-anime-characters-a-beginners-practice-plan-for-indian-students"],
"how-to-start-an-anime-club-at-your-college-a-practical-plan-for-indian-student-communities":["anime-between-lectures-and-chai-breaks-inside-indias-college-fan-culture","how-anime-communities-are-taking-shape-across-indian-cities-online-fandom-to-local-meetups"],
"your-first-anime-convention-in-india-what-to-plan-before-you-go":["your-first-cosplay-on-a-budget-planning-a-costume-with-materials-available-in-india","how-anime-communities-are-taking-shape-across-indian-cities-online-fandom-to-local-meetups"],
"how-anime-communities-are-taking-shape-across-indian-cities-online-fandom-to-local-meetups":["how-to-start-an-anime-club-at-your-college-a-practical-plan-for-indian-student-communities","what-makes-an-anime-community-last-lessons-in-belonging-participation-and-local-leadership"],
"anime-merchandise-in-india-how-to-check-authenticity-pricing-and-seller-credibility":["manga-vs-anime-for-indian-readers-cost-availability-and-what-each-format-offers","your-first-anime-convention-in-india-what-to-plan-before-you-go"],
"manga-vs-anime-for-indian-readers-cost-availability-and-what-each-format-offers":["where-to-watch-anime-legally-in-india-a-practical-guide-to-platforms-languages-and-availability","new-to-anime-in-india-a-beginners-roadmap-based-on-your-interests-not-just-rankings"],
"could-india-build-a-bigger-animation-to-anime-pipeline-talent-training-and-industry-challenges":["learning-animation-in-india-skills-software-and-portfolio-projects-for-beginners","hand-drawn-frames-to-digital-pipelines-how-anime-production-techniques-have-evolved"],
"learning-animation-in-india-skills-software-and-portfolio-projects-for-beginners":["hand-drawn-frames-to-digital-pipelines-how-anime-production-techniques-have-evolved","could-india-build-a-bigger-animation-to-anime-pipeline-talent-training-and-industry-challenges"],
"hand-drawn-frames-to-digital-pipelines-how-anime-production-techniques-have-evolved":["learning-animation-in-india-skills-software-and-portfolio-projects-for-beginners","could-india-build-a-bigger-animation-to-anime-pipeline-talent-training-and-industry-challenges"],
"spoilers-fan-theories-and-online-debates-how-to-keep-anime-communities-welcoming":["what-makes-an-anime-community-last-lessons-in-belonging-participation-and-local-leadership","how-to-start-an-anime-club-at-your-college-a-practical-plan-for-indian-student-communities"],
"beyond-power-levels-how-to-analyse-anime-writing-worldbuilding-and-character-growth":["this-anime-scene-changed-how-fans-look-at-life","why-the-supporting-cast-matters-how-anime-builds-friendships-beyond-the-main-hero"],
"fan-art-screenshots-and-copyright-what-indian-anime-creators-should-understand-before-publishing":["from-fan-idea-to-finished-edit-a-beginners-guide-to-making-anime-inspired-videos","how-to-start-drawing-anime-characters-a-beginners-practice-plan-for-indian-students"],
"what-makes-an-anime-community-last-lessons-in-belonging-participation-and-local-leadership":["how-anime-communities-are-taking-shape-across-indian-cities-online-fandom-to-local-meetups","spoilers-fan-theories-and-online-debates-how-to-keep-anime-communities-welcoming"],
"the-next-chapter-of-anime-in-india-language-access-local-creators-and-community-growth":["could-india-build-a-bigger-animation-to-anime-pipeline-talent-training-and-industry-challenges","how-anime-communities-are-taking-shape-across-indian-cities-online-fandom-to-local-meetups"]
};
const articleTitles={
"this-anime-scene-changed-how-fans-look-at-life":"How to Explain Why an Anime Scene Stayed With You",
"when-anime-became-a-family-debate-how-indian-viewers-explain-their-favourite-shows-at-home":"Explaining Anime at Home: How Indian Fans Navigate Family Assumptions",
"hindi-tamil-telugu-or-japanese-audio-how-language-changes-the-indian-anime-experience":"Hindi, Tamil, Telugu or Japanese Audio? Choosing an Anime Language Track",
"anime-between-lectures-and-chai-breaks-inside-indias-college-fan-culture":"Anime on Campus in India: How Students Turn Shared Interests into Community",
"beyond-watching-how-indian-anime-fans-turn-their-favourite-stories-into-art-edits-and-cosplay":"Beyond Watching: A Beginner's Guide to Anime-Inspired Creative Projects",
"where-to-watch-anime-legally-in-india-a-practical-guide-to-platforms-languages-and-availability":"Where to Watch Anime Legally in India: A Practical Availability Checklist",
"new-to-anime-in-india-a-beginners-roadmap-based-on-your-interests-not-just-rankings":"New to Anime in India: A Beginner's Roadmap",
"anime-watch-orders-explained-how-to-navigate-seasons-films-specials-and-spin-offs":"Anime Watch Orders Explained: Seasons, Movies, Specials and Spin-Offs",
"subtitles-vs-dubs-how-indian-anime-viewers-can-choose-what-works-for-them":"Hindi, Tamil, Telugu or Japanese Audio? Choosing an Anime Language Track",
"building-an-anime-watchlist-on-a-student-budget-a-smarter-guide-for-indian-fans":"Building an Anime Watchlist on a Student Budget",
"why-anime-underdogs-resonate-with-indian-audiences-effort-family-expectations-and-ambition":"Why Anime Underdogs Resonate with Indian Audiences",
"festivals-food-and-family-exploring-everyday-cultural-details-in-anime-and-indian-life":"Festivals, Food and Family: Cultural Details in Anime and Indian Life",
"the-mentor-the-student-and-the-journey-what-anime-training-arcs-reveal-about-learning":"The Mentor, the Student and the Journey: Anime Training Arcs",
"why-the-supporting-cast-matters-how-anime-builds-friendships-beyond-the-main-hero":"Why the Supporting Cast Matters in Anime",
"when-the-hero-makes-the-wrong-choice-understanding-moral-dilemmas-in-anime-stories":"When the Hero Makes the Wrong Choice: Understanding Moral Dilemmas in Anime Stories",
"how-to-start-drawing-anime-characters-a-beginners-practice-plan-for-indian-students":"How to Start Drawing Anime Characters",
"your-first-cosplay-on-a-budget-planning-a-costume-with-materials-available-in-india":"Your First Cosplay on a Budget",
"from-fan-idea-to-finished-edit-a-beginners-guide-to-making-anime-inspired-videos":"From Fan Idea to Finished Edit: A Beginner's Guide",
"how-to-start-an-anime-club-at-your-college-a-practical-plan-for-indian-student-communities":"How to Start an Anime Club at Your College",
"your-first-anime-convention-in-india-what-to-plan-before-you-go":"Your First Anime Convention in India",
"how-anime-communities-are-taking-shape-across-indian-cities-online-fandom-to-local-meetups":"How Anime Communities Are Taking Shape Across Indian Cities",
"anime-merchandise-in-india-how-to-check-authenticity-pricing-and-seller-credibility":"Anime Merchandise in India: Authenticity, Pricing and Seller Credibility",
"manga-vs-anime-for-indian-readers-cost-availability-and-what-each-format-offers":"Manga vs Anime for Indian Readers",
"could-india-build-a-bigger-animation-to-anime-pipeline-talent-training-and-industry-challenges":"Could India Build a Bigger Animation-to-Anime Pipeline?",
"learning-animation-in-india-skills-software-and-portfolio-projects-for-beginners":"Learning Animation in India: Skills, Software and Portfolio Projects",
"hand-drawn-frames-to-digital-pipelines-how-anime-production-techniques-have-evolved":"How Anime Production Techniques Have Evolved",
"spoilers-fan-theories-and-online-debates-how-to-keep-anime-communities-welcoming":"Spoilers, Fan Theories and Online Debates: Keeping Communities Welcoming",
"beyond-power-levels-how-to-analyse-anime-writing-worldbuilding-and-character-growth":"Beyond Power Levels: Analysing Anime Writing and Worldbuilding",
"fan-art-screenshots-and-copyright-what-indian-anime-creators-should-understand-before-publishing":"Anime Fan Art and Copyright in India: What Creators Should Check",
"what-makes-an-anime-community-last-lessons-in-belonging-participation-and-local-leadership":"What Makes an Anime Community Last?",
"the-next-chapter-of-anime-in-india-language-access-local-creators-and-community-growth":"The Next Chapter of Anime in India"
};
const slug=location.pathname.replace(/\/+$/,'').split('/').pop();
const escText=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const sourceSets={
copyright:[['India Code: Copyright Act, 1957','https://www.indiacode.nic.in/handle/123456789/1367','Official legislation. Read the relevant provisions and amendments for your situation.'],['Copyright Office, Government of India','https://copyright.gov.in/','Official information about copyright in India.'],['YouTube Copyright Help','https://support.google.com/youtube/topic/2676339','Platform guidance on claims, removal requests and copyright processes.']],
streaming:[['Crunchyroll','https://www.crunchyroll.com/','Check the official title page for current regional availability.'],['Netflix Help Center','https://help.netflix.com/','Help with audio, subtitles and title availability; catalogues vary by region.'],['Prime Video Help','https://www.primevideo.com/help','Check supported playback language and subtitle options.']],
community:[['Indian Anime Club Community Guidelines','/community-guidelines/','The community’s own expectations for respectful participation.'],['Google Safety Center','https://safety.google/','General information about online safety and privacy.'],['UNICEF India','https://www.unicef.org/india/','Further reading on youth participation and wellbeing.']],
production:[['Association of Japanese Animations','https://aja.gr.jp/english/','Industry organisation and animation-sector resources.'],['Japan Media Arts Festival Archive','https://j-mediaarts.jp/en/','Examples of animation and media art for further study.'],['Autodesk Education','https://www.autodesk.com/education/edu-software/overview','Software and learning resources; check current eligibility and terms.']],
story:[['Japan Media Arts Festival Archive','https://j-mediaarts.jp/en/','Explore animation and media art through selected works.'],['Anime News Network','https://www.animenewsnetwork.com/','Editorial reporting and reference material about anime and manga.'],['Crunchyroll','https://www.crunchyroll.com/','Official anime catalogue; check individual title listings for current details.']]
};
let sourceSet='story';
if(/copyright|fan-art|screenshots/.test(slug))sourceSet='copyright';
else if(/where-to-watch|watch-orders|subtitles|language|watchlist|manga-vs-anime|merchandise/.test(slug))sourceSet='streaming';
else if(/community|club|convention|college|spoilers|family-debate/.test(slug))sourceSet='community';
else if(/animation|production|drawing|cosplay|creative|edit/.test(slug))sourceSet='production';
let sources=body.querySelector('.sources');
if(!sources){sources=document.createElement('section');sources.className='sources';body.appendChild(sources)}
sources.innerHTML='<h2>Sources &amp; further reading</h2><p>This article is original explanatory analysis. The links below offer additional context. For time-sensitive details, consult the original source directly.</p><ul>'+sourceSets[sourceSet].map(s=>'<li><a href="'+s[1]+'" target="_blank" rel="noopener noreferrer">'+escText(s[0])+'</a> - '+escText(s[2])+'</li>').join('')+'</ul>';
/* Move sources after the full article content, not between editorial sections. */
body.appendChild(sources);
let keep=body.querySelector('.related');
if(!keep){keep=document.createElement('section');keep.className='related';body.appendChild(keep)}
const rel=(endMatterBySlug[slug]||[]).filter(s=>articleTitles[s]);
keep.innerHTML='<h2>Keep reading</h2><ul>'+rel.map(s=>'<li><a href="./'+s+'">'+escText(articleTitles[s])+'</a></li>').join('')+'</ul>';
body.appendChild(keep);

let p=document.querySelector('.reading-progress');if(!p){p=document.createElement('div');p.className='reading-progress';p.setAttribute('aria-hidden','true');p.innerHTML='<span></span>';document.body.appendChild(p)}
const fill=p.querySelector('span');function update(){const e=document.documentElement,m=e.scrollHeight-e.clientHeight;fill.style.width=(m>0?Math.min(100,Math.max(0,e.scrollTop/m*100)):0)+'%'}
window.addEventListener('scroll',update,{passive:true});update();
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhance);else enhance();
})();