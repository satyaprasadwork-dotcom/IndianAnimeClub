/* Resilient homepage interactions. Kept separate so a failure in optional animation code
   cannot hide content or disable the core controls. */
(function () {
  'use strict';
  function init() {
    document.documentElement.classList.add('js');
    // Content must remain visible even if an animation/reveal API is unavailable.
    document.querySelectorAll('.rv').forEach(function (el) {
      el.style.opacity = '1';
      el.style.clipPath = 'none';
      el.style.transform = 'none';
      el.classList.add('in');
    });

    // Genre mood buttons. Use delegated click handling so the controls still work
    // even if another homepage script binds or replaces their handlers.
    var genrePalette = {
      shonen: { accent: '#ff5a1f', tc: '#22e4ff', ts: '#ffd23f', glow: '#ff8a1f' },
      'sci-fi': { accent: '#22e4ff', tc: '#b6ff3b', ts: '#ffd23f', glow: '#1f6fff' },
      'slice-of-life': { accent: '#ffd23f', tc: '#ff8a1f', ts: '#22e4ff', glow: '#ff5a1f' },
      isekai: { accent: '#b6ff3b', tc: '#22e4ff', ts: '#ff8a1f', glow: '#8ad600' }
    };
    function applyGenreMood(button) {
      if (!button || !button.matches('.chips button[data-c]')) return;
      var label = (button.textContent || '').trim().toLowerCase();
      var key = label === 'sci-fi' ? 'sci-fi' : label === 'slice of life' ? 'slice-of-life' : label;
      var palette = genrePalette[key] || { accent: button.dataset.c, tc: '#22e4ff', ts: '#ffd23f', glow: button.dataset.c };
      var root = document.documentElement;
      root.style.setProperty('--accent', palette.accent);
      root.style.setProperty('--tc', palette.tc);
      root.style.setProperty('--ts', palette.ts);
      root.style.setProperty('--genre-glow', palette.glow);
      root.setAttribute('data-genre-mood', key);
      document.querySelectorAll('.chips button[data-c]').forEach(function (other) {
        var active = other === button;
        other.setAttribute('aria-pressed', String(active));
        other.classList.toggle('genre-active', active);
      });
    }
    document.addEventListener('click', function (event) {
      var button = event.target.closest && event.target.closest('.chips button[data-c]');
      if (button) applyGenreMood(button);
    }, true);
    document.querySelectorAll('.chips button[data-c]').forEach(function (button) {
      button.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' || event.key === ' ') applyGenreMood(button);
      });
    });
    // Apply the default selected genre on first load, not just after a click.
    var selectedGenre = document.querySelector('.chips button[data-c][aria-pressed="true"]');
    if (selectedGenre) applyGenreMood(selectedGenre);

    // Keep the theme visibly responsive across the header, hero, focus rings and progress accents.
    if (!document.getElementById('iac-genre-mood-style')) {
      var moodStyle = document.createElement('style');
      moodStyle.id = 'iac-genre-mood-style';
      moodStyle.textContent = [
        'html[data-genre-mood] nav { border-bottom-color: var(--accent) !important; }',
        'html[data-genre-mood] .logo b, html[data-genre-mood] .hero h1 .a { background-color: var(--accent); color: var(--dk); }',
        'html[data-genre-mood] .hero h1 .a { background: transparent; color: var(--accent); text-shadow: 5px 5px 0 var(--bg2); }',
        'html[data-genre-mood] .hero h1 .o { -webkit-text-stroke-color: var(--tc); }',
        'html[data-genre-mood] .type #tw { color: var(--ts); border-right-color: var(--ts); }',
        'html[data-genre-mood] .btn { box-shadow: 6px 6px 0 var(--accent); }',
        'html[data-genre-mood] .chips button[aria-pressed="true"] { background: var(--accent); border-color: var(--accent); }',
        'html[data-genre-mood] :focus-visible { outline-color: var(--tc); }',
        'html[data-genre-mood] #bar { box-shadow: 0 0 10px var(--genre-glow); }'
      ].join('\n');
      document.head.appendChild(moodStyle);
    }

    // Genre rail controls.
    var rail = document.getElementById('rail');
    var next = document.getElementById('nx');
    var previous = document.getElementById('pv');
    if (rail && next && !next.dataset.fixBound) {
      next.dataset.fixBound = '1';
      next.addEventListener('click', function () {
        rail.scrollBy({ left: Math.max(260, Math.round(rail.clientWidth * 0.8)), behavior: 'smooth' });
      });
    }
    if (rail && previous && !previous.dataset.fixBound) {
      previous.dataset.fixBound = '1';
      previous.addEventListener('click', function () {
        rail.scrollBy({ left: -Math.max(260, Math.round(rail.clientWidth * 0.8)), behavior: 'smooth' });
      });
    }

    // Anime watch-night idea picker. This is independent of the main page script.
    var spin = document.getElementById('spin');
    var slot = document.getElementById('slot');
    var ideas = [
      'Mecha night + pani puri', 'Cosplay couch-watch',
      'Shonen marathon, 3 episodes', 'Slice-of-life with chai',
      'Isekai bingo night', 'Sports anime hype hour',
      'Horror with the lights off', 'Studio classics double bill'
    ];
    if (spin && slot && !spin.dataset.fixBound) {
      spin.dataset.fixBound = '1';
      spin.addEventListener('click', function () {
        var idea = ideas[Math.floor(Math.random() * ideas.length)];
        slot.textContent = idea;
        slot.classList.remove('spin');
        // Re-trigger a short visual feedback without relying on animation for functionality.
        void slot.offsetWidth;
        slot.classList.add('spin');
        window.setTimeout(function () { slot.classList.remove('spin'); }, 650);
      });
    }

    // Mascot speech bubble.
    var mascot = document.getElementById('mb');
    var speech = document.getElementById('say');
    var lines = ['Yoroshiku!', 'Snacks included!', 'Sub or dub? Both!', 'Watch the opening. Always.', 'Join the WhatsApp group!', 'Is that a cosplay? Yes.'];
    if (mascot && speech && !mascot.dataset.fixBound) {
      mascot.dataset.fixBound = '1';
      mascot.addEventListener('click', function () {
        var current = Number(mascot.dataset.line || '0');
        current = (current + 1) % lines.length;
        mascot.dataset.line = String(current);
        speech.textContent = lines[current];
      });
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();

/* Genre mood accents should propagate across all homepage accent elements. */
