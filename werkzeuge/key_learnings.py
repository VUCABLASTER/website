"""Key Learnings für Folgen ohne Learnings, automatisch aus dem Transkript (GitHub Models, läuft im Workflow).

  python3 werkzeuge/key_learnings.py            # alle Folgen mit Transkript und leeren key_learnings
  python3 werkzeuge/key_learnings.py --nr 63    # nur diese Folge
  python3 werkzeuge/key_learnings.py --trocken  # nichts schreiben, nur anzeigen

Der Zugang kommt vom GitHub-Token des Workflows (Berechtigung „models: read“), es ist kein eigener Schlüssel nötig.
Regeln wie bei der Handarbeit: genau 3 sachliche Learnings, je höchstens 15 Wörter, nur aus dem Transkript;
lässt sich das nicht sicher sagen, bleibt das Feld leer. Gefüllte Folgen werden nie überschrieben. Der Eintrag
bleibt „geprueft: false“, bei Fehlern passiert nichts (der Workflow läuft weiter)."""
import argparse, json, os, re, sys, time, urllib.error, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from layout import REPO
import transkripte

URL = 'https://models.github.ai/inference/chat/completions'
MODELL = os.environ.get('KL_MODELL', 'openai/gpt-4.1')
BLOCK = 2500  # Wörter pro Anfrage (Eingabelimits der kostenlosen Stufe)

REGELN = ('Du arbeitest für den deutschsprachigen Podcast „VUCA Blaster“ (New Work, Führung, Change). '
          'Das Transkript ist maschinell erstellt, Namen und Fachbegriffe können falsch geschrieben sein; '
          'verwende nur Begriffe, die du sicher erkennst. Schreibe sachlich, prägnant und ohne Werbesprache. '
          'Erfinde nichts, was nicht im Text steht.')


def frage(nutzer, versuche=3):
    body = json.dumps({'model': MODELL, 'temperature': 0.2, 'max_tokens': 900,
                       'messages': [{'role': 'system', 'content': REGELN}, {'role': 'user', 'content': nutzer}]}).encode()
    for i in range(versuche):
        req = urllib.request.Request(URL, body, {'Authorization': f'Bearer {os.environ["GITHUB_TOKEN"]}',
                                                'Content-Type': 'application/json', 'Accept': 'application/vnd.github+json'})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)['choices'][0]['message']['content'].strip()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and i < versuche - 1:
                time.sleep(20 * (i + 1))
                continue
            raise


def learnings(nr, titel, gast):
    woerter = ' '.join(t for _, t in transkripte.lesen(nr)).split()
    teile = [' '.join(woerter[i:i + BLOCK]) for i in range(0, len(woerter), BLOCK)]
    notizen = []
    for k, teil in enumerate(teile, 1):
        notizen.append(frage(f'Folge: {titel}. Gast: {gast or "unbekannt"}. Teil {k} von {len(teile)} des Transkripts.\n'
                             'Nenne die 3 wichtigsten inhaltlichen Aussagen oder Erkenntnisse dieses Teils als kurze Stichpunkte.\n\n' + teil))
    fassung = '\n\n'.join(notizen)
    antwort = frage(f'Folge: {titel}. Gast: {gast or "unbekannt"}.\nHier sind Stichpunkte aus allen Teilen der Folge:\n\n{fassung}\n\n'
                    'Wähle daraus genau 3 Key Learnings für Hörerinnen und Hörer. Jedes hat höchstens 15 Wörter, ist ein ganzer Satz '
                    'mit sachlicher Aussage und hat einen Lernwert. Antworte nur mit einer JSON-Liste aus 3 Strings, z. B. ["…","…","…"]. '
                    'Lassen sich keine 3 sicher bestimmen, antworte mit null.')
    m = re.search(r'\[.*\]', antwort, re.S)
    if not m:
        return None
    try:
        liste = [str(x).strip() for x in json.loads(m.group(0))]
    except ValueError:
        return None
    if len(liste) != 3 or any(not x or len(x.split()) > 16 for x in liste):
        return None
    return liste


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--nr', type=int)
    ap.add_argument('--trocken', action='store_true')
    a = ap.parse_args()
    if 'GITHUB_TOKEN' not in os.environ:
        sys.exit('GITHUB_TOKEN fehlt (läuft nur im Workflow).')
    for p in sorted((REPO / 'inhalte' / 'folgen').glob('[0-9][0-9][0-9].json')):
        nr = int(p.stem)
        if a.nr and nr != a.nr:
            continue
        info = json.loads(p.read_text(encoding='utf-8'))
        if info.get('key_learnings') or info.get('geprueft') or not transkripte.pfad(nr).exists():
            continue
        try:
            liste = learnings(nr, info.get('titel', ''), info.get('gast', ''))
        except Exception as e:  # nie den Workflow stoppen
            print(f'#{nr}: Key Learnings nicht erzeugt ({e})')
            continue
        if not liste:
            print(f'#{nr}: keine 3 sicheren Learnings, Feld bleibt leer.')
            continue
        print(f'#{nr}: ' + ' | '.join(liste))
        if not a.trocken:
            info['key_learnings'] = liste
            hinweis = info.get('hinweis', '')
            if hinweis.startswith('Automatischer Entwurf'):
                info['hinweis'] = hinweis.replace('Key Learnings', 'Key Learnings (automatisch aus dem Transkript erzeugt, bitte gegenlesen)', 1)
            p.write_text(json.dumps(info, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
