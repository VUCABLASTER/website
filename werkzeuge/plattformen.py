"""Links zu den einzelnen Folgen auf allen Plattformen. Einmal gefundene Links werden in daten/plattform-links.json
gespeichert und gehen nicht mehr verloren.

Quellen, in dieser Reihenfolge:
  1. Feld in inhalte/folgen/NNN.json (link_spotify, link_amazon, link_deezer, link_apple) – von Hand, gewinnt immer
  2. Apple Podcasts: öffentliche Lookup-API (automatisch, im Feed-Import)
     Deezer: öffentliche API (automatisch)
     Spotify: Web API, wenn SPOTIFY_CLIENT_ID/SECRET gesetzt sind (automatisch)
  3. daten/plattform-links.json: einmalig ausgelesene Links (Spotify, Amazon Music)
Fehlt ein Folgen-Link, zeigt der Button auf die Podcast-Seite der Plattform.
"""
import base64, html, json, os, re, sys, unicodedata, urllib.request

from layout import REPO

DATEN = REPO / 'daten'
esc = lambda s: html.escape(s or '', quote=True)

SHOWS = {
    'spotify': 'https://open.spotify.com/show/3OQW0akZgxBxK4AWFQSKtf',
    'apple': 'https://podcasts.apple.com/de/podcast/vuca-blaster/id1541461336',
    'deezer': 'https://www.deezer.com/show/2000202',
    'amazon': 'https://music.amazon.de/podcasts/3eb46224-be51-446b-a8b1-cc0ab2cd83b0/vuca-blaster',
}
NAMEN = {'spotify': 'Spotify', 'apple': 'Apple Podcasts', 'deezer': 'Deezer', 'amazon': 'Amazon Music'}
REIHENFOLGE = ['spotify', 'apple', 'deezer', 'amazon']
SPOTIFY_SHOW_ID = '3OQW0akZgxBxK4AWFQSKtf'
DEEZER_SHOW_ID = '2000202'

ICONS = {
    'apple': ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="1" y="1" width="22" height="22" rx="6" fill="currentColor"/>'
              '<circle cx="12" cy="10" r="2.3" fill="#fff"/><path d="M12 13.4v5.2" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>'
              '<path d="M7.7 14.3a5.6 5.6 0 1 1 8.6 0" stroke="#fff" stroke-width="1.7" fill="none" stroke-linecap="round"/></svg>'),
    'spotify': ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="11" fill="currentColor"/>'
                '<path d="M6.4 9.3c3.7-1.1 8-.8 11.2 1.1M7.1 12.5c3-.8 6.4-.5 9 1M7.8 15.6c2.4-.6 4.8-.4 6.9.8" stroke="#fff" stroke-width="1.8" fill="none" stroke-linecap="round"/></svg>'),
    'deezer': ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="1" y="1" width="22" height="22" rx="6" fill="currentColor"/>'
               '<path d="M6 17.5h2.4M10.8 17.5h2.4M15.6 17.5h2.4M10.8 14.5h2.4M15.6 14.5h2.4M15.6 11.5h2.4M15.6 8.5h2.4" stroke="#fff" stroke-width="2" stroke-linecap="round"/></svg>'),
    'amazon': ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="1" y="1" width="22" height="22" rx="6" fill="currentColor"/>'
               '<path d="M9 7.5v6.2M9 13.7a1.8 1.8 0 1 1-1.8-1.8M9 7.5l6.5-1.2v6.1M15.5 12.4a1.8 1.8 0 1 1-1.8-1.8" stroke="#fff" stroke-width="1.7" fill="none" stroke-linecap="round"/>'
               '<path d="M6 17.2c3.8 2 8.2 2 12 0M16.3 16.4l1.8.8-.6 1.8" stroke="#fff" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'),
}


def schluessel(s):
    s = unicodedata.normalize('NFD', (s or '').lower())
    return re.sub(r'[^a-z0-9]', '', ''.join(c for c in s if unicodedata.category(c) != 'Mn'))


def _json(url, headers=None):
    req = urllib.request.Request(url, headers=dict({'User-Agent': 'vucablaster.de-build'}, **(headers or {})))
    return json.loads(urllib.request.urlopen(req, timeout=40).read())


def _deezer(offline):
    cache = DATEN / 'deezer.json'
    links = json.loads(cache.read_text()) if cache.exists() else {}
    if not offline:
        try:
            neu, url = {}, f'https://api.deezer.com/podcast/{DEEZER_SHOW_ID}/episodes?limit=100'
            while url:
                d = _json(url)
                for ep in d.get('data', []):
                    neu[schluessel(ep['title'])] = f'https://www.deezer.com/episode/{ep["id"]}'
                url = d.get('next')
            if neu:
                links = neu
                cache.write_text(json.dumps(links, indent=1, sort_keys=True) + '\n')
        except Exception as e:
            print(f'Hinweis: Deezer nicht erreichbar ({e}), nutze Ersatzkopie.', file=sys.stderr)
    return links


def _spotify_api(offline):
    cid, sec = os.environ.get('SPOTIFY_CLIENT_ID'), os.environ.get('SPOTIFY_CLIENT_SECRET')
    if not (cid and sec) or offline:
        return {}
    try:
        auth = base64.b64encode(f'{cid}:{sec}'.encode()).decode()
        req = urllib.request.Request('https://accounts.spotify.com/api/token', data=b'grant_type=client_credentials',
                                     headers={'Authorization': f'Basic {auth}', 'Content-Type': 'application/x-www-form-urlencoded'})
        token = json.loads(urllib.request.urlopen(req, timeout=30).read())['access_token']
        neu, url = {}, f'https://api.spotify.com/v1/shows/{SPOTIFY_SHOW_ID}/episodes?market=DE&limit=50'
        while url:
            d = _json(url, {'Authorization': f'Bearer {token}'})
            for ep in d.get('items') or []:
                if ep:
                    neu[schluessel(ep['name'])] = ep['external_urls']['spotify']
            url = d.get('next')
        return neu
    except Exception as e:
        print(f'Hinweis: Spotify-API nicht erreichbar ({e}).', file=sys.stderr)
        return {}


def links_setzen(folgen, infos, offline=False):
    """Setzt f['links'] = {plattform: url} für jede Folge. Leerer Wert = kein Folgen-Link bekannt."""
    datei = DATEN / 'plattform-links.json'
    fest = json.loads(datei.read_text(encoding='utf-8')) if datei.exists() else {}
    deezer = _deezer(offline)
    spotify_api = _spotify_api(offline)
    geaendert = False
    for f in folgen:
        nr, key, info = str(f['nr']), schluessel(f['titel_roh']), infos[f['nr']]
        sp = spotify_api.get(key) or fest.get('spotify', {}).get(nr, '')
        api = {'spotify': spotify_api.get(key, ''), 'apple': f.get('apple', ''), 'deezer': deezer.get(key, '')}
        # Einmal gefundene Links bleiben gespeichert, auch wenn eine Schnittstelle sie später kurz nicht liefert.
        for p, wert in api.items():
            if wert and fest.setdefault(p, {}).get(nr) != wert:
                fest[p][nr] = wert
                geaendert = True
        f['links'] = {
            'spotify': info.get('link_spotify') or sp,
            'apple': info.get('link_apple') or api['apple'] or fest.get('apple', {}).get(nr, ''),
            'deezer': info.get('link_deezer') or api['deezer'] or fest.get('deezer', {}).get(nr, ''),
            'amazon': info.get('link_amazon') or fest.get('amazon', {}).get(nr, ''),
        }
    if geaendert:
        for p in ('spotify', 'apple', 'deezer', 'amazon'):
            if p in fest:
                fest[p] = dict(sorted(fest[p].items(), key=lambda x: int(x[0])))
        datei.write_text(json.dumps(fest, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    fehlend = {p: [f['nr'] for f in folgen if not f['links'][p]] for p in REIHENFOLGE}
    for p, nrs in fehlend.items():
        if nrs:
            print(f'Hinweis: {NAMEN[p]} ohne Folgen-Link bei #{", #".join(map(str, sorted(nrs, reverse=True)))} – Button zeigt auf die Podcast-Seite.', file=sys.stderr)
    return fehlend


def url(f, p):
    return f['links'].get(p) or SHOWS[p]


def buttons(f, nur=None):
    """Text-Buttons (Startseite, Folgenseite)."""
    return ''.join(f'<a class="btn" href="{esc(url(f, p))}">{NAMEN[p]}</a>' for p in (nur or REIHENFOLGE))


def icons(f):
    """Logo-Links (Archiv)."""
    teile = []
    for p in REIHENFOLGE:
        label = f'#{f["nr"]} auf {NAMEN[p]} hören' if f['links'].get(p) else f'VUCA Blaster auf {NAMEN[p]}'
        teile.append(f'<a class="pf-link" href="{esc(url(f, p))}" aria-label="{label}" title="{NAMEN[p]}">{ICONS[p]}</a>')
    return ''.join(teile)
