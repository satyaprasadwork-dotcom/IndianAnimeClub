/* Homepage discovery utilities. No trackers, account, external API or stored visitor data. */
(() => {
  "use strict";
  const dialog = document.createElement("dialog");
  dialog.className = "iac-tools-dialog";
  dialog.id = "iac-tools-dialog";
  dialog.setAttribute("aria-labelledby", "iac-tools-heading");
  dialog.innerHTML = '<div class="iac-tools-shell"><button type="button" class="iac-tools-close" aria-label="Close tool">×</button><p class="iac-tools-eyebrow">INDIAN ANIME CLUB · FAN TOOLS</p><h2 id="iac-tools-heading"></h2><p id="iac-tools-intro"></p><div id="iac-tools-fields"></div><div id="iac-tools-output" role="status" aria-live="polite"></div><p class="iac-tools-note">Suggestions are editorial starting points, not live streaming listings. Check age ratings, title, season, language tracks and legal availability for India before watching.</p></div>';
  document.body.append(dialog);
  const heading=dialog.querySelector("#iac-tools-heading");
  const intro=dialog.querySelector("#iac-tools-intro");
  const fields=dialog.querySelector("#iac-tools-fields");
  const output=dialog.querySelector("#iac-tools-output");
  const note=dialog.querySelector(".iac-tools-note");
  let opener=null;
  const guide='/where-to-watch-anime-legally-in-india-a-practical-guide-to-platforms-languages-and-availability/';
  const picks={
    shonen:{name:"Shonen",description:"Action, rivalry, progress and consequences.",titles:[
      ["Fullmetal Alchemist: Brotherhood","A completed adventure with an unusually strong focus on the cost of decisions."],
      ["Mob Psycho 100","A character-led supernatural story about power, belonging and growing up."],
      ["Haikyu!!","A team-sport alternative if training and friendships interest you more than battles."]]},
    mecha:{name:"Mecha",description:"Technology, relationships and the human cost of conflict.",titles:[
      ["Mobile Suit Gundam: The Witch from Mercury","A school setting that develops into a larger political and personal conflict."],
      ["86 Eighty-Six","A war drama that asks whose stories and losses are made visible."],
      ["Neon Genesis Evangelion","An introspective, often intense classic; check content suitability first."]]},
    slice:{name:"Slice of life",description:"Everyday rhythms, gentle humour and personal growth.",titles:[
      ["Barakamon","A young calligrapher learns from a close-knit island community."],
      ["Laid-Back Camp","Outdoor routines, friendship and a relaxed pace."],
      ["K-On!","Friendship and music-club life rather than a high-stakes quest."]]},
    isekai:{name:"Isekai",description:"New worlds, unfamiliar rules and changed identities.",titles:[
      ["Ascendance of a Bookworm","A book-loving protagonist learns how a very different society works."],
      ["Re:Zero","A darker story about consequences, repeated attempts and emotional strain."],
      ["That Time I Got Reincarnated as a Slime","A lighter fantasy focused partly on building a community."]]},
    sports:{name:"Sports",description:"Competition, collaboration and the work between victories.",titles:[
      ["Run with the Wind","A team running story about motivation and shared effort."],
      ["Haikyu!!","Volleyball, setbacks, teamwork and evolving rivals."],
      ["Blue Lock","An intense football competition with a different approach to individual ambition."]]},
    horror:{name:"Horror",description:"Mystery, unease and heavier themes; review age guidance.",titles:[
      ["Mononoke","A distinctive supernatural mystery driven by layered storytelling."],
      ["Another","A suspense mystery with disturbing and violent elements."],
      ["Shiki","An unsettling slow-burn story about fear and community decisions."]]}
  };
  const esc = value=>String(value).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  function open(title,description,markup){
    heading.textContent=title;intro.textContent=description;fields.innerHTML=markup;output.replaceChildren();output.hidden=true;
    note.hidden=false;
    if(typeof dialog.showModal === "function"){dialog.showModal();dialog.querySelector(".iac-tools-close").focus();}
    else { dialog.setAttribute("open","");dialog.querySelector(".iac-tools-close").focus(); }
  }
  function reveal(text,extra){
    output.hidden=false;output.replaceChildren();
    const p=document.createElement("p");p.textContent=text;output.append(p);
    if(extra){const a=document.createElement("a");a.href=extra;a.textContent="How to verify legal viewing options in India ↗";output.append(a);}
  }
  function genre(key){
    const g=picks[key];if(!g)return;
    open("Explore "+g.name,g.description+' These are examples, not a real-time catalogue.',
      '<div class="iac-pick-list">'+g.titles.map(([title,why],i)=>'<div><b>'+(i+1)+'. '+esc(title)+'</b><p>'+esc(why)+'</p></div>').join('')+'</div><a class="iac-tools-action" href="'+guide+'">Verify viewing options in India ↗</a>');
    output.hidden=true;
  }
  function starter(){
    const options=Object.entries(picks).map(([key,g])=>'<option value="'+key+'">'+esc(g.name)+'</option>').join('');
    open("Find your next anime","Choose a story mood and viewing commitment. Get three specific titles to investigate.",
      '<div class="iac-tools-form"><label for="iac-starter-mood">What are you in the mood for?</label><select id="iac-starter-mood">'+options+'</select><label for="iac-starter-time">How much time do you want to commit?</label><select id="iac-starter-time"><option value="sample">Try one episode first</option><option value="weekly">Watch a few episodes each week</option><option value="binge">Explore a longer story</option></select><button type="button" class="iac-tools-action" data-iac-calc="starter">Find three starting points</button></div>');
  }
  function prompt(){
    open("Spoiler-safe conversation starter","Generate an original prompt you can take to an anime group chat without assuming everyone is caught up.",
      '<div class="iac-tools-form"><label for="iac-prompt-topic">Discussion topic</label><select id="iac-prompt-topic"><option value="character">Character choices</option><option value="sound">Music and sound</option><option value="craft">Animation and visual style</option><option value="world">Worldbuilding</option></select><label for="iac-spoiler-level">Spoiler boundary</label><select id="iac-spoiler-level"><option value="none">No plot spoilers</option><option value="early">Only the first episode</option><option value="full">Full-series spoilers, clearly marked</option></select><button type="button" class="iac-tools-action" data-iac-calc="prompt">Make a discussion prompt</button></div>');
  }
  function cosplay(){
    open("Cosplay budget check","Estimate materials and leave room for overruns. These are your own inputs, not live shop prices.",
      '<div class="iac-tools-form"><label for="iac-cosplay-limit">Your maximum spend (₹)</label><input id="iac-cosplay-limit" type="number" min="0" max="1000000" step="1" value="2500"><label for="iac-cosplay-costume">Costume and fabric (₹)</label><input id="iac-cosplay-costume" type="number" min="0" max="1000000" step="1" value="900"><label for="iac-cosplay-props">Props and accessories (₹)</label><input id="iac-cosplay-props" type="number" min="0" max="1000000" step="1" value="400"><label for="iac-cosplay-other">Makeup, travel and other costs (₹)</label><input id="iac-cosplay-other" type="number" min="0" max="1000000" step="1" value="450"><button type="button" class="iac-tools-action" data-iac-calc="cosplay">Calculate budget</button></div>');
  }
  function decisions(){
    open("Character choice mapper","Examine a fictional character's decision without claiming there is only one right interpretation.",
      '<div class="iac-tools-form"><label for="iac-choice-character">Character or story</label><input id="iac-choice-character" type="text" maxlength="90" placeholder="Character name"><label for="iac-choice-action">Decision they faced</label><input id="iac-choice-action" type="text" maxlength="160" placeholder="What did they choose?"><label for="iac-choice-other">Alternative they could have taken</label><input id="iac-choice-other" type="text" maxlength="160" placeholder="What else was possible?"><button type="button" class="iac-tools-action" data-iac-calc="decisions">Build a discussion worksheet</button></div>');
    note.hidden=true;
  }
  function scene(){
    open("Scene analysis worksheet","Turn a first impression into an evidence-led interpretation. Avoid reproducing copyrighted dialogue or images.",
      '<div class="iac-tools-form"><label for="iac-scene-title">Anime and scene (briefly)</label><input id="iac-scene-title" type="text" maxlength="120" placeholder="Series and scene"><label for="iac-scene-observe">What is directly observable?</label><textarea id="iac-scene-observe" maxlength="350" rows="2" placeholder="Camera movement, composition, pacing, gesture..."></textarea><label for="iac-scene-read">What might that detail suggest?</label><textarea id="iac-scene-read" maxlength="350" rows="2" placeholder="Your interpretation, not a proven creator intention"></textarea><button type="button" class="iac-tools-action" data-iac-calc="scene">Build my scene note</button></div>');
    note.hidden=true;
  }
  function clean(id){return (dialog.querySelector('#'+id)?.value||"").trim().slice(0,350);}
  function amount(id){
    const v=Number(clean(id));
    return Number.isSafeInteger(v)&&v>=0&&v<=1000000?v:null;
  }
  const rupee=n=>'₹'+n.toLocaleString('en-IN');
  dialog.querySelector(".iac-tools-close").addEventListener("click",()=>dialog.close());
  dialog.addEventListener("click",event=>{if(event.target===dialog)dialog.close();});
  dialog.addEventListener("close",()=>{if(opener&&opener.isConnected)opener.focus();});
  fields.addEventListener("click",event=>{
    const key=event.target.closest("[data-iac-calc]")?.dataset.iacCalc;
    if(!key)return;
    if(key==="starter"){
      const g=picks[clean("iac-starter-mood")]||picks.shonen;
      const pace={sample:"Try the opening episode and decide whether the tone works for you.",weekly:"Pick one title and schedule a few episodes each week.",binge:"Check its season and episode count before you commit."}[clean("iac-starter-time")];
      reveal(g.name+": "+g.titles.map(t=>t[0]).join(" · ")+". "+pace+" None of these titles has been checked for current regional availability.",guide);
    }
    if(key==="prompt"){
      const prompts={character:"What is one choice that reveals a character's values without relying on a major twist?",sound:"How does background sound or silence change the atmosphere of a scene?",craft:"Which visual detail makes a moment readable before any character speaks?",world:"What small everyday detail makes a fictional setting feel consistent?"};
      const boundary={none:"No plot spoilers, please.",early:"Discussion limited to episode one; label any spoilers.",full:"FULL-SERIES SPOILERS: please warn readers before sharing plot details."};
      reveal(boundary[clean("iac-spoiler-level")]+" "+prompts[clean("iac-prompt-topic")]);note.hidden=true;
    }
    if(key==="cosplay"){
      const values=["iac-cosplay-limit","iac-cosplay-costume","iac-cosplay-props","iac-cosplay-other"].map(amount);
      if(values.some(v=>v===null)){reveal("Enter valid whole-number amounts from ₹0 to ₹10,00,000.");return;}
      const [limit,costume,props,other]=values,total=costume+props+other,balance=limit-total;
      reveal("Estimated total: "+rupee(total)+". "+(balance>=0?rupee(balance)+" remaining for a contingency.":"Over budget by "+rupee(-balance)+". Consider simplifying props or reusing materials.")+" This is an estimate, not a quotation.");note.hidden=true;
    }
    if(key==="decisions"){
      const person=clean("iac-choice-character")||"The character";
      const action=clean("iac-choice-action"),other=clean("iac-choice-other");
      if(!action||!other){reveal("Enter both the decision and an alternative to compare.");return;}
      reveal(person+" chose: "+action+". Alternative: "+other+". Compare what each option protects, who bears the cost, and what scene evidence supports your interpretation. What would change your mind?");
    }
    if(key==="scene"){
      const title=clean("iac-scene-title"),observed=clean("iac-scene-observe"),reading=clean("iac-scene-read");
      if(!observed||!reading){reveal("Add both an observable detail and a possible interpretation.");return;}
      reveal((title?title+". ":"")+"Observation: "+observed+". Possible interpretation: "+reading+". Evidence to recheck: the scene's immediate context, camera or sound choices, and what happens next. Other readings may also fit.");
    }
  });
  const tools={starter,prompt,cosplay,decisions,scene,genre:()=>genre("shonen")};
  function activate(el,event){
    if(event){if(event.type==="keydown"&&!["Enter"," "].includes(event.key))return;if(event.type==="keydown")event.preventDefault();}
    const key=el.dataset.iacTool, genreKey=el.dataset.iacGenre;
    if(typeof dialog.showModal!=="function")return;
    if(key&&!tools[key]&&!genreKey)return;
    if(event)event.preventDefault();
    opener=el;
    if(genreKey)genre(genreKey);else tools[key]();
  }
  document.querySelectorAll("[data-iac-tool],[data-iac-genre]").forEach(el=>{
    el.addEventListener("click",event=>activate(el,event));
    if(!["A","BUTTON"].includes(el.tagName))el.addEventListener("keydown",event=>activate(el,event));
  });
})();