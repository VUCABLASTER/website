/* Werbetest (Fake Door), siehe werkzeuge/werbetest.py.
   Banner-Fassungen: Der Platz .ad-test-platz enthält alle Varianten, eine wird zufällig gezeigt.
   Post-it-Fassung: Der Vorrat .ad-store enthält alle Zettel, die Seite hat mehrere Plätze .ad-slot. Pro Seitenaufruf
   kommt ein zufälliger Zettel an einen zufälligen Platz, mit zufälligen Klebestreifen, Farbe und Neigung.
   Gezählt wird nur mit Zähler (data-zaehler): Pfad werbetest/<fassung>/<variante>[/<platz>]/gesehen bzw. /klick,
   „gesehen“ einmal, sobald der Zettel zur Hälfte sichtbar ist, „klick“ einmal pro Seitenaufruf.
   Die Anfrage geht direkt an GoatCounter (keine Cookies, kein GoatCounter-Skript). */
(function () {
  function zaehlen(zaehler, pfad) {
    if (!zaehler) return;
    var url = 'https://' + zaehler + '.goatcounter.com/count?e=true&p=' + encodeURIComponent(pfad) +
      '&t=' + encodeURIComponent(pfad) + '&rnd=' + Math.random().toString(36).slice(2);
    if (navigator.sendBeacon) { navigator.sendBeacon(url); } else { new Image().src = url; }
  }

  function zufall(liste) { return liste[Math.floor(Math.random() * liste.length)]; }

  function einrichten(banner, zaehler, pfad) {
    var geklickt = false;
    banner.querySelector('.ad-test__werbung').addEventListener('click', function () {
      if (geklickt) return;
      geklickt = true;
      zaehlen(zaehler, pfad + '/klick');
      banner.classList.add('ist-geklickt');
      var hinweis = banner.querySelector('.ad-test__hinweis');
      setTimeout(function () { hinweis.focus({ preventScroll: true }); }, 60);
    });
    if (!zaehler) return;
    if (!('IntersectionObserver' in window)) { zaehlen(zaehler, pfad + '/gesehen'); return; }
    var io = new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (e) {
        if (e.isIntersecting) { zaehlen(zaehler, pfad + '/gesehen'); io.disconnect(); }
      });
    }, { threshold: 0.5 });
    io.observe(banner);
  }

  /* Banner-Fassungen (V1–V3) */
  document.querySelectorAll('.ad-test-platz').forEach(function (platz) {
    var alle = platz.querySelectorAll('.ad-test');
    if (!alle.length) return;
    var banner = zufall(alle);
    var fassung = platz.getAttribute('data-fassung');
    banner.hidden = false;
    platz.classList.add('ist-bereit');
    einrichten(banner, platz.getAttribute('data-zaehler'),
      'werbetest/' + (fassung ? fassung + '/' : '') + banner.getAttribute('data-variante'));
  });

  /* Post-it-Fassung */
  var vorrat = document.querySelector('.ad-store');
  if (vorrat) {
    var plaetze = Array.prototype.slice.call(document.querySelectorAll('.ad-slot'));
    var wunsch = vorrat.getAttribute('data-platz');
    if (wunsch) plaetze = plaetze.filter(function (p) { return p.getAttribute('data-platz') === wunsch; });
    var zettel = vorrat.querySelectorAll('.ad-note');
    if (plaetze.length && zettel.length) {
      var platz = zufall(plaetze);
      var notiz = zufall(zettel);
      notiz.classList.add(zufall(['band-1', 'band-2', 'band-3']), zufall(['farbe-rose', 'farbe-aqua']));
      notiz.style.setProperty('--kipp', zufall(['-2.5deg', '-1.5deg', '1.2deg', '2.2deg']));
      platz.appendChild(notiz);
      notiz.hidden = false;
      einrichten(notiz, vorrat.getAttribute('data-zaehler'),
        'werbetest/' + vorrat.getAttribute('data-fassung') + '/' + notiz.getAttribute('data-variante') + '/' + platz.getAttribute('data-platz'));
    }
  }

  /* Vorschauseiten: alle Banner und Zettel sichtbar, Klick zeigt den Hinweis, ohne Zählung */
  document.querySelectorAll('.wtv .ad-test').forEach(function (banner) { einrichten(banner, '', ''); });
})();
