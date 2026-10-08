"""Werbetest (Fake Door): drei Produktbanner auf Startseite und Folgenseiten, gesteuert über inhalte/werbetest.json.

Das Skript assets/js/werbetest.js zeigt pro Seitenaufruf zufällig eine Variante. Nach dem Klick tauscht sich das Banner
an derselben Stelle gegen den Testhinweis aus (kein Seitenwechsel). Gezählt werden nur „gesehen“ und „klick“ pro
Variante, direkt an den GoatCounter-Endpunkt (ohne Cookies, ohne GoatCounter-Skript).
Zusätzlich entsteht die Abnahmeseite /werbetest-vorschau/ (noindex, ohne Zählung) mit allen Fassungen und Fotos."""
import datetime, html, json, shutil

from layout import REPO, page, version

DATEI = REPO / 'inhalte' / 'werbetest.json'
esc = lambda s: html.escape(str(s), quote=True)


def laden():
    return json.loads(DATEI.read_text(encoding='utf-8')) if DATEI.exists() else {}


def aktiv(cfg=None):
    cfg = cfg if cfg is not None else laden()
    if not cfg.get('aktiv'):
        return False
    if cfg.get('ende') and datetime.date.today().isoformat() > cfg['ende']:
        return False
    if not cfg.get('goatcounter'):
        raise SystemExit('Werbetest: "goatcounter" fehlt in inhalte/werbetest.json')
    return True


def fassung(cfg, version=None):
    """Texte und Varianten einer Fassung. v1 steht oben in der Datei, weitere Fassungen (v2 …) unter ihrem Namen."""
    version = version or cfg.get('version', 'v1')
    basis = {'hinweis_titel': cfg['hinweis_titel'], 'hinweis_text': cfg['hinweis_text'], 'varianten': cfg['varianten'], 'stil': ''}
    return dict(basis, **cfg.get(version, {}), version=version) if version != 'v1' else dict(basis, version='v1')


def _bild_quadrat(pre, name, b):
    p = f'{pre}assets/img/werbetest/{name}'
    return (f'<picture class="ad-test__bild"><source type="image/webp" srcset="{p}-q.webp"><img src="{p}-q.jpg" width="320" height="320" '
            f'alt="{esc(b["alt"])}" loading="lazy" decoding="async"></picture><!-- Foto: {esc(b["von"])} auf Unsplash, {esc(b["seite"])} -->')


def _bild(pre, name, b):
    p = f'{pre}assets/img/werbetest/{name}'
    return (f'<picture class="ad-test__bild"><source type="image/webp" srcset="{p}-600.webp 600w, {p}-1200.webp 1200w" '
            f'sizes="(min-width: 768px) 520px, 100vw"><img src="{p}-600.jpg" srcset="{p}-600.jpg 600w, {p}-1200.jpg 1200w" '
            f'sizes="(min-width: 768px) 520px, 100vw" width="600" height="400" alt="{esc(b["alt"])}" loading="lazy" decoding="async"></picture>'
            f'<!-- Foto: {esc(b["von"])} auf Unsplash, {esc(b["seite"])} -->')


def _banner(pre, cfg, f, v, bild=None, hidden=True, zustand=''):
    name = bild or v['bild']
    b = cfg['bilder'][name]
    hinweis = esc(f['hinweis_text']).replace('{produkt}', esc(v['produkt']))
    stil = f' ad-test--{f["stil"]}' if f.get('stil') else ''
    foto = _bild_quadrat(pre, name, b) if f.get('stil') == 'dezent' else _bild(pre, name, b)
    preis = f'<span class="ad-test__preis">{esc(v["preis"])}</span>' if v.get('preis') else ''
    return f'''<aside class="ad-test{stil}{zustand}" data-variante="{esc(v["id"])}" aria-label="Angebot"{" hidden" if hidden else ""}>
  <div class="ad-test__werbung">
    {foto}
    <div class="ad-test__inhalt">
      <span class="ad-test__label">{esc(v["label"])}</span>
      <h2 class="ad-test__titel">{esc(v["titel"])}</h2>
      <p class="ad-test__text">{esc(v["text"])}</p>
      <div class="ad-test__fuss">{preis}
        <button type="button" class="ad-test__btn">{esc(v["button"])} <span aria-hidden="true">→</span></button></div>
    </div>
  </div>
  <div class="ad-test__hinweis" role="status" tabindex="-1">
    <span class="ad-test__haken" aria-hidden="true"><svg viewBox="0 0 24 24" width="28" height="28"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
    <div><p class="ad-test__hinweis-titel">{esc(f["hinweis_titel"])}</p>
    <p class="ad-test__hinweis-text">{hinweis}</p></div>
  </div>
</aside>'''


def banner_html(pre):
    """Alle Varianten (versteckt) für eine Seite; leer, wenn der Test aus ist."""
    cfg = laden()
    if not aktiv(cfg):
        return ''
    f = fassung(cfg)
    if f.get('stil') == 'postit':
        return ''  # Post-its setzt postit_seiten() ein
    teile = ''.join(_banner(pre, cfg, f, v) for v in f['varianten'])
    return f'<div class="ad-test-platz" data-zaehler="{esc(cfg["goatcounter"])}" data-fassung="{esc(f["version"])}">{teile}</div>\n'


def skript(pre):
    if laden() and fassung(laden()).get('stil') == 'postit':
        return ''
    return f'<script src="{pre}assets/js/werbetest.js?v={version("js/werbetest.js")}" defer></script>\n' if aktiv() else ''


def vorschau(site):
    """Abnahmeseiten /werbetest-vorschau/ (v1, große Banner) und /werbetest-vorschau/v2/ (dezent): alle Fassungen
    als Desktop- und Mobilbanner, dazu der Testhinweis. Ohne Zählung. Nach dem Start des Tests werden sie entfernt."""
    cfg = laden()
    ordner = site / 'werbetest-vorschau'
    if not cfg or cfg.get('aktiv'):
        shutil.rmtree(ordner, ignore_errors=True)
        return
    fassungen = ['v1'] + [k for k in cfg if k.startswith('v') and k[1:].isdigit()]
    for name_f in fassungen:
        f = fassung(cfg, name_f)
        if f.get('stil') == 'postit':
            continue
        ziel = ordner if name_f == 'v1' else ordner / name_f
        pre = '../' if name_f == 'v1' else '../../'
        reihen = []
        for v in f['varianten']:
            reihen.append(f'<h2 class="wtv-h">{esc(v["titel"])}</h2>')
            for i, name in enumerate(v.get('kandidaten') or [v['bild']], 1):
                b = cfg['bilder'][name]
                nr = f'Foto {i}{" (Vorschlag)" if name == v["bild"] else ""} · ' if v.get('kandidaten') else 'Foto: '
                reihen.append(f'''<section class="wtv-reihe">
  <p class="wtv-name">{nr}{esc(b["von"])} auf <a href="{esc(b["seite"])}">Unsplash</a></p>
  <div class="wtv-paar">
    <div class="wtv-desktop"><p class="wtv-tag">Desktop</p>{_banner(pre, cfg, f, v, name, hidden=False)}</div>
    <div class="wtv-mobil"><p class="wtv-tag">Mobil</p>{_banner(pre, cfg, f, v, name, hidden=False)}</div>
  </div>
</section>''')
        v = f['varianten'][0]
        reihen.append(f'''<h2 class="wtv-h">Nach dem Klick: Testhinweis</h2>
<section class="wtv-reihe"><div class="wtv-paar">
  <div class="wtv-desktop"><p class="wtv-tag">Desktop</p>{_banner(pre, cfg, f, v, hidden=False, zustand=" ist-geklickt")}</div>
  <div class="wtv-mobil"><p class="wtv-tag">Mobil</p>{_banner(pre, cfg, f, v, hidden=False, zustand=" ist-geklickt")}</div>
</div></section>''')
        def link(x):
            ziel_url = f'{pre}werbetest-vorschau/' + ('' if x == 'v1' else x + '/')
            aktuell = ' aria-current="page"' if x == name_f else ''
            text = 'V1: große Banner' if x == 'v1' else x.upper() + (': Post-its' if fassung(cfg, x).get('stil') == 'postit' else ': dezente Banner')
            return f'<a href="{ziel_url}"{aktuell}>{text}</a>'
        links = ' · '.join(link(x) for x in fassungen)
        live = cfg.get('version', 'v1')
        einleitung = (f'<p>Abnahme für den Werbetest. Fassungen: {links}. Geplant für den Start: <strong>{live.upper()}</strong>. '
                      'Ein Klick auf ein Banner zeigt den Testhinweis (hier ohne Zählung). Diese Seite ist nicht verlinkt und nicht indexiert.</p>')
        ziel.mkdir(parents=True, exist_ok=True)
        (ziel / 'index.html').write_text(page(
            f'Werbetest Vorschau {name_f.upper()} – VUCA Blaster', '', pre, f'Werbetest: Vorschau {name_f.upper()}',
            (einleitung, '<div class="wtv">' + '\n'.join(reihen) + '</div>'),
            extra_head=f'<meta name="robots" content="noindex">\n<script src="{pre}assets/js/werbetest.js?v={version("js/werbetest.js")}" defer></script>\n'),
            encoding='utf-8')


def testseiten(site, folgen):
    """Pro Banner der geplanten Fassung eine Testseite im echten Umfeld: die neueste Folgenseite mit genau diesem Banner
    an der späteren Stelle (zwischen Key Learnings und „Weiterstöbern“). Liegt unter /werbetest-vorschau/<fassung>/<id>/,
    noindex, ohne Zählung. Wird mit der Vorschau entfernt, sobald der Test läuft."""
    import re
    cfg = laden()
    if not cfg or cfg.get('aktiv') or not folgen:
        return
    f = fassung(cfg)
    if f.get('stil') == 'postit':
        return
    quelle = (site / 'folgen' / folgen[0]['slug'] / 'index.html').read_text(encoding='utf-8')
    # Pfade von /folgen/<slug>/ (Tiefe 2) auf /werbetest-vorschau/<fassung>/<id>/ (Tiefe 3) umstellen
    seite = re.sub(r'(?<=["\s,])\.\./\.\./', '../../../', quelle)
    seite = re.sub(r'(?<=["\s,])\.\./(?!\.\./)', '../../../folgen/', seite)
    seite = seite.replace('<head>', '<head>\n<meta name="robots" content="noindex">', 1)
    seite = seite.replace('</head>', f'<script src="../../../assets/js/werbetest.js?v={version("js/werbetest.js")}" defer></script>\n</head>', 1)
    for v in f['varianten']:
        platz = f'<div class="ad-test-platz" data-zaehler="" data-fassung="{esc(f["version"])}">{_banner("../../../", cfg, f, v)}</div>\n'
        hinweis = (f'<p class="wtv-testhinweis">Testseite (nicht verlinkt): So erscheint das Banner „{esc(v["titel"])}“ auf einer Folgenseite. '
                   f'Weiter unten, nach den Key Learnings. <a href="../">Alle Banner dieser Fassung</a></p>\n')
        neu = seite.replace('<section class="section ep-more"', platz + '<section class="section ep-more"', 1)
        neu = neu.replace('<main id="inhalt">', '<main id="inhalt">\n' + hinweis, 1)
        ziel = site / 'werbetest-vorschau' / f['version'] / v['id']
        ziel.mkdir(parents=True, exist_ok=True)
        (ziel / 'index.html').write_text(neu, encoding='utf-8')


# ---------------------------------------------------------------- Post-it-Fassung (stil "postit")
# Statt eines festen Banners: ein Klebezettel mit kleinem Foto, der pro Seitenaufruf an einer von mehreren Stellen
# erscheint (neben den Key Learnings, unter dem Folgenbild, unter dem VUCA-Blaster-Bild). Klebestreifen (1–3),
# Farbe und Neigung wechseln zufällig. Alles, was eingesetzt wird, steht zwischen WT-Markern und wird bei jedem
# Build zuerst entfernt, damit nichts doppelt entsteht und der Test sauber verschwindet, wenn er aus ist.
import re as _re

WT_A, WT_E = '<!--WT:START-->', '<!--WT:ENDE-->'


def _notiz(pre, cfg, f, v):
    b = cfg['bilder'][v['bild']]
    p = f'{pre}assets/img/werbetest/{v["bild"]}'
    hinweis = esc(f['hinweis_text']).replace('{produkt}', esc(v['produkt']))
    preis = f'<span class="ad-note__preis">{esc(v["preis"])}</span>' if v.get('preis') else ''
    return f'''<aside class="ad-test ad-note" data-variante="{esc(v["id"])}" aria-label="Angebot" hidden>
  <span class="ad-note__band ad-note__band--a" aria-hidden="true"></span><span class="ad-note__band ad-note__band--b" aria-hidden="true"></span><span class="ad-note__band ad-note__band--c" aria-hidden="true"></span>
  <div class="ad-test__werbung">
    <span class="ad-note__foto"><picture><source type="image/webp" srcset="{p}-q.webp"><img src="{p}-q.jpg" width="320" height="320" alt="{esc(b["alt"])}" loading="lazy" decoding="async"></picture></span><!-- Foto: {esc(b["von"])} auf Unsplash, {esc(b["seite"])} -->
    <span class="ad-note__inhalt">
      <span class="ad-note__label">{esc(v["label"])}</span>
      <strong class="ad-note__titel">{esc(v["titel"])}</strong>
      <span class="ad-note__text">{esc(v["text"])}</span>
      <span class="ad-note__fuss">{preis}<button type="button" class="ad-note__btn">{esc(v["button"])} <span aria-hidden="true">→</span></button></span>
    </span>
  </div>
  <div class="ad-test__hinweis" role="status" tabindex="-1">
    <span class="ad-test__haken" aria-hidden="true"><svg viewBox="0 0 24 24" width="20" height="20"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
    <div><p class="ad-test__hinweis-titel">{esc(f["hinweis_titel"])}</p><p class="ad-test__hinweis-text">{hinweis}</p></div>
  </div>
</aside>'''


def entfernen(seite):
    return _re.sub(_re.escape(WT_A) + r'.*?' + _re.escape(WT_E) + r'\n?', '', seite, flags=_re.S)


def _nach(seite, anker, ende, einsatz):
    """einsatz direkt nach dem ersten `ende`, das auf `anker` folgt."""
    i = seite.find(anker)
    if i < 0:
        return seite
    j = seite.find(ende, i)
    if j < 0:
        return seite
    j += len(ende)
    return seite[:j] + einsatz + seite[j:]


def einbauen(seite, art, pre, cfg, f, zaehler, platz=''):
    """Setzt Plätze, Zettel-Vorrat und Skript in eine fertige Seite (art = 'folge' oder 'start')."""
    slot = lambda name: f'{WT_A}<div class="ad-slot" data-platz="{name}"></div>{WT_E}'
    plaetze = f.get('plaetze', {}).get(art, [])
    if 'learnings' in plaetze:
        seite = _nach(seite, '<ol class="stickies"', '</ol>', slot('learnings'))
    if 'bild' in plaetze:
        seite = _nach(seite, '<div class="ep-side">', '</figure>', slot('bild'))
    if 'about' in plaetze:
        seite = _nach(seite, '<figure class="print print--cover">', '</figure>', slot('about'))
    vorrat = ''.join(_notiz(pre, cfg, f, v) for v in f['varianten'])
    seite = seite.replace('</main>', f'{WT_A}<div class="ad-store" hidden data-zaehler="{esc(zaehler)}" data-fassung="{esc(f["version"])}"'
                          f' data-platz="{esc(platz)}">{vorrat}</div>{WT_E}\n</main>', 1)
    seite = seite.replace('</head>', f'{WT_A}<script src="{pre}assets/js/werbetest.js?v={version("js/werbetest.js")}" defer></script>{WT_E}\n</head>', 1)
    return seite


def postit_seiten(site, folgen):
    """Live-Einbau der Post-it-Fassung in Startseite und Folgenseiten (oder Entfernen, wenn der Test aus ist)."""
    cfg = laden()
    an = bool(cfg) and aktiv(cfg) and fassung(cfg).get('stil') == 'postit'
    f = fassung(cfg) if cfg else {}
    ziele = [(site / 'index.html', 'start', '')] + [(site / 'folgen' / x['slug'] / 'index.html', 'folge', '../../') for x in folgen]
    for pfad, art, pre in ziele:
        if not pfad.exists():
            continue
        alt = pfad.read_text(encoding='utf-8')
        neu = entfernen(alt)
        if an:
            neu = einbauen(neu, art, pre, cfg, f, cfg['goatcounter'])
        if neu != alt:
            pfad.write_text(neu, encoding='utf-8')


def _tiefer(seite, von_wurzel):
    """Relative Pfade einer Seite auf /werbetest-vorschau/<fassung>/<name>/ (Tiefe 3) umstellen."""
    if von_wurzel:  # Startseite: "assets/…", "folgen/…", "#…"
        return _re.sub(r'((?:href|src|srcset)=")(?!https?:|//|#|mailto:|data:|/|\.\./)', r'\g<1>../../../', seite)
    seite = _re.sub(r'(?<=["\s,])\.\./\.\./', '../../../', seite)
    return _re.sub(r'(?<=["\s,])\.\./(?!\.\./)', '../../../folgen/', seite)


def postit_testseiten(site, folgen):
    """Testseiten im echten Umfeld, je Platz eine: Folgenseite (neben Key Learnings / unter dem Folgenbild) und
    Startseite (neben Key Learnings / unter dem VUCA-Blaster-Bild). Produkt, Klebestreifen und Farbe wechseln bei jedem
    Neuladen. Ohne Zählung, noindex."""
    cfg = laden()
    if not cfg or cfg.get('aktiv') or not folgen:
        return
    for name_f in [k for k in cfg if k.startswith('v') and k[1:].isdigit()]:
        f = fassung(cfg, name_f)
        if f.get('stil') != 'postit':
            continue
        basis = {'folge': (site / 'folgen' / folgen[0]['slug'] / 'index.html', False),
                 'start': (site / 'index.html', True)}
        seiten = []
        for art, plaetze in f.get('plaetze', {}).items():
            quelle, wurzel = basis[art]
            roh = entfernen(quelle.read_text(encoding='utf-8'))
            for platz in plaetze:
                seite = _tiefer(roh, wurzel).replace('<head>', '<head>\n<meta name="robots" content="noindex">', 1)
                seite = einbauen(seite, art, '../../../', cfg, f, '', platz)
                titel = {'learnings': 'neben den Key Learnings', 'bild': 'unter dem Folgenbild', 'about': 'unter dem VUCA-Blaster-Bild'}[platz]
                ort = 'Startseite' if art == 'start' else 'Folgenseite'
                hinweis = (f'<p class="wtv-testhinweis">Testseite (nicht verlinkt): Post-it auf der {ort}, {titel}. '
                           f'Neu laden zeigt ein anderes Produkt und andere Klebestreifen. <a href="../">Übersicht</a></p>\n')
                seite = seite.replace('<main id="inhalt">', '<main id="inhalt">\n' + hinweis, 1)
                ziel = site / 'werbetest-vorschau' / name_f / f'{art}-{platz}'
                ziel.mkdir(parents=True, exist_ok=True)
                (ziel / 'index.html').write_text(seite, encoding='utf-8')
                seiten.append((f'{art}-{platz}/', f'{ort}: {titel}'))
        # Übersicht: alle Zettel mit 1, 2 und 3 Klebestreifen
        zettel = []
        for v in f['varianten']:
            for band, farbe in (('band-1', 'farbe-rose'), ('band-2', 'farbe-aqua'), ('band-3', 'farbe-rose')):
                n = _notiz('../../', cfg, f, v).replace(' hidden>', '>', 1).replace('class="ad-test ad-note"', f'class="ad-test ad-note {band} {farbe}"', 1)
                zettel.append(f'<div class="wtv-zettel">{n}</div>')
        links = ''.join(f'<li><a href="{u}">{esc(t)}</a></li>' for u, t in seiten)
        inhalt = (f'<p>Post-it-Fassung ({name_f.upper()}). Auf der Website erscheint pro Seitenaufruf ein Zettel an einer zufälligen Stelle, '
                  'mit wechselnden Klebestreifen, Farben und Neigungen. Klick zeigt den Testhinweis (hier ohne Zählung).</p>'
                  f'<p><strong>Testseiten im echten Umfeld:</strong></p><ul>{links}</ul>')
        (site / 'werbetest-vorschau' / name_f).mkdir(parents=True, exist_ok=True)
        (site / 'werbetest-vorschau' / name_f / 'index.html').write_text(page(
            f'Werbetest Vorschau {name_f.upper()} – VUCA Blaster', '', '../../', f'Werbetest: Post-its ({name_f.upper()})',
            (inhalt, '<div class="wtv"><div class="wtv-zettelwand">' + ''.join(zettel) + '</div></div>'),
            extra_head=f'<meta name="robots" content="noindex">\n<script src="../../assets/js/werbetest.js?v={version("js/werbetest.js")}" defer></script>\n'),
            encoding='utf-8')
