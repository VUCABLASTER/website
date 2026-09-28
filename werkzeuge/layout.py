"""Gemeinsamer Rahmen (Head, Header, Footer) für alle erzeugten Seiten.

`pre` ist der relative Weg zur Website-Wurzel, z. B. "" (Startseite), "../" (eine Ebene tiefer)
oder "/" (404-Seite, die GitHub unter jeder Adresse ausliefert).
"""
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def version(datei):
    """Kurzer Prüfwert einer Datei aus docs/assets – ändert sich bei jeder Änderung, damit Browser nichts Veraltetes zeigen."""
    import hashlib
    p = REPO / 'docs' / 'assets' / datei
    return hashlib.sha1(p.read_bytes()).hexdigest()[:8] if p.exists() else '1'

SPOTIFY = 'https://open.spotify.com/show/3OQW0akZgxBxK4AWFQSKtf'
APPLE = 'https://podcasts.apple.com/de/podcast/vuca-blaster/id1541461336'
LINKEDIN = 'https://www.linkedin.com/showcase/vucablaster/'
MAIL = 'hello@vucablaster.com'
BASE_URL = 'https://vucablaster.de/'

# Archiv verlinken: False = /folgen/ ist erreichbar, aber nicht verlinkt und für Suchmaschinen gesperrt,
# Startseite und Navigation bleiben unverändert. True = Navigation „Folgen“, Archiv-Teaser und
# automatische aktuelle Folge auf der Startseite, Sitemap.
ARCHIV_VERLINKT = False

# Nach dem WORCamp 2026 auf False setzen und neu bauen: entfernt die türkise Leiste über dem Header.
GEWINNSPIEL_LEISTE = True


def leiste(pre):
    if not GEWINNSPIEL_LEISTE:
        return ''
    return (
        '<!-- GEWINNSPIEL-LEISTE:START (nach dem Event in werkzeuge/layout.py abschalten) -->\n'
        f'<a class="gw-strip" href="{pre}worccamp/"><span>Gewinnspiel beim WORCamp 2026:</span> '
        '<strong>Welches Buch nimmst du mit? →</strong></a>\n'
        '<!-- GEWINNSPIEL-LEISTE:ENDE -->\n'
    )


def nav_items(pre):
    home = pre if pre else './'
    ueber = '#ueber-uns' if pre == '' else home + '#ueber-uns'
    kontakt = '#kontakt' if pre == '' else home + '#kontakt'
    erster = (f'<a href="{pre}folgen/">Folgen</a>' if ARCHIV_VERLINKT
              else f'<a href="{"#aktuell" if pre == "" else home + "#aktuell"}">Aktuelle Folge</a>')
    return f'''      <li>{erster}</li>
      <li><a href="{ueber}">Über uns</a></li>
      <li class="guest-li"><a class="guest-note" href="{kontakt}">Für Gäste</a></li>
      <li><a href="{kontakt}">Kontakt</a></li>'''


def header(pre, strip=True):
    home = pre if pre else './'
    return f'''<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<div class="page">
{leiste(pre) if strip else ''}
<header class="site-head">
  <a class="wordmark" href="{home}">VUCA Blaster</a>
  <nav class="site-nav" aria-label="Hauptnavigation">
    <ul>
{nav_items(pre)}
    </ul>
  </nav>
</header>
'''


def footer(pre):
    return f'''<footer class="site-foot">
  <div class="foot-top">
    <p class="foot-mark">VUCA Blaster</p>
    <p class="foot-claim">Die Welt ist komplex. Wir sehen darin Gestaltungsraum.</p>
    <ul class="foot-links">
      <li><a href="{SPOTIFY}">Spotify</a></li>
      <li><a href="{APPLE}">Apple Podcasts</a></li>
      <li><a href="{LINKEDIN}">LinkedIn</a></li>
    </ul>
  </div>
  <p class="foot-legal">© 2020–2026 VUCA Blaster · <a href="{pre}impressum/">Impressum</a> · <a href="{pre}datenschutz/">Datenschutz</a></p>
</footer>

</div>
'''


def head(title, pre, canonical='', extra=''):
    if canonical.startswith('<'):
        can = canonical if canonical.endswith('\n') else canonical + '\n'
    else:
        can = f'<link rel="canonical" href="{canonical}">\n' if canonical else ''
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{can}<link rel="icon" href="{pre}favicon.ico" sizes="32x32">
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{pre}apple-touch-icon.png">
<meta name="theme-color" content="#FAFAF7">
<link rel="preload" href="{pre}assets/fonts/bricolage-grotesque-latin-opsz-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{pre}assets/css/style.css?v={version('css/style.css')}">
{extra}</head>
<body>
'''


def page(title, canonical, pre, h1, body, extra_head='', strip=True):
    """Unterseite mit kleinem Board als Kopf. body = (Inhalt im Board, Inhalt danach)."""
    return (head(title, pre, canonical, extra_head) + header(pre, strip) +
            f'''
<main id="inhalt">
<div class="board-sm">
  <h1>{h1}</h1>
{body[0]}</div>
{body[1]}
</main>

''' + footer(pre) + '</body>\n</html>\n')
