(()=>{'use strict';
const progress=document.getElementById('reading-progress');
const article=document.querySelector('article.article');
const readingBody=document.querySelector('article.article>.body');
const updateProgress=()=>{
 if(!progress||!readingBody)return;
 const start=readingBody.getBoundingClientRect().top+window.scrollY;
 const distance=Math.max(1,readingBody.offsetHeight-window.innerHeight);
 const value=Math.min(1,Math.max(0,(window.scrollY-start)/distance));
 progress.style.transform='scaleX('+value+')';
};
if(progress&&readingBody){
 addEventListener('scroll',updateProgress,{passive:true});
 addEventListener('resize',updateProgress);
 updateProgress();
}
const nav=document.querySelector('body>nav[aria-label="Main navigation"]');
const menu=nav?.querySelector('.menu');
if(nav&&menu){
 menu.addEventListener('click',()=>{
  const open=nav.classList.toggle('open');
  menu.setAttribute('aria-expanded',String(open));
  menu.setAttribute('aria-label',open?'Close navigation':'Open navigation');
  menu.textContent=open?'×':'☰';
 });
}
const toc=document.querySelector('.article-toc ol');
const tocBox=document.querySelector('.article-toc');
if(toc&&readingBody){
 const excluded=' .article-toc,.visual-explainer,.original-analysis,.key-takeaways,.sources,.related';
 const headings=[...readingBody.querySelectorAll('h2')].filter(h=>
  !h.closest(excluded)&&h.textContent.trim()
 );
 toc.replaceChildren();
 headings.forEach((heading,index)=>{
  if(!heading.id)heading.id='article-section-'+(index+1);
  const item=document.createElement('li');
  const link=document.createElement('a');
  link.href='#'+heading.id;
  link.textContent=heading.textContent.trim();
  item.appendChild(link);
  toc.appendChild(item);
 });
 const count=tocBox?.querySelector('.toc-count');
 if(count)count.textContent=headings.length+' sections';
 if(!headings.length&&tocBox)tocBox.hidden=true;
}
})();