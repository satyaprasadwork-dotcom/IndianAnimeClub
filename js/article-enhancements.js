(function(){
'use strict';
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
let visual=body.querySelector('.visual-explainer');
const d=D[slug];
if(!visual){
  visual=document.createElement('section');visual.className='visual-explainer';
  visual.innerHTML='<p class="eyebrow">Decision framework</p><h2></h2>';
  const anchor=body.querySelector('.quick-answer')||body.querySelector('.key-takeaways')||body.firstElementChild;
  if(anchor)anchor.insertAdjacentElement('beforebegin',visual);else body.prepend(visual);
}
const h=visual.querySelector('h2'),e=visual.querySelector('.eyebrow');
if(d){
  if(h)h.textContent=d[1];if(e)e.textContent='Topic diagram';
  const svg=diagram(slug);
  if(svg){visual.querySelectorAll('.visual-grid,.topic-diagram-svg').forEach(n=>n.remove());visual.insertAdjacentHTML('beforeend',svg)}
  else if(!visual.querySelector('.visual-grid')){
    const fallback=document.createElement('div');fallback.className='visual-grid';
    d[2].slice(0,3).forEach((label,i)=>{const card=document.createElement('div'),b=document.createElement('b'),span=document.createElement('span');b.textContent=label;span.textContent=['Define the requirement and constraints','Evaluate evidence and trade-offs','Choose controls and review the outcome'][i];card.append(b,span);fallback.appendChild(card)});visual.appendChild(fallback);
  }
}else{
  if(h)h.textContent='A practical decision path';if(e)e.textContent='Decision framework';
  if(!visual.querySelector('.visual-grid,.topic-diagram-svg')){
    const fallback=document.createElement('div');fallback.className='visual-grid';
    [['Define','State the goal, user and constraints'],['Evaluate','Compare evidence, risks and alternatives'],['Decide','Choose an action, owner and review point']].forEach(([label,desc])=>{const card=document.createElement('div'),b=document.createElement('b'),span=document.createElement('span');b.textContent=label;span.textContent=desc;card.append(b,span);fallback.appendChild(card)});visual.appendChild(fallback);
  }
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
let p=document.querySelector('.reading-progress');if(!p){p=document.createElement('div');p.className='reading-progress';p.setAttribute('aria-hidden','true');p.innerHTML='<span></span>';document.body.appendChild(p)}
const fill=p.querySelector('span');function update(){const e=document.documentElement,m=e.scrollHeight-e.clientHeight;fill.style.width=(m>0?Math.min(100,Math.max(0,e.scrollTop/m*100)):0)+'%'}
window.addEventListener('scroll',update,{passive:true});update();
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhance);else enhance();
})();