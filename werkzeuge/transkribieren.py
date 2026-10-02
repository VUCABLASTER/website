"""Transkribiert Folgen mit whisper.cpp (läuft im GitHub-Workflow „Website aktualisieren“).

  python3 werkzeuge/transkribieren.py --planen fehlende       # JSON-Liste der Folgen ohne Transkript
  python3 werkzeuge/transkribieren.py --planen 61,62          # bestimmte Folgen (auch wenn schon vorhanden)
  python3 werkzeuge/transkribieren.py --nr 62 --whisper PFAD --modell PFAD [--ziel ergebnis/]

Ergebnis: inhalte/transkripte/NNN.vtt (WebVTT mit Zeitmarken). Nichts wird nachbearbeitet oder ergänzt –
die Datei enthält genau das, was die Spracherkennung gehört hat.
"""
import argparse, datetime, json, re, shutil, subprocess, sys, tempfile, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from layout import REPO
import build, transkripte

# Sprache pro Folge, falls nicht Deutsch (laut Shownotes)
SPRACHE = {25: 'en'}
MODELL_NAME = 'large-v3-turbo'


def folgen_laden():
    apple = build.apple_lesen(build.holen(build.APPLE_LOOKUP, build.DATEN / 'apple.json', False))
    folgen, _ = build.feed_lesen(build.holen(build.FEED_URL, build.DATEN / 'feed.xml', False), apple)
    return folgen


def planen(auswahl):
    folgen = folgen_laden()
    nrs = [f['nr'] for f in folgen]
    if auswahl in ('', 'keine'):
        return []
    if auswahl == 'fehlende':  # ohne eigenes Transkript und ohne Transkript im Feed
        return [f['nr'] for f in folgen if not transkripte.pfad(f['nr']).exists() and not f.get('feed_transkript')]
    gewuenscht = {int(x) for x in auswahl.replace(' ', '').split(',') if x.isdigit()}
    return [n for n in nrs if n in gewuenscht]


def start_hinweis(f):
    """Kurzer, korrekt geschriebener Satz als Orientierung für Whisper (Schreibweise, Satzzeichen, Namen).
    Er steht nicht im Transkript."""
    info_pfad = REPO / 'inhalte' / 'folgen' / f'{f["nr"]:03d}.json'
    gast = json.loads(info_pfad.read_text(encoding='utf-8')).get('gast', '') if info_pfad.exists() else ''
    titel = re.sub(r'^\s*#\s*\d+\s*[-–:]?\s*', '', f['titel_roh'])
    if gast and gast.split()[-1].lower() in titel.lower():
        pos = titel.lower().rfind(' mit ')
        titel = titel[:pos].rstrip(' –-:') if pos > 0 else titel
    satz = f'Willkommen beim VUCA Blaster, dem Podcast mit Manuel Wyszynski und Sebastian Oremek. Folge {f["nr"]}: {titel}.'
    return satz + (f' Zu Gast ist {gast}.' if gast else '')


def schleifen_entfernen(vtt):
    """Entfernt Wiederholungsschleifen (bekannter Whisper-Fehler bei Musik/Stille). Es wird nur entfernt, nie
    etwas hinzugefügt; gekürzte Stellen enden mit „[…]“. Normales Stottern oder Wiederholen bleibt stehen.
      1. Wiederholt sich eine Wortfolge aus mindestens 4 Wörtern mindestens dreimal direkt hintereinander,
         bleibt nur ihr erstes Vorkommen; der Rest des Abschnitts entfällt (die Schleife läuft dort weiter).
      2. Beginnt ein Abschnitt mit dem kompletten Text des vorherigen (mindestens 6 Wörter), fällt diese
         Wiederholung weg; bleibt nichts übrig, entfällt der Abschnitt."""
    schleife = re.compile(r'(?i)\b((?:\S+\s+){3,14}?)(?:\1){2,}')
    bloecke, vorher, gekuerzt = [], '', 0
    for block in re.split(r'\n\s*\n', vtt.strip()):
        zeilen = block.split('\n')
        if not zeilen or '-->' not in zeilen[0]:
            bloecke.append(block)
            continue
        text = ' '.join(z.strip() for z in zeilen[1:]).strip()
        neu, gekuerzt_hier = text, False
        m = schleife.search(neu + ' ')
        if m:
            neu, gekuerzt_hier = (neu[:m.start()] + m.group(1)).strip(), True
        if len(vorher.split()) >= 6 and neu.startswith(vorher):
            neu, gekuerzt_hier = neu[len(vorher):].strip(), True
        if gekuerzt_hier:
            gekuerzt += 1
            if not neu:
                continue
            neu += ' […]'
        vorher = text
        bloecke.append(zeilen[0] + '\n' + neu)
    return '\n\n'.join(bloecke) + '\n', gekuerzt


def transkribieren(nr, whisper, modell, ziel, vad_modell=None):
    f = next(x for x in folgen_laden() if x['nr'] == nr)
    with tempfile.TemporaryDirectory() as tmp:
        mp3, wav, aus = Path(tmp) / 'folge.mp3', Path(tmp) / 'folge.wav', Path(tmp) / 'ergebnis'
        url = build.mp3_url(f['mp3'])
        print(f'#{nr}: lade {url}', flush=True)
        req = urllib.request.Request(url, headers={'User-Agent': 'vucablaster.de-transkription'})
        with urllib.request.urlopen(req, timeout=300) as r, open(mp3, 'wb') as out:
            shutil.copyfileobj(r, out)
        subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-i', str(mp3), '-ar', '16000', '-ac', '1', '-c:a', 'pcm_s16le', str(wav)], check=True)
        sprache = SPRACHE.get(nr, 'de')
        print(f'#{nr}: transkribiere ({sprache}) …', flush=True)
        befehl = [whisper, '-m', modell, '-l', sprache, '-t', '4', '-ovtt', '-of', str(aus), '-f', str(wav),
                  '--prompt', start_hinweis(f), '--carry-initial-prompt', '--suppress-nst']
        if vad_modell:
            befehl += ['--vad', '-vm', vad_modell]
        r = subprocess.run(befehl, stdout=subprocess.DEVNULL)
        if r.returncode != 0:
            raise SystemExit(f'#{nr}: whisper-cli beendet mit Code {r.returncode} (negativ = Signal, z. B. -4 = unbekannter Prozessorbefehl)')
        vtt, gekuerzt = schleifen_entfernen(Path(str(aus) + '.vtt').read_text(encoding='utf-8'))
        if gekuerzt:
            print(f'#{nr}: {gekuerzt} Wiederholungsschleife(n) entfernt.', flush=True)
    heute = datetime.date.today().isoformat()
    kopf = (f'WEBVTT\n\nNOTE\nVUCA Blaster #{nr}: {f["titel_roh"]}\n'
            f'Automatisch transkribiert mit whisper.cpp (Modell {MODELL_NAME}, Sprache {sprache}, VAD {"an" if vad_modell else "aus"}) am {heute}.\n'
            'Nicht nachbearbeitet. Korrekturen nur im Text, Zeitmarken bitte nicht ändern.\n')
    inhalt = kopf + vtt.split('WEBVTT', 1)[-1]
    ziel.mkdir(parents=True, exist_ok=True)
    datei = ziel / f'{nr:03d}.vtt'
    datei.write_text(inhalt, encoding='utf-8')
    print(f'#{nr}: fertig, {inhalt.count("-->")} Abschnitte → {datei}', flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--planen')
    ap.add_argument('--nr', type=int)
    ap.add_argument('--whisper', default='whisper-cli')
    ap.add_argument('--modell')
    ap.add_argument('--vad-modell')
    ap.add_argument('--ziel', default=str(transkripte.ORDNER))
    a = ap.parse_args()
    if a.planen is not None:
        print(json.dumps(planen(a.planen.strip())))
    elif a.nr:
        transkribieren(a.nr, a.whisper, a.modell, Path(a.ziel), a.vad_modell)
    else:
        ap.error('--planen oder --nr angeben')


if __name__ == '__main__':
    main()
