/* Single, accessible homepage genre controller. Never duplicates event listeners. */
(() => {
  'use strict';
  const chips = Array.from(document.querySelectorAll('.chips button[data-genre]'));
  if (!chips.length) return;
  const palettes = {
    shonen: {fire:'#ff5a1f',cyan:'#22e4ff',sun:'#ffd23f',lime:'#b6ff3b',blue:'#1f6fff',accent:'#ff5a1f',tc:'#006f94',ts:'#8a5200'},
    'sci-fi': {fire:'#2677ff',cyan:'#17c5e5',sun:'#d9f04d',lime:'#9ce9ff',blue:'#4752e8',accent:'#2677ff',tc:'#006f94',ts:'#426800'},
    'slice-of-life': {fire:'#e76b9b',cyan:'#72cee0',sun:'#ffce58',lime:'#a9d47a',blue:'#a678d5',accent:'#e76b9b',tc:'#006f94',ts:'#8a5200'},
    isekai: {fire:'#8a5cff',cyan:'#22e4ff',sun:'#ffcd55',lime:'#b6ff3b',blue:'#7049cb',accent:'#8a5cff',tc:'#006f94',ts:'#8a5200'}
  };
  const root = document.documentElement;
  function select(button) {
    const key = button?.dataset.genre;
    const palette = palettes[key];
    if (!palette) return;
    root.dataset.genreMood = key;
    // site-shell.css defines default color tokens with !important.
    // Setting inline tokens with the same priority is necessary to override them.
    Object.entries(palette).forEach(([token, value]) => root.style.setProperty('--' + token, value, 'important'));
    chips.forEach(chip => {
      const active = chip === button;
      chip.setAttribute('aria-pressed', active ? 'true' : 'false');
      chip.classList.toggle('genre-active', active);
    });
    try { sessionStorage.setItem('iac-genre-mood', key); } catch (_error) { /* private browsing */ }
  }
  chips.forEach(chip => chip.addEventListener('click', () => select(chip)));
  let stored = null;
  try { stored = sessionStorage.getItem('iac-genre-mood'); } catch (_error) { /* private browsing */ }
  select(chips.find(chip => chip.dataset.genre === stored) || chips.find(chip => chip.getAttribute('aria-pressed') === 'true') || chips[0]);
})();
