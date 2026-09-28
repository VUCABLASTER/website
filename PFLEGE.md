# Pflege der Website vucablaster.de

Die Website liegt im Repo `VUCABLASTER/website`. GitHub Pages veröffentlicht den Ordner `docs/` aus dem Branch `main`, jede Änderung ist nach 1–2 Minuten live.

## Was automatisch passiert

`werkzeuge/build.py` erzeugt aus dem Feed von podcaster.de:

- das Archiv `vucablaster.de/folgen/` (auch erreichbar über `/archiv/`) mit Suche und Filtern nach Wert, Staffel und Jahr
- eine Seite pro Folge (Titel, Datum, Dauer, Folgenbild, Beschreibung, Links zu Apple Podcasts und Spotify)
- Kurzlinks wie `vucablaster.de/62` für LinkedIn-Posts

Titel, Bild und Beschreibung pflegst du wie bisher bei **podcaster.de**. Die Links zu den einzelnen Folgen bei Apple Podcasts holt der Build automatisch. Spotify verlinkt vorerst auf die Podcast-Seite.

Der Build läuft vorerst lokal mit `python3 werkzeuge/build.py` (oder per Claude Code). Der GitHub-Workflow „Website bauen“ liegt als Vorlage in `werkzeuge/website-bauen.yml.vorlage` und wird nach dem WORCamp 2026 nach `.github/workflows/` verschoben (braucht einmalig `gh auth refresh -s workflow`). Dann läuft der Build per Knopfdruck, täglich und nach Änderungen an den Folgen-Infos.

## Was du von Hand pflegst: die Folgen-Infos

Pro Folge gibt es eine Datei `inhalte/folgen/062.json` usw. mit:

| Feld | Beispiel |
|---|---|
| Gast | Dr. Maja Storch |
| Rolle | Psychologin |
| Staffel | mut |
| Hauptwert | mutig |
| Nebenwerte | authentisch |
| Key Learnings | bis zu drei kurze Sätze |

Für neue Folgen legt der Build die Datei selbst an. Du ergänzt nur die Felder.

**Am einfachsten mit Pages CMS** (Formular im Browser):

1. Einmalig: https://app.pagescms.org öffnen → mit GitHub anmelden → die Pages-CMS-App für die Organisation VUCABLASTER installieren (nur für das Repo `website`).
2. Danach: https://app.pagescms.org → Repo `website` → **Folgen** → Folge auswählen → Felder ausfüllen → **Save**.
3. Build starten (siehe oben).

**Alternativ im GitHub-Webeditor:** Datei `inhalte/folgen/062.json` öffnen → Stift → nur den Text zwischen den Anführungszeichen ändern → Commit.

**Mit Claude Code:** „Trag in inhalte/folgen/063.json ein: Gast …, Rolle …, Hauptwert …, Key Learnings … Dann baue die Website mit python3 werkzeuge/build.py und zeig mir den Diff.“

## Schalter in `werkzeuge/layout.py`

| Schalter | Wirkung |
|---|---|
| `ARCHIV_VERLINKT = False` | Archiv ist erreichbar, aber nicht verlinkt und für Suchmaschinen gesperrt. Startseite unverändert. |
| `ARCHIV_VERLINKT = True` | Navigation „Folgen“, Archiv-Abschnitt und automatische aktuelle Folge auf der Startseite, Sitemap. |
| `GEWINNSPIEL_LEISTE = True/False` | Türkise Gewinnspiel-Leiste über dem Header an/aus. |

Nach dem Umstellen den Build laufen lassen.

## Rollback (zurück zum Stand vor dem Archiv)

Der Live-Stand vor dem Archiv ist mit dem Git-Tag **`vor-archiv`** markiert. Zurück geht es ohne Verlust von Historie so (im Projektordner):

```
git checkout main
git pull
git restore --source=vor-archiv --staged --worktree -- docs
git commit -m "Rollback: Website auf Stand vor dem Archiv"
git push
```

Oder Claude Code bitten: „Setz docs/ auf den Stand von Tag vor-archiv zurück, committe und pushe.“
Nach 1–2 Minuten ist die alte Version live. Werkzeuge und Folgen-Infos bleiben erhalten, man kann jederzeit wieder vorwärts bauen.
