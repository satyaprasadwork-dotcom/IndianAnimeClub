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

(()=>{'use strict';
const progress=document.getElementById('reading-progress');
const readingBody=document.querySelector('article.article>.body');
const updateProgress=()=>{
 if(!progress||!readingBody)return;
 const start=readingBody.getBoundingClientRect().top+window.scrollY;
 const distance=Math.max(1,readingBody.offsetHeight-window.innerHeight);
 progress.style.transform='scaleX('+Math.min(1,Math.max(0,(window.scrollY-start)/distance))+')';
};
if(progress&&readingBody){
 addEventListener('scroll',updateProgress,{passive:true});
 addEventListener('resize',updateProgress);
 updateProgress();
}
const toc=document.querySelector('.article-toc ol');
const tocBox=document.querySelector('.article-toc');
if(toc&&readingBody){
 const excluded='.article-toc,.visual-explainer,.original-analysis,.key-takeaways,.sources,.related';
 const headings=[...readingBody.querySelectorAll('h2')].filter(h=>!h.closest(excluded)&&h.textContent.trim());
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