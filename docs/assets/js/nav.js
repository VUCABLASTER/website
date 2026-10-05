/* Menü: bleibt oben stehen (CSS), wird beim Scrollen schmal (Handy) und hebt auf der Startseite
   den Abschnitt hervor, in dem man gerade ist. Ohne JavaScript bleibt das Menü einfach oben stehen. */
(function () {
  var kopf = document.querySelector('.site-head');
  if (!kopf) return;

  function schmal() {
    kopf.classList.toggle('is-stuck', window.scrollY > 8);
  }
  schmal();
  window.addEventListener('scroll', function () { window.requestAnimationFrame(schmal); }, { passive: true });

  // Hervorhebung nur dort, wo die Links auf Abschnitte derselben Seite zeigen (data-spy)
  var links = Array.prototype.slice.call(kopf.querySelectorAll('.site-nav a[data-spy]'));
  if (!links.length || !('IntersectionObserver' in window)) return;

  var abschnitte = {};
  links.forEach(function (a) {
    a.getAttribute('data-spy').split(/\s+/).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) abschnitte[id] = el;
    });
  });
  var sichtbar = {};

  function anzeigen() {
    var aktiv = null, hoechster = -1;
    Object.keys(sichtbar).forEach(function (id) {
      if (sichtbar[id] && abschnitte[id].offsetTop > hoechster) {
        hoechster = abschnitte[id].offsetTop;
        aktiv = id;
      }
    });
    links.forEach(function (a) {
      var ids = a.getAttribute('data-spy').split(/\s+/);
      if (aktiv && ids.indexOf(aktiv) !== -1) a.setAttribute('aria-current', 'location');
      else a.removeAttribute('aria-current');
    });
  }

  // Ein Abschnitt zählt als „aktuell“, solange er das Band im oberen Drittel des Bildschirms berührt
  var beobachter = new IntersectionObserver(function (eintraege) {
    eintraege.forEach(function (e) { sichtbar[e.target.id] = e.isIntersecting; });
    anzeigen();
  }, { rootMargin: '-30% 0px -60% 0px' });
  Object.keys(abschnitte).forEach(function (id) { beobachter.observe(abschnitte[id]); });
})();
