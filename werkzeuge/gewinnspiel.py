"""Erzeugt die Gewinnspielseite /worccamp/."""
import re
from layout import REPO, page

# ---- Werte (bis zur Freigabe Platzhalter) ----
F=lambda s: f'<mark class="fehlt">{s}</mark>'
W={'event':'WORCamp 2026','zeitraum':'29.\xa0&amp;\xa030.09.2026','ende':'30.09.2026'}
LI='https://www.linkedin.com/showcase/vucablaster/'
SHARE='https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fvucablaster.de%2Fworccamp%2F'
v=lambda k: f'<span data-wert="{k}">{W[k]}</span>'
NEW=' target="_blank" rel="noopener"'

head='''<meta name="description" content="VUCA Blaster × WORCamp 2026: 4 Gewinne, 5 Bücher. Wähl deinen Wunschgewinn und lande im Lostopf. Wir losen nach dem Event aus und melden uns per Mail.">
<meta name="robots" content="noindex">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<meta property="og:title" content="Welches Buch nimmst du mit nach Hause? – VUCA Blaster × WORCamp 2026">
<meta property="og:description" content="4 Gewinne. 5 Bücher. 4 Gewinner:innen. Such dir deinen Wunschgewinn aus und lande im Lostopf.">
<meta property="og:url" content="https://vucablaster.de/worccamp/">
<meta property="og:image" content="https://vucablaster.de/assets/img/og-default.png">
<script src="../assets/js/gewinnspiel.js" defer></script>
'''

pflege='''<!--
  PFLEGE – änderbare Werte dieser Seite
  Jeder Wert steht in einem <span data-wert="…">. Mit Strg+F nach dem Namen suchen und ALLE Fundstellen ändern:
    data-wert="event"     Eventname          (Hero, Danke-Ansicht, Auslosung, Teilnahmebedingungen)
    data-wert="zeitraum"  Eventtage          (Hero, Teilnahmebedingungen)
    data-wert="ende"      Teilnahmeschluss   (Teilnahmebedingungen)
  Mail-Betreff „Gewinnspiel WORCamp 2026“: im Formular (action) UND in assets/js/gewinnspiel.js
  LinkedIn-Seite:  https://www.linkedin.com/showcase/vucablaster/  (3 Links: Suche nach "showcase/vucablaster")
  Mail-Empfänger:  hello@vucablaster.com  (im Formular UND in assets/js/gewinnspiel.js)
-->'''

hero=f'''<div class="board-sm gw-hero">
{pflege}
  <p class="gw-sub">VUCA Blaster × {v('event')}</p>
  <h1>Welches Buch nimmst du mit nach Hause? <span aria-hidden="true">🎁</span></h1>
  <p class="gw-lead">4&nbsp;Gewinne. 5&nbsp;Bücher. 4&nbsp;Gewinner:innen.</p>
  <p class="gw-text">Im Rahmen des {v('event')} verlosen wir Bücher rund um Mut, Psychologie und Veränderung. Such dir deinen Wunschgewinn aus, mach mit und erzähl es gern weiter.</p>
  <ol class="gw-steps">
    <li><span class="no" aria-hidden="true">1</span>Wunschgewinn auswählen</li>
    <li><span class="no" aria-hidden="true">2</span>Namen eintragen und Mail abschicken</li>
    <li><span class="no" aria-hidden="true">3</span>Nach dem Event losen wir aus und melden uns per Mail</li>
  </ol>
  <p class="gw-date"><strong>Gewinnspiel beim {v('event')}</strong> · {v('zeitraum')}</p>
  <a class="btn gw-jump" href="#mitmachen"><span aria-hidden="true">↓</span>&nbsp;Wunschgewinn auswählen</a>
</div>'''

books=[
 ('Jonas Deichmann','Weil ich es kann','Für alle, die Mut, Ausdauer und Grenzen im Kopf neu denken wollen.','gewinn-weil-ich-es-kann','Weil ich es kann'),
 ('Dr. Nico Rose','Arbeit besser machen','Für alle, die Arbeit menschlicher, motivierender und wirksamer gestalten wollen.','gewinn-arbeit-besser-machen','Arbeit besser machen'),
 ('Dr. Maja Storch','Der Glückskind-Effekt','Für alle, die Psychologie, innere Stärke und echte Veränderung besser verstehen wollen.','gewinn-glueckskind-effekt','Der Glückskind-Effekt'),
 ('Dana Hoffmann &amp; Hendric Mostert','Bundle: Conflict Culture Playbook + Restorative Circles Workbook','Für alle, die Konflikte konstruktiv nutzen, Kultur aktiv gestalten und Konfliktklärung praktisch anwenden wollen.','gewinn-bundle-conflict-culture','Bundle Conflict Culture Playbook + Restorative Circles Workbook'),
]
tiles='\n'.join(f'''        <label class="book">
          <input type="radio" name="wunschbuch" value="{val} ({a.replace('&amp;','&')})"{' required' if i==0 else ''}>
          <span class="book-img"><picture><source srcset="../assets/img/{img}.webp" type="image/webp"><img src="../assets/img/{img}.jpg" alt="" width="720" height="720" loading="lazy" decoding="async"></picture></span>
          <span class="book-no" aria-hidden="true">{i+1}</span>
          <span class="book-author">{a}</span>
          <span class="book-title">{t}</span>
          <span class="book-hook">{h}</span>
          <span class="book-pick">Das möchte ich gewinnen</span>
        </label>''' for i,(a,t,h,img,val) in enumerate(books))

nomail='Kein Mailprogramm? Schreib an <strong>hello@vucablaster.com</strong> mit dem Betreff „Gewinnspiel WORCamp 2026“, deinem Namen und deinem Wunschgewinn.'

rest=f'''<form class="gw-form" action="mailto:hello@vucablaster.com?subject=Gewinnspiel%20WORCamp%202026" method="post" enctype="text/plain" data-gw-form>
  <section id="mitmachen" class="gw-section" aria-labelledby="books-h">
    <fieldset class="books">
      <legend id="books-h">Such dir deinen Wunsch&shy;gewinn aus</legend>
      <p class="gw-text gw-books-note">4 Gewinne: drei Einzelbücher und ein Bundle aus zwei Büchern.</p>
      <div class="book-grid">
{tiles}
      </div>
    </fieldset>
  </section>

  <section id="lostopf" class="gw-section" aria-labelledby="form-h">
    <h2 id="form-h" class="section-title">Ab in den Lostopf</h2>
    <p class="gw-text gw-form-intro">Trag deinen Namen ein. Mit „Jetzt teilnehmen“ öffnet sich dein Mailprogramm mit einer fertigen Mail an uns. Die musst du nur noch abschicken.</p>
    <div class="gw-form-grid">
      <div class="field">
        <label for="gw-vorname">Vorname *</label>
        <input id="gw-vorname" name="vorname" type="text" autocomplete="given-name" required>
      </div>
      <div class="field">
        <label for="gw-nachname">Nachname <small>(optional)</small></label>
        <input id="gw-nachname" name="nachname" type="text" autocomplete="family-name">
      </div>
      <label class="consent full">
        <input type="checkbox" name="einwilligung" value="ja" required>
        <span>Ich akzeptiere die <a href="#bedingungen">Teilnahmebedingungen</a> und <a href="../datenschutz/">Datenschutzhinweise</a>. *</span>
      </label>
      <label class="consent full">
        <input type="checkbox" name="linkedin_nennung" value="ja">
        <span>Optional: Falls ich gewinne, dürft ihr mich mit Namen auf LinkedIn nennen. Hat keinen Einfluss auf die Gewinnchance.</span>
      </label>
      <div class="gw-submit full">
        <button type="submit" class="btn">Jetzt teilnehmen</button>
      </div>
      <p class="gw-follow full"><a href="{LI}"{NEW}>Folge VUCA Blaster auf LinkedIn – dann verpasst du die Auslosung nicht.</a> Dort geben wir die Auslosung zusätzlich bekannt.</p>
      <p class="gw-micro full">{nomail}</p>
    </div>
  </section>
</form>

<section class="gw-thanks" data-gw-thanks aria-labelledby="thanks-h" hidden>
  <div class="gw-thanks-in">
    <p class="gw-over">Fast geschafft: Schick jetzt die Mail ab.</p>
    <h2 id="thanks-h" class="section-title" tabindex="-1">Dann bist du im Lostopf! <span aria-hidden="true">🎉</span></h2>
    <p class="gw-lead">Nach dem {v('event')} losen wir die vier Gewinner:innen aus und melden uns per Mail.</p>
    <div class="gw-li">
      <h3>Noch nicht Teil der VUCA-Blaster-Community?</h3>
      <p>Folge uns auf LinkedIn für Mut, Veränderung, Psychologie und die Zukunft der Arbeit.</p>
      <a class="btn" href="{LI}"{NEW}>+ VUCA Blaster folgen</a>
    </div>
    <div class="gw-mut">
      <h3>Was war dein mutigster Moment im Arbeitsleben?</h3>
      <p>Teile ihn auf LinkedIn und markiere @VUCA BLASTER.</p>
      <a class="btn-outline" href="{SHARE}"{NEW}>Mut-Moment teilen</a>
    </div>
    <p class="gw-micro">Beides ist freiwillig und hat keinen Einfluss auf deine Gewinnchance.</p>
    <p class="gw-micro">Es hat sich kein Mailprogramm geöffnet? Schreib an <strong>hello@vucablaster.com</strong> mit dem Betreff „Gewinnspiel WORCamp 2026“, deinem Namen und deinem Wunschgewinn. <button type="button" class="linkish" data-gw-back>Zurück zum Formular</button></p>
  </div>
</section>

<section class="gw-section gw-about-sec" aria-label="Über VUCA Blaster">
  <details class="gw-about">
    <summary><h2 class="section-title">Was ist ein VUCA Blaster?</h2></summary>
    <div class="about-grid gw-about-grid">
      <div>
        <div class="lex">
          <p class="lex-word">VUCA Blaster</p>
          <p class="lex-pos">Substantiv</p>
          <p class="lex-def">Ein VUCA Blaster begegnet einer unübersichtlichen Welt mit Neugier, Mut, Op&shy;ti&shy;mis&shy;mus und Au&shy;then&shy;ti&shy;zi&shy;tät. Surft auf dem Chaos, statt darin un&shy;ter&shy;zu&shy;ge&shy;hen. Ge&shy;stal&shy;tet Ver&shy;än&shy;de&shy;rung aktiv mit und bringt Men&shy;schen durch ver&shy;bin&shy;den&shy;de Kom&shy;mu&shy;ni&shy;ka&shy;tion zu&shy;sam&shy;men.</p>
        </div>
        <p class="about-text">Die Welt wird schneller, komplexer und manchmal ziemlich unübersichtlich. Im VUCA BLASTER sprechen wir mit Menschen aus Wissenschaft, Wirtschaft, Psychologie, Sport und Gesellschaft darüber, wie wir mit Veränderung und Unsicherheit umgehen können. Es geht um Mut, Selbstwirksamkeit, Führung, Zusammenarbeit und Optimismus. Wir suchen Geschichten und konkrete Impulse, die im Arbeitsleben und darüber hinaus helfen.</p>
        <p><a class="host-link" href="../">Zum Podcast VUCA Blaster</a></p>
      </div>
      <figure class="print print--cover">
        <div class="photo"><picture><source srcset="../assets/img/vuca-blaster-motiv.webp" type="image/webp"><img src="../assets/img/vuca-blaster-motiv.jpg" alt="Illustration einer VUCA Blasterin mit Kopfhörern und Mikrofon, daneben die Worte Mut, Neugier, Zuversicht" width="900" height="900" loading="lazy" decoding="async"></picture></div>
      </figure>
    </div>
  </details>
</section>

<section id="auslosung" class="gw-section" aria-labelledby="draw-h">
  <h2 id="draw-h" class="section-title">So läuft die Auslosung</h2>
  <p class="gw-text gw-draw-when">Im Anschluss an das {v('event')} losen wir aus und melden uns bei den Gewinner:innen.</p>
  <ul class="rules">
    <li>Jede Person kann einmal teilnehmen.</li>
    <li>Pro Person ist ein Wunschgewinn auswählbar.</li>
    <li>Nach dem Event ziehen wir pro Gewinn zufällig eine Person.</li>
    <li>Die Gewinner:innen benachrichtigen wir per E-Mail an die Adresse, von der die Teilnahme-Mail kam.</li>
    <li>Die Gewinne verschicken wir per Post. Dafür fragen wir die Gewinner:innen per E-Mail nach ihrer Postanschrift.</li>
    <li>Die Auslosung geben wir zusätzlich auf LinkedIn bekannt. Mit Namen nennen wir nur Gewinner:innen, die im Formular zugestimmt haben.</li>
    <li>Folgen auf LinkedIn ist freiwillig und keine Voraussetzung für die Teilnahme.</li>
  </ul>

  <details id="bedingungen" class="terms">
    <summary>Teilnahmebedingungen</summary>
    <ul>
      <li>Veranstalter des Gewinnspiels ist VUCA BLASTER.</li>
      <li>Teilnahmeberechtigt sind natürliche Personen ab 18 Jahren, die am {v('event')} teilnehmen.</li>
      <li>Die Teilnahme ist kostenlos und unabhängig vom Erwerb von Waren oder Dienstleistungen.</li>
      <li>Das Gewinnspiel findet im Rahmen des {v('event')} am {v('zeitraum')} statt. Teilnahmeschluss ist das Ende des Events am {v('ende')}.</li>
      <li>Die Gewinner:innen werden im Anschluss an das Event zufällig ausgelost und per E-Mail benachrichtigt. Die Gewinne werden per Post verschickt. Dafür teilen die Gewinner:innen uns per E-Mail ihre Postanschrift mit.</li>
      <li>Mit Namen auf LinkedIn nennen wir Gewinner:innen nur, wenn sie im Formular zugestimmt haben. Die Zustimmung ist freiwillig, hat keinen Einfluss auf die Gewinnchance und kann jederzeit per E-Mail an hello@vucablaster.com widerrufen werden.</li>
      <li>Pro Person ist nur eine Teilnahme möglich. Mehrfachteilnahmen können ausgeschlossen werden.</li>
      <li>Zu gewinnen gibt es insgesamt vier Gewinne: drei Einzelbücher und ein Bundle aus zwei Büchern (Conflict Culture Playbook + Restorative Circles Workbook). Die Zuordnung erfolgt entsprechend des im Formular ausgewählten Wunschgewinns. Sollte ein Gewinn nicht verfügbar sein, behält sich der Veranstalter vor, einen gleichwertigen Ersatz zu vergeben.</li>
      <li>Der Rechtsweg ist ausgeschlossen. Eine Barauszahlung des Gewinns ist nicht möglich.</li>
    </ul>
    <h3>Datenschutzhinweis</h3>
    <p>Die im Rahmen des Gewinnspiels erhobenen personenbezogenen Daten werden ausschließlich zur Durchführung des Gewinnspiels verwendet. Weitere Informationen zur Verarbeitung personenbezogener Daten finden sich in der Datenschutzerklärung unter: <a href="../datenschutz/">vucablaster.de/datenschutz</a>.</p>
  </details>
</section>'''

html=page('Gewinnspiel WORCamp 2026 – VUCA Blaster','<link rel="canonical" href="https://vucablaster.de/worccamp/">\n','../','XXH1',('',rest),extra_head=head,strip=False)
html=re.sub(r'<div class="board-sm">\n  <h1>XXH1</h1>\n</div>', lambda m: hero, html, count=1)
assert 'XXH1' not in html

def main(site):
    (site/'worccamp').mkdir(exist_ok=True)
    open(site/'worccamp'/'index.html','w',encoding='utf-8').write(html)

if __name__ == '__main__':
    main(REPO/'docs')
