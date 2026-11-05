"""Impulse: kurze Gäste-Botschaften mit eingebundenem Video.

Daten: inhalte/impulse/*.json. Erscheint nur, wenn "freigegeben": true.
Erzeugt: docs/impulse/ (Übersicht + eine Seite pro Impuls) und den Teaser auf der Startseite.
Der Video-Player lädt erst nach Klick (youtube-nocookie).
"""
import json, html, shutil
from pathlib import Path
from layout import REPO, BASE_URL, head, header, footer

ORDNER = REPO / 'inhalte' / 'impulse'
esc = lambda s: html.escape(s or '', quote=True)

SKRIPT = """<script>
(function () {
  document.querySelectorAll('[data-impuls-video]').forEach(function (box) {
    var id = box.getAttribute('data-impuls-video');
    var btn = box.querySelector('[data-impuls-load]');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) + '?autoplay=1';
      f.title = box.getAttribute('data-title') || 'Video';
      f.allow = 'accelerometer; autoplay; encrypted-media; picture-in-picture';
      f.allowFullscreen = true;
      box.replaceChildren(f);
    });
  });
})();
</script>
"""

STIL = """<style>
.impuls-video{position:relative;width:100%;aspect-ratio:16/9;background:var(--c-ink);color:#FFFFFF;display:flex;align-items:center;justify-content:center;text-align:center;border:1.5px solid var(--c-frame)}
.impuls-video--hoch{aspect-ratio:9/16;max-width:360px}
.impuls-video iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.impuls-video button{font:inherit;font-weight:700;padding:14px 22px;border:2px solid #FFFFFF;background:transparent;color:#FFFFFF;cursor:pointer;min-height:48px}
.impuls-video button:hover{background:#FFFFFF;color:var(--c-ink)}
.impuls-note{margin:12px 16px 0;font-size:14px;opacity:.85}
.impuls-note a{color:#FFFFFF}
</style>
"""


def laden():
    """Nur freigegebene Impulse mit Video-ID, nach Dateiname sortiert."""
    liste = []
    if ORDNER.exists():
        for p in sorted(ORDNER.glob('*.json')):
            d = json.loads(p.read_text(encoding='utf-8'))
            if d.get('freigegeben') is True and d.get('slug') and d.get('video_id'):
                liste.append(d)
    return liste


def video(d, pre):
    klasse = 'impuls-video' + (' impuls-video--hoch' if d.get('format') == 'hoch' else '')
    return (f'<div class="{klasse}" data-impuls-video="{esc(d["video_id"])}" data-title="{esc(d["titel"])}">'
            f'<button type="button" data-impuls-load>Video laden</button>'
            f'<p class="impuls-note">Beim Laden werden Daten an YouTube übertragen. '
            f'Mehr dazu in der <a href="{pre}datenschutz/">Datenschutzerklärung</a>.</p></div>')


def teaser_html(pre=''):
    """Teaser für die Startseite. Leer, solange kein Impuls freigegeben ist."""
    liste = laden()
    if not liste:
        return ''
    punkte = ''.join(
        f'<li><a href="{pre}impulse/{esc(d["slug"])}/"><span class="impuls-t">{esc(d["titel"])}</span>'
        f'<span class="impuls-g">mit {esc(d.get("gast", ""))}</span></a></li>' for d in liste)
    return f'''<section class="section impuls-teaser" aria-labelledby="impulse-h">
  <p class="kicker">Impulse</p>
  <h2 id="impulse-h" class="section-title">Kurze Botschaften unserer Gäste</h2>
  <ul class="impuls-liste">{punkte}</ul>
  <a class="btn" href="{pre}impulse/">Alle Impulse</a>
</section>'''


def seite(site, d):
    pre = '../../'
    titel = d['titel']
    gast = d.get('gast', '')
    rolle = d.get('rolle', '')
    folge = ''
    if d.get('folge_nummer') and d.get('folge_slug'):
        folge = f'<a class="btn-outline" href="{pre}folgen/{esc(d["folge_slug"])}/">Zur Folge #{d["folge_nummer"]}</a>'
    gast_html = ''
    if gast:
        rolle_html = f'<p class="guest-role">{esc(rolle)}</p>' if rolle else ''
        gast_html = f'<div class="guest ep-guest-block"><div><p class="guest-name">{esc(gast)}</p>{rolle_html}</div></div>'
    inhalt = f'''
<main id="inhalt">
<div class="board-sm ep-head">
  <p class="gw-sub">Impuls{(" · " + esc(gast)) if gast else ""}</p>
  <h1>{esc(titel)}</h1>
</div>
<section class="section ep-section" aria-label="Impuls">
  <div class="ep-grid">
    <div class="ep-main">
      {gast_html}
      {video(d, pre)}
      {f'<div class="btn-row">{folge}</div>' if folge else ''}
    </div>
  </div>
</section>
<section class="section ep-more" aria-label="Weiterstöbern">
  <a class="btn-outline" href="../">Alle Impulse</a>
  <a class="btn-outline" href="{pre}folgen/">Alle Folgen</a>
</section>
</main>

'''
    doc = (head(f'{esc(titel)} – Impuls mit {esc(gast)} – VUCA Blaster' if gast else f'{esc(titel)} – Impuls – VUCA Blaster',
                pre, f'{BASE_URL}impulse/{d["slug"]}/', STIL) +
           header(pre) + inhalt + footer(pre) + SKRIPT + '</body>\n</html>\n')
    (site / 'impulse' / d['slug']).mkdir(parents=True, exist_ok=True)
    (site / 'impulse' / d['slug'] / 'index.html').write_text(doc, encoding='utf-8')


def uebersicht(site, liste):
    pre = '../'
    if liste:
        eintraege = ''.join(
            f'<li class="impuls-eintrag"><a href="{esc(d["slug"])}/"><span class="impuls-t">{esc(d["titel"])}</span>'
            f'<span class="impuls-g">mit {esc(d.get("gast", ""))}</span></a></li>' for d in liste)
        text = f'<ul class="impuls-liste">{eintraege}</ul>'
    else:
        text = '<p>Noch keine Impulse veröffentlicht.</p>'
    inhalt = f'''
<main id="inhalt">
<div class="board-sm">
  <p class="kicker">Impulse</p>
  <h1>Kurze Botschaften unserer Gäste</h1>
</div>
<section class="section" aria-label="Alle Impulse">
  {text}
</section>
</main>

'''
    doc = head('Impulse – VUCA Blaster', pre, f'{BASE_URL}impulse/', STIL) + header(pre) + inhalt + footer(pre) + SKRIPT + '</body>\n</html>\n'
    (site / 'impulse' / 'index.html').write_text(doc, encoding='utf-8')


def seiten(site):
    """Erzeugt docs/impulse/ neu. Alte Impulse, die nicht mehr freigegeben sind, verschwinden dabei."""
    ziel = site / 'impulse'
    if ziel.exists():
        shutil.rmtree(ziel)
    ziel.mkdir(parents=True)
    liste = laden()
    uebersicht(site, liste)
    for d in liste:
        seite(site, d)


def urls():
    return ['impulse/'] + [f'impulse/{d["slug"]}/' for d in laden()]
