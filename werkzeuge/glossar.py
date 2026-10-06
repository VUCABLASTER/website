"""Glossar für die Transkripte: Begriffe für den Whisper-Prompt und eine Korrekturliste.

  python3 werkzeuge/glossar.py --pruefen      # zählt Treffer der Korrekturliste in allen Transkripten (ändert nichts)
  python3 werkzeuge/glossar.py --anwenden     # schreibt die Korrekturen in inhalte/transkripte/*.vtt

Datenquelle: inhalte/glossar.json (hosts, global, folgen[Nr] = Begriffe, korrekturen = Regex → Schreibweise).
Korrigiert wird nur Text, nie Zeitmarken. Neue Fehler beim Gegenlesen einfach in die Liste eintragen."""
import argparse, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from layout import REPO

DATEI = REPO / 'inhalte' / 'glossar.json'


def laden():
    return json.loads(DATEI.read_text(encoding='utf-8')) if DATEI.exists() else {}


def begriffe(nr, maxzeichen=450):
    """Kommagetrennte Begriffe für den Whisper-Prompt (Whisper liest nur die letzten ~220 Token)."""
    g = laden()
    text = ', '.join(x for x in (g.get('folgen', {}).get(str(nr), ''), g.get('global', '')) if x)
    return text[:maxzeichen].rsplit(',', 1)[0] if len(text) > maxzeichen else text


def korrigieren(vtt, zaehler=None):
    """Wendet die Korrekturliste auf Textzeilen an (Zeilen mit „-->“ und WEBVTT/NOTE bleiben unberührt)."""
    regeln = [(re.compile(rf'\b(?:{k})'), v) for k, v in laden().get('korrekturen', {}).items()]
    out = []
    for zeile in vtt.split('\n'):
        if '-->' not in zeile and not zeile.startswith(('WEBVTT', 'NOTE')):
            for rx, v in regeln:
                zeile, n = rx.subn(v, zeile)
                if n and zaehler is not None:
                    zaehler[v] = zaehler.get(v, 0) + n
        out.append(zeile)
    return '\n'.join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pruefen', action='store_true')
    ap.add_argument('--anwenden', action='store_true')
    a = ap.parse_args()
    if not (a.pruefen or a.anwenden):
        ap.error('--pruefen oder --anwenden angeben')
    zaehler = {}
    for p in sorted((REPO / 'inhalte' / 'transkripte').glob('*.vtt')):
        alt = p.read_text(encoding='utf-8')
        neu = korrigieren(alt, zaehler)
        if a.anwenden and neu != alt:
            p.write_text(neu, encoding='utf-8')
    for v, n in sorted(zaehler.items(), key=lambda x: -x[1]):
        print(f'{n:4d}  → {v}')
    print('Geändert.' if a.anwenden else 'Nur geprüft, nichts geändert.')


if __name__ == '__main__':
    main()
