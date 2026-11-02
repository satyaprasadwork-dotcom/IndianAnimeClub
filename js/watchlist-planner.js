/* Original watchlist planner: arithmetic only, no persistent data, no network calls. */
(function(){
 'use strict';
 const form=document.getElementById('iac-watch-form');
 if(!form)return;
 const rows=document.getElementById('iac-series-rows');
 const add=document.getElementById('iac-add-row');
 const copy=document.getElementById('iac-copy-plan');
 const status=document.getElementById('iac-copy-status');
 let nextId=2;
 let copyText='';
 function intIn(el,min,max,fallback){
   const n=Number(el.value);
   return Number.isSafeInteger(n)&&n>=min&&n<=max?n:fallback;
 }
 function hours(){
   const n=Number(document.getElementById('iac-weekly-hours').value);
   return Number.isFinite(n)&&n>=0.5&&n<=60?n:0;
 }
 function addRow(){
   if(rows.children.length>=8)return;
   const id=nextId++;
   const row=document.createElement('div');
   row.className='iac-series-row';
   row.innerHTML='<div><label for="iac-title-'+id+'">Anime title</label><input id="iac-title-'+id+'" class="iac-series-title" type="text" maxlength="90" placeholder="Title or season"></div>'+
   '<div><label for="iac-episodes-'+id+'">Episodes left</label><input id="iac-episodes-'+id+'" class="iac-series-episodes" type="number" min="0" max="999" step="1" value="6"></div>'+
   '<div><label for="iac-minutes-'+id+'">Minutes / episode</label><input id="iac-minutes-'+id+'" class="iac-series-minutes" type="number" min="1" max="240" step="1" value="24"></div>'+
   '<button type="button" class="iac-remove-row" aria-label="Remove this anime">Remove</button>';
   rows.appendChild(row);
   row.querySelector('input').focus();
   add.disabled=rows.children.length>=8;
 }
 add.addEventListener('click',addRow);
 rows.addEventListener('click',event=>{
   if(!event.target.matches('.iac-remove-row'))return;
   if(rows.children.length<=1){const row=rows.children[0];row.querySelector('.iac-series-title').value='';row.querySelector('.iac-series-episodes').value='0';return;}
   event.target.closest('.iac-series-row').remove();
   add.disabled=false;
 });
 form.addEventListener('submit',event=>{
   event.preventDefault();
   status.textContent='';
   const budgetMinutes=Math.floor(hours()*60);
   if(budgetMinutes<30){status.textContent='Enter at least 0.5 hours of available viewing time.';return;}
   let remaining=budgetMinutes,used=0,total=0;
   const lines=[];
   const list=document.getElementById('iac-result-list');
   list.replaceChildren();
   Array.from(rows.children).forEach((row,index)=>{
     const title=(row.querySelector('.iac-series-title').value||'Untitled series').trim();
     const episodes=intIn(row.querySelector('.iac-series-episodes'),0,999,0);
     const minutes=intIn(row.querySelector('.iac-series-minutes'),1,240,24);
     const fit=Math.min(episodes,Math.floor(remaining/minutes));
     remaining-=fit*minutes;used+=fit*minutes;total+=fit;
     const item=document.createElement('li');
     item.textContent=title+': '+fit+' of '+episodes+' episodes ('+minutes+' min each).'+(episodes>fit?' '+(episodes-fit)+' remain for later.':'');
     list.appendChild(item);
     lines.push((index+1)+'. '+item.textContent);
   });
   document.getElementById('iac-total-episodes').textContent=String(total);
   document.getElementById('iac-time-result').textContent='Planned '+used+' of '+budgetMinutes+' minutes. '+remaining+' minutes unallocated.';
   const limit=intIn(document.getElementById('iac-budget-limit'),0,1000000,0);
   const spend=intIn(document.getElementById('iac-budget-spend'),0,1000000,0);
   const difference=limit-spend;
   const finance='Budget: ₹'+limit.toLocaleString('en-IN')+' ceiling, ₹'+spend.toLocaleString('en-IN')+' planned; '+(difference>=0?'₹'+difference.toLocaleString('en-IN')+' remaining.':'₹'+Math.abs(difference).toLocaleString('en-IN')+' over your ceiling.');
   document.getElementById('iac-money-result').textContent=finance;
   copyText='Indian Anime Club weekly watchlist\n'+lines.join('\n')+'\n'+used+'/'+budgetMinutes+' minutes allocated.\n'+finance+'\nVerify licensing and language tracks independently.';
 });
 copy.addEventListener('click',()=>{
   if(!copyText){status.textContent='Calculate a plan first.';return;}
   if(!navigator.clipboard||!navigator.clipboard.writeText){status.textContent='Clipboard is unavailable here. You can select the results and copy them.';return;}
   navigator.clipboard.writeText(copyText).then(()=>status.textContent='Plan copied.',()=>status.textContent='Clipboard access is blocked. You can select the results and copy them.');
 });
 form.requestSubmit();
})();
