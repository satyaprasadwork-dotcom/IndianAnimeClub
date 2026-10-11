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

    // Genre mood buttons.
    document.querySelectorAll('.chips button[data-c]').forEach(function (button) {
      if (button.dataset.fixBound) return;
      button.dataset.fixBound = '1';
      button.addEventListener('click', function () {
        document.querySelectorAll('.chips button[data-c]').forEach(function (other) {
          other.setAttribute('aria-pressed', String(other === button));
        });
        document.documentElement.style.setProperty('--accent', button.dataset.c);
      });
    });

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