// Minimal deck viewer: arrows / space / click to move, N = speaker notes, O = overview, P = print with notes.
(function () {
  var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
  var notes = Array.prototype.slice.call(document.querySelectorAll('.notes-src'));
  var stage = document.querySelector('.stage');
  var panel = document.querySelector('.notes-panel');
  var counter = document.querySelector('.hud .count');
  var i = 0;

  function fit() {
    if (document.body.classList.contains('overview')) return;
    var box = stage.getBoundingClientRect();
    var s = Math.min(box.width / 1320, box.height / 760);
    slides.forEach(function (el) { el.style.transform = 'translate(-50%, -50%) scale(' + s + ')'; });
  }
  function show(n) {
    i = Math.max(0, Math.min(slides.length - 1, n));
    slides.forEach(function (el, k) { el.classList.toggle('active', k === i); });
    if (counter) counter.textContent = (i + 1) + ' / ' + slides.length;
    var src = notes[i];
    panel.querySelector('.nbody').innerHTML = src ? src.querySelector('.nb').innerHTML : '';
    panel.querySelector('.nref').textContent = src ? src.getAttribute('data-ref') : '';
    if (location.hash !== '#' + (i + 1)) history.replaceState(null, '', '#' + (i + 1));
  }
  function toggleNotes() {
    panel.classList.toggle('on');
    stage.classList.toggle('with-notes', panel.classList.contains('on'));
    fit();
  }
  function toggleOverview() {
    document.body.classList.toggle('overview');
    if (!document.body.classList.contains('overview')) fit();
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') { show(i + 1); e.preventDefault(); }
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { show(i - 1); e.preventDefault(); }
    else if (e.key === 'Home') show(0);
    else if (e.key === 'End') show(slides.length - 1);
    else if (e.key === 'n' || e.key === 'N') toggleNotes();
    else if (e.key === 'o' || e.key === 'O') toggleOverview();
    else if (e.key === 'p' || e.key === 'P') { document.body.classList.add('print-notes'); window.print(); document.body.classList.remove('print-notes'); }
  });
  slides.forEach(function (el, k) {
    el.addEventListener('click', function (e) {
      if (e.target.closest('a')) return;
      if (document.body.classList.contains('overview')) { toggleOverview(); show(k); }
      else show(i + 1);
    });
  });
  document.querySelector('.hud .tn').addEventListener('click', function (e) { e.preventDefault(); toggleNotes(); });
  document.querySelector('.hud .to').addEventListener('click', function (e) { e.preventDefault(); toggleOverview(); });
  window.addEventListener('resize', fit);
  var start = parseInt((location.hash || '#1').slice(1), 10) - 1;
  if (/[?&]notes=1/.test(location.search)) toggleNotes();
  window.deckShow = show;
  fit();
  show(isNaN(start) ? 0 : start);
})();
