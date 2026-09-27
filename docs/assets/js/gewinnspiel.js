/* Gewinnspiel: Teilnahme per E-Mail, wie beim Kontakt-Button.
   Klick auf „Jetzt teilnehmen“ öffnet das Mailprogramm mit einer fertigen Mail an hello@vucablaster.com.
   Es werden keine Daten an Dritte übertragen und nichts gespeichert. */
(function () {
  var form = document.querySelector('[data-gw-form]');
  if (!form) return;
  var thanks = document.querySelector('[data-gw-thanks]');
  var back = document.querySelector('[data-gw-back]');
  var TO = 'hello@vucablaster.com';

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    var data = new FormData(form);
    var book = data.get('wunschbuch');
    var name = [data.get('vorname'), data.get('nachname')].filter(Boolean).join(' ').trim();

    var subject = 'Gewinnspiel WORC Camp: ' + book;
    var body = 'Hallo VUCA Blaster,\n\n' +
      'ich möchte am Gewinnspiel beim WORC Camp teilnehmen.\n\n' +
      'Name: ' + name + '\n' +
      'Wunschgewinn: ' + book + '\n\n' +
      'Die Teilnahmebedingungen und Datenschutzhinweise habe ich gelesen und akzeptiert.\n';

    window.location.href = 'mailto:' + TO +
      '?subject=' + encodeURIComponent(subject) +
      '&body=' + encodeURIComponent(body);

    form.hidden = true;
    thanks.hidden = false;
    thanks.scrollIntoView({ block: 'start' });
    var heading = thanks.querySelector('h2');
    if (heading) heading.focus();
  });

  if (back) back.addEventListener('click', function () {
    thanks.hidden = true;
    form.hidden = false;
    form.scrollIntoView({ block: 'start' });
  });
})();
