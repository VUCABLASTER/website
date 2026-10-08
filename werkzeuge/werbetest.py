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
    teile = ''.join(_banner(pre, cfg, f, v) for v in f['varianten'])
    return f'<div class="ad-test-platz" data-zaehler="{esc(cfg["goatcounter"])}" data-fassung="{esc(f["version"])}">{teile}</div>\n'


def skript(pre):
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
            text = 'V1: große Banner' if x == 'v1' else x.upper() + ': dezente Banner'
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
