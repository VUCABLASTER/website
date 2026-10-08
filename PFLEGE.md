# Pflege der Website vucablaster.de

Die Website liegt im Repo `VUCABLASTER/website`. GitHub Pages veröffentlicht den Ordner `docs/` aus dem Branch `main`, jede Änderung ist nach 1–2 Minuten live.

## Was automatisch passiert

Der GitHub-Workflow **„Website aktualisieren“** (`.github/workflows/website-aktualisieren.yml`) läuft **stündlich** (eine neue Folge ist spätestens eine gute Stunde nach dem Erscheinen auf der Website), nach jeder Änderung an `inhalte/` (z. B. über Pages CMS) und per Knopfdruck (**GitHub → Actions → „Website aktualisieren“ → Run workflow**). Er

1. holt neue Folgen aus dem Feed von podcaster.de (Titel, Datum, Bild, Beschreibung, MP3),
2. **transkribiert Folgen nur auf Knopfdruck** (Whisper, läuft bei GitHub, kostenlos) → `inhalte/transkripte/NNN.vtt`. Automatisch transkribieren lässt sich einschalten mit der Repository-Variable `TRANSKRIBIEREN_AUTO` = `fehlende` (GitHub → Settings → Secrets and variables → Actions → Variables); Standard ist aus.
   **Transkripte erscheinen auf der Website erst nach Freigabe:** Folgennummer in `inhalte/transkripte/freigegeben.json` eintragen (Pages CMS → „Transkripte freigeben“), nachdem das Transkript gelesen wurde. Freigegeben: alle 62 (Stand 06.10.2026).
3. holt die **Links zu jeder einzelnen Folge**:
   - Apple Podcasts und Deezer: automatisch über deren öffentliche Schnittstellen. Apple und Deezer listen eine neue Folge oft erst nach einigen Stunden; die stündlichen Läufe tragen den Link dann von selbst nach.
   - Spotify und Amazon Music: automatisch, ohne Konto. Ein Browser auf GitHub liest die öffentlichen Podcast-Seiten und ordnet jede Folge über die Nummer „#NN“ im Titel zu (`werkzeuge/plattform_links_holen.py`). Gespeichert wird nur bei eindeutiger Zuordnung.
   - Fehlt ein Link (z. B. weil die Folge dort noch nicht gelistet ist, oder eine Plattform ihr Seitenlayout geändert hat), zeigt der Button auf die Podcast-Seite der Plattform. Der Workflow-Log nennt die betroffenen Folgen, und du kannst den Link im Pages CMS eintragen (Felder „Spotify-Link“ und „Amazon-Music-Link“). Handeinträge haben immer Vorrang.
4. baut Startseite (aktuelle Folge), Archiv `/folgen/` (Suche auch in den Transkripten), Folgenseiten (mit Transkript zum Aufklappen) und Kurzlinks wie `/62`,
5. veröffentlicht das Ergebnis und legt für **jede neue Folge ein GitHub-Issue** „Neue Folge #NN: Angaben prüfen und ergänzen“ an. Es zeigt, was automatisch vorausgefüllt wurde (Gast aus dem Titel, Rolle und Satz zum Inhalt aus den Shownotes, Hauptwert nur bei eindeutigem Befund), was noch offen ist und welche Plattform-Links gefunden wurden. Alles Vorausgefüllte ist ungeprüft markiert; erfunden wird nichts, bei Unsicherheit bleibt ein Feld leer. Wer das Repo beobachtet, bekommt dazu eine E-Mail.

Die Transkripte sind maschinell erstellt und nicht nachbearbeitet. Hörfehler kannst du direkt in der `.vtt`-Datei korrigieren (nur den Text, nicht die Zeitmarken). Eine Folge neu transkribieren: Run workflow → bei „Transkribieren“ die Nummer eintragen, z. B. `62`.

Lokal geht der Build auch: `python3 werkzeuge/build.py` (braucht `pip install pillow`).

## Pages CMS einrichten (einmalig, durch Manuel als Owner der Organisation)

Pages CMS ist ein kostenloses Open-Source-Werkzeug, das Dateien aus dem GitHub-Repo als Formulare im Browser zeigt. Es speichert direkt als Commit ins Repo; danach aktualisiert sich die Website von selbst.

1. https://app.pagescms.org öffnen → **Sign in with GitHub** → Zugriff erlauben.
2. Die **GitHub-App** von Pages CMS installieren: Organisation **VUCABLASTER** wählen, **Only select repositories** → **website** → Install.
3. In Pages CMS das Repo `VUCABLASTER/website`, Branch `main` öffnen.
4. Es erscheinen die Formulare **Folgen**, **Staffeln** und **Transkripte freigeben** (definiert in `.pages.yml`).
5. Test: Folge #63 öffnen, Angaben prüfen und ergänzen, **Save**. Nach 1–2 Minuten ist die Website aktualisiert.

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
| Ein Satz zum Inhalt (Teaser) | erscheint im Archiv unter dem Titel |
| Hinweis | Notiz zum Prüfen, danach leeren |
| Geprüft | Haken setzen, wenn alles stimmt |

**Stand 28.09.2026:** Für alle 62 Folgen sind Gast, Rolle, Teaser und Werte als **Entwurf aus den Shownotes** eingetragen (Key Learnings bei 22 Folgen, wo die Shownotes klare Aussagen enthalten). Alle Einträge stehen auf „Geprüft: nein“ – bitte durchgehen und abhaken.

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

## Rollback

Rollback-Punkte (Git-Tags): **`vor-werbetest`** (Stand vor dem Werbetest, 08.10.2026), **`vor-archiv`** (Stand vor dem Archiv), **`vor-verlinkung`** (Archiv online, aber unverlinkt), **`vor-transkripten`** (vor Plattform-Links und Transkripten). Zurück geht es ohne Verlust von Historie so (im Projektordner):

```
git checkout main
git pull
git restore --source=vor-archiv --staged --worktree -- docs
git commit -m "Rollback: Website auf Stand vor dem Archiv"
git push
```

Oder Claude Code bitten: „Setz docs/ auf den Stand von Tag vor-archiv zurück, committe und pushe.“
Nach 1–2 Minuten ist die alte Version live. Werkzeuge und Folgen-Infos bleiben erhalten, man kann jederzeit wieder vorwärts bauen.

## Werbetest (Fake Door)

Drei Produktbanner (Check-in-Journal, Mut-Bücherpaket, Exercise Snacks; Fassung laut "version" in der JSON) auf Startseite und Folgenseiten. Wer klickt, sieht an derselben Stelle „Danke! Das testen wir gerade.“ Gezählt werden nur Ansichten und Klicks pro Banner in GoatCounter: https://vucablaster.goatcounter.com (Einträge „werbetest/…“). Keine Cookies.

- **Vorschau zur Abnahme:** https://vucablaster.de/werbetest-vorschau/v4/ (geplante Fassung: Post-its) mit Testseiten im echten Umfeld (Folgenseite neben den Key Learnings / unter dem Folgenbild, Startseite neben den Key Learnings / unter dem VUCA-Blaster-Bild). Ältere Fassungen: /werbetest-vorschau/ (V1) und /werbetest-vorschau/v3/. Alles nicht verlinkt, noindex, ohne Zählung. Verschwindet automatisch, sobald der Test läuft.
- **Post-its (V4):** Pro Seitenaufruf ein zufälliger Zettel an einer zufälligen Stelle, mit 1–3 Klebestreifen, Farbe Rosa/Türkis und leichter Neigung. GoatCounter-Pfade: werbetest/v4/<produkt>/<platz>/gesehen bzw. /klick.
- **Einstellungen:** `inhalte/werbetest.json` – Texte, Preise, Fotos, `aktiv`, `ende`.
- **Starten:** `"aktiv": true` setzen und pushen. Der Workflow baut die Website neu, die Banner erscheinen.
- **Beenden (schnell, empfohlen):** `"aktiv": false` setzen und pushen (oder Claude Code bitten: „Werbetest ausschalten“). Der Build entfernt Banner, Skript und Zählung von allen Seiten. Nach 1–2 Minuten ist alles weg. Am Datum `ende` passiert das automatisch.
- **Vollständiger Rollback:** Code und Seiten auf den Stand vor dem Test zurücksetzen, ohne Historie zu verlieren:

```
git checkout main
git pull
git restore --source=vor-werbetest --staged --worktree -- werkzeuge docs/assets/css/style.css
git rm -r --quiet docs/assets/js/werbetest.js docs/assets/img/werbetest docs/werbetest-vorschau inhalte/werbetest.json werkzeuge/werbetest.py werkzeuge/werbetest_bilder.py
python3 werkzeuge/build.py
git add -A docs werkzeuge inhalte
git commit -m "Rollback: Werbetest vollständig entfernt"
git push
```

  Hinweis: `werkzeuge` wird dabei komplett auf den Stand des Tags gesetzt. Gab es seitdem andere Änderungen an den Werkzeugen, lieber Claude Code bitten: „Entferne den Werbetest vollständig (Rollback auf vor-werbetest), andere Änderungen behalten.“
