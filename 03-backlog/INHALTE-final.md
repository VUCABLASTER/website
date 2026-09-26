# VUCA Blaster – Inhalte zum Ausfüllen

Dieses Dokument geht ihr **Schritt für Schritt** durch. Jeder Schritt ist ein kleiner Block, den ihr in 5–20 Minuten schafft. Wenn ein Block fertig ist, gebt ihr die Datei an Claude Code (Prompt steht ganz unten).

## So funktioniert's

1. Nur die Werte **zwischen den Anführungszeichen** ändern. Die Wörter links vom Doppelpunkt bleiben, wie sie sind.
2. Wisst ihr etwas noch nicht: den Platzhalter `[[PFLICHT: …]]` oder `[[OFFEN: …]]` einfach **stehen lassen**. Nichts erfinden.
3. Längere Texte stehen hinter `|` und dürfen über mehrere Zeilen gehen – nur jede Zeile mit denselben Leerzeichen einrücken.
4. Vorausgefüllte Werte (aus Apple Podcasts, Spotify oder dem Design) sind mit `# prüfen` markiert. Stimmt der Wert, einfach `# prüfen` löschen.
5. Status oben im Schritt abhaken: `[ ]` → `[x]`.

**Bedeutung**

- `[[PFLICHT: …]]` = muss vor dem Livegang da sein. Ohne diese Angaben geht die Seite nicht unter vucablaster.de online.
- `[[OFFEN: …]]` = fehlt noch, die Seite funktioniert aber. Das Element wird bis dahin einfach ausgeblendet.

---

## Übersicht

| Schritt | Thema | Priorität | Wer | Status |
|---|---|---|---|---|
| 1 | Zugänge und Verantwortung | PFLICHT | Manuel | [ ] |
| 2 | Impressum | PFLICHT | Manuel + Sebastian | [ ] |
| 3 | Datenschutzerklärung | PFLICHT | Manuel + Sebastian | [ ] |
| 4 | Kontakt | PFLICHT | beide | [ ] |
| 5 | Grunddaten und Plattform-Links | PFLICHT | Manuel | [ ] |
| 6 | Host-Profile | PFLICHT | jeder für sich | [ ] |
| 7 | Was ist ein VUCA Blaster? | PFLICHT | beide | [ ] |
| 8 | Die fünf Werte | WICHTIG | beide | [ ] |
| 9 | Staffeln | WICHTIG | beide | [ ] |
| 10 | Folgen zuordnen (2026) | WICHTIG | Manuel | [ ] |
| 11 | Player und Video | WICHTIG | Manuel | [ ] |
| 12 | Für Gäste | WICHTIG | beide | [ ] |
| 13 | Archiv 2020–2025 | SPÄTER | beide | [ ] |
| 14 | Bilder und Rechte | WICHTIG | beide | [ ] |
| 15 | Texte für Suche und LinkedIn | SPÄTER | Manuel | [ ] |
| 16 | Freigabe und Livegang | PFLICHT | beide | [ ] |

Empfohlene Reihenfolge für die erste Sitzung: 1 → 5 → 10 → 11. Damit kann Claude Code schon die komplette Startseite mit echten Daten bauen. Die Rechtstexte (2, 3) könnt ihr parallel mit einem Generator erstellen.

---

## Schritt 1 – Zugänge und Verantwortung · PFLICHT

**Warum:** Die Seite soll dauerhaft bei euch liegen, nicht bei Thomas.
**Landet in:** `docs/ENTSCHEIDUNGEN.md`, GitHub-Einstellungen

```yaml
github:
  ort: "[[PFLICHT: Manuel hat eine Organisation in GitHub erstellt ]]"
  repo_name: "[[PFLICHT: https://github.com/VUCABLASTER/website.git]]"
  oeffentlich: ja
  owner: "Manuel Wyszynski"
  mitarbeitende: ["Thomas Wordenbeck"]
domain:
  name: "vucablaster.de, vucablaster.com, vucablaster.store, vucablaster.global"
  registrar: "[[PFLICHT: IONOS]]"
  dns_zugang_hat: "[[PFLICHT: wer kann DNS-Einträge setzen?]]"
  registriert_am: "[[OFFEN: 25.09.2016]]"
email_postfach:
  vorhanden: "[[OFFEN: gibt es ein Postfach @vucablaster.de? ja/nein]]"
```

---

## Schritt 2 – Impressum · PFLICHT

**Warum:** Gesetzlich vorgeschrieben (§ 5 DDG, § 18 Abs. 2 MStV). Ich bin kein Anwalt – nutzt einen Impressum-Generator oder lasst es prüfen.
**Landet in:** `src/content/seiten/impressum.md`

Vorab-Fragen (beeinflussen den Text):

```yaml
anbieter_form: "[[PFLICHT: Privatpersonen]]"
gewerblich: "[[PFLICHT: Gibt es Einnahmen, Sponsoring, Werbung? nein]]"
ust_id: "[[gibts nicht]]"
```

Angaben:

```yaml
name_anbieter: "[[PFLICHT: vollständiger Name bzw. Name der GbR + vertretungsberechtigte Personen]]"
anschrift: "[[PFLICHT: ladungsfähige Anschrift – Straße, PLZ, Ort; kein Postfach]]"
email: "[[PFLICHT: E-Mail]]"
zweiter_kontaktweg: "[[PFLICHT: Telefon o. ä. – empfohlen]]"
verantwortlich_redaktionell: "[[PFLICHT: Name + Anschrift der verantwortlichen Person nach § 18 Abs. 2 MStV]]"
text_komplett: |
  [[PFLICHT: fertigen Impressumstext aus Generator/Anwalt hier einfügen]]
```

---

## Schritt 3 – Datenschutzerklärung · PFLICHT

**Warum:** Pflicht, sobald Daten verarbeitet werden – und das tut schon das Hosting.
**Landet in:** `src/content/seiten/datenschutz.md`

Diese Punkte muss der Generator abdecken (für euch zum Ankreuzen):

- [ ] Verantwortliche:r (wie Impressum)
- [ ] Hosting: GitHub Pages (GitHub, Inc., USA) – speichert IP-Adressen der Besucher:innen zu Sicherheitszwecken
- [ ] Keine Cookies, kein Tracking, keine Analyse-Tools, Schriften lokal eingebunden
- [ ] Audio-Player: MP3 wird erst nach Klick vom Podcast-Hoster geladen (Anbieter siehe Schritt 11)
- [ ] Video-Player (nur falls es Video gibt): YouTube, erst nach Klick
- [ ] Externe Links zu Spotify, Apple Podcasts, Deezer, Amazon Music, podcast.de
- [ ] Kontaktaufnahme per E-Mail
- [ ] Rechte der Betroffenen, zuständige Aufsichtsbehörde

```yaml
bundesland_verantwortliche: "[[PFLICHT: Bundesland – bestimmt die Aufsichtsbehörde]]"
generator_oder_anwalt: "[[OFFEN: womit erstellt?]]"
text_komplett: |
  [[PFLICHT: fertigen Datenschutztext hier einfügen]]
```

---

## Schritt 4 – Kontakt · PFLICHT

**Warum:** Gastanfragen sind ein Hauptziel der Seite.
**Landet in:** `src/content/site.yaml` → `kontakt`, `src/content/seiten/kontakt.md`

```yaml
email_gaeste: "[[PFLICHT: E-Mail für Gastanfragen]]"
email_allgemein: "[[OFFEN: sonst wird die Gäste-Adresse verwendet]]"
antwortzeit: "[[OFFEN: z. B. „Wir melden uns innerhalb einer Woche.“]]"
linkedin_podcast_seite: "[[OFFEN: URL, falls es eine eigene Seite gibt]]"
weitere_kanaele: []            # z. B. - { label: "Instagram", url: "…" }
```

---

## Schritt 5 – Grunddaten und Plattform-Links · PFLICHT

**Warum:** Diese Buttons sind der wichtigste Klick auf der Seite.
**Landet in:** `src/content/site.yaml`

```yaml
name: "VUCA Blaster"
claim: "Die Welt ist komplex. Wir sehen darin Gestaltungsraum."   # fix
aussprache_ipa: "[ˈvuːka ˈblaːstɐ]"                              # prüfen
aussprache_klartext: "Wuka Blaster"                               # prüfen – so liest es ein Screenreader vor
start_jahr: 2020
rhythmus: "alle zwei Wochen neu"   # prüfen – die letzten Folgen kamen laut Apple in kürzeren Abständen
feed_url: "https://evjjod.podcaster.de/VUCABlaster.rss"          # prüfen – in podcaster.de nachsehen

plattformen:
  spotify: "https://open.spotify.com/show/3OQW0akZgxBxK4AWFQSKtf"                  # prüfen
  apple: "https://podcasts.apple.com/de/podcast/vuca-blaster/id1541461336"          # prüfen
  deezer: "[[OFFEN: Deezer-Link]]"
  amazon_music: "[[OFFEN: Amazon-Music-Link]]"
  podcast_de: "[[OFFEN: podcast.de-Link – der bekannte Link war beim Test nicht erreichbar]]"
  youtube: "[[OFFEN: nur falls es Video gibt]]"
  weitere: []                   # z. B. - { name: "Audible", url: "…" }

hervorheben: ["spotify", "apple"]   # schwarze Buttons; laut Briefing, weil dort Abos und Bewertungen zählen
```

---

## Schritt 6 – Host-Profile · PFLICHT

**Warum:** Gäste wollen wissen, mit wem sie sprechen. Ohne Profile wirkt „Über uns“ leer.
**Landet in:** `src/content/hosts.yaml`
**Tipp:** Kurz-Bio in der Du-Form ans Publikum oder neutral in der 3. Person – aber beide gleich.

```yaml
- name: "Manuel Wyszynski"                # prüfen – Schreibweise
  rolle: "[[PFLICHT: z. B. Host · Organisationsentwickler bei …]]"
  bio_kurz: "[[PFLICHT: max. 300 Zeichen]]"
  bio_lang: |
    [[OFFEN: 3–6 Sätze: Hintergrund, warum der Podcast, was dich an Mut/Wandel interessiert]]
  foto: "[[PFLICHT: Dateiname, Hochformat, mind. 1200 px hoch]]"
  foto_credit: "[[OFFEN: Fotograf:in, falls Nennung nötig]]"
  links:
    - { label: "LinkedIn", url: "[[OFFEN: URL]]" }

- name: "Sebastian Oremek"                # prüfen – Schreibweise
  rolle: "[[PFLICHT: …]]"
  bio_kurz: "[[PFLICHT: max. 300 Zeichen]]"
  bio_lang: |
    [[OFFEN: 3–6 Sätze]]
  foto: "[[PFLICHT: Dateiname]]"
  foto_credit: "[[OFFEN]]"
  links:
    - { label: "LinkedIn", url: "[[OFFEN: URL]]" }
```

Rückfrage: podcast.de nennt als Autoren „Manuel & Ricardo“.

```yaml
ricardo_erwaehnen: "[[nicht mehr dabei und nicht erwähnen]]"
```

---

## Schritt 7 – Was ist ein VUCA Blaster? · PFLICHT

**Warum:** Der Name ist erklärungsbedürftig. Die Erklärung ist der Kern von „Über uns“.
**Landet in:** `src/content/seiten/ueber-uns.md`

```yaml
wortart: "Substantiv, der"                 # prüfen
definition: |
  [[PFLICHT: 1–3 Sätze. Was ist ein VUCA Blaster – eine Person, eine Haltung, ein Werkzeug?]]
vuca_erklaert: |
  [[OFFEN: 1 Satz zu V-U-C-A (volatil, unsicher, komplex, mehrdeutig) – oder weglassen]]
warum_wir_das_machen: |
  [[OFFEN: 3–6 Sätze in eurer Sprache. Warum gibt es den Podcast seit 2020?]]
fuer_wen: "[[OFFEN: 1 Satz – wer hört euch zu?]]"
```

---

## Schritt 8 – Die fünf Werte · WICHTIG

**Warum:** Jede Folge der Themenstaffeln hat genau einen Hauptwert. Jede Karte führt zu einer Themenseite.
**Landet in:** `src/content/werte.yaml`
Die Sätze unten sind **Vorschläge aus dem ersten Prototyp**, nicht von euch. Ersetzen oder bestätigen.

```yaml
- slug: optimistisch
  beschreibung: "Möglichkeiten sehen, bevor alles geklärt ist."            # Vorschlag – prüfen
- slug: neugierig
  beschreibung: "Fragen stellen, auf die es noch keine Antwort gibt."      # Vorschlag – prüfen
- slug: mutig
  beschreibung: "Handeln, obwohl die Unsicherheit bleibt."                 # Vorschlag – prüfen
- slug: authentisch
  beschreibung: "Stimmig sein, auch wenn es mal holpert."                  # Vorschlag – prüfen
- slug: verbindend
  beschreibung: "Brücken bauen zwischen Menschen und Strukturen."          # Vorschlag – prüfen
```

```yaml
werte_ohne_staffel_text: "[[OFFEN: Was steht auf den Themenseiten „neugierig“, „authentisch“, „verbindend“, solange es dazu keine Staffel gibt? Vorschlag: „Die Staffel dazu kommt noch.“]]"
naechste_staffel_wert: "[[OFFEN: Welcher Wert kommt 2027 dran? Darf das schon auf die Seite?]]"
```

---

## Schritt 9 – Staffeln · WICHTIG

**Warum:** Die laufende Staffel ist das zweitwichtigste Element der Startseite.
**Landet in:** `src/content/staffeln.yaml`

```yaml
- slug: mut
  titel: "Mut"
  wert: "mutig"
  jahr: 2026
  status: "laufend"
  folgen_geplant: 8
  zeitraum_text: "läuft bis Jahresende"
  beschreibung: |
    [[OFFEN: 2–3 Sätze: Worum geht es in der Staffel Mut?]]
  kommende_gaeste_zeigen: "[[OFFEN: Dürfen Namen der Folgen 5–8 vorab auf die Seite? ja/nein]]"
  kommende_gaeste: []           # nur wenn ja: - { position: 5, name: "…", rolle: "…" }

- slug: optimismus
  titel: "Optimismus"
  wert: "optimistisch"
  jahr: 2026                    # prüfen
  status: "abgeschlossen"
  folgen_geplant: "[[OFFEN: 3? Wie viele Folgen hatte die Staffel?]]"
  beschreibung: |
    [[OFFEN: 2–3 Sätze]]
```

---

## Schritt 10 – Folgen zuordnen (2026) · WICHTIG

**Warum:** Der Feed kennt keine Staffeln, Werte oder Key Learnings. Das kommt von euch.
**Landet in:** `src/content/folgen/<nummer>.yaml`
Vorausgefüllt aus Apple Podcasts und dem Design. Nummern in Klammern sind **vermutet**: Zwischen #57 und #61 gäbe es dann keine Lücke.

### #62 – Warum echter Mut mit Stimmigkeit beginnt

```yaml
nummer: 62
staffel: "mut"
staffel_position: 4
hauptwert: "mutig"
nebenwerte: ["authentisch"]
gast:
  name: "Claudia Jahn"
  rolle_kurz: "Schauspielerin"
  rolle_lang: "Schauspielerin, Sprecherin, Executive Coach"
  foto: "[[OFFEN: Datei + Nutzungsrecht]]"
  links: []
key_learnings:
  - "Wirklich mutige Menschen fühlen sich oft gar nicht mutig."
  - "„Wie wirke ich?“ ist vielleicht die falsche Frage."
  - "Mut beginnt mit Stimmigkeit, nicht mit Überwindung."
plattform_links:
  spotify: "[[OFFEN: Link direkt zur Folge]]"
  apple: "[[OFFEN: Link direkt zur Folge]]"
video_url: "[[OFFEN: nur falls Video]]"
```

### #61 – Mut ohne Überwindung

```yaml
nummer: 61
staffel: "mut"
staffel_position: 3
hauptwert: "mutig"
nebenwerte: []
gast:
  name: "Dr. Maja Storch"
  rolle_kurz: "Psychologin"
  rolle_lang: "[[OFFEN: ausführliche Rolle]]"
  foto: "[[OFFEN]]"
key_learnings: []               # [[OFFEN: 3 Sätze oder leer lassen]]
```

### (#60) – Mutig oder nur bequem?

```yaml
nummer: "[[OFFEN: 60? bestätigen]]"
staffel: "mut"
staffel_position: 2
hauptwert: "mutig"
gast:
  name: "Dr. Rüdiger Maas"
  rolle_kurz: "Generationenforscher"
  rolle_lang: "[[OFFEN]]"
  foto: "[[OFFEN]]"
key_learnings: []
```

### (#59) – Warum Mut mit kleinen Schritten beginnt

```yaml
nummer: "[[OFFEN: 59? bestätigen]]"
staffel: "mut"
staffel_position: 1
hauptwert: "mutig"
gast:
  name: "Jennifer Wendland"
  rolle_kurz: "Freitaucherin"
  rolle_lang: "[[OFFEN: z. B. Weltmeisterin im Freitauchen – prüfen]]"
  foto: "[[OFFEN]]"
key_learnings: []
```

### (#58) – Mut und Unternehmertum

```yaml
nummer: "[[OFFEN: 58? bestätigen]]"
staffel: "[[OFFEN: optimismus, mut oder keine?]]"
staffel_position: "[[OFFEN]]"
hauptwert: "[[OFFEN]]"
gast:
  name: "Thomas Hoppe"
  rolle_kurz: "[[OFFEN: z. B. Unternehmer]]"
key_learnings: []
```

### #57 – Optimismus & warum Wissen überschätzt wird

```yaml
nummer: 57
staffel: "optimismus"
staffel_position: "[[OFFEN: 2?]]"
hauptwert: "optimistisch"
gast:
  name: "Prof. Dr. Thomas de Nocker"      # prüfen – Schreibweise
  rolle_kurz: "[[OFFEN: z. B. Professor für …]]"
key_learnings: []
```

### #56 – Bedingungsloser Optimismus

```yaml
nummer: 56
staffel: "optimismus"
staffel_position: "[[OFFEN: 1?]]"
hauptwert: "optimistisch"
gast:
  name: "Jonas Deichmann"
  rolle_kurz: "Extremsportler"            # prüfen
key_learnings: []
```

### (#55) – Warum Vorsätze scheitern

```yaml
nummer: "[[OFFEN: 55? bestätigen]]"
staffel: "[[OFFEN: keine? oder Optimismus?]]"
gast:
  name: "Prof. Axel Koch"
  rolle_kurz: "[[OFFEN]]"
```

Ältere Folgen (bis 2025) braucht ihr **nicht** auszufüllen. Sie erscheinen automatisch aus dem Feed im Archiv.

---

## Schritt 11 – Player und Video · WICHTIG

**Warum:** Bestimmt, welcher Player eingebettet wird und was in der Datenschutzerklärung steht.
**Landet in:** `src/content/site.yaml`

Empfehlung (9/10): Audio über den **eingebauten Browser-Player** mit der MP3-Datei aus dem Feed. Kein Spotify-Widget (Fremd-Skript, Cookies, schlechter bedienbar).

```yaml
audio_player: "nativ"            # nativ | spotify | podcaster – Empfehlung: nativ
audio_hoster: "[[OFFEN: Wo liegen die MP3s? Vermutlich podcaster.de – bestätigen]]"
video_vorhanden: "[[OFFEN: Gibt es die Folgen als Video (YouTube)? ja/nein]]"
youtube_kanal: "[[OFFEN: URL, falls ja]]"
```

---

## Schritt 12 – Für Gäste · WICHTIG

**Warum:** Eines der Hauptziele. Ein Gast soll in 30 Sekunden wissen, worauf er sich einlässt.
**Landet in:** `src/content/seiten/fuer-gaeste.md`

```yaml
headline: "Lust auf ein Gespräch?"       # Vorschlag – prüfen
intro: |
  [[OFFEN: 2–3 Sätze: Wen sucht ihr? Welche Geschichten passen?]]
ablauf:                                  # genau 3 Schritte (werden Haftnotizen)
  - "[[OFFEN: 1. z. B. Vorgespräch, 20 Minuten]]"
  - "[[OFFEN: 2. z. B. Aufnahme remote, ca. 60 Minuten]]"
  - "[[OFFEN: 3. z. B. Veröffentlichung + Material für LinkedIn]]"
aufnahme:
  ort: "[[OFFEN: remote / vor Ort / beides]]"
  werkzeug: "[[OFFEN: z. B. Riverside, Zoom …]]"
  dauer: "[[OFFEN: Folgen sind aktuell ca. 45–55 Minuten lang]]"
  freigabe: "[[OFFEN: Bekommt der Gast die Folge vorab? ja/nein]]"
was_wir_brauchen:
  - "Foto (Hochformat)"                  # Vorschlag – prüfen
  - "Kurz-Bio (2–3 Sätze)"
  - "Rolle in einer Zeile"
  - "Links (LinkedIn, Website)"
was_du_bekommst: "[[OFFEN: z. B. Grafiken zum Teilen, Link zur Folge]]"
gaeste_wand_zeigen: true                 # Namen + Rolle der letzten 12 Gäste
```

---

## Schritt 13 – Archiv 2020–2025 · SPÄTER

**Warum:** Das Flipchart auf der Startseite fasst die alten Folgen zusammen.
**Landet in:** `src/content/archiv.yaml`

```yaml
label: "Protokoll 2020 bis 2025"
titel: "Methoden und Organisationsentwicklung"
stichworte: ["Selbstorganisation", "Loop Approach", "Fehlerkultur"]   # prüfen – max. 3
text: "Die Folgen von 2020 bis 2025 drehen sich stärker um Methoden und Organisationsentwicklung – etwa Selbstorganisation, Loop Approach und Fehlerkultur."
empfehlungen: []   # [[OFFEN: 3–5 Lieblingsfolgen aus dem Archiv als Nummern, z. B. [15, 34, 48]]]
```

---

## Schritt 14 – Bilder und Rechte · WICHTIG

**Warum:** Fotos ohne Nutzungsrecht sind ein echtes Abmahnrisiko.
**Landet in:** `src/assets/` (Dateien) + Einträge in Schritt 6 und 10

Dateien bitte als JPG oder PNG, mindestens 1200 px an der kurzen Seite, Dateiname `vorname-nachname.jpg`.

```yaml
cover_hochaufloesend: "[[PFLICHT: Podcast-Cover als Datei, ideal 3000 × 3000 px]]"
host_fotos: "[[PFLICHT: siehe Schritt 6]]"
gaeste_fotos_rechte: "[[OFFEN: Dürft ihr Fotos verwenden, die Gäste euch schicken? Habt ihr das schriftlich?]]"
fotos_von_folgen: "[[OFFEN: Gibt es Fotos von Aufnahmen? Nur mit Einverständnis aller Abgebildeten]]"
```

---

## Schritt 15 – Texte für Suche und LinkedIn · SPÄTER

**Warum:** So sieht die Seite in Google und in LinkedIn-Vorschauen aus.
**Landet in:** `src/content/site.yaml`

```yaml
seitentitel: "VUCA Blaster – Podcast über Mut, Wandel und Gestaltungsraum"   # Vorschlag – prüfen
beschreibung_meta: "[[OFFEN: max. 155 Zeichen. Vorschlag: „Der Podcast für alle, die Wandel gestalten wollen. Gespräche über Mut, Optimismus und neue Arbeit – mit Manuel Wyszynski und Sebastian Oremek.“]]"
```

---

## Schritt 16 – Freigabe und Livegang · PFLICHT

**Landet in:** `src/content/site.yaml` → `livegang`

- [ ] Alle PFLICHT-Punkte ausgefüllt (Claude Code zeigt sie im Platzhalter-Report)
- [ ] Beide Hosts haben Startseite, Über uns, Für Gäste, Impressum, Datenschutz gelesen
- [ ] Eine Folgenseite in LinkedIn als Vorschau getestet
- [ ] Domain zeigt auf GitHub Pages, HTTPS aktiv

```yaml
freigabe_manuel: "[[PFLICHT: Datum]]"
freigabe_sebastian: "[[PFLICHT: Datum]]"
livegang_datum: "[[OFFEN: Wunschtermin]]"
```

---

## Übergabe an Claude Code

Speichert diese Datei im Repo unter `docs/INHALTE.md` (die alte Version ersetzen) und startet Claude Code im Repo-Ordner.

**Prompt A – Erster Aufbau (einmalig)**

```
Lies CLAUDE.md, docs/BRIEF.md, docs/INHALTE.md und sieh dir docs/design/ an.
Setze Phase 0 und Phase 1 aus BRIEF Kapitel 16 um. Nutze alle Inhalte aus
INHALTE.md, die schon ausgefüllt sind; alles andere bleibt Platzhalter.
Arbeite phasenweise und hör nach Phase 1 auf. Zeig mir dann die Screenshots
bei 390 und 1440 px neben der Referenz und den Platzhalter-Report.
```

**Prompt B – Inhalte nachliefern (beliebig oft)**

```
Ich habe docs/INHALTE.md aktualisiert (Schritte: …). Übertrage alle ausgefüllten
Werte in die Dateien unter src/content/, entferne die erledigten Platzhalter
und erfinde nichts dazu. Führe npm run check aus und gib mir:
1. was du übernommen hast, 2. was noch offen ist, 3. Rückfragen.
```

**Prompt C – Nächste Phase**

```
Setze Phase <Nummer> aus docs/BRIEF.md Kapitel 16 um. Halte dich an CLAUDE.md.
Zeig mir am Ende, was fertig ist, was offen ist und den Platzhalter-Report.
```

**Prompt D – Livegang-Check**

```
Prüfe, ob wir live gehen können: Platzhalter-Report ohne PFLICHT, alle Checks
und Tests grün, Lighthouse-Ziele aus BRIEF Kapitel 11 erreicht, keine
Fremd-Requests beim Seitenaufruf. Liste alles, was fehlt. Setze livegang erst
auf true, wenn ich es bestätige.
```
