/* 2-Klick-Player: Die Audiodatei wird erst nach Klick von podcaster.de geladen.
   Keine Einwilligung wird gespeichert. Ohne JavaScript bleibt der MP3-Link sichtbar. */
(function () {
  var box = document.querySelector('[data-player]');
  if (!box) return;
  var button = box.querySelector('[data-player-load]');
  var fallback = box.querySelector('[data-player-fallback]');
  var status = box.querySelector('[data-player-status]');
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
    button.replaceWith(audio);
    if (status) status.textContent = 'Der Player ist geladen.';
    audio.focus();
    var playing = audio.play();
    if (playing && playing.catch) playing.catch(function () {});
  });
})();
