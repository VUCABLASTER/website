import re, html
ROOT='/Users/thomaswordenbeck/Claude Code/CodingDojo/VUCA-Blaster/vuca-blaster-website/'
SP='https://open.spotify.com/show/3OQW0akZgxBxK4AWFQSKtf'
AP='https://podcasts.apple.com/de/podcast/vuca-blaster/id1541461336'

STRIP=lambda pre: '''<!-- GEWINNSPIEL-LEISTE:START (nach dem Event diesen Block löschen) -->
<a class="gw-strip" href="'''+pre+'''worccamp/"><span>Gewinnspiel beim WORCamp 2026:</span> <strong>Welches Buch nimmst du mit? →</strong></a>
<!-- GEWINNSPIEL-LEISTE:ENDE -->
'''

def page(title, canonical, pre, h1, body, extra_head='', strip=True):
    home = pre if pre else './'
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{canonical}<link rel="icon" href="{pre}favicon.ico" sizes="32x32">
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{pre}apple-touch-icon.png">
<meta name="theme-color" content="#FAFAF7">
<link rel="preload" href="{pre}assets/fonts/bricolage-grotesque-latin-opsz-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{pre}assets/css/style.css">
{extra_head}</head>
<body>
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<div class="page">
{STRIP(pre) if strip else ''}
<header class="site-head">
  <a class="wordmark" href="{home}">VUCA Blaster</a>
  <nav class="site-nav" aria-label="Hauptnavigation">
    <ul>
      <li><a href="{home}#aktuell">Aktuelle Folge</a></li>
      <li><a href="{home}#ueber-uns">Über uns</a></li>
      <li class="guest-li"><a class="guest-note" href="{home}#kontakt">Für Gäste</a></li>
      <li><a href="{home}#kontakt">Kontakt</a></li>
    </ul>
  </nav>
</header>

<main id="inhalt">
<div class="board-sm">
  <h1>{h1}</h1>
{body[0]}</div>
{body[1]}
</main>

<footer class="site-foot">
  <div class="foot-top">
    <p class="foot-mark">VUCA Blaster</p>
    <p class="foot-claim">Die Welt ist komplex. Wir sehen darin Gestaltungsraum.</p>
    <ul class="foot-links">
      <li><a href="{SP}">Spotify</a></li>
      <li><a href="{AP}">Apple Podcasts</a></li>
      <li><a href="https://www.linkedin.com/showcase/vucablaster/">LinkedIn</a></li>
    </ul>
  </div>
  <p class="foot-legal">© 2020–2026 VUCA Blaster · <a href="{pre}impressum/">Impressum</a> · <a href="{pre}datenschutz/">Datenschutz</a></p>
</footer>

</div>
</body>
</html>
'''

def linkify(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'(https?://[^\s)]+)', lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>', t)
    t = re.sub(r'\b([\w.+-]+@[\w-]+\.[\w.]+)\b', r'<a href="mailto:\1">\1</a>', t)
    t = re.sub(r'Telefon: (\d+)', r'Telefon: <a href="tel:\1">\1</a>', t)
    return t

# ---- Impressum (1:1 aus dem Fragebogen, ohne interne Anmerkung) ----
imp = '''  <div class="legal-body">
    <p>Immanuel Wyszynski<br>
    Kortumstraße 9<br>
    45130 Essen</p>
    <h2>Kontakt</h2>
    <p>Telefon: <a href="tel:017662512658">017662512658</a><br>
    E-Mail: <a href="mailto:manuel.wy@googlemail.com">manuel.wy@googlemail.com</a></p>
    <p>Quelle: <a href="https://www.e-recht24.de/impressum-generator.html">https://www.e-recht24.de/impressum-generator.html</a></p>
  </div>'''
open(ROOT+'docs/impressum/index.html','w').write(page(
  'Impressum – VUCA Blaster','<link rel="canonical" href="https://vucablaster.de/impressum/">\n','../','Impressum',
  ('', f'<section class="legal" aria-label="Impressum">\n{imp}\n</section>')))

# ---- Datenschutz (1:1 aus DATENSCHUTZ.md) ----
md = open(ROOT+'01-von-manuel/DATENSCHUTZ.md').read().strip().split('\n\n')
assert md[0].startswith('# Datenschutzerklärung')
out=[]
for block in md[1:]:
    if block.startswith('## '):
        out.append(f'    <h2>{html.escape(block[3:], quote=False)}</h2>')
    else:
        lines=[linkify(l) for l in block.split('\n')]
        out.append('    <p>' + '<br>\n    '.join(lines) + '</p>')
ds='  <div class="legal-body">\n' + '\n'.join(out) + '\n  </div>'
open(ROOT+'docs/datenschutz/index.html','w').write(page(
  'Datenschutzerklärung – VUCA Blaster','<link rel="canonical" href="https://vucablaster.de/datenschutz/">\n','../','Datenschutzerklärung',
  ('', f'<section class="legal" aria-label="Datenschutzerklärung">\n{ds}\n</section>')))

# ---- 404 (absolute Pfade, weil GitHub sie unter jeder URL ausliefert) ----
nf_board = '  <p class="notfound-note">Hier steht noch nichts.</p>\n'
nf_body = '<div class="notfound-body"><a class="btn" href="/">Zur Startseite</a></div>'
open(ROOT+'docs/404.html','w').write(page(
  'Seite nicht gefunden – VUCA Blaster','','/','Seite nicht gefunden',(nf_board, nf_body)))
print('ok')
