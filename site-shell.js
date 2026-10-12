/* Canonical Indian Anime Club site shell: shared homepage header and footer. */
(()=>{'use strict';
const header="<nav class=\"legacy-site-nav\" aria-label=\"Main navigation\"><div class=\"wrap\"><a class=\"logo\" href=\"/#top\"><b>IAC</b> <span class=\"ln\">Indian Anime Club</span></a><ul id=\"site-links\"><li><a href=\"/#about\">About</a></li><li><a href=\"/#worlds\">Worlds</a></li><li><a href=\"/#events\">Explore</a></li><li><a href=\"/#chapters\">Chapters</a></li><li><a href=\"/articles/\">Articles</a></li></ul><a class=\"btn\" href=\"/#join\" style=\"padding:8px 16px;font-size:14px;box-shadow:4px 4px 0 var(--accent)\">Join us</a><button class=\"menu\" id=\"menu\" type=\"button\" aria-label=\"Toggle navigation\" aria-controls=\"site-links\" aria-expanded=\"false\">&#9776;</button></div></nav>";
const footer="<footer class=\"iac-footer\"><div class=\"iac-footer-inner\"><a class=\"iac-footer-brand\" href=\"/\" aria-label=\"Indian Anime Club home\"><span>Indian Anime Club</span></a><p class=\"iac-footer-tagline\">A community, not a sales pitch. Made for India's anime community.</p><nav class=\"iac-footer-social\" aria-label=\"Social and contact links\"><a href=\"https://chat.whatsapp.com/IOR7VBI25dW9ltnofX6Frz\" target=\"_blank\" rel=\"noopener noreferrer\">WhatsApp</a><a href=\"https://instagram.com/indiananime.club\" target=\"_blank\" rel=\"noopener noreferrer\">Instagram</a><a href=\"https://www.facebook.com/people/indiananimeclub/61582607151767/\" target=\"_blank\" rel=\"noopener noreferrer\">Facebook</a><a href=\"mailto:prasad@indiananimeclub.com\">Email</a></nav><nav class=\"iac-footer-site\" aria-label=\"Website information\"><a href=\"/about/\">About</a><a href=\"/contact/\">Contact</a><a href=\"/community-guidelines/\">Community guidelines</a><a href=\"/editorial-policy/\">Editorial policy</a><a href=\"/privacy-policy/\">Privacy</a><a href=\"/terms/\">Terms</a><a href=\"/disclaimer/\">Disclaimer</a></nav><p class=\"iac-footer-copy\">© 2026 Indian Anime Club · indiananimeclub.com · Independent fan community, not affiliated with anime studios or rights holders.</p></div></footer>";
{const links=[...document.querySelectorAll('link[rel="stylesheet"]')].filter(l=>/\/(?:site-shell\.css)(?:\?|$)/.test(l.getAttribute('href')||''));let l=links.shift();if(!l){l=document.createElement('link');l.rel='stylesheet';document.head.appendChild(l)}l.href='/site-shell.css?v=20261012-4';l.dataset.iacShellCss='true';links.forEach(x=>x.remove())}
let n=document.querySelector('nav[aria-label="Main navigation"]');if(n)n.outerHTML=header;else{const m=document.querySelector('main');if(m)m.insertAdjacentHTML('beforebegin',header)}
const f=document.querySelector('footer');if(f)f.outerHTML=footer;else document.body.insertAdjacentHTML('beforeend',footer);
n=document.querySelector('nav.legacy-site-nav');const b=n&&n.querySelector('#menu');if(b&&!b.dataset.shellBound){b.dataset.shellBound='true';const close=()=>{n.classList.remove('open');b.setAttribute('aria-expanded','false');b.setAttribute('aria-label','Toggle navigation')};b.addEventListener('click',()=>{const o=n.classList.toggle('open');b.setAttribute('aria-expanded',String(o));b.setAttribute('aria-label',o?'Close navigation':'Toggle navigation')});n.querySelectorAll('ul a').forEach(a=>a.addEventListener('click',close));document.addEventListener('keydown',e=>{if(e.key==='Escape'&&n.classList.contains('open')){close();b.focus()}})}

/* Remove legacy Decision Framework cards by their visible heading, even when markup differs. */
document.querySelectorAll('article.article h1,article.article h2,article.article h3,article.article h4,article.article [role="heading"]').forEach(heading=>{
 if((heading.textContent||'').trim().replace(/\s+/g,' ').toLowerCase()!=='decision framework')return;
 let card=heading.closest('.decision-framework,[class*="decision-framework" i],[id*="decision-framework" i],.card,.panel,.callout,.framework,aside,section');
 if(!card){
  card=heading.parentElement;
  while(card&&card!==document.body&&card!==document.querySelector('article.article')&&!/^(SECTION|ASIDE|DIV)$/.test(card.tagName))card=card.parentElement;
 }
 if(card&&card!==document.body&&card!==document.querySelector('article.article')&&card!==document.querySelector('main'))card.remove();
});

/* Build one consistent, linked table of contents for every article body. */
const articleBody=document.querySelector('article.article .body');
if(articleBody){
  const headings=[...articleBody.querySelectorAll('section h2')].filter(h=>!['in brief','on this page'].includes((h.textContent||'').trim().toLowerCase()));
  const items=headings.map((h,i)=>{
    const section=h.closest('section')||h.parentElement;
    if(!section.id)section.id='article-section-'+(i+1);
    return {id:section.id,title:(h.textContent||'').trim()};
  });
  let toc=articleBody.querySelector('.article-toc');
  if(!toc){toc=document.createElement('section');toc.className='article-toc';toc.innerHTML='<h2>On this page</h2><ol></ol>';const first=articleBody.querySelector(':scope > section');if(first&&first.classList.contains('quick-answer'))first.insertAdjacentElement('afterend',toc);else articleBody.insertAdjacentElement('afterbegin',toc);}
  const list=toc.querySelector('ol')||toc.appendChild(document.createElement('ol'));
  list.replaceChildren();
  items.forEach(item=>{const li=document.createElement('li'),a=document.createElement('a');a.href='#'+item.id;a.textContent=item.title;li.appendChild(a);list.appendChild(li)});
}

/* Article pages do not display the homepage news ticker/scroller. */
document.querySelectorAll('.tick,.news-scroller,#news-scroller,.news-ticker,#news-ticker,[data-news-scroller]').forEach(el=>el.remove());

})();