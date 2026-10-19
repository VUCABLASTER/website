"""Key Learnings automatisch aus dem Transkript – mit einem freien Sprachmodell, das im GitHub-Workflow selbst läuft
(llama.cpp + Qwen2.5-14B-Instruct, Apache-2.0-Lizenz). Kein Konto, kein Schlüssel, keine Kosten, kein eigener Rechner.

Im Workflow (Job „learnings“):
  python3 werkzeuge/key_learnings.py --erzeugen --nr 64 --vtt inhalte/transkripte/064.vtt --ausgabe kl/064.json
  (erwartet einen laufenden llama-server unter KL_URL, Standard http://127.0.0.1:8080)
Im Job „bauen“:
  python3 werkzeuge/key_learnings.py --uebernehmen kl/

Regeln wie bei der Handarbeit: genau 3 sachliche Learnings, je höchstens 15 Wörter, nur aus dem Transkript. Lässt sich
das nicht sicher sagen, bleibt das Feld leer. Gefüllte oder geprüfte Folgen werden nie überschrieben. Bei Fehlern
passiert nichts (der Workflow läuft weiter)."""
import argparse, json, os, re, sys, time, urllib.error, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from layout import REPO

URL = os.environ.get('KL_URL', 'http://127.0.0.1:8080').rstrip('/') + '/v1/chat/completions'
BLOCK = 1800  # Wörter pro Anfrage, passt mit Antwort in 8.192 Token Kontext

REGELN = ('Du arbeitest für den deutschsprachigen Podcast „VUCA Blaster“ über New Work, Führung, Mut und Veränderung. '
          'Das Transkript ist maschinell erstellt; Namen und Fachbegriffe können falsch geschrieben sein, verwende nur '
          'Begriffe, die du sicher erkennst. Schreibe auf Deutsch, sachlich, prägnant, ohne Werbesprache. '
          'Erfinde nichts, was nicht im Text steht.')


def frage(nutzer, json_antwort=False, versuche=2):
    daten = {'messages': [{'role': 'system', 'content': REGELN}, {'role': 'user', 'content': nutzer}],
             'temperature': 0.2, 'max_tokens': 700}
    if json_antwort:
        daten['response_format'] = {'type': 'json_object'}
    body = json.dumps(daten).encode()
    for i in range(versuche):
        try:
            req = urllib.request.Request(URL, body, {'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=1800) as r:
                return json.load(r)['choices'][0]['message']['content'].strip()
        except (urllib.error.URLError, KeyError, ValueError) as e:
            if i == versuche - 1:
                raise RuntimeError(f'Sprachmodell antwortet nicht ({e})')
            time.sleep(10)


def text_aus_vtt(pfad):
    zeilen, im_text = [], False
    for z in Path(pfad).read_text(encoding='utf-8').splitlines():
        z = z.strip()
        if '-->' in z:
            im_text = True  # Kopf (WEBVTT, NOTE mit Titel und Hinweis) steht vor dem ersten Abschnitt
            continue
        if im_text and z and not z.isdigit():
            zeilen.append(re.sub(r'<[^>]+>', '', z))
    return ' '.join(zeilen)


def pruefen(liste):
    liste = [re.sub(r'\s+', ' ', str(x)).strip().strip('"„“') for x in liste if str(x).strip()]
    if len(liste) != 3 or any(len(x.split()) > 16 or len(x.split()) < 5 for x in liste):
        return None
    return [x if x.endswith(('.', '!', '?')) else x + '.' for x in liste]


# Vorbilder aus handgeschriebenen Learnings anderer Folgen (Stil: konkret, sachlich, ganzer Satz)
BEISPIELE = [
    'Fehlerkultur braucht psychologische Sicherheit: Fehler zugeben ohne negative Konsequenzen.',
    'Einstieg gelingt mit zehn Minuten Fehlerrunde in bestehenden Meetings oder Retros.',
    'Erst klären, dann lösen: Verstehen kommt vor der Lösung, etwa mit Restorative Circles.',
    'Konflikte entstehen oft aus verschiedenen Strategien für dasselbe Bedürfnis.',
    "Innovator's Dilemma: Erfolgreiche Unternehmen kannibalisieren ihr Kerngeschäft ungern, siehe Nokia und Kodak.",
    'In die Manöverkritik gehören auch Gefühle; dafür braucht es psychologische Sicherheit.',
]


def learnings(titel, gast, text):
    kopf = f'Folge: {titel}. Gast: {gast or "unbekannt"}.'
    woerter = text.split()
    teile = [' '.join(woerter[i:i + BLOCK]) for i in range(0, len(woerter), BLOCK)]
    notizen = []
    for k, teil in enumerate(teile, 1):
        t0 = time.time()
        notizen.append(frage(f'{kopf} Teil {k} von {len(teile)} des Transkripts.\n'
                             'Fasse die wichtigsten inhaltlichen Aussagen dieses Teils in 3 bis 5 Stichpunkten auf Deutsch '
                             'zusammen. Schreib zu jedem Stichpunkt ein kurzes wörtliches Zitat aus dem Text als Beleg in Klammern. '
                             'Lass Begrüßung, Smalltalk und Werbung weg.\n\n' + teil))
        print(f'  Teil {k}/{len(teile)} in {time.time() - t0:.0f} s', flush=True)
    stichpunkte = '\n\n'.join(notizen)
    # 1) Kandidaten mit Beleg sammeln
    t0 = time.time()
    kandidaten = frage(f'{kopf}\nStichpunkte mit Belegen aus der ganzen Folge:\n\n{stichpunkte}\n\n'
                       'Formuliere 6 verschiedene Kandidaten für Key Learnings dieser Folge. Jeder Kandidat ist ein ganzer '
                       'deutscher Satz mit 8 bis 15 Wörtern, enthält eine konkrete Erkenntnis oder Empfehlung und gibt den '
                       'Inhalt sinngemäß richtig wieder. Antworte als JSON: {"kandidaten": [{"satz": "…", "beleg": "…"}]}.',
                       json_antwort=True)
    print(f'  Kandidaten in {time.time() - t0:.0f} s', flush=True)
    # 2) Die 3 besten wählen, gegen die Belege prüfen und im Stil der Vorbilder schärfen
    vorbilder = '\n'.join(f'- {x}' for x in BEISPIELE)
    auftrag = (f'{kopf}\nKandidaten mit Belegen:\n{kandidaten}\n\n'
               f'So sehen gute Key Learnings aus (aus anderen Folgen, nur als Stilvorbild):\n{vorbilder}\n\n'
               'Wähle die 3 Kandidaten mit dem größten Lernwert für Hörerinnen und Hörer, die sich inhaltlich nicht '
               'wiederholen. Prüfe jeden gegen seinen Beleg: Der Sinn darf nicht verdreht sein. Schärfe die Formulierung im '
               'Stil der Vorbilder: konkret statt allgemein, ganzer Satz, 8 bis 15 Wörter. '
               'Antworte nur als JSON: {"learnings": ["…", "…", "…"]}. '
               'Lassen sich keine 3 sicher bestimmen, antworte {"learnings": null}.')
    for versuch in (1, 2):  # ein zweiter Versuch, wenn Form oder Länge nicht passen
        antwort = frage(auftrag, json_antwort=True)
        liste = _lesen(antwort)
        if liste:
            return liste
        print('  Antwort verworfen:', antwort[:300].replace('\n', ' '), flush=True)
    return None


def _lesen(antwort):
    try:
        roh = json.loads(re.search(r'\{.*\}', antwort, re.S).group(0)).get('learnings')
    except (AttributeError, ValueError):
        return None
    return pruefen(roh) if isinstance(roh, list) else None


def erzeugen(nr, vtt, ausgabe):
    info_pfad = REPO / 'inhalte' / 'folgen' / f'{nr:03d}.json'
    info = json.loads(info_pfad.read_text(encoding='utf-8')) if info_pfad.exists() else {}
    titel = info.get('titel') or f'#{nr}'
    if not Path(vtt).exists():
        print(f'#{nr}: kein Transkript unter {vtt}')
        return
    t0 = time.time()
    try:
        liste = learnings(titel, info.get('gast', ''), text_aus_vtt(vtt))
    except Exception as e:  # nie den Workflow stoppen
        print(f'#{nr}: Key Learnings nicht erzeugt ({e})')
        return
    print(f'#{nr}: {time.time() - t0:.0f} s')
    if not liste:
        print(f'#{nr}: keine 3 sicheren Learnings, Feld bleibt leer.')
        return
    for x in liste:
        print('  -', x)
    Path(ausgabe).parent.mkdir(parents=True, exist_ok=True)
    Path(ausgabe).write_text(json.dumps({'nummer': nr, 'key_learnings': liste}, ensure_ascii=False, indent=2), encoding='utf-8')


MAX_VERSUCHE = 3  # so oft wird es pro Folge automatisch versucht, danach bleibt das Feld leer (von Hand nachtragen)


def offene():
    """Folgen mit Transkript, aber ohne Key Learnings, ungeprüft und mit weniger als MAX_VERSUCHE Versuchen.
    Der Workflow holt sie bei jedem Lauf automatisch nach, falls ein früherer Versuch nichts geliefert hat."""
    nrs = []
    for p in sorted((REPO / 'inhalte' / 'folgen').glob('[0-9][0-9][0-9].json')):
        info = json.loads(p.read_text(encoding='utf-8'))
        nr = int(p.stem)
        if (not info.get('key_learnings') and not info.get('geprueft') and info.get('kl_versuche', 0) < MAX_VERSUCHE
                and (REPO / 'inhalte' / 'transkripte' / f'{nr:03d}.vtt').exists()):
            nrs.append(nr)
    return nrs


def versuche_zaehlen(nrs):
    """Nach einem Lauf: Folgen, die versucht wurden und weiterhin leer sind, bekommen einen Versuch mehr."""
    for nr in nrs:
        p = REPO / 'inhalte' / 'folgen' / f'{nr:03d}.json'
        if not p.exists():
            continue
        info = json.loads(p.read_text(encoding='utf-8'))
        if not info.get('key_learnings') and not info.get('geprueft'):
            info['kl_versuche'] = info.get('kl_versuche', 0) + 1
            p.write_text(json.dumps(info, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            print(f'#{nr}: noch keine Key Learnings, Versuch {info["kl_versuche"]} von {MAX_VERSUCHE}.')


def uebernehmen(ordner):
    for p in sorted(Path(ordner).glob('*.json')) if Path(ordner).exists() else []:
        neu = json.loads(p.read_text(encoding='utf-8'))
        nr = int(neu['nummer'])
        ziel = REPO / 'inhalte' / 'folgen' / f'{nr:03d}.json'
        if not ziel.exists():
            continue
        info = json.loads(ziel.read_text(encoding='utf-8'))
        if info.get('key_learnings') or info.get('geprueft'):
            print(f'#{nr}: hat schon Key Learnings, nichts geändert.')
            continue
        info['key_learnings'] = neu['key_learnings']
        hinweis = info.get('hinweis', '')
        if hinweis.startswith('Automatischer Entwurf') and 'automatisch aus dem Transkript' not in hinweis:
            info['hinweis'] = hinweis.replace('Key Learnings', 'Key Learnings (automatisch aus dem Transkript erzeugt, bitte gegenlesen)', 1)
        ziel.write_text(json.dumps(info, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'#{nr}: Key Learnings übernommen.')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--erzeugen', action='store_true')
    ap.add_argument('--nr', type=int)
    ap.add_argument('--vtt')
    ap.add_argument('--ausgabe')
    ap.add_argument('--uebernehmen')
    ap.add_argument('--offene', action='store_true')
    ap.add_argument('--versucht', default='')
    a = ap.parse_args()
    if a.offene:
        print(json.dumps(offene()))
    elif a.erzeugen and a.nr:
        erzeugen(a.nr, a.vtt or REPO / 'inhalte' / 'transkripte' / f'{a.nr:03d}.vtt', a.ausgabe or f'kl/{a.nr:03d}.json')
    elif a.uebernehmen:
        uebernehmen(a.uebernehmen)
        versuche_zaehlen([int(x) for x in re.findall(r'\d+', a.versucht)])
    else:
        ap.error('--erzeugen --nr N oder --uebernehmen ORDNER angeben')


if __name__ == '__main__':
    main()
