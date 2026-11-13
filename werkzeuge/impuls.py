"""Impulse: kurze Gäste-Botschaften als Post-it-Wand mit Video.

Daten: inhalte/impulse/*.json. Erscheint nur, wenn "freigegeben": true.
Erzeugt: docs/impulse/ (eine Seite mit allen Impulsen) und den Teaser auf der Startseite.
Der Video-Player lädt erst nach Klick (youtube-nocookie), erst dann fließen Daten an YouTube.
"""
import json, html, shutil
from pathlib import Path
from layout import REPO, BASE_URL, head, header, footer

ORDNER = REPO / 'inhalte' / 'impulse'
esc = lambda s: html.escape(str(s or ''), quote=True)

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@700;900&family=Caveat:wght@600;700&display=swap" rel="stylesheet">\n')

STIL = """<style>
.impuls-wrap{max-width:1120px;margin:0 auto;padding:36px 32px 80px}
.impuls-h1{font-family:"Archivo",sans-serif;font-weight:900;font-size:clamp(48px,8vw,88px);line-height:.95;letter-spacing:-.03em;margin:0 0 4px}
.impuls-sub{font-family:"Caveat",cursive;font-size:64px;line-height:1;margin:0 0 8px;color:var(--c-ink)}
.impuls-intro{font-size:18px;max-width:60ch;margin:0 0 56px;opacity:.85}
.impuls-wall{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:56px 36px;list-style:none;margin:0;padding:0}
.impuls-note{position:relative;background:#fff1a8;padding:26px 22px 24px;box-shadow:0 10px 18px rgba(0,0,0,.09),0 2px 4px rgba(0,0,0,.06);transform:rotate(var(--r,0deg));transition:transform .3s cubic-bezier(.2,.7,.2,1),box-shadow .3s ease;display:flex;flex-direction:column;gap:14px;color:#161616}
.impuls-note--pink{background:#f6cfe0}
.impuls-note:nth-child(odd){--r:-1.2deg}
.impuls-note:nth-child(even){--r:1deg}
.impuls-note:hover,.impuls-note:focus-within{transform:rotate(0) translateY(-6px);box-shadow:0 22px 30px rgba(0,0,0,.15)}
.impuls-tape{position:absolute;top:-14px;left:50%;width:100px;height:28px;background:rgba(232,221,190,.9);transform:translateX(-50%) rotate(-3deg);box-shadow:0 1px 2px rgba(0,0,0,.08)}
.impuls-video{position:relative;width:100%;aspect-ratio:16/9;border:2px solid #161616;background:repeating-linear-gradient(45deg,#e9e9df 0 10px,#f3f3eb 10px 20px)}
.impuls-video iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.impuls-cover{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.impuls-play{position:absolute;inset:0;width:100%;height:100%;border:0;background:transparent;cursor:pointer;font:inherit;color:#161616;padding:0}
.impuls-play span.kreis{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:56px;height:56px;border-radius:50%;background:#161616;display:grid;place-items:center;transition:transform .25s ease}
.impuls-play:hover span.kreis{transform:translate(-50%,-50%) scale(1.08)}
.impuls-play span.kreis::after{content:"";border-left:16px solid #fff;border-top:10px solid transparent;border-bottom:10px solid transparent;margin-left:4px}
.impuls-play .hinweis{position:absolute;left:10px;right:10px;bottom:10px;background:#fff;font-size:12px;padding:3px 8px;text-align:left}
.impuls-t{font-family:"Archivo",sans-serif;font-size:22px;line-height:1.15;margin:0;font-weight:700}
.impuls-g{font-size:14px;margin:0;opacity:.8}
.impuls-g a{color:inherit}
.impuls-lern{font-family:"Caveat",cursive;font-size:25px;line-height:1.15;margin:0}
.impuls-btns{display:flex;flex-wrap:wrap;gap:10px;margin-top:auto}
.impuls-btn{display:inline-block;text-decoration:none;color:#161616;border:2px solid #161616;background:transparent;font-weight:600;font-size:15px;padding:9px 16px;transition:background .2s ease,color .2s ease}
.impuls-btn:hover{background:#161616;color:#fff}
.impuls-btn--gestrichelt{border-style:dashed}
.impuls-btn--aus{border-style:dashed;opacity:.55;cursor:not-allowed}
.impuls-btn--aus:hover{background:transparent;color:#161616}
@media (max-width:760px){.impuls-wrap{padding:28px 20px 64px}.impuls-sub{font-size:44px}}
@media (prefers-reduced-motion:reduce){.impuls-note,.impuls-play span.kreis{transition:none!important}}
</style>
"""

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


def laden():
    """Nur freigegebene Impulse mit Video-ID, nach Dateiname sortiert."""
    liste = []
    if ORDNER.exists():
        for p in sorted(ORDNER.glob('*.json')):
            d = json.loads(p.read_text(encoding='utf-8'))
            if d.get('freigegeben') is True and d.get('slug') and d.get('video_id'):
                liste.append(d)
    return liste


def karte(d, n, pre):
    titel = esc(d['titel'])
    gast = d.get('gast', '')
    rolle = d.get('rolle', '')
    name = esc(gast)
    if d.get('website'):
        name = f'<a href="{esc(d["website"])}" target="_blank" rel="noopener">{name}</a>'
    gast_zeile = name + (f' · {esc(rolle)}' if rolle else '')
    yt = f'https://www.youtube.com/watch?v={esc(d["video_id"])}'
    if d.get('folge_slug') and d.get('folge_nummer'):
        folge = (f'<a class="impuls-btn impuls-btn--gestrichelt" href="{pre}folgen/{esc(d["folge_slug"])}/">'
                 f'Zur ganzen Folge</a>')
    else:
        hinweis = esc(d.get('folge_hinweis', 'Folge folgt'))
        folge = f'<span class="impuls-btn impuls-btn--aus" aria-disabled="true">{hinweis}</span>'
    cover = ''
    if d.get('cover'):
        cover = f'<img class="impuls-cover" src="{pre}{esc(d["cover"])}" alt="" width="640" height="360" loading="lazy">'
    klasse = 'impuls-note' + (' impuls-note--pink' if n % 3 == 1 else '')
    return f'''    <li class="{klasse}">
      <span class="impuls-tape" aria-hidden="true"></span>
      <div class="impuls-video" data-impuls-video="{esc(d["video_id"])}" data-title="{titel}">
        {cover}
        <button type="button" class="impuls-play" data-impuls-load aria-label="Video „{titel}“ laden und abspielen">
          <span class="kreis" aria-hidden="true"></span>
          <span class="hinweis">Video laden · Daten werden erst dann an YouTube übertragen</span>
        </button>
      </div>
      <h2 class="impuls-t">{titel}</h2>
      <p class="impuls-g">{gast_zeile}</p>
      <p class="impuls-lern">„{esc(d.get("learning", ""))}“</p>
      <div class="impuls-btns">
        <a class="impuls-btn" href="{yt}" target="_blank" rel="noopener">Zum Impuls auf YouTube</a>
        {folge}
      </div>
    </li>'''


def teaser_html(pre=''):
    """Teaser für die Startseite. Leer, solange kein Impuls freigegeben ist."""
    liste = laden()
    if not liste:
        return ''
    punkte = ''.join(
        f'<li><a href="{pre}impulse/"><span class="impuls-t">{esc(d["titel"])}</span>'
        f'<span class="impuls-g">mit {esc(d.get("gast", ""))}</span></a></li>' for d in liste)
    return f'''<section class="section impuls-teaser" aria-labelledby="impulse-h">
  <p class="kicker">Impulse</p>
  <h2 id="impulse-h" class="section-title">Kurze Botschaften unserer Gäste</h2>
  <ul class="impuls-liste">{punkte}</ul>
  <a class="btn" href="{pre}impulse/">Alle Impulse</a>
</section>'''


def uebersicht(site, liste):
    pre = '../'
    if liste:
        karten = '\n'.join(karte(d, n, pre) for n, d in enumerate(liste))
        inhalt_liste = f'<ul class="impuls-wall">\n{karten}\n</ul>'
    else:
        inhalt_liste = '<p>Noch keine Impulse veröffentlicht.</p>'
    inhalt = f'''
<main id="inhalt">
<div class="impuls-wrap">
  <h1 class="impuls-h1">Kurz gedacht.</h1>
  <p class="impuls-sub">Impulse to go</p>
  <p class="impuls-intro">Gedanken unserer Gäste, die du sofort mitnehmen kannst.</p>
  {inhalt_liste}
</div>
</main>

'''
    doc = (head('Impulse – VUCA Blaster', pre, f'{BASE_URL}impulse/', FONTS + STIL) + header(pre) + inhalt
           + footer(pre) + SKRIPT + '</body>\n</html>\n')
    (site / 'impulse' / 'index.html').write_text(doc, encoding='utf-8')


def seiten(site):
    """Erzeugt docs/impulse/ neu. Nicht mehr freigegebene Impulse verschwinden dabei."""
    ziel = site / 'impulse'
    if ziel.exists():
        shutil.rmtree(ziel)
    ziel.mkdir(parents=True)
    uebersicht(site, laden())


def urls():
    return ['impulse/']
