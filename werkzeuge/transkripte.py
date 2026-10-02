"""Transkripte: lesen (WebVTT aus inhalte/transkripte/NNN.vtt), als HTML ausgeben, Suchindex schreiben.

Die Transkripte werden automatisch mit Whisper aus den MP3-Dateien erzeugt (werkzeuge/transkribieren.py,
läuft im GitHub-Workflow). Korrekturen: die .vtt-Datei direkt bearbeiten, nur den Text, nicht die Zeitmarken.
"""
import html, json, re, unicodedata

from layout import REPO

ORDNER = REPO / 'inhalte' / 'transkripte'
ZEIT = re.compile(r'(?:(\d+):)?(\d{2}):(\d{2})[.,](\d{3})\s*-->')


def pfad(nr):
    return ORDNER / f'{nr:03d}.vtt'


def lesen(nr):
    """Liste von (startsekunde, text). Leer, wenn es kein Transkript gibt."""
    p = pfad(nr)
    if not p.exists():
        return []
    segmente, start = [], None
    for zeile in p.read_text(encoding='utf-8').splitlines():
        m = ZEIT.match(zeile.strip())
        if m:
            h, mi, s = int(m.group(1) or 0), int(m.group(2)), int(m.group(3))
            start = h * 3600 + mi * 60 + s
        elif zeile.strip() and start is not None and not zeile.startswith(('WEBVTT', 'NOTE')):
            text = re.sub(r'<[^>]+>', '', zeile).strip()
            if text:
                segmente.append((start, text))
    return segmente


def zeit(sek):
    h, rest = divmod(sek, 3600)
    m, s = divmod(rest, 60)
    return f'{h}:{m:02d}:{s:02d}' if h else f'{m}:{s:02d}'


def absaetze(segmente, dauer=75):
    """Fasst Segmente zu Absätzen von etwa `dauer` Sekunden zusammen, getrennt an Satzenden."""
    out, akt, beginn = [], [], None
    for start, text in segmente:
        if beginn is None:
            beginn = start
        akt.append(text)
        if start - beginn >= dauer and re.search(r'[.!?…]["“»]?$', text):
            out.append((beginn, ' '.join(akt)))
            akt, beginn = [], None
    if akt:
        out.append((beginn, ' '.join(akt)))
    return out


def als_html(nr):
    segmente = lesen(nr)
    if not segmente:
        return ''
    teile = ''.join(f'<p><span class="ts">{zeit(b)}</span> {html.escape(t, quote=False)}</p>' for b, t in absaetze(segmente))
    return f'''<details id="transkript" class="transcript">
    <summary>Transkript lesen</summary>
    <p class="transcript-note">Automatisch erstellt mit Spracherkennung (Whisper) aus der Audiodatei. Kann Hörfehler enthalten, besonders bei Namen und Fachbegriffen.</p>
    <div class="transcript-text">{teile}</div>
  </details>
  <script>if (location.hash === '#transkript') document.getElementById('transkript').open = true;</script>'''


def normal(s):
    s = unicodedata.normalize('NFD', s.lower())
    return re.sub(r'\s+', ' ', ''.join(c for c in s if unicodedata.category(c) != 'Mn'))


def suchindex(site, folgen):
    """folgen/transkripte.json: {nr: normalisierter Text} – lädt das Archiv erst, wenn jemand sucht."""
    index = {}
    for f in folgen:
        seg = lesen(f['nr'])
        if seg:
            index[str(f['nr'])] = normal(' '.join(t for _, t in seg))
    ziel = site / 'folgen' / 'transkripte.json'
    if index:
        ziel.write_text(json.dumps(index, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    elif ziel.exists():
        ziel.unlink()
    return len(index)


def aus_feed(folgen, offline=False):
    """Übernimmt Transkripte, die podcaster.de im Feed mitliefert (<podcast:transcript>, VTT oder SRT).
    Vorhandene Dateien werden nicht überschrieben. Whisper transkribiert nur Folgen ohne Transkript."""
    import sys, urllib.request
    if offline:
        return
    for f in folgen:
        quelle = f.get('feed_transkript')
        if not quelle or pfad(f['nr']).exists():
            continue
        url, typ = quelle
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'vucablaster.de-build'})
            text = urllib.request.urlopen(req, timeout=60).read().decode('utf-8-sig')
            if 'vtt' not in typ:  # SRT → WebVTT
                text = 'WEBVTT\n\n' + re.sub(r'(\d{2}:\d{2}:\d{2}),(\d{3})', r'\1.\2', text)
            kopf = f'NOTE\nTranskript von podcaster.de aus dem Feed übernommen ({url}).\n\n'
            ORDNER.mkdir(parents=True, exist_ok=True)
            pfad(f['nr']).write_text(text.replace('WEBVTT', 'WEBVTT\n\n' + kopf, 1), encoding='utf-8')
            print(f'Transkript für #{f["nr"]} aus dem Feed übernommen.', file=sys.stderr)
        except Exception as e:
            print(f'Hinweis: Feed-Transkript für #{f["nr"]} nicht ladbar ({e}).', file=sys.stderr)
