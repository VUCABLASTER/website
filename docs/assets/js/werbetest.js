/* Werbetest (Fake Door), siehe werkzeuge/werbetest.py.
   Zeigt pro Seitenaufruf zufällig eine Variante. Gezählt wird nur, wenn der Platz einen Zähler hat:
   „gesehen“ einmal, sobald das Banner zur Hälfte sichtbar ist, „klick“ einmal pro Seitenaufruf.
   Die Anfrage geht direkt an GoatCounter (keine Cookies, kein GoatCounter-Skript). */
(function () {
  function zaehlen(zaehler, pfad) {
    if (!zaehler) return;
    var url = 'https://' + zaehler + '.goatcounter.com/count?e=true&p=' + encodeURIComponent(pfad) +
      '&t=' + encodeURIComponent(pfad) + '&rnd=' + Math.random().toString(36).slice(2);
    if (navigator.sendBeacon) { navigator.sendBeacon(url); } else { new Image().src = url; }
  }

  function einrichten(banner, zaehler) {
    var id = banner.getAttribute('data-variante');
    var geklickt = false;
    banner.querySelector('.ad-test__werbung').addEventListener('click', function () {
      if (geklickt) return;
      geklickt = true;
      zaehlen(zaehler, 'werbetest/' + id + '/klick');
      banner.classList.add('ist-geklickt');
      var hinweis = banner.querySelector('.ad-test__hinweis');
      hinweis.focus({ preventScroll: true });
    });
    if (!zaehler) return;
    if (!('IntersectionObserver' in window)) { zaehlen(zaehler, 'werbetest/' + id + '/gesehen'); return; }
    var io = new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (e) {
        if (e.isIntersecting) { zaehlen(zaehler, 'werbetest/' + id + '/gesehen'); io.disconnect(); }
      });
    }, { threshold: 0.5 });
    io.observe(banner);
  }

  document.querySelectorAll('.ad-test-platz').forEach(function (platz) {
    var alle = platz.querySelectorAll('.ad-test');
    if (!alle.length) return;
    var banner = alle[Math.floor(Math.random() * alle.length)];
    banner.hidden = false;
    platz.classList.add('ist-bereit');
    einrichten(banner, platz.getAttribute('data-zaehler'));
  });

  /* Vorschauseite: alle Banner sichtbar, Klick zeigt den Hinweis, ohne Zählung */
  document.querySelectorAll('.wtv .ad-test').forEach(function (banner) { einrichten(banner, ''); });
})();
