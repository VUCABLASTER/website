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


def _bild(pre, name, b):
    p = f'{pre}assets/img/werbetest/{name}'
    return (f'<picture class="ad-test__bild"><source type="image/webp" srcset="{p}-600.webp 600w, {p}-1200.webp 1200w" '
            f'sizes="(min-width: 768px) 520px, 100vw"><img src="{p}-600.jpg" srcset="{p}-600.jpg 600w, {p}-1200.jpg 1200w" '
            f'sizes="(min-width: 768px) 520px, 100vw" width="600" height="400" alt="{esc(b["alt"])}" loading="lazy" decoding="async"></picture>'
            f'<!-- Foto: {esc(b["von"])} auf Unsplash, {esc(b["seite"])} -->')


def _banner(pre, cfg, v, bild=None, hidden=True, zustand=''):
    name = bild or v['bild']
    b = cfg['bilder'][name]
    hinweis = esc(cfg['hinweis_text']).replace('{produkt}', esc(v['produkt']))
    return f'''<aside class="ad-test{zustand}" data-variante="{esc(v["id"])}" aria-label="Angebot"{" hidden" if hidden else ""}>
  <div class="ad-test__werbung">
    {_bild(pre, name, b)}
    <div class="ad-test__inhalt">
      <span class="ad-test__label">{esc(v["label"])}</span>
      <h2 class="ad-test__titel">{esc(v["titel"])}</h2>
      <p class="ad-test__text">{esc(v["text"])}</p>
      <div class="ad-test__fuss"><span class="ad-test__preis">{esc(v["preis"])}</span>
        <button type="button" class="ad-test__btn">{esc(v["button"])} <span aria-hidden="true">→</span></button></div>
    </div>
  </div>
  <div class="ad-test__hinweis" role="status" tabindex="-1">
    <span class="ad-test__haken" aria-hidden="true"><svg viewBox="0 0 24 24" width="28" height="28"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
    <div><p class="ad-test__hinweis-titel">{esc(cfg["hinweis_titel"])}</p>
    <p class="ad-test__hinweis-text">{hinweis}</p></div>
  </div>
</aside>'''


def banner_html(pre):
    """Alle Varianten (versteckt) für eine Seite; leer, wenn der Test aus ist."""
    cfg = laden()
    if not aktiv(cfg):
        return ''
    teile = ''.join(_banner(pre, cfg, v) for v in cfg['varianten'])
    return f'<div class="ad-test-platz" data-zaehler="{esc(cfg["goatcounter"])}">{teile}</div>\n'


def skript(pre):
    return f'<script src="{pre}assets/js/werbetest.js?v={version("js/werbetest.js")}" defer></script>\n' if aktiv() else ''


def vorschau(site):
    """Abnahmeseite mit allen Fassungen: pro Produkt jedes Foto als Desktop- und Mobilbanner, dazu der Hinweis."""
    cfg = laden()
    ordner = site / 'werbetest-vorschau'
    if not cfg or cfg.get('aktiv'):
        shutil.rmtree(ordner, ignore_errors=True)  # nach dem Start nicht mehr nötig
        return
    pre = '../'
    reihen = []
    for v in cfg['varianten']:
        reihen.append(f'<h2 class="wtv-h">{esc(v["titel"])}</h2>')
        for i, name in enumerate(v.get('kandidaten') or [v['bild']], 1):
            b = cfg['bilder'][name]
            reihen.append(f'''<section class="wtv-reihe">
  <p class="wtv-name">Foto {i}{" (Vorschlag)" if name == v["bild"] else ""} · {esc(b["von"])} auf <a href="{esc(b["seite"])}">Unsplash</a></p>
  <div class="wtv-paar">
    <div class="wtv-desktop"><p class="wtv-tag">Desktop</p>{_banner(pre, cfg, v, name, hidden=False)}</div>
    <div class="wtv-mobil"><p class="wtv-tag">Mobil</p>{_banner(pre, cfg, v, name, hidden=False)}</div>
  </div>
</section>''')
    v = cfg['varianten'][0]
    reihen.append(f'''<h2 class="wtv-h">Nach dem Klick: Testhinweis</h2>
<section class="wtv-reihe"><div class="wtv-paar">
  <div class="wtv-desktop"><p class="wtv-tag">Desktop</p>{_banner(pre, cfg, v, hidden=False, zustand=" ist-geklickt")}</div>
  <div class="wtv-mobil"><p class="wtv-tag">Mobil</p>{_banner(pre, cfg, v, hidden=False, zustand=" ist-geklickt")}</div>
</div></section>''')
    einleitung = ('<p>Abnahme für den Werbetest. Pro Produkt sind drei Fotos zur Auswahl, jeweils als Desktop- und Mobilfassung. '
                  'Ein Klick auf ein Banner zeigt den Testhinweis (hier ohne Zählung). Diese Seite ist nicht verlinkt und nicht indexiert.</p>')
    ordner.mkdir(exist_ok=True)
    (ordner / 'index.html').write_text(page(
        'Werbetest Vorschau – VUCA Blaster', '', pre, 'Werbetest: Vorschau',
        (einleitung, '<div class="wtv">' + '\n'.join(reihen) + '</div>'),
        extra_head=f'<meta name="robots" content="noindex">\n<script src="{pre}assets/js/werbetest.js?v={version("js/werbetest.js")}" defer></script>\n'),
        encoding='utf-8')
