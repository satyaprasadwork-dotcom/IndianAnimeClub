/* Google AdSense publisher tag. Guard against duplicate loading when shared scripts overlap. */
(function(){
  if (document.querySelector('script[data-iac-adsense="true"]') || document.querySelector('script[src*="pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"]')) return;
  var adsenseScript = document.createElement('script');
  adsenseScript.async = true;
  adsenseScript.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7937216909291905';
  adsenseScript.crossOrigin = 'anonymous';
  adsenseScript.setAttribute('data-iac-adsense', 'true');
  (document.head || document.documentElement).appendChild(adsenseScript);
})();

/* Header and footer are rendered from /partials/ at build time.
   This script only attaches behaviour; it never replaces shared DOM markup. */
(() => {
  'use strict';
  const scriptSrc = document.currentScript?.src || '';
  const version = (scriptSrc.match(/[?&]v=([^&]+)/) || [])[1] || 'shared';
  const links = [...document.querySelectorAll('link[rel="stylesheet"]')]
    .filter(link => /\/site-shell\.css(?:\?|$)/.test(link.getAttribute('href') || ''));
  let css = links.shift();
  if (!css) {
    css = document.createElement('link');
    css.rel = 'stylesheet';
    document.head.appendChild(css);
  }
  // Preserve the build's content hash. Replacing it with "shared" or a stale
  // script query string made raw Hostinger pages reuse an old stylesheet.
  if (!css.getAttribute('href')) css.href = '/site-shell.css?v=' + encodeURIComponent(version);
  css.dataset.iacShellCss = 'true';
  links.forEach(link => link.remove());

  const nav = document.querySelector('nav.legacy-site-nav[aria-label="Main navigation"]');
  const button = nav?.querySelector('#menu');
  if (button && !button.dataset.shellBound) {
    button.dataset.shellBound = 'true';
    const close = () => {
      nav.classList.remove('open');
      button.setAttribute('aria-expanded', 'false');
      button.setAttribute('aria-label', 'Toggle navigation');
    };
    button.addEventListener('click', event => {
      // Capture this click before legacy inline handlers can toggle the menu twice.
      event.stopImmediatePropagation();
      const open = nav.classList.toggle('open');
      button.setAttribute('aria-expanded', String(open));
      button.setAttribute('aria-label', open ? 'Close navigation' : 'Toggle navigation');
    }, true);
    nav.querySelectorAll('ul a').forEach(link => link.addEventListener('click', close));
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && nav.classList.contains('open')) {
        close();
        button.focus();
      }
    });
    window.matchMedia('(min-width:901px)').addEventListener('change', close);
  }
  // Article pages never show the homepage news ticker.
  if (document.querySelector('article.article')) {
    document.querySelectorAll('.tick,.news-scroller,#news-scroller,.news-ticker,#news-ticker,[data-news-scroller]')
      .forEach(element => element.remove());
  }
})();

/* Microsoft Clarity analytics for Indian Anime Club. Load once on every page. */
if(!window.__iacClarityLoaded && typeof window.clarity !== 'function'){
  window.__iacClarityLoaded=true;
  (function(c,l,a,r,i,t,y){
    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
  })(window,document,"clarity","script","ywqdm8xkj7");
}

/* Load GA4 once for article routes. Other pages have an explicit head tag. */
(function(){
 var id='G-M4738D1ZND';
 if(document.querySelector('script[src*="googletagmanager.com/gtag/js?id='+id+'"]'))return;
 window.dataLayer=window.dataLayer||[];
 if(typeof window.gtag!=='function')window.gtag=function(){window.dataLayer.push(arguments);};
 window.gtag('js',new Date());
 window.gtag('config',id);
 var s=document.createElement('script');s.async=true;
 s.src='https://www.googletagmanager.com/gtag/js?id='+encodeURIComponent(id);
 s.dataset.iacGa4='true';document.head.appendChild(s);
})();
/* Accessible keyboard escape route where one is not already present. */
(function(){
 var main=document.querySelector('main');
 if(!main||document.querySelector('a.skip-link,a.skip'))return;
 if(!main.id)main.id='main-content';
 var a=document.createElement('a');a.className='skip-link';a.href='#'+main.id;
 a.textContent='Skip to main content';document.body.insertBefore(a,document.body.firstChild);
})();
