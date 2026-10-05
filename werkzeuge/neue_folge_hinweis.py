"""Text für das GitHub-Issue zu einer neuen Folge: was vorausgefüllt wurde, was noch fehlt, welche Links gefunden sind.

  python3 werkzeuge/neue_folge_hinweis.py 63            # Issue-Text (Markdown)
  python3 werkzeuge/neue_folge_hinweis.py 63 --titel    # Titel der Folge
"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from layout import REPO
import build, plattformen


def main():
    nr = int(sys.argv[1])
    apple = build.apple_lesen((build.DATEN / 'apple.json').read_bytes())
    folgen, _ = build.feed_lesen((build.DATEN / 'feed.xml').read_bytes(), apple)
    f = next(x for x in folgen if x['nr'] == nr)
    if '--titel' in sys.argv:
        print(f['titel_roh'])
        return
    infos = build.infos_laden(folgen)
    plattformen.links_setzen(folgen, infos, offline=True)
    i = infos[nr]
    felder = [('Gast', 'gast'), ('Rolle', 'rolle'), ('Satz zum Inhalt', 'teaser'), ('Hauptwert', 'hauptwert')]
    vor = [f'- **{n}:** {i[k]}' for n, k in felder if i.get(k)]
    offen = [f'- [ ] {n}' for n, k in felder if not i.get(k)]
    offen += ['- [ ] Nebenwerte (optional)', '- [ ] Key Learnings (optional)', '- [ ] Staffel, falls die Folge zu einer Themenstaffel gehört']
    links = ' · '.join(f'{plattformen.NAMEN[p]} {"✓" if f["links"].get(p) else "– (folgt, sonst im Pages CMS eintragen)"}' for p in plattformen.REIHENFOLGE)
    print(f'''Die Website hat **{f["titel_roh"]}** automatisch übernommen: Folgenseite, Archiv-Eintrag, Bild, Beschreibung, Kurzlink `/{nr}`.

**Automatisch vorausgefüllt, bitte prüfen** (aus Titel und Shownotes, nichts erfunden):
{chr(10).join(vor) if vor else '- (nichts eindeutig erkennbar)'}

**Noch offen:**
{chr(10).join(offen)}

**Links zur Folge:** {links}

Eintragen im Pages CMS (Folgen → #{nr}) oder in `inhalte/folgen/{nr:03d}.json`. Danach aktualisiert sich die Website von selbst (nach dem Speichern, spätestens nach einer Stunde). Anleitung: [PFLEGE.md](https://github.com/VUCABLASTER/website/blob/main/PFLEGE.md). Haken bei „Geprüft“ setzen und das Feld „Hinweis“ leeren, wenn alles stimmt.''')


if __name__ == '__main__':
    main()
