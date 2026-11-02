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

/* Analytics, AdSense and Clarity are now loaded exactly once from the HTML head.
   Never load them again in this shared navigation script. */

/* Accessible keyboard escape route where one is not already present. */
(function(){
 var main=document.querySelector('main');
 if(!main||document.querySelector('a.skip-link,a.skip'))return;
 if(!main.id)main.id='main-content';
 var a=document.createElement('a');a.className='skip-link';a.href='#'+main.id;
 a.textContent='Skip to main content';document.body.insertBefore(a,document.body.firstChild);
})();
