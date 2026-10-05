"""Holt die Links zu einzelnen Folgen bei Spotify und Amazon Music aus deren öffentlichen Podcast-Seiten.

Beide Plattformen haben keine offene Schnittstelle ohne Konto, die Seiten sind aber öffentlich lesbar. Ein
Browser (Chrome, ohne Fenster) öffnet die Podcast-Seite, liest die Folgenliste und ordnet jede Folge über die
Nummer „#NN“ im Titel zu. Gespeichert wird nur bei eindeutiger Zuordnung; fehlt etwas, bleibt der Link zur
Podcast-Seite und der Build meldet es. Es werden nur fehlende Links ergänzt, vorhandene nie überschrieben.

  python3 werkzeuge/plattform_links_holen.py            # nur Folgen ohne Link
  python3 werkzeuge/plattform_links_holen.py --alle     # alle Folgen neu lesen und mit der Datei vergleichen

Braucht: pip install playwright und Google Chrome (auf GitHub-Rechnern vorinstalliert).
"""
import argparse, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from layout import REPO
import build

DATEI = REPO / 'daten' / 'plattform-links.json'
SPOTIFY_SHOW = 'https://open.spotify.com/show/3OQW0akZgxBxK4AWFQSKtf'
AMAZON_SHOW = 'https://music.amazon.de/podcasts/3eb46224-be51-446b-a8b1-cc0ab2cd83b0/vuca-blaster'
NR = re.compile(r'#\s*(\d+)')


def nummer(titel):
    m = NR.search(titel or '')
    return int(m.group(1)) if m else None


def eindeutig(paare, kennung):
    """paare: [(nummer, url)] → {nummer: url}. Eine Nummer mit zwei verschiedenen Links wird verworfen."""
    out, strittig = {}, set()
    for nr, url in paare:
        if nr is None:
            continue
        if nr in out and out[nr] != url:
            strittig.add(nr)
        out[nr] = url
    for nr in strittig:
        del out[nr]
        print(f'Hinweis: {kennung}: #{nr} mehrdeutig, übersprungen.', file=sys.stderr)
    return out


def spotify_lesen(page, gesucht, alle):
    page.goto(SPOTIFY_SHOW, wait_until='domcontentloaded', timeout=60000)
    page.wait_for_timeout(5000)
    try:  # Cookie-Hinweis: datensparsamste Option
        page.get_by_role('button', name=re.compile(r'alle ablehnen|reject all|decline', re.I)).first.click(timeout=3000)
    except Exception:
        pass
    gefunden = {}
    for _ in range(40):
        paare = page.eval_on_selector_all(
            'a[href*="/episode/"]',
            "els => els.map(e => [(e.textContent||'').trim(), e.href.split('?')[0]])")
        gefunden = eindeutig([(nummer(t), u) for t, u in paare], 'Spotify')
        if (not alle and gesucht <= set(gefunden)) or not gesucht:
            break
        mehr = page.get_by_role('button', name=re.compile(r'weitere folgen laden|load more|more episodes', re.I))
        if mehr.count() == 0:
            break
        try:
            mehr.first.scroll_into_view_if_needed(timeout=3000)
            mehr.first.click(timeout=3000)
        except Exception:
            break
        page.wait_for_timeout(1500)
    return gefunden


AMAZON_JS = """
() => {
  const out = [];
  const walk = root => root.querySelectorAll('*').forEach(e => {
    const h = e.getAttribute && (e.getAttribute('primary-href') || e.getAttribute('href'));
    const t = e.getAttribute && (e.getAttribute('primary-text') || '');
    if (h && t && /\\/episodes\\//.test(h)) out.push([t, h]);
    if (e.shadowRoot) walk(e.shadowRoot);
  });
  walk(document);
  return out;
}
"""


def amazon_lesen(page, gesucht, alle):
    page.goto(AMAZON_SHOW, wait_until='domcontentloaded', timeout=60000)
    page.wait_for_timeout(6000)
    gefunden = {}
    for _ in range(25):
        paare = page.evaluate(AMAZON_JS)
        kurz = lambda h: 'https://music.amazon.de' + re.search(r'(/podcasts/[0-9a-f-]{36}/episodes/[0-9a-f-]{36})', h).group(1)
        gefunden = eindeutig([(nummer(t), kurz(h)) for t, h in paare if re.search(r'/podcasts/[0-9a-f-]{36}/episodes/[0-9a-f-]{36}', h)], 'Amazon')
        if (not alle and gesucht <= set(gefunden)) or not gesucht:
            break
        page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
        page.wait_for_timeout(1200)
    return gefunden


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--alle', action='store_true', help='alle Folgen lesen und mit der Datei vergleichen (ändert nichts)')
    a = ap.parse_args()

    apple = build.apple_lesen(build.holen(build.APPLE_LOOKUP, build.DATEN / 'apple.json', False))
    folgen, _ = build.feed_lesen(build.holen(build.FEED_URL, build.DATEN / 'feed.xml', False), apple)
    nrs = {f['nr'] for f in folgen}
    daten = json.loads(DATEI.read_text(encoding='utf-8')) if DATEI.exists() else {}
    fest = {p: {int(k): v for k, v in daten.get(p, {}).items()} for p in ('spotify', 'amazon')}
    fehlt = {p: nrs - set(fest[p]) for p in fest}
    if not a.alle and not any(fehlt.values()):
        print('Spotify und Amazon: nichts zu tun, alle Folgen haben einen Link.')
        return

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('Hinweis: playwright fehlt (pip install playwright) – Spotify/Amazon-Links nicht aktualisiert.', file=sys.stderr)
        return

    gelesen = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel='chrome', headless=True)
        ctx = browser.new_context(locale='de-DE', viewport={'width': 1280, 'height': 900})
        for plattform, funktion in (('spotify', spotify_lesen), ('amazon', amazon_lesen)):
            if not a.alle and not fehlt[plattform]:
                continue
            page = ctx.new_page()
            try:
                gelesen[plattform] = funktion(page, set(fehlt[plattform]), a.alle)
            except Exception as e:
                print(f'Hinweis: {plattform} nicht lesbar ({type(e).__name__}: {str(e)[:120]}) – Link bleibt die Podcast-Seite.', file=sys.stderr)
            page.close()
        browser.close()

    if a.alle:  # Vergleichsmodus: ändert nichts
        for p, neu in gelesen.items():
            gleich = sum(1 for n, u in neu.items() if fest[p].get(n) == u)
            abweichend = sorted(n for n, u in neu.items() if n in fest[p] and fest[p][n] != u)
            nur_neu = sorted(n for n in neu if n not in fest[p])
            print(f'{p}: gelesen {len(neu)}, davon identisch mit Datei {gleich}, abweichend {abweichend}, nur neu gelesen {nur_neu}')
        return

    geaendert = False
    for p, neu in gelesen.items():
        for n in sorted(fehlt[p]):
            if n in neu:
                daten.setdefault(p, {})[str(n)] = neu[n]
                geaendert = True
                print(f'{p}: Link für #{n} ergänzt.')
        offen = sorted(fehlt[p] - set(neu))
        if offen:
            print(f'Hinweis: {p}: kein Link gefunden für #{", #".join(map(str, offen[::-1]))} (noch nicht gelistet?).', file=sys.stderr)
    if geaendert:
        daten['spotify'] = dict(sorted(daten['spotify'].items(), key=lambda x: int(x[0])))
        daten['amazon'] = dict(sorted(daten['amazon'].items(), key=lambda x: int(x[0])))
        DATEI.write_text(json.dumps(daten, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
