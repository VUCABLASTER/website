> **Überholt seit 28.09.2026:** Die aktuelle Folge auf der Startseite wird jetzt automatisch aus dem Feed von podcaster.de erzeugt (`werkzeuge/build.py`). Von Hand pflegst du nur noch die Folgen-Infos in `inhalte/folgen/NNN.json` – siehe **PFLEGE.md**. Die Anleitung unten gilt nur noch, falls der automatische Build einmal ausfällt.

# Neue Folge eintragen und Fotos einbauen

Alles, was sich pro Folge ändert, steht in **`docs/index.html`** in zwei markierten Blöcken:

| Block | Was drinsteht |
|---|---|
| `<!-- HERO-NOTIZ:START -->` … `<!-- HERO-NOTIZ:ENDE -->` | Türkise Haftnotiz oben rechts (nur am Desktop sichtbar): Nummer, Titel, Gast |
| `<!-- AKTUELLE-FOLGE:START -->` … `<!-- AKTUELLE-FOLGE:ENDE -->` | Abschnitt „Aktuelle Folge“: Nummer, Staffel, Datum, Titel, Gast, Rolle, Werte, Foto, Player (MP3), 3 Key Learnings |

Außerhalb dieser Blöcke musst du nichts ändern.

## Was du pro Folge änderst

Im Block **HERO-NOTIZ**:
- `Neu · #62` → neue Nummer
- Titel in `<span class="n-title">…</span>`
- `mit Claudia Jahn →` → neuer Gast

Im Block **AKTUELLE-FOLGE**:
1. **Meta-Zeile:** `#62 · Staffel Mut, 4 von 8 · <time datetime="2026-09-23">23.09.2026</time>`
   Nummer, Staffel und Datum ändern. Das Datum steht zweimal: `datetime="JJJJ-MM-TT"` und sichtbar `TT.MM.JJJJ`.
2. **Titel:** im `<h2 …>` – die Nummer steht dort ein zweites Mal im unsichtbaren Teil `<span class="sr-only">#62 – </span>` (für Screenreader), bitte mitändern.
3. **Gast und Rolle:** `mit Claudia Jahn` und die Zeile darunter.
4. **Werte:** `mutig · Hauptwert` (gefüllt) und `authentisch` (Nebenwert). Kein Nebenwert? Die zweite `<li>`-Zeile löschen.
5. **Foto des Gastes:** kommt zweimal vor (kleines Bild für Handy, großes für Desktop): `assets/img/claudia-jahn.jpg` → `assets/img/vorname-nachname.jpg`, beim großen Bild auch `alt="Claudia Jahn"`. Fehlt das Foto, erscheint automatisch das Cover, fehlt auch das, die Schraffur.
6. **Player:** Die MP3-Adresse steht **zweimal** im Player-Block: in `data-src="…"` und im Link `href="…"`. Außerdem `data-title="#62 – …"` anpassen.
   Klammern in der Adresse müssen kodiert sein: `(` → `%28`, `)` → `%29`, Leerzeichen → `%20`.
   Die MP3-Adresse findest du bei podcaster.de in der Folge (Download-Link) oder im RSS-Feed.
7. **Key Learnings:** die drei Texte in `<span class="sticky-text">…</span>`. Typografische Anführungszeichen verwenden: „ … “.

Die Zahl im Hero **„62 Folgen seit 2020“** steht außerhalb der Blöcke (Suche nach `hero-meta`) – bei jeder neuen Folge hochzählen.

## Weg A: im GitHub-Webeditor (ohne Installation)

1. https://github.com/VUCABLASTER/website öffnen → Ordner `docs` → `index.html`.
2. Oben rechts auf den **Stift** („Edit this file“) klicken.
3. Mit **Strg + F** nach `HERO-NOTIZ:START` suchen, Texte ändern. Dann nach `AKTUELLE-FOLGE:START` suchen und die Punkte 1–7 oben abarbeiten. Nur Text zwischen den spitzen Klammern ändern, keine `<` `>` löschen.
4. Oben rechts **„Commit changes…“** → kurze Nachricht, z. B. „Folge #63 eingetragen“ → **Commit changes**.
5. Nach 1–2 Minuten ist die Seite live. Unter **Actions** (Reiter oben) siehst du, ob der Pages-Build grün ist.
6. https://vucablaster.de öffnen, **Strg + F5** (neu laden ohne Cache), Player einmal testen.

## Weg B: mit Claude Code

Im Projektordner Claude Code starten und zum Beispiel einfügen:

```
Trag in docs/index.html die neue aktuelle Folge ein. Ändere nur die Blöcke
HERO-NOTIZ und AKTUELLE-FOLGE sowie die Folgenzahl im Hero (hero-meta).

Nummer: #63
Titel: …
Gast: …, Rolle: …
Staffel: Staffel Mut, 5 von 8
Werte: Hauptwert …, Nebenwert …
Datum: TT.MM.JJJJ
MP3: https://…
Foto: assets/img/vorname-nachname.jpg (falls vorhanden)
Key Learnings:
1. …
2. …
3. …

Kodiere Klammern in der MP3-URL als %28/%29 und prüfe, ob die Datei lädt.
Erfinde nichts. Zeig mir danach den Diff, committe erst nach meinem OK.
```

## Fotos einbauen

Die Seite ist schon auf diese Dateinamen vorbereitet. Solange eine Datei fehlt, zeigt der Foto-Abzug eine Schraffur (kein kaputtes Bildsymbol).

| Datei | Wo sie erscheint | Empfohlene Größe |
|---|---|---|
| `docs/assets/img/cover.jpg` | „Was ist ein VUCA Blaster?“ und als Ersatz, wenn kein Gastfoto da ist | 1200 × 1200 px |
| `docs/assets/img/manuel-wyszynski.jpg` | „Wer spricht hier?“ | 960 × 1200 px (Hochformat 4:5) |
| `docs/assets/img/sebastian-oremek.jpg` | „Wer spricht hier?“ | 960 × 1200 px (Hochformat 4:5) |
| `docs/assets/img/claudia-jahn.jpg` | Aktuelle Folge | 880 × 560 px (Querformat), Ausschnitt wird automatisch zugeschnitten |

So geht's:
1. Fotos **vorher verkleinern** (Ziel: je unter 300 KB). Ein 3000-px-Cover würde die Seite unnötig langsam machen. Am einfachsten: Claude Code bitten „Verkleinere die Fotos in 01-von-manuel/bilder/ auf die Größen aus NEUE-FOLGE.md und leg sie als JPG unter docs/assets/img/ ab“.
2. Dateien **genau so benennen** (kleingeschrieben, Bindestrich, `.jpg`) und in `docs/assets/img/` ablegen. Im GitHub-Webeditor: Ordner `docs/assets/img` öffnen → **Add file → Upload files**.
3. Committen. Mehr ist nicht nötig – der HTML-Code verweist schon auf diese Namen.
4. Muss eine Fotografin oder ein Fotograf genannt werden? Dann in `docs/index.html` nach `FEHLT: Fotonachweis` suchen und den Kommentar durch eine sichtbare Zeile ersetzen (oder Claude Code bitten).
