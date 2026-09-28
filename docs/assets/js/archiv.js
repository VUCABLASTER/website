/* Archiv: Suche und Filter im Browser. Ohne JavaScript bleibt die komplette Liste sichtbar. */
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

  function normal(s) {
    return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/\s+/g, ' ').trim();
  }

  function filtern() {
    var woerter = normal(felder.text.value).split(' ').filter(Boolean);
    var wert = felder.wert.value, staffel = felder.staffel.value, jahr = felder.jahr.value;
    var sichtbar = 0;
    items.forEach(function (li) {
      var passt =
        (!wert || (' ' + li.dataset.werte + ' ').indexOf(' ' + wert + ' ') !== -1) &&
        (!staffel || li.dataset.staffel === staffel) &&
        (!jahr || li.dataset.jahr === jahr) &&
        woerter.every(function (w) { return li.dataset.text.indexOf(w) !== -1; });
      li.hidden = !passt;
      if (passt) sichtbar++;
    });
    anzahl.textContent = sichtbar === 1 ? '1 Folge' : sichtbar + ' Folgen';
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
