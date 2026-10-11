/* Keep the original homepage navigation labels and mobile behavior consistent across every page. */
(()=>{const nav=document.querySelector('.iac-site-nav');if(!nav)return;const list=nav.querySelector('.iac-links');const btn=nav.querySelector('.iac-menu');if(!list||!btn)return;
const desired=[["About","/#about"],["Worlds","/#worlds"],["Events","/#events"],["Chapters","/#chapters"],["Articles","/articles/"]];
list.replaceChildren(...desired.map(([label,href])=>{const li=document.createElement("li");const a=document.createElement("a");a.textContent=label;a.href=href;li.append(a);return li;}));
const close=()=>{nav.classList.remove('iac-open');btn.setAttribute('aria-expanded','false');btn.setAttribute('aria-label','Toggle navigation');btn.textContent='☰'};
btn.addEventListener('click',()=>{const open=nav.classList.toggle('iac-open');btn.setAttribute('aria-expanded',String(open));btn.setAttribute('aria-label',open?'Close navigation':'Toggle navigation');btn.textContent=open?'×':'☰'});
list.querySelectorAll('a').forEach(a=>a.addEventListener('click',close));document.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav.classList.contains('iac-open')){close();btn.focus()}});
})();