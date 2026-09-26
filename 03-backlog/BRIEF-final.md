# VUCA Blaster – Umsetzungs-Brief für Claude Code

Stand: 25.09.2026 · Design: Richtung 03 „Whiteboard nach dem Workshop“ (freigegeben, unverändert umsetzen)

---

## 0. So liest du dieses Dokument

- **MUSS** = Pflicht. **SOLL** = Standard, Abweichung nur mit Begründung in `docs/ENTSCHEIDUNGEN.md`. **KANN** = optional, erst wenn alles andere steht.
- Maße der Startseite stehen exakt im HTML unter `docs/design/`. Dieses Dokument beschreibt **Verhalten, Datenbindung, Erweiterung auf weitere Seiten und Technik**.
- Inhalte, die fehlen, sind als `[[PFLICHT: …]]` oder `[[OFFEN: …]]` markiert (Konvention siehe Kapitel 4.5).
- Fakten in diesem Dokument stammen aus dem Briefing der Hosts und aus der Apple-Podcasts-Seite (Stand 25.09.2026). Wo etwas nur vermutet ist, steht „vermutet“ dabei.

---

## 1. Projekt in 60 Sekunden

**Was:** Eigene Website für den deutschsprachigen Podcast „VUCA Blaster“ (seit 2020, 62 Folgen, Kategorie Management). Hosts: Manuel Wyszynski und Sebastian Oremek.

**Claim (fix):** „Die Welt ist komplex. Wir sehen darin Gestaltungsraum.“

**Wozu die Seite da ist (Priorität absteigend):**

1. **Zentrale Adresse zum Verlinken** – in LinkedIn-Posts und bei Gastanfragen. Jede Folge braucht eine kurze, stabile URL (`vucablaster.de/62`).
2. **Reinhören auslösen** – die aktuelle Folge prominent, sonst Weiterleitung auf die Plattformen (Spotify und Apple Podcasts bevorzugt, weil dort Abos und Bewertungen zählen).
3. **Gäste gewinnen** – potenzielle Gäste sollen in 30 Sekunden verstehen, worum es geht, wer schon da war und wie sie Kontakt aufnehmen.
4. **Orientierung** – Themenstaffel „Mut“ (läuft), fünf Werte, Archiv mit allen Folgen.

**Zielgruppen:** Hörer:innen aus Organisationsentwicklung, Führung, Agilität; potenzielle Gäste (Expert:innen, Coaches, Forschende, Menschen mit Mut-Geschichten); das eigene Netzwerk der Hosts auf LinkedIn.

**Nicht-Ziele (MUSS nicht, SOLL nicht):** Kein eigenes Podcast-Hosting, kein Login, kein CMS im MVP, kein Newsletter, kein Shop, keine Kommentare, kein Dark Mode, keine Mehrsprachigkeit.

**Rahmen:** Budget ca. 10 €/Monat (Domain + ggf. E-Mail; Hosting kostenlos über GitHub Pages). Pflege durch Manuel (Windows, keine Adminrechte, hat Claude und GitHub). Thomas baut die Basis und macht die ersten Deploys; danach liegt alles bei Manuel.

---

## 2. Fixe Entscheidungen (nicht neu diskutieren)

| Thema | Entscheidung |
|---|---|
| Design | D3 „Whiteboard nach dem Workshop“, Markenfarben aus dem Cover, unverändert |
| Ansprache | Du |
| Domain | `vucablaster.de` (www leitet auf Apex um) |
| Hosting | GitHub Pages, Deploy per GitHub Actions |
| Einbettung | Nur die aktuelle Folge bzw. die Folge auf ihrer eigenen Seite, per 2-Klick |
| Tracking | Keines |
| Merch-Shirt | Kein CI-Vorbild, nicht verwenden |

---

## 3. Tech-Stack und Architektur

### 3.1 Stack

| Baustein | Wahl | Warum |
|---|---|---|
| Framework | Astro, aktuelle stabile Version, `output: 'static'` | Statisches HTML, null JS per Default, Content Layer mit eigenen Loadern (RSS) |
| Sprache | TypeScript strict | Schemas für Inhalte, Fehler beim Build statt live |
| Styles | Plain CSS mit Custom Properties, Astro-scoped | Das Design hat viele Einzelmaße und Drehungen; Utility-Klassen würden es unlesbar machen |
| JS | Vanilla TS, als `<script>` in Astro-Komponenten | Menü, Player, Filter, Motion – jeweils < 3 KB |
| Schriften | Fontsource (npm), selbst gehostet | DSGVO: kein Google-CDN |
| RSS | `fast-xml-parser` | klein, ohne native Abhängigkeiten |
| Shownotes | `sanitize-html` | Feed-HTML ist fremder Input |
| Sitemap | `@astrojs/sitemap` | |
| Tests | Playwright + `@axe-core/playwright` | Smoke, A11y, Reduced Motion, Fremd-Requests |
| Node | aktuelle LTS | lokal optional, CI reicht |

Weitere Abhängigkeiten nur mit Begründung in `docs/ENTSCHEIDUNGEN.md`.

### 3.2 Repo-Struktur (SOLL)

```
/
├─ CLAUDE.md
├─ docs/
│  ├─ BRIEF.md              # dieses Dokument
│  ├─ INHALTE.md            # Ausfüllformular der Hosts
│  ├─ PFLEGE.md             # entsteht in Phase 6: Anleitungen für Manuel
│  ├─ ENTSCHEIDUNGEN.md     # Log eigener Entscheidungen
│  ├─ ABWEICHUNGEN.md       # bewusste Abweichungen vom Design
│  ├─ design/               # D3-Referenz (HTML + PNG), nicht Teil des Builds
│  └─ qa/                   # Screenshots je Phase
├─ public/
│  ├─ favicon.svg, favicon.ico, apple-touch-icon.png
│  ├─ og/default.png        # Standard-Teilen-Bild 1200×630
│  └─ robots.txt            # wird je nach livegang generiert (siehe 13.4)
├─ src/
│  ├─ content/
│  │  ├─ site.yaml          # Grunddaten, Plattformen, Kontakt, livegang
│  │  ├─ hosts.yaml
│  │  ├─ werte.yaml
│  │  ├─ staffeln.yaml
│  │  ├─ archiv.yaml        # Flipchart-Inhalt „Protokoll 2020 bis 2025“
│  │  ├─ folgen/            # je Folge eine Datei: 62.yaml, 61.yaml …
│  │  ├─ gaeste/            # optional, falls Gäste mehrfach vorkommen
│  │  └─ seiten/            # ueber-uns.md, fuer-gaeste.md, kontakt.md, impressum.md, datenschutz.md
│  ├─ content.config.ts     # Collections + Schemas + RSS-Loader
│  ├─ data/feed-snapshot.xml
│  ├─ lib/                  # rss.ts, folgen.ts (Merge), slug.ts, rotation.ts, platzhalter.ts, format.ts
│  ├─ components/           # siehe Kapitel 6.6
│  ├─ layouts/Base.astro
│  ├─ pages/                # siehe Kapitel 5
│  ├─ scripts/              # menu.ts, player.ts, motion.ts, filter.ts
│  └─ styles/               # tokens.css, base.css, fonts.css, motion.css
├─ scripts/                 # platzhalter-report.mjs, check-links.mjs, feed-update.mjs, visual-qa.mjs
├─ tests/                   # Playwright
└─ .github/workflows/deploy.yml
```

### 3.3 Umgebungsvariablen (Build)

| Variable | Default | Zweck |
|---|---|---|
| `SITE_URL` | `https://vucablaster.de` | `site` in `astro.config.mjs`, Canonicals, Sitemap, OG |
| `BASE_PATH` | `/` | nur falls vor der Domain unter `*.github.io/<repo>/` getestet wird |
| `FEED_URL` | Wert aus `site.yaml` | Überschreiben für Tests |
| `FEED_OFFLINE` | `false` | `true` = nur Snapshot verwenden |

Alle internen Links und Assets MÜSSEN `import.meta.env.BASE_URL` respektieren, damit ein Test unter `/<repo>/` funktioniert.

---

## 4. Inhaltsmodell

### 4.1 Quellen und Vorrang

1. **RSS-Feed** (Build-Zeit): Titel, Datum, Beschreibung/Shownotes, Audio-Datei (Enclosure), Dauer, Folgenbild, GUID, ggf. `itunes:episode`.
2. **YAML-Overrides** `src/content/folgen/<nr>.yaml`: alles, was der Feed nicht hat (Staffel, Position, Werte, Gast-Rolle, Key Learnings, Foto, Deep-Links, Video).
3. Override schlägt Feed bei gleichem Feld (z. B. ein kürzerer Anzeigetitel).

**Feed-URL:** `https://evjjod.podcaster.de/VUCABlaster.rss` – [[OFFEN: Feed-URL bei podcaster.de bestätigen; aus der Entwicklungsumgebung war sie nicht erreichbar]].

### 4.2 RSS-Import (MUSS)

- Eigener Loader im Content Layer (`src/content.config.ts`), Collection `rssFolgen`.
- Timeout 10 s, 2 Wiederholungen. Schlägt der Abruf fehl oder ist `FEED_OFFLINE=true`: `src/data/feed-snapshot.xml` verwenden und im Build-Log **deutlich warnen**. Der Build darf wegen des Feeds **nie** fehlschlagen.
- `npm run feed:update` lädt den Feed und überschreibt den Snapshot (lokal oder in CI manuell auslösbar).
- **Folgennummer ermitteln:** zuerst `itunes:episode`, dann Titel-Regex `^#(\d+)`, sonst Zuordnung über `guid` in der Override-Datei. Folgen ohne ermittelbare Nummer bekommen **keine** erfundene Nummer; sie erscheinen im Archiv mit Datum und landen im Platzhalter-Report („Nummer fehlt“).
- Titel bereinigen für die Anzeige: führendes `#62 – ` bzw. `#62 ` entfernen, wenn die Nummer separat angezeigt wird; Gastname am Ende (`… mit Claudia Jahn`) nur entfernen, wenn der Gast im Override steht.
- Shownotes: `sanitize-html` mit Whitelist (`p, br, a, ul, ol, li, strong, em`), Links `rel="noopener"` und `target` nicht setzen. Keine Bilder/iframes aus dem Feed übernehmen.
- Trailer/Bonus-Folgen (`itunes:episodeType` = `trailer`/`bonus`) nicht mitzählen, aber im Archiv zeigen, wenn vorhanden.

### 4.3 Collections und Felder

Alle Schemas mit Zod in `content.config.ts`. Felder, die Platzhalter enthalten dürfen, als `string` typisieren.

**`site.yaml`**

```yaml
name: "VUCA Blaster"
claim: "Die Welt ist komplex. Wir sehen darin Gestaltungsraum."
claim_markiert: "Gestaltungsraum"      # Wort mit rotem Kringel
aussprache_ipa: "[ˈvuːka ˈblaːstɐ]"
aussprache_klartext: "Wuka Blaster"     # für Screenreader
beschreibung_meta: "…"                  # ≤ 155 Zeichen
start_jahr: 2020
rhythmus: "alle zwei Wochen neu"
feed_url: "https://evjjod.podcaster.de/VUCABlaster.rss"
livegang: false
kontakt:
  email_gaeste: "[[PFLICHT: E-Mail für Gastanfragen]]"
  email_allgemein: "[[OFFEN: allgemeine E-Mail, sonst wie oben]]"
plattformen:                            # Reihenfolge = Anzeige-Reihenfolge
  - { name: "Spotify", url: "https://open.spotify.com/show/3OQW0akZgxBxK4AWFQSKtf", primaer: true }
  - { name: "Apple Podcasts", url: "https://podcasts.apple.com/de/podcast/vuca-blaster/id1541461336", primaer: true }
  - { name: "Deezer", url: "[[OFFEN: Deezer-Link]]", primaer: false }
  - { name: "Amazon Music", url: "[[OFFEN: Amazon-Music-Link]]", primaer: false }
  - { name: "podcast.de", url: "[[OFFEN: podcast.de-Link prüfen]]", primaer: false }
social: []                              # LinkedIn-Seite o. ä.
```

**`hosts.yaml`** – Liste: `name`, `slug`, `rolle`, `bio_kurz` (≤ 300 Zeichen), `bio_lang` (Markdown), `foto` (Pfad), `foto_credit`, `links[] {label, url}`.

**`werte.yaml`** – genau 5 Einträge, Reihenfolge wie im Design: `slug` (`optimistisch`, `neugierig`, `mutig`, `authentisch`, `verbindend`), `name`, `farbe` (Token-Name), `beschreibung` (1–2 Sätze).

**`staffeln.yaml`** – Liste: `slug`, `titel` („Mut“), `wert` (Slug), `jahr`, `status` (`laufend` | `abgeschlossen` | `geplant`), `folgen_geplant` (Zahl), `zeitraum_text` („läuft bis Jahresende“), `beschreibung`, `marker_notiz` (optional, überschreibt die Automatik aus 7.4).

**`folgen/<nr>.yaml`**

```yaml
nummer: 62
guid: ""                     # nur nötig, wenn Nummer nicht aus dem Feed kommt
slug: "62-claudia-jahn"      # wird beim ersten Build erzeugt und danach nie mehr geändert
staffel: "mut"
staffel_position: 4
hauptwert: "mutig"
nebenwerte: ["authentisch"]
gast:
  name: "Claudia Jahn"
  rolle_kurz: "Schauspielerin"                               # Kanban-Karte
  rolle_lang: "Schauspielerin, Sprecherin, Executive Coach"  # Folgenkopf
  foto: "[[OFFEN: Foto + Nutzungsrecht]]"
  foto_credit: ""
  links: []
key_learnings:
  - "Wirklich mutige Menschen fühlen sich oft gar nicht mutig."
  - "„Wie wirke ich?“ ist vielleicht die falsche Frage."
  - "Mut beginnt mit Stimmigkeit, nicht mit Überwindung."
plattform_links:             # Deep-Links zur Folge; fehlt einer → Show-Link verwenden
  spotify: ""
  apple: ""
video_url: ""                # leer = kein Video-Umschalter
```

**`archiv.yaml`** – Flipchart der Startseite: `label` („Protokoll 2020 bis 2025“), `titel` („Methoden und Organisations­entwicklung“ – mit weichem Trennstrich), `stichworte[]` („Selbstorganisation“, „Loop Approach“, „Fehlerkultur“), `text`.

**`seiten/*.md`** – Frontmatter `titel`, `label`, `beschreibung_meta`; Body in Markdown.

### 4.4 Slugs und Kurzlinks (MUSS)

- Folgen-URL: `/folgen/<nr>-<gast-oder-titel>/`, z. B. `/folgen/62-claudia-jahn/`. Ohne Nummer: `/folgen/<jjjj-mm-tt>-<titel>/`.
- **Slugs sind nach dem ersten Livegang eingefroren.** Beim ersten Build erzeugte Slugs werden in `src/data/slugs.lock.json` geschrieben und committed; spätere Titeländerungen ändern die URL nicht.
- **Kurzlinks** für LinkedIn: `/62/` → Weiterleitungsseite auf die Folgen-URL (statische Seite mit `<meta http-equiv="refresh" content="0;url=…">`, `<link rel="canonical">` und sichtbarem Link). Für jede nummerierte Folge.
- Weitere Kurzlinks: `/gast/` → `/fuer-gaeste/`, `/mut/` → `/staffeln/mut/`.
- Umlaute im Slug transliterieren (ä→ae, ö→oe, ü→ue, ß→ss).

### 4.5 Platzhalter-System (MUSS)

| Marker | Bedeutung | Öffentlich | Dev |
|---|---|---|---|
| `[[PFLICHT: …]]` | blockiert den Livegang | Build bricht ab, wenn `livegang: true` | gestrichelter Kasten, Rot-Rand, Text sichtbar |
| `[[OFFEN: …]]` | fehlt, blockiert nicht | Feld gilt als leer → Fallback der Komponente | gestrichelter Kasten, Grau-Rand, Text sichtbar |

- `src/lib/platzhalter.ts`: `istPlatzhalter(v)`, `wert(v)` (gibt `undefined` für Platzhalter zurück), `<Platzhalter>`-Komponente für Dev.
- **Jede Komponente definiert ihr Fallback**: Button ohne URL wird nicht gerendert; Bio ohne Text → Abschnitt ausblenden; Foto fehlt → Folgenbild aus dem Feed im selben Rahmen, sonst schraffierte Fläche ohne Beschriftung.
- `npm run platzhalter` durchsucht `src/content/**` und die gemergten Folgen und schreibt `PLATZHALTER-REPORT.md`: gruppiert nach PFLICHT/OFFEN, mit Datei und Zeile, plus automatisch erkannte Lücken (Folge ohne Nummer, Folge ohne Hauptwert in einer Themenstaffel, Gast ohne Rolle, Plattform ohne URL).
- In CI wird der Report in die Job-Zusammenfassung geschrieben (`$GITHUB_STEP_SUMMARY`).

---

## 5. Seiten und Routen

| Route | Inhalt | Phase |
|---|---|---|
| `/` | Startseite, exakt D3 | 1 |
| `/folgen/` | Archiv aller Folgen mit Filter (Staffel, Wert, Jahr) | 2 |
| `/folgen/<slug>/` | Folgenseite | 2 |
| `/<nr>/` | Kurzlink → Folgenseite | 2 |
| `/staffeln/<slug>/` | Staffelseite (Kanban) – `mut`, `optimismus` | 3 |
| `/themen/` | Übersicht der 5 Werte (Karten-Cluster) | 3 |
| `/themen/<wert>/` | Folgen je Wert | 3 |
| `/ueber-uns/` | Was ist ein VUCA Blaster? · Hosts · Haltung | 3 |
| `/fuer-gaeste/` | Infos für Gäste + Kontakt | 3 |
| `/kontakt/` | Kontaktwege | 3 |
| `/impressum/` | Impressum | 3 |
| `/datenschutz/` | Datenschutzerklärung | 3 |
| `/404` | Fehlerseite | 3 |
| `/sitemap-index.xml`, `/robots.txt` | automatisch | 4 |

Navigation (wie Design): **Folgen · Themen · Über uns · Für Gäste · Kontakt**. „Für Gäste“ ist als rosé Zettel hervorgehoben (−2°). Aktive Seite: `aria-current="page"` + 3 px Unterstrich in Petrol, Offset 6 px.

### 5.1 Seitenaufbau-Muster für Unterseiten

Das Design liefert nur die Startseite. Unterseiten MÜSSEN aus denselben Bausteinen gebaut werden (Kapitel 6.6) und diesen Mustern folgen:

- **Seitenkopf = kleines Board:** Rahmen `#D9D6CF` (12 px Desktop / 8 px Mobile, unten offen), Punktraster, Padding 56/28 px, darin Label (18/16 px, 700, `#5E5A55`) + h1 (80/50 px, 800, −0.045em) + optional Intro (20/17 px). Markerleiste unten wie auf der Startseite, aber nur ein Stift (Petrol). Höchstens **ein** Handelement pro Seitenkopf.
- **Abschnitte** durch `border-top: 2px solid #161414` getrennt, Padding 88/48 px oben, 96/56 px unten (wie Startseite).
- **Fließtext-Seiten** (Impressum, Datenschutz, Bios): max. 68 ch, 20/17 px, Zeilenhöhe 1.5, keine Drehungen.

### 5.2 Folgenseite `/folgen/<slug>/`

Aufbau spiegelt den Abschnitt „Aktuelle Folge“ der Startseite:

1. Seitenkopf-Board mit Meta-Zeile (Label „Folge #62“ schwarz + „Staffel Mut, 4 von 8 · 24.09.2026 · 51 Min.“), h1 = Titel (Folgentitel-Größe 72/40), Gast + Rolle, Werte-Labels.
2. Zweispaltig (≥ 1024 px) wie Startseite: links „Diese Folge hören“ + Plattform-Buttons + Hinweis; rechts Foto-Abzug + Player-Blatt.
3. Key Learnings (3 Haftnotizen), falls vorhanden.
4. Shownotes (Fließtext-Muster) unter der Überschrift „Shownotes“.
5. „Mehr aus der Staffel Mut“ – Mini-Kanban mit den anderen Folgen der Staffel (max. 4 Karten sichtbar, Rest verlinkt).
6. Vor/Zurück-Navigation (vorige/nächste Folge nach Datum).

Ältere Folgen ohne Overrides zeigen nur 1, 2 (ohne Foto → Folgenbild), 4, 6. Kein leerer Abschnitt.

### 5.3 Archiv `/folgen/`

- Seitenkopf: Label „Archiv“, h1 „Alle 62 Folgen“ (Zahl dynamisch), Intro aus `archiv.yaml`.
- Filterleiste: Staffel · Wert · Jahr als Umschalt-Buttons im Magnet-Stil (Kreis 18 px + Text; aktiv = gefüllter Türkis-Magnet mit Rand). Mehrfachauswahl nein, je Gruppe ein Wert. Zustand in URL-Parametern (`?wert=mutig&jahr=2026`), damit Links teilbar sind. **Ohne JS:** alle Folgen sichtbar, Filter-Buttons sind Links auf `/themen/<wert>/` bzw. `/staffeln/<slug>/`.
- Liste gruppiert nach Jahr als **Protokoll-Blätter** (weißes Blatt, grauer Kopfbalken 20 px wie das Flipchart der Startseite, gerade, keine Drehung – Lesbarkeit geht vor). Zeile: `#62` (Petrol, 700) · Titel (700) · Gast · Datum · Dauer · Werte-Punkte. Ganze Zeile klickbar, Mindesthöhe 56 px.
- Suche KANN (Phase 4+): einfaches Textfeld, filtert Titel + Gast clientseitig, ohne Library.
- Keine 62 Haftnotizen. Haftnotizen sind für Hervorhebung reserviert.

### 5.4 Staffelseite `/staffeln/<slug>/`

Seitenkopf mit Label „Themenstaffel 2026 · läuft bis Jahresende“, h1 „Staffel Mut“, Beschreibung. Darunter Magnet-Reihe + „4 von 8 Folgen veröffentlicht“ + Kanban exakt wie auf der Startseite, aber jede veröffentlichte Karte zusätzlich mit Folgentitel (17 px) und Link. Abgeschlossene Staffel: nur Spalte „Veröffentlicht“, Magnet-Reihe voll, Marker-Notiz „Geschafft!“.

### 5.5 Themen `/themen/` und `/themen/<wert>/`

- `/themen/`: Karten-Cluster wie Startseite (Abschnitt 5) mit Überschrift „Fünf Werte, ein Cluster“ + je Karte die Beschreibung aus `werte.yaml` darunter als Liste (für Screenreader und Mobile).
- `/themen/<wert>/`: Seitenkopf in der Kartenfarbe des Werts (Kopf-Board bleibt weiß; die große Werte-Karte sitzt als gedrehte Moderationskarte rechts im Kopf, 400 px, wie „mutig“ auf der Startseite). Darunter: „Hauptwert“-Liste, dann „Kommt auch vor in“ (Nebenwert). **Leerzustand:** „Zu diesem Wert gibt es noch keine Themenstaffel. Die Folgen der Staffel Mut findest du hier: …“ – keine leere Seite.

### 5.6 Über uns `/ueber-uns/`

1. Seitenkopf: Label „Über uns“, h1 „Was ist ein VUCA Blaster?“, darunter Aussprache (IPA) und die Definition als **Lexikon-Karte** (weißes Blatt, 2 px Tinte, Wortart-Zeile „Substantiv, der“ in Petrol, Definitionstext 24/20 px). Text: [[PFLICHT: Definition „VUCA Blaster“]].
2. Hosts: je Host ein **Foto-Abzug mit Klebeband** (wie Gastfoto, 300 × 360, gedreht ±2°) + Name (40/28, 800) + Rolle + Kurz-Bio + Links. Zwei Spalten ab 768 px. [[PFLICHT: Host-Profile]].
3. „Warum wir das machen“ – Fließtext [[OFFEN: Warum-Text]], optional mit einem Marker-Kringel um ein Wort.
4. Werte-Kurzform: Liste der 5 Werte mit Beschreibung, Link zu `/themen/`.

### 5.7 Für Gäste `/fuer-gaeste/`

1. Seitenkopf: Label „Für Gäste“, h1 „Lust auf ein Gespräch?“ [[OFFEN: Headline bestätigen]], Intro.
2. „So läuft's ab“ – 3 Schritte als Haftnotizen (eine Reihe, max. 3), Inhalte [[OFFEN: Ablauf]].
3. „Was wir von dir brauchen“ – Checkliste (Foto, Kurz-Bio, Rolle, Links), als Liste mit Magnet-Punkten.
4. „Wer schon da war“ – Gäste-Wand: Namen + Rolle der letzten 12 Gäste als kleine Karten (keine Fotos, keine Logos), Link „Alle Folgen“.
5. Kontakt-Block: großer Primär-Button „Gastanfrage per E-Mail“ (`mailto:` mit Betreff „Gastanfrage VUCA Blaster“) + Hinweis zur Antwortzeit [[OFFEN]].

### 5.8 Kontakt, Impressum, Datenschutz, 404

- **Kontakt:** E-Mail-Adressen (als `mailto:`), LinkedIn-Profile der Hosts, Hinweis „Für Gastanfragen → Für Gäste“. **Kein Formular** (bräuchte Backend + Datenschutz-Aufwand).
- **Impressum / Datenschutz:** Fließtext-Muster, Inhalt vollständig aus `seiten/*.md`. Solange PFLICHT offen: Seite existiert, zeigt im Dev den Platzhalter.
- **404:** Kleines Board, Marker-Notiz „Hier steht noch nichts.“ (Permanent Marker, Petrol, −4°), darunter Links: Startseite, Alle Folgen, Aktuelle Folge.

### 5.9 Footer (nicht im Design – so bauen)

Hintergrund `#FAFAF7`, `border-top: 2px solid #161414`, Padding 56/40 px. Drei Spalten ab 1024 px, sonst gestapelt:

1. Wortmarke „VUCA Blaster“ (26/22, 800) + Claim (17 px, `#5E5A55`).
2. Links: Folgen · Themen · Über uns · Für Gäste · Kontakt.
3. Hören auf: Plattform-Links als Text-Links + RSS-Feed-Link.

Unterzeile (14 px, `#5E5A55`): „© 2020–<aktuelles Jahr> VUCA Blaster · Impressum · Datenschutz“. Keine Deko-Elemente im Footer.

---

## 6. Designsystem D3 „Whiteboard nach dem Workshop“

**Idee:** Die Seite sieht aus wie das Whiteboard nach einem guten Workshop. Helle Fläche, Marker, Haftnotizen, Magnete, Moderationskarten, Flipchart-Protokoll. Das Material trägt die Farben, nicht Verläufe oder Schatten. **Signatur:** die quadratische Haftnotiz mit Magnet.

### 6.1 Farb-Tokens (MUSS, `src/styles/tokens.css`)

```css
:root {
  color-scheme: light;
  /* Flächen */
  --c-page:    #FAFAF7;  /* Seitengrund */
  --c-board:   #FFFFFF;  /* Whiteboard, Papier */
  --c-frame:   #D9D6CF;  /* Board-Rahmen, Markerleiste, Papierkanten */
  --c-dot:     #E4E1DA;  /* Punktraster */
  --c-tape:    #EDE8DA;  /* Klebeband */
  --c-archive: #F1EFE9;  /* Archiv-Fläche, Foto-Platzhalter */
  --c-hatch:   #DEDAD2;  /* Schraffur */
  /* Marke */
  --c-ink:     #161414;  /* Marker Schwarz – Text 17,5:1 auf Page */
  --c-petrol:  #046464;  /* Marker Petrol – 6,7:1 auf Page, Fokus */
  --c-violet:  #80027D;  /* Moderationskarte „mutig“ – Weiß darauf 9,4:1 */
  --c-rose:    #F5D7D7;  /* Haftnotiz Rosé */
  --c-aqua:    #7AE7F2;  /* Haftnotiz Aqua */
  --c-teal:    #04B8B2;  /* Magnet – nur mit 2–3 px Tinte-Rand, nie Text */
  --c-red:     #E9022C;  /* Marker Rot – nur Kringel und Marker-Notizen ≥ 24 px */
  /* Text */
  --c-muted:   #5E5A55;  /* Sekundärtext 6,5:1 auf Page */
  --c-dashed:  #8D877E;  /* gestrichelte Rahmen „kommt bald“ (3,4:1, nur Nicht-Text) */
}
```

Gemessene Kontraste (WCAG): Petrol auf Rosé 5,2:1 · Petrol auf Aqua 4,8:1 · Tinte auf Aqua 12,7:1 · Muted auf Archiv 5,95:1. Alle Textpaare im Design bestehen AA. Neue Kombinationen MÜSSEN geprüft werden (Petrol auf Aqua nur ≥ 16 px fett).

### 6.2 Schriften (MUSS)

| Rolle | Schrift | Paket / Datei | Einsatz |
|---|---|---|---|
| Alles | Bricolage Grotesque (variabel, wght + opsz) | `@fontsource-variable/bricolage-grotesque/opsz.css` | 800 Headlines mit enger Laufweite, 700 Notizen/Labels, 400–600 Text |
| Randbemerkung | Permanent Marker | `@fontsource/permanent-marker/latin-400.css` | nur Marker-Notizen („hier reinhören!“, „Halbzeit!“), max. 3 Handelemente pro Screen |
| Lautschrift | Andika | `@fontsource/andika/latin-400.css` + `latin-ext-400.css` | nur `[ˈvuːka ˈblaːstɐ]` – Bricolage hat keine IPA-Zeichen |

- Fallbacks: `'Trebuchet MS', sans-serif` bzw. `'Comic Sans MS', cursive` (wie Referenz), zusätzlich `size-adjust`-Fallback-Face für Bricolage, damit der Schriftwechsel keinen Layout-Sprung erzeugt.
- `font-display: swap`. Preload **nur** die Bricolage-Latin-Datei.
- `font-optical-sizing: auto` (Standard) – die opsz-Achse ist Teil des Looks bei großen Graden.
- Deutsche Texte: `lang="de"`, `hyphens: manual` für Headlines (weiche Trennstriche in den Daten, z. B. `Organisations­entwicklung`), `text-wrap: balance` für h1/h2, `text-wrap: pretty` für Fließtext. Typografische Anführungszeichen „ “, Halbgeviertstrich –, geschützte Leerzeichen in „#62“, „Mut 4/8“, „4 von 8“.

### 6.3 Typo-Skala (fluid zwischen 390 und 1440 px Viewport)

Bei genau 390 und 1440 px ergeben sich exakt die Werte des Designs.

| Rolle | 390 | 1440 | CSS |
|---|---|---|---|
| Display h1 (Startseite) | 88 | 156 | `clamp(5.5rem, 3.921rem + 6.476vw, 9.75rem)` |
| Staffel-Titel | 60 | 96 | `clamp(3.75rem, 2.914rem + 3.429vw, 6rem)` |
| Seiten-h1 / Archiv-h2 | 50 | 80 | `clamp(3.125rem, 2.429rem + 2.857vw, 5rem)` |
| Folgentitel h2 | 40 | 72 | `clamp(2.5rem, 1.757rem + 3.048vw, 4.5rem)` |
| Werte-h2 | 46 | 72 | `clamp(2.875rem, 2.271rem + 2.476vw, 4.5rem)` |
| Claim | 32 | 54 | `clamp(2rem, 1.489rem + 2.095vw, 3.375rem)` |
| Werte-Karte „mutig“ | 56 | 72 | `clamp(3.5rem, 3.129rem + 1.524vw, 4.5rem)` |
| Werte-Karte | 25 | 40 | `clamp(1.562rem, 1.214rem + 1.429vw, 2.5rem)` |
| Aussprache (IPA) | 21 | 30 | `clamp(1.312rem, 1.104rem + 0.8571vw, 1.875rem)` |
| Marker-Notiz | 24 | 32 | `clamp(1.5rem, 1.314rem + 0.7619vw, 2rem)` |
| Haftnotiz-Nummer | 36 | 44 | `clamp(2.25rem, 2.064rem + 0.7619vw, 2.75rem)` |
| Haftnotiz-Text | 24 | 29 | `clamp(1.5rem, 1.384rem + 0.4762vw, 1.812rem)` |
| Kanban-Name | 24 | 27 | `clamp(1.5rem, 1.43rem + 0.2857vw, 1.688rem)` |
| Gastname | 21 | 26 | `clamp(1.312rem, 1.196rem + 0.4762vw, 1.625rem)` |
| Wortmarke | 22 | 26 | `clamp(1.375rem, 1.282rem + 0.381vw, 1.625rem)` |
| Fließtext | 17 | 20 | `clamp(1.062rem, 0.9929rem + 0.2857vw, 1.25rem)` |
| Label | 16 | 18 | `clamp(1rem, 0.9536rem + 0.1905vw, 1.125rem)` |

Laufweiten: Display −0.05em · Staffel/Archiv −0.045em · Folgentitel −0.035em · Werte-h2 und Werte-Karten −0.04/−0.03em · Claim −0.025em · Haftnotiz −0.015em. Zeilenhöhen siehe Referenz (Display 0.86, Staffel 0.95, Folgentitel 1.0, Claim 1.08, Haftnotiz 1.15, Text 1.5).

Unter 390 px (bis 320 px) MUSS alles ohne horizontales Scrollen funktionieren: Display darf dort auf 72 px fallen (`min()` zusätzlich zum `clamp`).

### 6.4 Raster, Abstände, Form

- Seitenrand: 64 px (≥ 1024) / 16 px (< 600), dazwischen fluid. Max. Inhaltsbreite 1440 px, darüber zentriert, Seitengrund läuft durch.
- Abstands-Skala: 12 · 18 · 28 · 44 · 88 px (+ 8, 22, 64, 104 wie in der Referenz).
- Ecken: Buttons und Labels 4 px, Papier/Notizen/Karten 0 px.
- **Keine Schatten, keine Verläufe, keine Glas-Effekte.** Tiefe entsteht nur durch Drehung, Überlappung, Klebeband und Magnete.
- Drehung: Papier −3.5° bis +3.5°, Buttons, Labels und Fließtext 0°. Fließtext nie gedreht außer in Haftnotizen/Karten.

### 6.5 Breakpoints

| Name | Breite | Verhalten |
|---|---|---|
| S | < 600 | Mobile-Referenz (`D3-Mobile.html`), muss bis 320 px funktionieren |
| M | 600–1023 | Mobile-Struktur, breitere Spalten; Kanban „Veröffentlicht“ 2-spaltig; Key Learnings bleiben gestaffelt untereinander (max. 2 nebeneinander) |
| L | 1024–1279 | Desktop-Struktur, Hero **einspaltig**: Haftnotiz „Neu · #62“ rutscht unter die Plattform-Buttons, rechtsbündig, 280 px; Desktop-Navigation sichtbar |
| XL | ≥ 1280 | Desktop-Referenz (`D3-Desktop.html`); bei 1440 pixelgenau |

Header: Desktop-Navigation ab 1024 px, darunter „Für Gäste“-Zettel + Button „Menü“ (Mobile-Referenz).
Abnahme: keine Überlappung von Text, kein horizontales Scrollen, keine abgeschnittenen Wörter bei 320, 390, 600, 768, 1024, 1280, 1440, 1920 px und bei 200 % Browser-Zoom.

### 6.6 Komponentenkatalog (MUSS, `src/components/`)

| Komponente | Referenz | Kern |
|---|---|---|
| `SiteHeader` | Header | Wortmarke-Link (≥ 44 px Höhe), Nav, „Für Gäste“-Zettel (Rosé, −2°), `MobileMenu` |
| `MobileMenu` | Button „Menü“ | Disclosure-Muster: `button[aria-expanded][aria-controls]`, Liste darunter als weißes Blatt mit 2 px Tinte, schließt mit Esc und bei Klick außerhalb, Fokus bleibt logisch. Kein Fokus-Trap, kein Overlay. |
| `Board` | Hero-Section | Rahmen (12/8 px, unten offen), Punktraster (SVG-Pattern 28/22 px, r 1.6/1.4, `--c-dot`), Slot, `MarkerTray` |
| `MarkerTray` | graue Leiste | 26/18 px hoch, 3 Stifte 110×12 / 60×8, Farben Tinte/Petrol/Rot, `aria-hidden` |
| `MarkerCircle` | Kringel um „Gestaltungsraum“ | SVG-Pfad aus Referenz, `pathLength="1000"`, Strich 4.5 (Desktop) / 6 (Mobile, weil skaliert), Animation A1 |
| `MarkerNote` | „hier reinhören!“, „Halbzeit!“ | Permanent Marker, Petrol oder Rot, −5° / −6°, dekorativ (`aria-hidden`, Inhalt steht auch als echter Text daneben) |
| `HandArrow` | Pfeil | SVG aus Referenz, Petrol, `aria-hidden` |
| `StickyNote` | Haftnotiz | Quadrat, Farbe Rosé/Aqua, Drehung, optional `Magnet` oben mittig. Varianten: `link` (ganze Notiz ist ein Link), `learning` (Nummer + Text, in `<ol>`) |
| `Magnet` | Kreis | 36/38/34 px, Türkis + 3 px Tinte-Rand (gefüllt) oder 3 px gestrichelt `--c-dashed` (leer) |
| `PlatformButtons` | Hören-Buttons | primär = Tinte gefüllt, 20/18 px 700, Padding 17×28; sekundär = 2 px Tinte-Rand, 18/16 px 600; fehlende URL → nicht rendern; Mobile: Primäre im 2-Spalten-Grid |
| `ValueLabel` | Werte-Labels | Hauptwert: Petrol gefüllt + Aqua-Punkt, Text „mutig · Hauptwert“; Nebenwert: 2 px Petrol-Rand + leerer Kreis; Link auf `/themen/<wert>/` |
| `PhotoPrint` | Foto mit Klebeband | weißer Rahmen 14 px, 1.5 px `--c-frame`, Drehung 2°, Klebeband 110×28 (−4°); Bild `object-fit: cover`; ohne Bild → Schraffur |
| `PlayerSheet` | Player-Blatt | Blatt mit 2 Klebestreifen (±30°), Drehung −0.8°, Umschalter Audio/Video (`aria-pressed`), 2-Klick-Logik (Kapitel 9) |
| `KanbanCard` | Staffel-Karten | min. 136 px hoch, Farben/Drehungen im Muster Rosé −1° · Weiß mit Rand +0.8° · Aqua +0.6° · Rosé −1.4° (zyklisch); neueste Folge: 3 px Tinte-Outline innen + Zusatz „· #62 · neu“ |
| `KanbanSlot` | „kommt bald“ | 2 px gestrichelt `--c-dashed`, Text Muted |
| `MagnetRow` | Staffel-Fortschritt | n Magnete, gefüllt = veröffentlicht; darunter echter Text „4 von 8 Folgen veröffentlicht“; Magnete `aria-hidden` |
| `ValueCard` | Moderationskarte | Farben: optimistisch Rosé · neugierig Weiß + 2 px Tinte · mutig Violett/Weiß · authentisch Petrol/Weiß · verbindend Aqua; Status-Zeile (Kapitel 7.5) |
| `ValueCluster` | 5 Karten | ≥ 1280 px absolut positioniert wie Referenz (Positionen in % der Containerbreite umrechnen, Höhe 470 px); 600–1279 px Flex-Wrap mit Drehungen; < 600 Mobile-Referenz. DOM-Reihenfolge = optimistisch, neugierig, mutig, authentisch, verbindend |
| `FlipchartStack` | Archiv-Stapel | 3 Blätter (+5°, −3°, 0°), oberstes mit 20 px Kopfbalken, `aria-hidden` (Inhalt steht als Text daneben) |
| `ProtocolSheet` | Archivliste | gerades weißes Blatt mit Kopfbalken, Zeilen wie 5.3 |
| `LexiconCard` | Über uns | Definition, IPA, Wortart |
| `SectionHead` | Label + h2 | Label 18/16 px 700 Muted, h2 in Skala |
| `SiteFooter` | – | Kapitel 5.9 |
| `Platzhalter` | – | nur Dev (Kapitel 4.5) |

**Drehungen bei generierten Listen:** `rotation.ts` bildet `hash(slug)` auf die Menge `[-3, -1.4, -1, 0.6, 0.8, 2, 3]` ab. Deterministisch, damit Builds identisch sind.

### 6.7 Regeln für alles, was das Design nicht zeigt

1. Nur Bausteine aus 6.6 kombinieren; neue Bausteine müssen aus dem Whiteboard-Material stammen (Papier, Notiz, Magnet, Karte, Marker, Klebeband, Flipchart).
2. Max. 3 Handelemente pro Bildschirmhöhe, max. 3 Haftnotizen nebeneinander, max. eine Violett-Fläche pro Seite.
3. Rot nur für Kringel und kurze Marker-Notizen. Türkis nur für Magnete.
4. Lesbarkeit vor Deko: Listen, Rechtstexte, Shownotes sind gerade und ruhig.
5. Keine Icons-Bibliotheken. Pfeile als Text „→“, Play-Dreieck als Inline-SVG wie in der Referenz.

---

## 7. Startseite – Abschnitt für Abschnitt

Maße: exakt nach `docs/design/D3-Desktop.html` und `D3-Mobile.html`. Hier nur Datenbindung und Verhalten.

### 7.1 Header
Wie 6.6 `SiteHeader`. Wortmarke verlinkt auf `/`.

### 7.2 Hero (Board)
- h1 „VUCA<br>Blaster“ – einzige h1 der Startseite.
- Aussprache: sichtbar `[ˈvuːka ˈblaːstɐ]` (`aria-hidden="true"`), dazu `<span class="sr-only">Aussprache: Wuka Blaster</span>`. Quelle `site.yaml`.
- Claim als `<p>`, Wort aus `claim_markiert` bekommt `MarkerCircle` (Animation A1).
- „hier reinhören!“ + Pfeil zeigen auf die Plattform-Buttons (dekorativ).
- `PlatformButtons` aus `site.yaml` (Show-Links).
- Zeile: `{anzahl} Folgen seit {start_jahr} · {rhythmus}` – `anzahl` aus dem Feed (ohne Trailer/Bonus).
- Haftnotiz rechts (nur ≥ 1024 px; Mobile-Referenz hat sie nicht): neueste Folge. Kopfzeile „Neu · #62“, wenn die Folge ≤ 21 Tage alt ist, sonst „Aktuell · #62“. Titel, „mit {gast} →“. Link auf `#aktuell`.
- `MarkerTray` unten.

### 7.3 Aktuelle Folge (`id="aktuell"`)
- Neueste Folge nach Datum (kein Trailer).
- Meta-Zeile: schwarzes Label „Aktuelle Folge“ + „#62 · Staffel Mut, 4 von 8“ (Mobile: „#62 · Mut 4/8“). Ohne Staffel: „#62 · 24. September 2026“.
- h2 = Titel, mit `sr-only`-Präfix „#62 – “.
- Gast (Name 26/21 px 700), `rolle_lang` (19/15 px Muted). Ohne Gast: Zeile weglassen.
- `ValueLabel`s (Hauptwert, Nebenwerte).
- „Diese Folge hören“: `PlatformButtons` mit Deep-Links der Folge (Fallback Show-Links) + Hinweis „Am besten auf Spotify oder Apple Podcasts: Dort hilft jedes Abo und jede Bewertung dem Podcast.“
- Rechts: `PhotoPrint` (Gastfoto → sonst Folgenbild aus dem Feed → sonst Schraffur ohne Text), darunter `PlayerSheet`. Mobile: kleines Foto (76 px, −3°) neben dem Gastnamen, Player-Blatt nach den Buttons.
- „3 Key Learnings“: drei `StickyNote`s (Rosé −3° · Aqua +2° / +36 px · Rosé −1.2° / +8 px) nur wenn genau 3 vorhanden. Sonst Block weglassen.

### 7.4 Staffel (laufende Staffel)
- Staffel mit `status: laufend`; gibt es keine, die zuletzt abgeschlossene.
- Label „Themenstaffel {jahr} · {zeitraum_text}“, h2 „Staffel {titel}“.
- `MagnetRow` (n = `folgen_geplant`, gefüllt = veröffentlichte Folgen der Staffel) + „{x} von {n} Folgen veröffentlicht“.
- **Marker-Notiz automatisch** (falls `marker_notiz` leer): x = n/2 → „Halbzeit!“ · x = n−1 → „Endspurt!“ · x = n → „Geschafft!“ · sonst keine Notiz. Rot, −6°.
- Kanban: Spalte „Veröffentlicht {x}“ (Karten in Staffel-Reihenfolge, Label „Mut 1/8“, Name, `rolle_kurz`, Link zur Folge), Spalte „Kommt bald {n−x}“ (`KanbanSlot`s „Mut 5/8 · kommt bald“).

### 7.5 Werte
- h2 „Fünf Werte, ein Cluster“, Text „Jede Folge der Themenstaffeln hat genau einen Hauptwert. Nimm eine Karte und sieh, welche Folgen dahinterstecken.“ (Mobile: nur erster Satz).
- `ValueCluster`. Status-Zeile je Karte automatisch: Wert einer laufenden Staffel → „Staffel läuft · 4 von 8 · Folgen →“; Wert einer abgeschlossenen Staffel → „Staffel beendet · Folgen →“; sonst „Folgen →“. Mobile: „Staffel beendet →“ statt „Staffel beendet · Folgen →“.
- Links auf `/themen/<wert>/`. Das `<nav aria-label="Folgen nach Wert">` bleibt.

### 7.6 Archiv
- Hintergrund `--c-archive`. `FlipchartStack` mit Inhalt aus `archiv.yaml`.
- Label „Archiv“, h2 „Alle {anzahl} Folgen“, Text aus `archiv.yaml`, Button „Zum Archiv →“ auf `/folgen/`.
- Unter einer 2-px-Linie: je abgeschlossener Staffel „Themenstaffel {titel} · abgeschlossen“ + Gastnamen mit „ · “ getrennt, jeder Name verlinkt.

---

## 8. Animationen – dezent

### 8.1 Grundregeln (MUSS)

1. **Einmal, nicht in Schleife.** Keine Endlos-Animation, kein Autoplay, kein Parallax, kein Scroll-Jacking, keine Zähl-Animationen.
2. **Max. eine Auftritts-Animation pro Bildschirmhöhe.** Mikro-Interaktionen (Hover, Fokus, Drücken) zählen nicht.
3. Nur `transform`, `opacity`, `stroke-dashoffset`. Keine Layout-Eigenschaften animieren. CLS bleibt 0.
4. Alle Animationen stehen in `@media (prefers-reduced-motion: no-preference) { … }`. Bei `reduce` gibt es Zustände, aber keine Bewegung.
5. **Ohne JavaScript ist alles sichtbar.** Scroll-Auftritte werden nur aktiviert, wenn `<html class="js">` gesetzt ist und `IntersectionObserver` existiert. Ein Element, das der Observer nach 3 s nicht gemeldet hat, wird trotzdem sichtbar.
6. Das LCP-Element (h1) wird nie animiert.
7. JS für Motion: eine Datei `src/scripts/motion.ts`, < 1,5 KB.

### 8.2 Motion-Tokens

```css
:root {
  --ease-out:  cubic-bezier(.2, .7, .2, 1);
  --ease-snap: cubic-bezier(.34, 1.56, .64, 1);   /* leichtes Überschwingen, nur Magnete */
  --t-micro:   160ms;
  --t-short:   240ms;
  --t-reveal:  420ms;
  --t-draw:    1100ms;
  --stagger:   90ms;
}
```

### 8.3 Katalog

| # | Wo | Auslöser | Was | Dauer / Easing |
|---|---|---|---|---|
| A1 | Hero: Kringel um „Gestaltungsraum“ | Seitenaufruf | `stroke-dashoffset` 1000 → 0 (wie Referenz) | 1100 ms, `ease-out`, 400 ms Verzögerung |
| A2 | Hero: Pfeil + „hier reinhören!“ | direkt nach A1 | Pfeil zeichnet sich (dasharray), Notiz blendet ein (opacity 0 → 1, rotate −8° → −5°) | 500 ms + 300 ms, Start 1500 ms. **KANN** – nur wenn A1+A2 zusammen ruhig wirken, sonst weglassen |
| A3 | Key Learnings | Abschnitt 30 % sichtbar | Notizen „werden angeklebt“: opacity 0 → 1, `translateY(10px) rotate(Endwinkel ± 1.5°)` → Endzustand | 420 ms, `ease-out`, Stagger 90 ms |
| A4 | Staffel: Magnet-Reihe | Reihe sichtbar | gefüllte Magnete nacheinander: `scale(.6)` → 1, opacity 0 → 1; danach Marker-Notiz opacity 0 → 1 | je 240 ms `ease-snap`, Stagger 80 ms; Notiz 300 ms |
| A5 | Haftnotizen, Karten, Kanban-Karten | Hover / Fokus | Drehung → 0°, `translateY(-3px)` | 160 ms `ease-out` |
| A6 | Archiv: Flipchart-Stapel | Hover/Fokus auf „Zum Archiv →“ | oberstes Blatt `translateY(-4px) rotate(-1deg)` | 240 ms |
| A7 | Player-Blatt | Klick „Player laden“ | Hinweistext blendet aus, Player blendet ein (Höhe per `grid-template-rows: 0fr → 1fr`, Ausnahme von Regel 3, weil nutzerausgelöst) | 240 ms |
| A8 | Buttons | Hover / Aktiv | Hover: Farbwechsel (primär: Hintergrund Petrol; sekundär: Hintergrund Rosé); Aktiv: `translateY(1px)` | 120 ms |
| A9 | Seitenwechsel | Navigation | Cross-Document View Transition, nur Crossfade: `@view-transition { navigation: auto; }` | 180 ms; ohne Browser-Support einfach kein Effekt |
| A10 | Mobile-Menü | Öffnen / Schließen | opacity + `translateY(-4px)` → 0 | 150 ms |

Nicht erlaubt: bewegte Hintergründe, wackelnde Notizen, Marker, die sich „schreiben“ (außer A1/A2), Konfetti, Cursor-Effekte.

### 8.4 Code-Skizze (Orientierung, nicht wörtlich)

```css
@media (prefers-reduced-motion: no-preference) {
  .js [data-reveal] { opacity: 0; transform: translateY(10px) rotate(calc(var(--rot) + var(--rot-in, 1.5deg))); }
  .js [data-reveal].is-in {
    opacity: 1; transform: rotate(var(--rot));
    transition: opacity var(--t-reveal) var(--ease-out), transform var(--t-reveal) var(--ease-out);
    transition-delay: calc(var(--i, 0) * var(--stagger));
  }
}
```

```ts
// motion.ts
const els = document.querySelectorAll<HTMLElement>('[data-reveal]');
if (!matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) {
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
  }, { threshold: 0.3 });
  els.forEach((el) => io.observe(el));
  setTimeout(() => els.forEach((el) => el.classList.add('is-in')), 3000);
} else {
  els.forEach((el) => el.classList.add('is-in'));
}
```

Drehwinkel als Custom Property `--rot` am Element, damit Hover (A5) und Reveal (A3) denselben Endzustand kennen.

---

## 9. Player und Einbettungen (MUSS)

**Empfehlung (so umsetzen, sofern die Hosts nichts anderes entscheiden):**

- **Audio:** nativer `<audio controls preload="none">` mit der MP3-Datei aus dem Feed (Enclosure). Kein Fremd-Skript, keine Cookies, voll barrierefrei, im D3-Look einrahmbar. Die Datei liegt beim Podcast-Hoster (podcaster.de) → trotzdem Datenübertragung beim Abspielen, deshalb 2-Klick.
- **Video:** nur wenn `video_url` gesetzt ist. YouTube über `youtube-nocookie.com`, erst nach Klick. Ohne Video-URL: Umschalter Audio/Video ausblenden.

**2-Klick-Ablauf:**

1. Ausgangszustand wie Referenz: Blatt „Player“, Umschalter, Text „Der Player ist noch nicht geladen. Beim Laden werden Daten an {Anbieter} übertragen. Mehr in der Datenschutzerklärung.“, Button „Audio-Player laden“ (bzw. „Video-Player laden“).
2. `{Anbieter}` aus Konfiguration: Audio → „podcaster.de“ [[OFFEN: bestätigen, wo die Audiodateien liegen]], Video → „YouTube (Google)“.
3. Klick = Einwilligung für diesen Seitenaufruf → Player wird eingefügt, Audio startet sofort (Nutzergeste), Fokus springt auf den Player.
4. Keine Speicherung der Einwilligung (kein Cookie, kein localStorage). Ohne JS: Link „Folge direkt anhören (MP3)“ statt Button.

Test (MUSS): Beim Laden jeder Seite gehen **null** Requests an fremde Hosts. Erst nach Klick auf „Player laden“ genau die Requests an den genannten Anbieter.

---

## 10. Barrierefreiheit (WCAG 2.2 AA, MUSS)

- Landmarks: `header`, `nav` (Hauptnavigation, Folgen nach Wert), `main`, `footer`. Skip-Link „Zum Inhalt“ als erstes fokussierbares Element.
- Überschriften lückenlos (eine h1 pro Seite).
- Fokus: `outline: 3px solid var(--c-petrol); outline-offset: 3px` auf allen interaktiven Elementen, auch auf gedrehten Karten; nie `outline: none` ohne Ersatz.
- Touch-Ziele ≥ 44 × 44 px (Buttons, Nav-Links, Filter, Menü).
- Dekoratives (`MarkerTray`, Magnete, Kringel, Pfeil, Punktraster, Klebeband, Flipchart-Stapel) `aria-hidden="true"`; jede Information, die sie tragen, steht auch als Text.
- Links sind als ganze Karten klickbar, der zugängliche Name ist kurz (z. B. „Mut 1/8: Jennifer Wendland, Freitaucherin“) – keine verschachtelten Links.
- Umschalter Audio/Video: `role="group"` + `aria-pressed`. Menü: Disclosure mit `aria-expanded`.
- Bilder: echte Alt-Texte („Claudia Jahn“), dekorative `alt=""`.
- Sprache: `lang="de"`; englische Begriffe („Key Learnings“, „Loop Approach“) ohne `lang`-Wechsel, sie sind im Deutschen gebräuchlich.
- Reflow bei 320 px und 200 % Zoom ohne Informationsverlust.
- Automatisiert: axe ohne Verstöße auf allen Seitentypen. Manuell: einmal komplett mit Tastatur und mit VoiceOver (macOS) bzw. NVDA (Windows) durch.

---

## 11. Performance (MUSS)

| Messgröße | Ziel (mobil, Lighthouse, gedrosselt) |
|---|---|
| LCP | < 2,0 s |
| CLS | < 0,02 |
| INP | < 100 ms |
| JS Startseite | ≤ 15 KB gzip |
| CSS gesamt | ≤ 30 KB gzip |
| Schriften Startseite | ≤ 180 KB woff2 gesamt |
| Lighthouse | Performance ≥ 95, Accessibility 100, Best Practices 100, SEO 100 |

- Bilder über `astro:assets` (`<Image>`/`<Picture>`), AVIF + WebP, feste `width`/`height`, `loading="lazy"` außer im ersten Viewport.
- Punktraster als SVG-Pattern oder `radial-gradient`, keine Bilddatei.
- Kein Third-Party-Code.

---

## 12. SEO, Teilen, strukturierte Daten

- `<title>`: Startseite „VUCA Blaster – Podcast über Mut, Wandel und Gestaltungsraum“ [[OFFEN: Title bestätigen]]; Folgen „#62 Warum echter Mut mit Stimmigkeit beginnt – mit Claudia Jahn | VUCA Blaster“; sonstige Seiten „{Titel} | VUCA Blaster“.
- Meta-Description je Seite (Folgen: erste 150 Zeichen der Beschreibung, sauber gekürzt).
- Canonical auf `https://vucablaster.de/…` (mit Slash am Ende, einheitlich).
- Open Graph + Twitter Cards: Standardbild `public/og/default.png` (1200×630, Board-Look mit Wortmarke und Claim, in Phase 4 gestalten). **KANN:** pro Folge generiertes OG-Bild (Haftnotiz mit Titel) per Satori zur Build-Zeit.
- JSON-LD: `PodcastSeries` auf `/` (Name, Beschreibung, URL, Webfeed, Autoren = Hosts), `PodcastEpisode` auf Folgenseiten (Name, Nummer, Datum, Dauer, `associatedMedia` mit MP3-URL, `partOfSeries`), `BreadcrumbList` auf Unterseiten.
- `<link rel="alternate" type="application/rss+xml" href="{feed_url}" title="VUCA Blaster">` im Head.
- Sitemap über `@astrojs/sitemap`, Kurzlink-Seiten (`/62/`) ausschließen.
- LinkedIn-Test: Folgen-URL im LinkedIn Post Inspector prüfen (Titel, Bild, Beschreibung).

---

## 13. Datenschutz und Recht – technische Umsetzung

> Hinweis: Das ist keine Rechtsberatung. Texte für Impressum und Datenschutzerklärung kommen von den Hosts (Generator oder Anwalt), Claude Code setzt nur um.

### 13.1 Impressum (`/impressum/`)
Pflichtangaben nach § 5 DDG (u. a. Name, ladungsfähige Anschrift, E-Mail, schneller zweiter Kontaktweg) und Verantwortliche:r für journalistisch-redaktionelle Inhalte nach § 18 Abs. 2 MStV. Inhalt: [[PFLICHT: Impressumstext]]. Von jeder Seite mit einem Klick erreichbar (Footer).

### 13.2 Datenschutzerklärung (`/datenschutz/`)
Muss mindestens abdecken (Checkliste für den Generator):
- Verantwortliche:r (wie Impressum)
- Hosting bei GitHub Pages (GitHub, Inc., USA): GitHub protokolliert beim Seitenaufruf IP-Adressen zu Sicherheitszwecken; Drittlandübermittlung
- Keine Cookies, kein Tracking, keine Analyse-Tools, Schriften lokal
- Audio-Player (Anbieter der MP3-Dateien) und ggf. YouTube – erst nach Klick
- Links zu Spotify, Apple Podcasts usw. (Datenübertragung erst beim Aufruf dort)
- Kontakt per E-Mail
- Betroffenenrechte, zuständige Aufsichtsbehörde
Inhalt: [[PFLICHT: Datenschutztext]].

### 13.3 Technische Garantien (MUSS)
- Keine Cookies, kein `localStorage` für Tracking, keine Fremd-Requests beim Seitenaufruf (Test in Kapitel 15).
- Content-Security-Policy per `<meta http-equiv="Content-Security-Policy">`: `default-src 'self'; img-src 'self' data: <Feed-Bild-Host>; media-src <Audio-Host>; frame-src https://www.youtube-nocookie.com; script-src 'self'; style-src 'self' 'unsafe-inline'`. Hosts aus der Konfiguration ableiten; die Feed-Bilder nach Möglichkeit zur Build-Zeit herunterladen und lokal ausliefern, dann entfällt der Bild-Host.
- `referrerpolicy="strict-origin-when-cross-origin"` (Standard) und `rel="noopener"` auf externen Links.

### 13.4 Livegang-Schalter
`site.yaml: livegang` steuert: `noindex` + `robots.txt` (`Disallow: /`) + „Vorschau“-Hinweis bei `false`; bei `true` Abbruch, falls PFLICHT-Platzhalter existieren.

---

## 14. Build, Deploy, Domain, Automatik

### 14.1 GitHub Actions `.github/workflows/deploy.yml` (MUSS)

Auslöser: `push` auf `main`, `workflow_dispatch`, `schedule` (täglich, z. B. `17 5 * * *` UTC – holt neue Folgen automatisch).
Jobs: Checkout → Node LTS mit npm-Cache → `npm ci` → `npm run check` → `npm run build` → Platzhalter-Report in `$GITHUB_STEP_SUMMARY` → Upload + Deploy mit den offiziellen Pages-Actions (Astro-Doku „Deploy to GitHub Pages“ folgen, aktuelle Major-Versionen).
Rechte: `pages: write`, `id-token: write`, `contents: read`. `concurrency: pages`.

Bekannte Einschränkung: GitHub deaktiviert zeitgesteuerte Workflows in öffentlichen Repos nach 60 Tagen ohne Aktivität im Repo. GitHub schickt dann eine E-Mail; ein Klick auf „Enable“ oder ein Commit reaktiviert ihn. In `PFLEGE.md` erwähnen.

Playwright-Tests laufen in einem separaten Workflow bei Pull Requests und manuell (nicht bei jedem Cron-Build).

### 14.2 Domain `vucablaster.de`
1. Repo → Settings → Pages → Source „GitHub Actions“, Custom domain `vucablaster.de`, „Enforce HTTPS“.
2. DNS beim Registrar: Apex `A` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`; `AAAA` → `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`; `www` `CNAME` → `<github-user-oder-org>.github.io`.
3. Domain im GitHub-Konto bzw. in der Organisation **verifizieren** (Schutz vor Domain-Übernahme).
4. Bei Deploy über Actions ist eine `CNAME`-Datei nicht nötig.
Werte vor dem Eintragen mit der aktuellen GitHub-Doku abgleichen.

### 14.3 Repository
Empfehlung: GitHub-Organisation (z. B. `vucablaster`), Owner Manuel, Thomas als Mitglied. Öffentliches Repo (GitHub Pages aus privaten Repos braucht einen kostenpflichtigen Plan). [[PFLICHT: Repo-Ort und Name festlegen]].

---

## 15. Qualitätssicherung

| Check | Wie | Wann |
|---|---|---|
| Typen/Schema | `astro check` | jeder Build |
| Platzhalter | `npm run platzhalter` | jeder Build |
| Interne Links | `scripts/check-links.mjs` über `dist/` | jeder Build |
| Smoke | Playwright: alle Routen 200, keine Konsolenfehler | PR / manuell |
| A11y | `@axe-core/playwright` auf `/`, `/folgen/`, eine Folge, `/themen/mutig/`, `/ueber-uns/`, `/fuer-gaeste/`, `/impressum/` | PR / manuell |
| Reduced Motion | Playwright mit `reducedMotion: 'reduce'`: keine laufenden Animationen, alles sichtbar | PR / manuell |
| Ohne JS | Playwright mit `javaScriptEnabled: false`: alle Inhalte sichtbar, Menü-Fallback | PR / manuell |
| Keine Fremd-Requests | Playwright: alle Requests beim Laden gehen an die eigene Origin | PR / manuell |
| Visual QA | `scripts/visual-qa.mjs`: Screenshots `/` bei 390 und 1440 neben die Referenz-PNGs legen (`docs/qa/`), Abweichungen notieren | Ende Phase 1 und 4 |
| Breiten | Screenshots bei 320 · 600 · 768 · 1024 · 1280 · 1920 | Ende Phase 1, 3, 4 |

---

## 16. Phasen und Definition of Done

| Phase | Inhalt | Fertig, wenn |
|---|---|---|
| 0 Setup | Astro-Projekt, Tokens, Fonts, Base-Layout, Skripte, Deploy-Workflow, `livegang: false` | Leere Seite mit Header/Footer ist unter der Pages-URL live, Checks grün |
| 1 Startseite | Alle Abschnitte aus 7, Inhalte aus YAML (Folge #62 manuell), keine Animationen | Visual QA bei 390/1440 deckungsgleich, Breiten-Screenshots ohne Fehler, axe grün |
| 2 Folgen | RSS-Loader + Snapshot, Merge, Folgenseiten, Archiv mit Filter, Kurzlinks, Slug-Lock | Alle Folgen aus dem Feed erreichbar, `/62/` leitet korrekt, Startseite zieht Daten aus dem Feed |
| 3 Unterseiten | Staffel, Themen, Über uns, Für Gäste, Kontakt, Impressum, Datenschutz, 404, Footer | Alle Routen aus Kapitel 5, Platzhalter sauber, Leerzustände geprüft |
| 4 Feinschliff | Animationen A1–A10, SEO/OG/JSON-LD, CSP, Performance, alle Tests | Lighthouse-Ziele erreicht, alle QA-Checks grün |
| 5 Livegang | Domain, HTTPS, PFLICHT-Platzhalter leer, `livegang: true` | `https://vucablaster.de` live, Build grün, LinkedIn-Vorschau geprüft |
| 6 Übergabe | `docs/PFLEGE.md`, Zugänge bei Manuel | Manuel hat einmal selbst eine Änderung live gebracht |

Nach jeder Phase: kurze Zusammenfassung (was gebaut, was offen, Rückfragen) + aktueller Platzhalter-Report.

---

## 17. Übergabe und Pflege

`docs/PFLEGE.md` (Phase 6) enthält Schritt-für-Schritt-Anleitungen, jeweils in zwei Varianten – **„im Browser auf github.com“** und **„mit Claude Code“**:

1. Neue Folge erscheint → passiert automatisch (täglicher Build). Danach Key Learnings, Werte, Gast-Rolle, Foto in `src/content/folgen/<nr>.yaml` ergänzen.
2. Neue Themenstaffel anlegen.
3. Gastfoto hinzufügen (Größe, Dateiname, Nutzungsrecht notieren).
4. Plattform-Link oder Text ändern.
5. Deploy manuell auslösen, Build-Fehler lesen.
6. Zeitgesteuerten Workflow wieder aktivieren.

**Manuel: Windows ohne Adminrechte** – drei Wege, vom einfachsten an:

- **A · Nur Browser:** Dateien direkt auf github.com bearbeiten (Stift-Symbol oder Taste `.` für den Web-Editor) → Commit → nach ca. 2 Minuten live. Reicht für alle Inhaltsänderungen.
- **B · Claude Code im Browser** (claude.ai/code, mit dem GitHub-Repo verbunden), falls im Claude-Plan verfügbar – keine lokale Installation.
- **C · Lokal:** Claude Code für Windows + portables Git (PortableGit) + Node als ZIP im Benutzerordner, `PATH` über „Umgebungsvariablen für dieses Konto bearbeiten“ (ohne Admin). Nur nötig für lokale Vorschau. Ob Firmenrichtlinien das blockieren, vorher prüfen.

**KANN (später):** Formular-Pflege mit einem Git-basierten CMS (z. B. Pages CMS), falls YAML im Browser zu fummelig wird.

---

## 18. Offene Punkte und Unsicherheiten

Diese Punkte sind **nicht** geklärt. Nicht raten, sondern Platzhalter setzen oder nachfragen:

1. Feed-URL `https://evjjod.podcaster.de/VUCABlaster.rss` – aus der Entwicklungsumgebung nicht erreichbar gewesen.
2. Folgennummern der Folgen ohne `#` im Titel (Wendland, Maas, Hoppe, Koch). Vermutet: Hoppe #58, Wendland #59, Maas #60 – die Zählung zwischen #57 und #61 ginge dann lückenlos auf. Bestätigen.
3. Dritte Folge der Staffel Optimismus. Vermutet: Thomas Hoppe (Beschreibung nennt Optimismus), Titel „Mut und Unternehmertum“ spricht eher für eine Brücken-Folge.
4. Rhythmus „alle zwei Wochen neu“ – die letzten Folgen kamen laut Apple in kürzeren Abständen. Text bestätigen.
5. Gibt es eine Videoversion (YouTube)? Davon hängt der Audio/Video-Umschalter ab.
6. Deep-Links je Folge (Spotify/Apple) und Links für Deezer, Amazon Music, podcast.de.
7. podcast.de listet als Autoren „Manuel & Ricardo“ – veralteter Eintrag oder ehemaliger Co-Host? Relevant für „Über uns“.
8. Fotos und Nutzungsrechte (Hosts, Gäste).
9. Impressum, Datenschutz, Kontakt-E-Mail.

---

## Anhang A – Fakten aus Apple Podcasts (Stand 25.09.2026)

| Nr. | Titel | Gast | Datum | Dauer |
|---|---|---|---|---|
| #62 | Warum echter Mut mit Stimmigkeit beginnt | Claudia Jahn | Sept. 2026 | 51 Min. |
| #61 | Mut ohne Überwindung | Dr. Maja Storch | Sept. 2026 | 56 Min. |
| (#60?) | Mutig oder nur bequem? | Dr. Rüdiger Maas | 4. Sept. | 47 Min. |
| (#59?) | Warum Mut mit kleinen Schritten beginnt | Jennifer Wendland | 15. Aug. | 50 Min. |
| (#58?) | Mut und Unternehmertum | Thomas Hoppe | 7. Juni | – |
| #57 | Optimismus & warum Wissen überschätzt wird | Prof. Dr. Thomas de Nocker | 23. März | 46 Min. |
| #56 | Bedingungsloser Optimismus | Jonas Deichmann | 18. Feb. | 50 Min. |
| (#55?) | Warum Vorsätze scheitern | Prof. Axel Koch | 1. Jan. | 49 Min. |

Wahrheit ist der Feed. Diese Tabelle dient nur zum Abgleich.
