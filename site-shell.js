/* Canonical Indian Anime Club site shell: shared homepage header and footer. */
(()=>{'use strict';
const header="<nav class=\"legacy-site-nav\" aria-label=\"Main navigation\"><div class=\"wrap\"><a class=\"logo\" href=\"/#top\"><b>IAC</b> <span class=\"ln\">Indian Anime Club</span></a><ul id=\"site-links\"><li><a href=\"/#about\">About</a></li><li><a href=\"/#worlds\">Worlds</a></li><li><a href=\"/#events\">Explore</a></li><li><a href=\"/#chapters\">Chapters</a></li><li><a href=\"/articles/\">Articles</a></li></ul><a class=\"btn\" href=\"/#join\" style=\"padding:8px 16px;font-size:14px;box-shadow:4px 4px 0 var(--accent)\">Join us</a><button class=\"menu\" id=\"menu\" type=\"button\" aria-label=\"Toggle navigation\" aria-controls=\"site-links\" aria-expanded=\"false\">&#9776;</button></div></nav>";
const footer="<footer class=\"iac-footer\"><div class=\"iac-footer-inner\"><a class=\"iac-footer-brand\" href=\"/\" aria-label=\"Indian Anime Club home\"><span>Indian Anime Club</span></a><p class=\"iac-footer-tagline\">A community, not a sales pitch. Made for India's anime community.</p><nav class=\"iac-footer-social\" aria-label=\"Social and contact links\"><a href=\"https://chat.whatsapp.com/IOR7VBI25dW9ltnofX6Frz\" target=\"_blank\" rel=\"noopener noreferrer\">WhatsApp</a><a href=\"https://instagram.com/indiananime.club\" target=\"_blank\" rel=\"noopener noreferrer\">Instagram</a><a href=\"https://www.facebook.com/people/indiananimeclub/61582607151767/\" target=\"_blank\" rel=\"noopener noreferrer\">Facebook</a><a href=\"mailto:prasad@indiananimeclub.com\">Email</a></nav><nav class=\"iac-footer-site\" aria-label=\"Website information\"><a href=\"/about/\">About</a><a href=\"/contact/\">Contact</a><a href=\"/community-guidelines/\">Community guidelines</a><a href=\"/editorial-policy/\">Editorial policy</a><a href=\"/privacy-policy/\">Privacy</a><a href=\"/terms/\">Terms</a><a href=\"/disclaimer/\">Disclaimer</a></nav><p class=\"iac-footer-copy\">© 2026 Indian Anime Club · indiananimeclub.com · Independent fan community, not affiliated with anime studios or rights holders.</p></div></footer>";
{const links=[...document.querySelectorAll('link[rel="stylesheet"]')].filter(l=>/\/(?:site-shell\.css)(?:\?|$)/.test(l.getAttribute('href')||''));let l=links.shift();if(!l){l=document.createElement('link');l.rel='stylesheet';document.head.appendChild(l)}const scriptSrc=document.currentScript?.src||'';const shellVersion=(scriptSrc.match(/[?&]v=([^&]+)/)||[])[1]||'20261013-4';l.href='/site-shell.css?v='+encodeURIComponent(shellVersion);l.dataset.iacShellCss='true';links.forEach(x=>x.remove())}
let n=document.querySelector('nav[aria-label="Main navigation"]');if(n)n.outerHTML=header;else{const m=document.querySelector('main');if(m)m.insertAdjacentHTML('beforebegin',header)}
const footers=[...document.querySelectorAll('footer')];if(footers.length){footers[0].outerHTML=footer;footers.slice(1).forEach(f=>f.remove())}else document.body.insertAdjacentHTML('beforeend',footer);
n=document.querySelector('nav.legacy-site-nav');const b=n&&n.querySelector('#menu');if(b&&!b.dataset.shellBound){b.dataset.shellBound='true';const close=()=>{n.classList.remove('open');b.setAttribute('aria-expanded','false');b.setAttribute('aria-label','Toggle navigation')};b.addEventListener('click',()=>{const o=n.classList.toggle('open');b.setAttribute('aria-expanded',String(o));b.setAttribute('aria-label',o?'Close navigation':'Toggle navigation')});n.querySelectorAll('ul a').forEach(a=>a.addEventListener('click',close));document.addEventListener('keydown',e=>{if(e.key==='Escape'&&n.classList.contains('open')){close();b.focus()}})}

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

/* Microsoft Clarity analytics for Indian Anime Club. Load once on every page. */
if(!window.__iacClarityLoaded){
  window.__iacClarityLoaded=true;
  (function(c,l,a,r,i,t,y){
    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
  })(window,document,"clarity","script","ywqdm8xkj7");
}
