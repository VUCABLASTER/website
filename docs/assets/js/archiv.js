/* Archiv: Suche und Filter im Browser. Ohne JavaScript bleibt die komplette Liste sichtbar.
   Die Transkripte (folgen/transkripte.json) werden erst geladen, wenn jemand ab 3 Zeichen sucht. */
(function () {
  var tools = document.querySelector('[data-archiv-tools]');
  var liste = document.querySelector('[data-archiv-liste]');
  if (!tools || !liste) return;
  var items = Array.prototype.slice.call(liste.querySelectorAll('.ep-item'));
  var anzahl = document.querySelector('[data-archiv-anzahl]');
  var leer = document.querySelector('[data-archiv-leer]');
  var reset = document.querySelector('[data-archiv-reset]');
  var felder = {
    text: tools.querySelector('[data-filter="text"]'),
    wert: tools.querySelector('[data-filter="wert"]'),
    staffel: tools.querySelector('[data-filter="staffel"]'),
    jahr: tools.querySelector('[data-filter="jahr"]')
  };
  var transkripte = null, laedt = false;

  function normal(s) {
    return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/\s+/g, ' ').trim();
  }

  function transkripteLaden() {
    if (transkripte || laedt) return;
    laedt = true;
    fetch('transkripte.json').then(function (r) { return r.ok ? r.json() : {}; })
      .then(function (d) { transkripte = d; filtern(); })
      .catch(function () { transkripte = {}; });
  }

  function enthaelt(text, woerter) {
    return woerter.every(function (w) { return text.indexOf(w) !== -1; });
  }

  function filtern() {
    var suche = normal(felder.text.value);
    var woerter = suche.split(' ').filter(Boolean);
    if (suche.length >= 3) transkripteLaden();
    var wert = felder.wert.value, staffel = felder.staffel.value, jahr = felder.jahr.value;
    var sichtbar = 0;
    items.forEach(function (li) {
      var filterOk =
        (!wert || (' ' + li.dataset.werte + ' ').indexOf(' ' + wert + ' ') !== -1) &&
        (!staffel || li.dataset.staffel === staffel) &&
        (!jahr || li.dataset.jahr === jahr);
      var metaOk = enthaelt(li.dataset.text, woerter);
      var t = transkripte && transkripte[li.dataset.nr];
      var transkriptOk = !metaOk && woerter.length > 0 && !!t && enthaelt(t, woerter);
      var passt = filterOk && (metaOk || transkriptOk);
      li.hidden = !passt;
      var hit = li.querySelector('.ep-hit');
      if (hit) hit.hidden = !(passt && transkriptOk);
      if (passt) sichtbar++;
    });
    anzahl.textContent = (sichtbar === 1 ? '1 Folge' : sichtbar + ' Folgen') +
      (laedt && !transkripte ? ' · durchsuche Transkripte …' : '');
    leer.hidden = sichtbar !== 0;
  }

  tools.hidden = false;
  tools.addEventListener('input', filtern);
  tools.addEventListener('change', filtern);
  if (reset) reset.addEventListener('click', function () {
    tools.reset();
    filtern();
    felder.text.focus();
  });

  // Filter aus der Adresse übernehmen, z. B. /folgen/?wert=mutig
  var params = new URLSearchParams(location.search);
  ['wert', 'staffel', 'jahr'].forEach(function (k) { if (params.get(k)) felder[k].value = params.get(k); });
  if (params.get('suche')) felder.text.value = params.get('suche');
  filtern();
})();
