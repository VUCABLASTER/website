/* 2-Klick-Player: Die Audiodatei wird erst nach Klick von podcaster.de geladen.
   Keine Einwilligung wird gespeichert. Ohne JavaScript bleibt der MP3-Link sichtbar.
   Funktioniert für mehrere Player auf einer Seite (Leiste oben und Karte bei der Folge);
   es spielt immer nur einer. */
(function () {
  var boxes = document.querySelectorAll('[data-player]');
  if (!boxes.length) return;
  var geladen = [];

  Array.prototype.forEach.call(boxes, function (box) {
    var button = box.querySelector('[data-player-load]');
    var fallback = box.querySelector('[data-player-fallback]');
    var status = box.querySelector('[data-player-status]');
    var note = box.querySelector('[data-player-note]');
    if (!button) return;

    button.hidden = false;
    if (fallback) fallback.hidden = true;

    button.addEventListener('click', function () {
      var audio = document.createElement('audio');
      audio.controls = true;
      audio.preload = 'none';
      audio.src = box.getAttribute('data-src');
      audio.setAttribute('aria-label', 'Audio-Player: ' + (box.getAttribute('data-title') || 'aktuelle Folge'));
      audio.tabIndex = 0;
      audio.addEventListener('play', function () {
        geladen.forEach(function (a) { if (a !== audio) a.pause(); });
      });
      geladen.push(audio);
      button.replaceWith(audio);
      box.classList.add('is-loaded');
      if (status) status.textContent = 'Der Player ist geladen.';
      if (note) note.hidden = true;
      audio.focus();
      var playing = audio.play();
      if (playing && playing.catch) playing.catch(function () {});
    });
  });
})();
