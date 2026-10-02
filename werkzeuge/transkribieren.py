"""Transkribiert Folgen mit whisper.cpp (läuft im GitHub-Workflow „Website aktualisieren“).

  python3 werkzeuge/transkribieren.py --planen fehlende       # JSON-Liste der Folgen ohne Transkript
  python3 werkzeuge/transkribieren.py --planen 61,62          # bestimmte Folgen (auch wenn schon vorhanden)
  python3 werkzeuge/transkribieren.py --nr 62 --whisper PFAD --modell PFAD [--ziel ergebnis/]

Ergebnis: inhalte/transkripte/NNN.vtt (WebVTT mit Zeitmarken). Nichts wird nachbearbeitet oder ergänzt –
die Datei enthält genau das, was die Spracherkennung gehört hat.
"""
import argparse, datetime, json, shutil, subprocess, sys, tempfile, urllib.request
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
    nrs = [f['nr'] for f in folgen_laden()]
    if auswahl in ('', 'keine'):
        return []
    if auswahl == 'fehlende':
        return [n for n in nrs if not transkripte.pfad(n).exists()]
    gewuenscht = {int(x) for x in auswahl.replace(' ', '').split(',') if x.isdigit()}
    return [n for n in nrs if n in gewuenscht]


def transkribieren(nr, whisper, modell, ziel):
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
        subprocess.run([whisper, '-m', modell, '-l', sprache, '-t', '4', '-ovtt', '-of', str(aus), '-f', str(wav)], check=True,
                       stdout=subprocess.DEVNULL)
        vtt = Path(str(aus) + '.vtt').read_text(encoding='utf-8')
    heute = datetime.date.today().isoformat()
    kopf = (f'WEBVTT\n\nNOTE\nVUCA Blaster #{nr}: {f["titel_roh"]}\n'
            f'Automatisch transkribiert mit whisper.cpp (Modell {MODELL_NAME}, Sprache {sprache}) am {heute}.\n'
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
    ap.add_argument('--ziel', default=str(transkripte.ORDNER))
    a = ap.parse_args()
    if a.planen is not None:
        print(json.dumps(planen(a.planen.strip())))
    elif a.nr:
        transkribieren(a.nr, a.whisper, a.modell, Path(a.ziel))
    else:
        ap.error('--planen oder --nr angeben')


if __name__ == '__main__':
    main()
