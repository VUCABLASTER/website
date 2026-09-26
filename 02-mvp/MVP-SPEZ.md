# MVP-Spezifikation – VUCA Blaster Website

Livegang: **Dienstag, 29.09.2026** unter `https://vucablaster.de`.
Diese Datei ist vollständig. Für den MVP brauchst du nichts aus `03-backlog/`.

## 1. Ziel und Zweck

Der Podcast „VUCA Blaster“ (Hosts Manuel Wyszynski und Sebastian Oremek, seit 2020, 62 Folgen) braucht eine eigene Adresse, die die Hosts in LinkedIn-Posts und bei Gastanfragen verlinken können. Der MVP muss drei Dinge leisten:

1. **Reinhören auslösen:** aktuelle Folge mit Player und Links zu Spotify und Apple Podcasts.
2. **Vertrauen schaffen:** wer steckt dahinter (Hosts), worum geht es (Beschreibung).
3. **Rechtlich sauber online sein:** Impressum und Datenschutzerklärung.

Claim (fix): „Die Welt ist komplex. Wir sehen darin Gestaltungsraum.“ Ansprache: Du.

## 2. Technik (fix)

- **Reines HTML, CSS und minimales Vanilla-JS.** Kein Framework, kein Astro, kein npm, kein Build-Schritt, keine GitHub Action.
- Die Website liegt komplett im Ordner **`docs/`** des Repos. GitHub Pages veröffentlicht nur diesen Ordner („Deploy from a branch“ → `main` → `/docs`). Alles andere im Repo (Planung, Infos von Manuel) wird nicht veröffentlicht.
- Pflegbar ohne Programmierkenntnisse: Manuel arbeitet unter Windows ohne Adminrechte und ändert Inhalte im GitHub-Webeditor oder mit Claude Code.

```
docs/
├─ index.html                 # Startseite
├─ impressum/index.html
├─ datenschutz/index.html
├─ 404.html
├─ CNAME                      # Inhalt: vucablaster.de
├─ robots.txt
├─ assets/css/style.css
├─ assets/js/main.js          # nur 2-Klick-Player
├─ assets/fonts/*.woff2       # lokal, siehe 4
├─ assets/img/                # Cover, Host-Fotos, og-default.png (1200×630)
├─ favicon.svg, favicon.ico, apple-touch-icon.png
└─ .nojekyll
```

## 3. Eingaben

- Inhalte: **nur** aus `01-von-manuel/Fragebogen-Manuel-VUCA-Blaster-ausgefuellt.docx` (ausgefüllt; grüner Text = vorausgefüllt und gilt, sofern nicht korrigiert). Bilder aus `01-von-manuel/bilder/` (optimiert als WebP + JPG-Fallback, feste width/height, passende Größen).
- Design: `02-mvp/design/D3-Desktop.png` + `.html` (1440 px), `D3-Mobile.png` + `.html` (390 px), `D3-Stil.png` + `.html`. Alle Maße stehen inline im HTML. **Das HTML ist Referenz, kein Produktionscode:** feste Artboard-Breite, Inline-Styles, Google-Fonts-Link – nichts davon übernehmen.
- **Nichts erfinden.** Ist ein Feld im Fragebogen leer, bleibt die Stelle im HTML als Kommentar `<!-- FEHLT: … -->` und das Element wird ausgeblendet (Button ohne URL, Bio ohne Text) bzw. zeigt einen neutralen Ersatz (Cover statt Foto). Kein Lorem ipsum, keine Fake-Texte.

## 4. Design-System (aus D3 „Whiteboard nach dem Workshop“)

### Farben (als Custom Properties in `style.css`)

```css
:root{
  color-scheme: light;
  --c-page:#FAFAF7; --c-board:#FFFFFF; --c-frame:#D9D6CF; --c-dot:#E4E1DA;
  --c-tape:#EDE8DA; --c-archive:#F1EFE9; --c-hatch:#DEDAD2;
  --c-ink:#161414; --c-petrol:#046464; --c-violet:#80027D;
  --c-rose:#F5D7D7; --c-aqua:#7AE7F2; --c-teal:#04B8B2; --c-red:#E9022C;
  --c-muted:#5E5A55; --c-dashed:#8D877E;
}
```

Türkis nur für Magnete (immer mit 3 px Tinte-Rand), Rot nur für den Kringel. Keine Schatten, keine Verläufe.

### Schriften (lokal, nie Google-CDN)

| Rolle | Schrift | Einsatz |
|---|---|---|
| alles | Bricolage Grotesque, variabel (wght + opsz) | 800 Headlines mit enger Laufweite, 700 Notizen/Labels, 400–600 Text |
| Randnotiz | Permanent Marker | nur „hier reinhören!“ |
| Lautschrift | Andika | nur `[ˈvuːka ˈblaːstɐ]` (Bricolage hat keine IPA-Zeichen) |

Bezugsquelle: npm-Pakete `@fontsource-variable/bricolage-grotesque`, `@fontsource/permanent-marker`, `@fontsource/andika` (woff2 latin + latin-ext) herunterladen und nach `docs/assets/fonts/` kopieren; `@font-face` selbst schreiben, `font-display: swap`, Bricolage-Latin preloaden. Lizenzen (OFL) mit ablegen. Falls npm lokal fehlt: woff2 direkt von der Fontsource-CDN-Downloadseite holen – eingebunden werden sie nur lokal.

### Typo (fluid zwischen 390 und 1440 px)

| Rolle | 390 → 1440 px | CSS |
|---|---|---|
| h1 „VUCA Blaster“ | 88 → 156 | `clamp(5.5rem, 3.921rem + 6.476vw, 9.75rem)`, lh .86, ls −.05em |
| h2 Folgentitel | 40 → 72 | `clamp(2.5rem, 1.757rem + 3.048vw, 4.5rem)`, lh 1, ls −.035em |
| h2 Abschnitt | 50 → 80 | `clamp(3.125rem, 2.429rem + 2.857vw, 5rem)`, lh .95, ls −.045em |
| Claim | 32 → 54 | `clamp(2rem, 1.489rem + 2.095vw, 3.375rem)`, lh 1.08 |
| Aussprache | 21 → 30 | `clamp(1.312rem, 1.104rem + .8571vw, 1.875rem)` |
| Marker-Notiz | 24 → 32 | `clamp(1.5rem, 1.314rem + .7619vw, 2rem)` |
| Haftnotiz-Zahl / -Text | 36 → 44 / 24 → 29 | lh 1 / 1.15 |
| Fließtext | 17 → 20 | lh 1.5 |
| Label | 16 → 18 | 700 |

Unter 390 px darf die h1 bis 72 px fallen. `hyphens: manual`, `text-wrap: balance` für Headlines, typografische Anführungszeichen „ “.

### Form

Seitenrand 64 px (≥ 1024) / 16 px (mobil). Max. Breite 1440 px. Abstände 12 · 18 · 28 · 44 · 88. Buttons 4 px Radius, Papier 0. Papier gedreht zwischen −3.5° und +3.5°, Buttons und Fließtext nie gedreht. Max. 3 Handelemente pro Bildschirmhöhe.

## 5. Seiten

### 5.1 Startseite `index.html`

| # | Abschnitt | Vorlage | Hinweise |
|---|---|---|---|
| 1 | Header | D3 | Wortmarke „VUCA Blaster“; Nav: **Aktuelle Folge · Über uns · Kontakt** (Anker `#aktuell`, `#ueber-uns`, `#kontakt`); rosé Zettel „Für Gäste“ (−2°) → `#kontakt`. Mobil: Links als Zeile unter der Wortmarke, kein Menü-Button. |
| 2 | Hero-Board | D3 exakt | Rahmen, Punktraster, h1, Aussprache (sichtbar `aria-hidden`, dazu `sr-only` „Aussprache: Wuka Blaster“), Claim mit rotem Kringel um „Gestaltungsraum“, Pfeil + „hier reinhören!“, Buttons Spotify + Apple Podcasts (schwarz), Zeile „62 Folgen seit 2020 · {rhythmus}“, Haftnotiz „Neu · #62“ (nur ≥ 1024 px, Link `#aktuell`), Markerleiste. Deezer/Amazon/podcast.de **weglassen**. |
| 3 | Aktuelle Folge `#aktuell` | D3 exakt | Label „Aktuelle Folge“ + „#62 · Staffel Mut, 4 von 8“, h2 Titel (mit `sr-only` „#62 – “), Gast + Rolle, Werte-Labels **ohne Link**, „Diese Folge hören“ (Spotify, Apple) + Hinweis „Am besten auf Spotify oder Apple Podcasts: Dort hilft jedes Abo und jede Bewertung dem Podcast.“, Foto-Abzug (Gastfoto, sonst Cover), Player-Blatt (siehe 6), 3 Key Learnings als Haftnotizen. |
| 4 | Über den Podcast `#ueber-uns` | neu, aus D3-Bausteinen | Label „Über uns“, h2 „Was ist ein VUCA Blaster?“, Lexikon-Karte (weißes Blatt, 2 px Tinte-Rand, Zeile „Substantiv, der“ in Petrol, Definition 24/20 px), darunter Beschreibung (Fließtext, max. 68 ch). |
| 5 | Hosts | neu | h2 „Wer spricht hier?“, zwei Foto-Abzüge mit Klebeband (weißer Rahmen 14 px, 1.5 px `--c-frame`, Klebestreifen `--c-tape`, Drehung −2° / +2°), Name (800), Rolle (Muted), Bio, LinkedIn-Link. Zweispaltig ab 768 px. |
| 6 | Kontakt `#kontakt` | neu | h2 „Lust auf ein Gespräch?“, ein Satz zu Gastanfragen, schwarzer Button „Schreib uns“ als `mailto:{email}?subject=Gastanfrage%20VUCA%20Blaster`. |
| 7 | Footer | neu | `border-top: 2px solid var(--c-ink)`; Wortmarke + Claim, Links Spotify / Apple Podcasts, Unterzeile „© 2020–2026 VUCA Blaster · Impressum · Datenschutz“. |

Abschnitte werden wie im Design durch `border-top: 2px solid var(--c-ink)` getrennt. Die D3-Abschnitte **Staffel Mut, Fünf Werte, Archiv** kommen im MVP **nicht** vor.

### 5.2 Impressum und Datenschutz

Gleicher Header (Nav-Anker zeigen auf `/#…`) und Footer. Kleines Board als Seitenkopf (Rahmen 12/8 px, Punktraster, h1). Text aus der Infodatei, Fließtext max. 68 ch, keine Deko.

### 5.3 404

Kleines Board, Marker-Notiz „Hier steht noch nichts.“, Link zur Startseite.

## 6. Player (2-Klick, Pflicht)

- Ausgangszustand wie D3-Player-Blatt: Titel „Player“, Text „Der Player ist noch nicht geladen. Beim Laden werden Daten an {audio_hoster} übertragen. Mehr in der Datenschutzerklärung.“, Button „Audio-Player laden“.
- **Audio/Video-Umschalter weglassen** (kein Video im MVP).
- Klick → `<audio controls preload="none" src="{mp3_url}">` einfügen, Wiedergabe starten, Fokus auf den Player.
- Keine Einwilligung speichern. Ohne JS: Link „Folge direkt anhören (MP3)“.
- Beim Seitenaufruf **null** Requests an fremde Hosts.

## 7. Animationen (dezent)

Nur eine: Der rote Kringel zeichnet sich einmal (`stroke-dashoffset` 1000 → 0, 1.1 s, ease-out, 0.4 s Verzögerung). Hover auf Buttons: nur Farbwechsel (120 ms). Alles in `@media (prefers-reduced-motion: no-preference)`. Inhalte sind ohne JS vollständig sichtbar.

## 8. Qualität (Pflicht)

- Keine Cookies, kein Tracking, keine externen Schriften/Skripte.
- Kein horizontales Scrollen bei 320, 390, 768, 1024, 1440, 1920 px und bei 200 % Zoom.
- WCAG 2.2 AA: eine h1, Landmarks, Skip-Link, sichtbarer Fokus (`outline: 3px solid var(--c-petrol); outline-offset: 3px`), Touch-Ziele ≥ 44 px, Alt-Texte, dekorative SVGs `aria-hidden`.
- Head: `lang="de"`, `<title>` „VUCA Blaster – Podcast über Mut, Wandel und Gestaltungsraum“, Meta-Description (≤ 155 Zeichen, aus der Beschreibung), Canonical `https://vucablaster.de/`, Open Graph + Twitter Card mit `og-default.png` (1200×630, Board-Look mit Wortmarke und Claim, selbst als statisches Bild erzeugen), Favicons.
- **Livegang-Sperre:** Solange Impressum- oder Datenschutztext im Fragebogen fehlt: `<meta name="robots" content="noindex">` auf allen Seiten und `robots.txt` mit `Disallow: /`. Sobald beide vollständig sind: entfernen bzw. `Allow: /`.

## 9. Pflege-Anleitung

Lege `NEUE-FOLGE.md` im Repo-Root an: Wie Manuel bei einer neuen Folge in `docs/index.html` die markierten Blöcke `<!-- AKTUELLE-FOLGE:START -->…<!-- AKTUELLE-FOLGE:ENDE -->` und `<!-- HERO-NOTIZ:START -->…<!-- HERO-NOTIZ:ENDE -->` ändert (Nummer, Titel, Gast, Rolle, Werte, Datum, MP3-URL, Foto, Key Learnings) – einmal per GitHub-Webeditor, einmal per Claude-Code-Prompt.

## 10. Fertig, wenn

- [ ] Alle Seiten gebaut, lokale Vorschau (`python3 -m http.server -d docs` oder Datei direkt öffnen) sieht bei 390 und 1440 px aus wie die D3-Referenz (ohne die weggelassenen Abschnitte)
- [ ] Liste aller noch offenen `FEHLT`-Stellen ausgegeben
- [ ] `NEUE-FOLGE.md` geschrieben
- [ ] Nach dem Push: `https://vucablaster.de` lädt per HTTPS, `www` leitet um, Player lädt erst nach Klick, LinkedIn Post Inspector zeigt Titel/Bild/Text
