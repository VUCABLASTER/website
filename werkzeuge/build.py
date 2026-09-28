"""Baut die VUCA-Blaster-Website.

Holt den RSS-Feed von podcaster.de und die Folgen-Links von Apple Podcasts, verbindet sie mit den
Folgen-Infos aus inhalte/folgen/*.json und erzeugt:
  - Archiv /folgen/ mit Suche und Filtern
  - eine Seite pro Folge /folgen/<slug>/
  - Kurzlinks /62/
  - die aktuelle Folge, die Folgenzahl und den Archiv-Teaser auf der Startseite
  - Impressum, Datenschutz, 404 und Gewinnspiel (über unterseiten.py / gewinnspiel.py)
  - sitemap.xml

Aufruf:
  python3 werkzeuge/build.py                         # baut direkt in docs/ (live)
  python3 werkzeuge/build.py --ziel PFAD --vorschau  # Kopie von docs/ nach PFAD, dort bauen, noindex + Hinweis
  python3 werkzeuge/build.py --offline               # nur Ersatzkopien aus daten/ verwenden

Braucht Python 3.9+ und Pillow (pip install pillow).
"""
import argparse, email.utils, hashlib, html, io, json, re, shutil, sys, unicodedata, urllib.parse, urllib.request
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
import layout
from layout import REPO, SPOTIFY, APPLE, BASE_URL, head, header, footer, nav_items, leiste
import unterseiten, gewinnspiel

FEED_URL = 'https://evjjod.podcaster.de/VUCABlaster.rss'
APPLE_ID = '1541461336'
APPLE_LOOKUP = f'https://itunes.apple.com/lookup?id={APPLE_ID}&entity=podcastEpisode&limit=300&country=de'
WERTE = ['optimistisch', 'neugierig', 'mutig', 'authentisch', 'verbindend']
NS = {'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd', 'content': 'http://purl.org/rss/1.0/modules/content/'}
DATEN = REPO / 'daten'
INHALTE = REPO / 'inhalte'
esc = lambda s: html.escape(s or '', quote=True)


# ---------------------------------------------------------------- Daten holen

def holen(url, ersatz, offline):
    """Lädt eine URL und legt eine Ersatzkopie ab. Klappt das nicht, wird die Ersatzkopie verwendet."""
    if not offline:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'vucablaster.de-build'})
            with urllib.request.urlopen(req, timeout=40) as r:
                daten = r.read()
            if len(daten) > 1000:
                ersatz.write_bytes(daten)
                return daten
        except Exception as e:
            print(f'Hinweis: {url} nicht erreichbar ({e}), nutze Ersatzkopie.', file=sys.stderr)
    if ersatz.exists():
        return ersatz.read_bytes()
    raise SystemExit(f'Fehler: weder {url} noch {ersatz} verfügbar.')


class Bereiniger(HTMLParser):
    """Lässt aus der Feed-Beschreibung nur einfache Textauszeichnung übrig."""
    ERLAUBT = {'p', 'br', 'strong', 'b', 'em', 'i', 'ul', 'ol', 'li', 'a'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.html, self.text, self.offen = [], [], []

    def handle_starttag(self, tag, attrs):
        if tag not in self.ERLAUBT:
            return
        if tag == 'a':
            href = dict(attrs).get('href', '')
            if not re.match(r'^(https?:|mailto:)', href):
                self.offen.append(None)
                return
            self.html.append(f'<a href="{esc(href)}">')
            self.offen.append('a')
        elif tag == 'br':
            self.html.append('<br>')
        else:
            self.html.append(f'<{tag}>')

    def handle_endtag(self, tag):
        if tag == 'a':
            if self.offen and self.offen.pop() == 'a':
                self.html.append('</a>')
        elif tag in self.ERLAUBT and tag != 'br':
            self.html.append(f'</{tag}>')
            if tag in ('p', 'li'):
                self.text.append(' ')

    def handle_data(self, data):
        self.html.append(html.escape(data, quote=False))
        self.text.append(data)


def bereinigen(roh):
    b = Bereiniger()
    b.feed(roh or '')
    b.close()
    return ''.join(b.html).strip(), re.sub(r'\s+', ' ', ''.join(b.text)).strip()


def minuten(dauer):
    if not dauer:
        return None
    teile = [int(x) for x in dauer.split(':') if x.strip().isdigit()]
    sek = 0
    for t in teile:
        sek = sek * 60 + t
    return max(1, round(sek / 60)) if sek else None


def slugify(s):
    s = unicodedata.normalize('NFKD', s.replace('ß', 'ss').replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue')
                              .replace('Ä', 'Ae').replace('Ö', 'Oe').replace('Ü', 'Ue'))
    s = re.sub(r'[^a-zA-Z0-9]+', '-', s.encode('ascii', 'ignore').decode()).strip('-').lower()
    return s[:80].strip('-')


def feed_lesen(xml_bytes, apple):
    ch = ET.fromstring(xml_bytes).find('channel')
    folgen = []
    for it in ch.findall('item'):
        titel_roh = (it.findtext('title') or '').strip()
        m = re.match(r'\s*#\s*(\d+)', titel_roh)
        nr = int(m.group(1)) if m else int(it.findtext('itunes:episode', namespaces=NS) or 0)
        if not nr:
            print(f'Hinweis: Folge ohne Nummer übersprungen: {titel_roh}', file=sys.stderr)
            continue
        link = (it.findtext('link') or '').rstrip('/')
        slug = link.split('/')[-1] if link else ''
        if not slug.startswith(f'{nr}-'):
            slug = f'{nr}-' + slugify(re.sub(r'^\s*#\s*\d+\s*[-–:]?\s*', '', titel_roh))
        img = it.find('itunes:image', NS)
        enc = it.find('enclosure')
        beschr_html, beschr_text = bereinigen(it.findtext('content:encoded', namespaces=NS) or it.findtext('description'))
        guid = it.findtext('guid') or ''
        folgen.append({
            'nr': nr,
            'titel_roh': titel_roh,
            'titel': re.sub(r'^\s*#\s*\d+\s*[-–:]?\s*', '', titel_roh).strip(),
            'slug': slug,
            'datum': email.utils.parsedate_to_datetime(it.findtext('pubDate')),
            'minuten': minuten(it.findtext('itunes:duration', namespaces=NS)),
            'bild_url': img.get('href') if img is not None else '',
            'mp3': enc.get('url') if enc is not None else '',
            'html': beschr_html,
            'text': beschr_text,
            'apple': apple.get(guid, ''),
        })
    doppelt = {f['nr'] for f in folgen if [g['nr'] for g in folgen].count(f['nr']) > 1}
    if doppelt:
        raise SystemExit(f'Fehler: doppelte Folgennummern im Feed: {sorted(doppelt)}')
    folgen.sort(key=lambda f: f['nr'], reverse=True)
    cover = ch.find('itunes:image', NS)
    return folgen, (cover.get('href') if cover is not None else '')


def apple_lesen(json_bytes):
    daten = json.loads(json_bytes)
    return {r.get('episodeGuid'): r.get('trackViewUrl', '').split('?')[0]
            for r in daten.get('results', []) if r.get('wrapperType') == 'podcastEpisode'}


# ---------------------------------------------------------------- Folgen-Infos (Pflege durch Manuel)

LEER = {'nummer': 0, 'titel': '', 'gast': '', 'rolle': '', 'staffel': '', 'hauptwert': '', 'nebenwerte': [], 'key_learnings': []}


def infos_laden(folgen):
    """Liest inhalte/folgen/NNN.json. Fehlt eine Datei, wird sie vorausgefüllt angelegt."""
    ordner = INHALTE / 'folgen'
    ordner.mkdir(parents=True, exist_ok=True)
    infos = {}
    for f in folgen:
        pfad = ordner / f'{f["nr"]:03d}.json'
        daten = dict(LEER)
        if pfad.exists():
            daten.update(json.loads(pfad.read_text(encoding='utf-8')))
        neu = dict(daten, nummer=f['nr'], titel=f['titel_roh'])
        if neu != daten or not pfad.exists():
            pfad.write_text(json.dumps(neu, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        neu['key_learnings'] = [k.strip() for k in neu.get('key_learnings') or [] if k and k.strip()]
        neu['nebenwerte'] = [w for w in neu.get('nebenwerte') or [] if w in WERTE and w != neu.get('hauptwert')]
        if neu.get('hauptwert') not in WERTE:
            neu['hauptwert'] = ''
        infos[f['nr']] = neu
    return infos


def staffeln_laden():
    pfad = INHALTE / 'staffeln.json'
    if not pfad.exists():
        return {}
    return {s['id']: s for s in json.loads(pfad.read_text(encoding='utf-8')).get('staffeln', [])}


def anzeige_titel(f, info):
    """Titel ohne Nummer und ohne angehängtes „mit <Gast>“, wenn der Gast bekannt ist."""
    t = f['titel']
    gast = (info.get('gast') or '').strip()
    if gast:
        nachname = gast.split()[-1].lower()
        pos = t.lower().rfind(' mit ')
        if pos > 0 and nachname in t[pos:].lower():
            t = t[:pos].rstrip(' –-:')
    return t or f['titel']


def staffel_label(f, info, staffeln, folgen, infos):
    s = staffeln.get(info.get('staffel') or '')
    if not s:
        return ''
    nrs = sorted(g['nr'] for g in folgen if infos[g['nr']].get('staffel') == s['id'])
    pos = nrs.index(f['nr']) + 1
    geplant = s.get('folgen_geplant')
    return f'{s["name"]}, {pos} von {geplant}' if geplant else s['name']


# ---------------------------------------------------------------- Bilder

def bilder(folgen, site, offline):
    """Lädt jedes Folgenbild einmal herunter und legt es lokal ab (600 px + 240 px, JPG + WebP)."""
    try:
        from PIL import Image
    except ImportError:
        raise SystemExit('Fehler: Pillow fehlt. Installieren mit: pip install pillow')
    ziel = site / 'assets' / 'folgen'
    ziel.mkdir(parents=True, exist_ok=True)
    index_pfad = DATEN / 'bilder.json'
    index = json.loads(index_pfad.read_text()) if index_pfad.exists() else {}
    vorhanden = {}
    for f in folgen:
        key, url = str(f['nr']), f['bild_url']
        dateien = [ziel / f'{f["nr"]}.jpg', ziel / f'{f["nr"]}.webp', ziel / f'{f["nr"]}-klein.jpg', ziel / f'{f["nr"]}-klein.webp']
        aktuell = index.get(key) == url and all(d.exists() for d in dateien)
        if url and not aktuell and not offline:
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'vucablaster.de-build'})
                with urllib.request.urlopen(req, timeout=40) as r:
                    im = Image.open(io.BytesIO(r.read())).convert('RGB')
                w, h = im.size
                s = min(w, h)
                im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))
                for groesse, suffix in ((600, ''), (240, '-klein')):
                    k = im.resize((groesse, groesse), Image.LANCZOS)
                    k.save(ziel / f'{f["nr"]}{suffix}.jpg', quality=82, optimize=True, progressive=True)
                    k.save(ziel / f'{f["nr"]}{suffix}.webp', quality=80, method=6)
                index[key] = url
                aktuell = True
            except Exception as e:
                print(f'Hinweis: Bild für #{f["nr"]} nicht geladen ({e}).', file=sys.stderr)
        vorhanden[f['nr']] = all(d.exists() for d in dateien)
    index_pfad.write_text(json.dumps(index, indent=1, sort_keys=True) + '\n')
    return vorhanden


def bild(pre, nr, alt, klein=False, lazy=True, groesse=None):
    s = '-klein' if klein else ''
    px = groesse or (240 if klein else 600)
    la = ' loading="lazy"' if lazy else ''
    return (f'<picture><source srcset="{pre}assets/folgen/{nr}{s}.webp" type="image/webp">'
            f'<img src="{pre}assets/folgen/{nr}{s}.jpg" alt="{esc(alt)}" width="{px}" height="{px}"{la} decoding="async"></picture>')


# ---------------------------------------------------------------- Bausteine

datum_de = lambda d: f'{d.day:02d}.{d.month:02d}.{d.year}'
mp3_url = lambda u: urllib.parse.quote(u, safe=':/%?=&')


def werte_liste(info, label='Werte dieser Folge'):
    items = []
    if info['hauptwert']:
        items.append(f'<li class="value value--main"><span class="dot" aria-hidden="true"></span>{info["hauptwert"]} · Hauptwert</li>')
    for w in info['nebenwerte']:
        items.append(f'<li class="value"><span class="dot" aria-hidden="true"></span>{w}</li>')
    return f'<ul class="values" aria-label="{label}">' + ''.join(items) + '</ul>' if items else ''


def learnings(info):
    if not info['key_learnings']:
        return ''
    li = ''.join(f'<li class="sticky"><span class="sticky-no" aria-hidden="true">{i + 1}</span>'
                 f'<span class="sticky-text">{esc(k)}</span></li>' for i, k in enumerate(info['key_learnings'][:3]))
    return f'''  <div class="learnings">
    <h3 class="label">{len(info["key_learnings"][:3])} Key Learnings</h3>
    <ol class="stickies" role="list">{li}</ol>
  </div>
'''


def plattformen(f):
    apple = f['apple'] or APPLE
    return (f'<a class="btn" href="{esc(apple)}">Apple Podcasts</a>'
            f'<a class="btn" href="{SPOTIFY}">Spotify</a>')


# ---------------------------------------------------------------- Startseite

def startseite(site, folgen, infos, staffeln, hat_bild):
    pfad = site / 'index.html'
    s = pfad.read_text(encoding='utf-8')
    f = folgen[0]
    info = infos[f['nr']]
    titel = anzeige_titel(f, info)
    gast = info['gast']
    staffel = staffel_label(f, info, staffeln, folgen, infos)
    meta = f'#{f["nr"]} · ' + (f'{staffel} · ' if staffel else '') + f'<time datetime="{f["datum"]:%Y-%m-%d}">{datum_de(f["datum"])}</time>'
    alt = f'Folgenbild #{f["nr"]}' + (f' mit {gast}' if gast else '')

    notiz = f'''<!-- HERO-NOTIZ:START (wird automatisch erzeugt) -->
    <a class="hero-note" href="#aktuell">
      <span class="magnet" aria-hidden="true"></span>
      <span class="n-kick">Neu · #{f["nr"]}</span>
      <span class="n-title">{esc(titel)}</span>
      <span class="n-guest">{('mit ' + esc(gast) + ' →') if gast else 'Jetzt reinhören →'}</span>
    </a>
    <!-- HERO-NOTIZ:ENDE -->'''

    gast_html = ''
    if gast:
        thumb = (f'<div class="thumb" aria-hidden="true"><div class="photo">{bild("", f["nr"], "", klein=True, lazy=False)}</div></div>'
                 if hat_bild[f['nr']] else '')
        rolle = f'<p class="guest-role">{esc(info["rolle"])}</p>' if info['rolle'] else ''
        gast_html = f'''<div class="guest">
        {thumb}
        <div>
          <p class="guest-name">mit {esc(gast)}</p>
          {rolle}
        </div>
      </div>'''
    abzug = (f'<figure class="print print--guest"><div class="photo">{bild("", f["nr"], alt, lazy=False)}</div></figure>'
             if hat_bild[f['nr']] else '')

    aktuell = f'''<!-- AKTUELLE-FOLGE:START (wird automatisch aus dem Feed erzeugt, Pflege in inhalte/folgen/{f["nr"]:03d}.json) -->
<section id="aktuell" class="section current" aria-labelledby="aktuell-h">
  <div class="current-grid">
    <div class="current-main">
      <p class="ep-meta"><span class="chip">Aktuelle Folge</span><span class="muted">{meta}</span></p>
      <h2 id="aktuell-h" class="ep-title"><span class="sr-only">#{f["nr"]} – </span>{esc(titel)}</h2>
      {gast_html}
      {werte_liste(info)}
      <p class="label listen-label">Diese Folge hören</p>
      <div class="btn-row">
        {plattformen(f)}
      </div>
      <p class="hint">Am besten auf Spotify oder Apple Podcasts: Dort hilft jedes Abo und jede Bewertung dem Podcast.</p>
      <a class="host-link" href="folgen/{f["slug"]}/">Mehr zur Folge #{f["nr"]}</a>
    </div>
    <div class="current-side">
      {abzug}
      <div class="player" data-player data-src="{esc(mp3_url(f["mp3"]))}" data-title="#{f["nr"]} – {esc(titel)}">
        <h3 class="player-title">Player</h3>
        <p><span data-player-status>Der Player ist noch nicht geladen.</span> Beim Laden werden Daten an podcaster.de übertragen. Mehr in der <a href="datenschutz/">Datenschutzerklärung</a>.</p>
        <button type="button" class="btn-outline" data-player-load hidden><svg width="10" height="12" viewBox="0 0 10 12" aria-hidden="true" focusable="false"><path d="M0 0 L10 6 L0 12 Z"/></svg>Audio-Player laden</button>
        <a class="btn-outline" data-player-fallback href="{esc(mp3_url(f["mp3"]))}">Folge direkt anhören (MP3)</a>
      </div>
    </div>
  </div>
{learnings(info)}</section>
<!-- AKTUELLE-FOLGE:ENDE -->'''

    jahr0 = min(g['datum'].year for g in folgen)
    archiv = f'''<!-- ARCHIV:START (wird automatisch erzeugt) -->
<section class="section archive-teaser" aria-labelledby="archiv-h">
  <p class="kicker">Archiv</p>
  <h2 id="archiv-h" class="section-title">Alle {len(folgen)} Folgen</h2>
  <p class="archive-teaser-text">Seit {jahr0} sprechen wir mit Menschen aus Wissenschaft, Wirtschaft, Psychologie, Sport und Gesellschaft. Such nach Gast, Thema oder Wert.</p>
  <a class="btn" href="folgen/">Zum Archiv</a>
</section>
<!-- ARCHIV:ENDE -->'''

    s = ersetzen(s, 'HERO-NOTIZ', notiz)
    s = ersetzen(s, 'AKTUELLE-FOLGE', aktuell)
    if '<!-- ARCHIV:START' in s:
        s = ersetzen(s, 'ARCHIV', archiv)
    else:
        s = s.replace('<!-- AKTUELLE-FOLGE:ENDE -->', '<!-- AKTUELLE-FOLGE:ENDE -->\n\n' + archiv, 1)
    s = re.sub(r'<p class="hero-meta">.*?</p>', f'<p class="hero-meta">{len(folgen)} Folgen seit {jahr0}</p>', s, count=1)
    s = re.sub(r'(<nav class="site-nav"[^>]*>\s*<ul>\n).*?(\n\s*</ul>)', lambda m: m.group(1) + nav_items('') + m.group(2), s, count=1, flags=re.S)
    # Gewinnspiel-Leiste an/aus
    s = re.sub(r'<!-- GEWINNSPIEL-LEISTE:START.*?<!-- GEWINNSPIEL-LEISTE:ENDE -->\n', '', s, flags=re.S)
    if layout.GEWINNSPIEL_LEISTE:
        s = s.replace('<div class="page">\n', '<div class="page">\n' + leiste(''), 1)
    pfad.write_text(s, encoding='utf-8')


def ersetzen(text, name, neu):
    muster = re.compile(r'<!-- ' + name + r':START.*?<!-- ' + name + r':ENDE -->', re.S)
    if not muster.search(text):
        raise SystemExit(f'Fehler: Markierung {name}:START/ENDE fehlt in index.html')
    return muster.sub(lambda m: neu, text, count=1)


# ---------------------------------------------------------------- Archiv

def suchtext(f, info, titel):
    teile = [f'#{f["nr"]}', str(f['nr']), titel, f['titel_roh'], info['gast'], info['rolle'], f['text'], ' '.join(info['key_learnings'])]
    t = ' '.join(x for x in teile if x).lower()
    t = unicodedata.normalize('NFD', t)
    return re.sub(r'\s+', ' ', ''.join(c for c in t if unicodedata.category(c) != 'Mn'))


def archiv(site, folgen, infos, staffeln, hat_bild):
    pre = '../'
    jahre = sorted({f['datum'].year for f in folgen}, reverse=True)
    zaehl_wert = {w: sum(1 for f in folgen if w == infos[f['nr']]['hauptwert'] or w in infos[f['nr']]['nebenwerte']) for w in WERTE}
    genutzte_staffeln = [s for s in staffeln.values() if any(infos[f['nr']]['staffel'] == s['id'] for f in folgen)]

    eintraege = []
    for f in folgen:
        info = infos[f['nr']]
        titel = anzeige_titel(f, info)
        werte = ([info['hauptwert']] if info['hauptwert'] else []) + info['nebenwerte']
        staffel = staffel_label(f, info, staffeln, folgen, infos)
        meta = ' · '.join(x for x in [f'#{f["nr"]}', datum_de(f['datum']), f'{f["minuten"]} Min.' if f['minuten'] else ''] if x)
        chips = ''.join(f'<li class="value{" value--main" if i == 0 and info["hauptwert"] else ""}">'
                        f'<span class="dot" aria-hidden="true"></span>{w}</li>' for i, w in enumerate(werte))
        thumb = (f'<span class="ep-thumb" aria-hidden="true">{bild(pre, f["nr"], "", klein=True)}</span>'
                 if hat_bild[f['nr']] else '<span class="ep-thumb ep-thumb--leer" aria-hidden="true"></span>')
        gast = f'<span class="ep-guest">mit {esc(info["gast"])}{", " + esc(info["rolle"]) if info["rolle"] else ""}</span>' if info['gast'] else ''
        eintraege.append(f'''    <li class="ep-item" data-werte="{" ".join(werte)}" data-staffel="{esc(info["staffel"])}" data-jahr="{f["datum"].year}" data-text="{esc(suchtext(f, info, titel))}">
      <a class="ep-card" href="{f["slug"]}/">
        {thumb}
        <span class="ep-body">
          <span class="ep-meta-line">{meta}{(" · " + esc(staffel)) if staffel else ""}</span>
          <span class="ep-title-line">{esc(titel)}</span>
          {gast}
        </span>
      </a>
      {f'<ul class="values ep-values" aria-label="Werte">{chips}</ul>' if chips else ''}
    </li>''')

    opt_werte = ''.join(f'<option value="{w}">{w} ({zaehl_wert[w]})</option>' for w in WERTE)
    opt_staffeln = ''.join(f'<option value="{esc(s["id"])}">{esc(s["name"])}</option>' for s in genutzte_staffeln)
    opt_jahre = ''.join(f'<option value="{j}">{j}</option>' for j in jahre)
    jahr0 = min(jahre)

    inhalt = f'''
<main id="inhalt">
<div class="board-sm">
  <p class="kicker">Archiv</p>
  <h1>Alle {len(folgen)} Folgen</h1>
  <p class="gw-text">Seit {jahr0} sprechen wir mit Menschen aus Wissenschaft, Wirtschaft, Psychologie, Sport und Gesellschaft. Hören kannst du jede Folge auf Apple Podcasts und Spotify.</p>
</div>
<section class="section archive" aria-label="Folgen durchsuchen">
  <form class="archive-tools" data-archiv-tools hidden role="search" onsubmit="return false">
    <div class="field archive-search">
      <label for="suche">Suchen</label>
      <input id="suche" type="search" placeholder="Gast, Thema, Stichwort" autocomplete="off" data-filter="text">
    </div>
    <div class="field">
      <label for="f-wert">Wert</label>
      <select id="f-wert" data-filter="wert"><option value="">Alle</option>{opt_werte}</select>
    </div>
    <div class="field">
      <label for="f-staffel">Staffel</label>
      <select id="f-staffel" data-filter="staffel"><option value="">Alle</option>{opt_staffeln}</select>
    </div>
    <div class="field">
      <label for="f-jahr">Jahr</label>
      <select id="f-jahr" data-filter="jahr"><option value="">Alle</option>{opt_jahre}</select>
    </div>
    <p class="archive-count" data-archiv-anzahl aria-live="polite">{len(folgen)} Folgen</p>
  </form>
  <ol class="ep-list" data-archiv-liste>
{chr(10).join(eintraege)}
  </ol>
  <p class="archive-empty" data-archiv-leer hidden>Keine Folge gefunden. Probier einen anderen Suchbegriff oder setz die Filter zurück. <button type="button" class="linkish" data-archiv-reset>Filter zurücksetzen</button></p>
</section>
</main>

'''
    extra = ('<meta name="description" content="Alle Folgen des Podcasts VUCA Blaster seit ' + str(jahr0) +
             ': durchsuchen und nach Wert, Staffel und Jahr filtern.">\n'
             f'<script src="{pre}assets/js/archiv.js" defer></script>\n')
    doc = (head(f'Alle {len(folgen)} Folgen – VUCA Blaster', pre, BASE_URL + 'folgen/', extra) + header(pre) +
           inhalt + footer(pre) + '</body>\n</html>\n')
    (site / 'folgen').mkdir(exist_ok=True)
    (site / 'folgen' / 'index.html').write_text(doc, encoding='utf-8')


# ---------------------------------------------------------------- Folgenseiten

def folgenseiten(site, folgen, infos, staffeln, hat_bild):
    pre = '../../'
    ordner = site / 'folgen'
    gueltig = {f['slug'] for f in folgen}
    for alt in ordner.iterdir():
        if alt.is_dir() and alt.name not in gueltig:
            shutil.rmtree(alt)
    for i, f in enumerate(folgen):
        info = infos[f['nr']]
        titel = anzeige_titel(f, info)
        staffel = staffel_label(f, info, staffeln, folgen, infos)
        kick = f'#{f["nr"]}' + (f' · {esc(staffel)}' if staffel else '')
        meta = ' · '.join(x for x in [f'<time datetime="{f["datum"]:%Y-%m-%d}">{datum_de(f["datum"])}</time>',
                                     f'{f["minuten"]} Min.' if f['minuten'] else ''] if x)
        gast = ''
        if info['gast']:
            rolle = f'<p class="guest-role">{esc(info["rolle"])}</p>' if info['rolle'] else ''
            gast = f'<div class="guest ep-guest-block"><div><p class="guest-name">mit {esc(info["gast"])}</p>{rolle}</div></div>'
        abzug = (f'<figure class="print print--episode"><div class="photo">{bild(pre, f["nr"], "Folgenbild #" + str(f["nr"]), lazy=False)}</div></figure>'
                 if hat_bild[f['nr']] else '')
        neuer = folgen[i - 1] if i > 0 else None
        aelter = folgen[i + 1] if i + 1 < len(folgen) else None
        blaettern = '<nav class="ep-pager" aria-label="Weitere Folgen">'
        blaettern += (f'<a href="../{aelter["slug"]}/"><span>← Ältere Folge</span>#{aelter["nr"]} {esc(anzeige_titel(aelter, infos[aelter["nr"]]))}</a>'
                      if aelter else '<span></span>')
        blaettern += (f'<a class="next" href="../{neuer["slug"]}/"><span>Neuere Folge →</span>#{neuer["nr"]} {esc(anzeige_titel(neuer, infos[neuer["nr"]]))}</a>'
                      if neuer else '<span></span>')
        blaettern += '</nav>'
        beschreibung = f['text'][:152].rsplit(' ', 1)[0] + ' …' if len(f['text']) > 155 else f['text']
        og_bild = f'{BASE_URL}assets/folgen/{f["nr"]}.jpg' if hat_bild[f['nr']] else f'{BASE_URL}assets/img/og-default.png'
        extra = (f'<meta name="description" content="{esc(beschreibung)}">\n'
                 f'<meta property="og:type" content="article">\n<meta property="og:locale" content="de_DE">\n'
                 f'<meta property="og:title" content="#{f["nr"]} {esc(titel)} – VUCA Blaster">\n'
                 f'<meta property="og:description" content="{esc(beschreibung)}">\n'
                 f'<meta property="og:url" content="{BASE_URL}folgen/{f["slug"]}/">\n'
                 f'<meta property="og:image" content="{og_bild}">\n<meta name="twitter:card" content="summary_large_image">\n')
        inhalt = f'''
<main id="inhalt">
<div class="board-sm ep-head">
  <p class="gw-sub">{kick}</p>
  <h1>{esc(titel)}</h1>
  <p class="ep-date">{meta}</p>
</div>
<section class="section ep-section" aria-label="Über diese Folge">
  <div class="ep-grid">
    <div class="ep-main">
      {gast}
      {werte_liste(info)}
      <p class="label listen-label">Diese Folge hören</p>
      <div class="btn-row">{plattformen(f)}</div>
      <p class="hint">Dort hilft jedes Abo und jede Bewertung dem Podcast.</p>
      <h2 class="ep-notes-h">Worum es geht</h2>
      <div class="ep-notes">{f["html"] or "<p>" + esc(f["text"]) + "</p>"}</div>
    </div>
    <div class="ep-side">{abzug}</div>
  </div>
{learnings(info)}</section>
<section class="section ep-more" aria-label="Weiterstöbern">
  {blaettern}
  <a class="btn-outline" href="../">Alle Folgen</a>
</section>
</main>

'''
        doc = (head(f'#{f["nr"]} {esc(titel)} – VUCA Blaster', pre, f'{BASE_URL}folgen/{f["slug"]}/', extra) +
               header(pre) + inhalt + footer(pre) + '</body>\n</html>\n')
        (ordner / f['slug']).mkdir(exist_ok=True)
        (ordner / f['slug'] / 'index.html').write_text(doc, encoding='utf-8')


def kurzlinks(site, folgen):
    """/62/ leitet auf die Folgenseite weiter."""
    for f in folgen:
        ziel = f'../folgen/{f["slug"]}/'
        d = site / str(f['nr'])
        d.mkdir(exist_ok=True)
        (d / 'index.html').write_text(f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><title>Folge #{f["nr"]} – VUCA Blaster</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{BASE_URL}folgen/{f["slug"]}/">
<meta http-equiv="refresh" content="0; url={ziel}">
</head><body><p><a href="{ziel}">Weiter zu Folge #{f["nr"]}</a></p></body></html>
''', encoding='utf-8')


def weiterleitung(site, pfad, ziel_ab_wurzel):
    d = site / pfad
    d.mkdir(exist_ok=True)
    ziel = '../' + ziel_ab_wurzel
    (d / 'index.html').write_text(f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><title>Archiv – VUCA Blaster</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{BASE_URL}{ziel_ab_wurzel}">
<meta http-equiv="refresh" content="0; url={ziel}">
</head><body><p><a href="{ziel}">Weiter zum Archiv</a></p></body></html>
''', encoding='utf-8')


def nicht_indexieren(ordner):
    for o in ordner:
        for p in o.rglob('*.html'):
            s = p.read_text(encoding='utf-8')
            if '<meta name="robots"' not in s:
                p.write_text(s.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex">', 1), encoding='utf-8')


def sitemap(site, folgen):
    urls = ['', 'folgen/', 'impressum/', 'datenschutz/'] + [f'folgen/{f["slug"]}/' for f in folgen]
    body = ''.join(f'  <url><loc>{BASE_URL}{u}</loc></url>\n' for u in urls)
    (site / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}</urlset>\n', encoding='utf-8')
    robots = site / 'robots.txt'
    if robots.exists() and 'Sitemap:' not in robots.read_text():
        robots.write_text(robots.read_text().rstrip('\n') + f'\nSitemap: {BASE_URL}sitemap.xml\n')


# ---------------------------------------------------------------- Vorschau

def als_vorschau(site):
    hinweis = ('<p style="margin:0;padding:10px 16px;background:#161414;color:#FFFFFF;font:600 15px/1.4 system-ui,sans-serif;text-align:center">'
               'Vorschau – noch nicht veröffentlicht. Nicht weitergeben.</p>\n')
    for p in site.rglob('*.html'):
        s = p.read_text(encoding='utf-8')
        if '<meta name="robots"' not in s:
            s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">', 1)
        s = s.replace('<body>\n', '<body>\n' + hinweis, 1)
        p.write_text(s, encoding='utf-8')
    for name in ('CNAME', 'robots.txt', '404.html', 'sitemap.xml', '.nojekyll'):
        (site / name).unlink(missing_ok=True)


# ---------------------------------------------------------------- Ablauf

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ziel', default=str(REPO / 'docs'))
    ap.add_argument('--vorschau', action='store_true')
    ap.add_argument('--offline', action='store_true')
    a = ap.parse_args()
    site = Path(a.ziel).resolve()
    quelle = (REPO / 'docs').resolve()
    if site != quelle:
        if site.exists():
            shutil.rmtree(site)
        shutil.copytree(quelle, site, ignore=shutil.ignore_patterns('vorschau-*', '.DS_Store'))
    DATEN.mkdir(exist_ok=True)

    apple = apple_lesen(holen(APPLE_LOOKUP, DATEN / 'apple.json', a.offline))
    folgen, _cover = feed_lesen(holen(FEED_URL, DATEN / 'feed.xml', a.offline), apple)
    infos = infos_laden(folgen)
    staffeln = staffeln_laden()
    hat_bild = bilder(folgen, site, a.offline)

    unterseiten.main(site)
    gewinnspiel.main(site)
    if layout.ARCHIV_VERLINKT:
        startseite(site, folgen, infos, staffeln, hat_bild)
    archiv(site, folgen, infos, staffeln, hat_bild)
    folgenseiten(site, folgen, infos, staffeln, hat_bild)
    kurzlinks(site, folgen)
    weiterleitung(site, 'archiv', 'folgen/')
    if layout.ARCHIV_VERLINKT:
        sitemap(site, folgen)
    else:
        nicht_indexieren([site / 'folgen'])
    if a.vorschau:
        als_vorschau(site)
    ohne_apple = [f['nr'] for f in folgen if not f['apple']]
    print(f'Fertig: {len(folgen)} Folgen, {sum(hat_bild.values())} Bilder, Apple-Direktlinks für {len(folgen) - len(ohne_apple)}.'
          + (f' Ohne Apple-Link: {ohne_apple}' if ohne_apple else ''))


if __name__ == '__main__':
    main()
