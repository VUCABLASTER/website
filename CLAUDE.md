# CLAUDE.md – VUCA Blaster Website

**Aktuelle Phase: MVP, Livegang Dienstag 29.09.2026. Nur GitHub Pages, reines HTML/CSS/JS.**

## Lies (in dieser Reihenfolge)

1. `02-mvp/MVP-SPEZ.md` – was gebaut wird, vollständig
2. `01-von-manuel/Fragebogen-Manuel-VUCA-Blaster-ausgefuellt.docx` (ausgefüllter Fragebogen, Word) + `01-von-manuel/bilder/` – einzige Quelle für Inhalte. Lesen z. B. mit `textutil -convert txt -stdout <datei>` (Mac) oder `pandoc -t plain`. Grüner Text = vorausgefüllt; „stimmt“ angekreuzt oder unkommentiert = gilt; leere Felder = fehlt.
3. `02-mvp/design/` – D3-Referenz (PNG + HTML) für Desktop 1440 und Mobile 390
4. `02-mvp/SETUP-GITHUB-DOMAIN.md` – was die Menschen klicken; darauf verweisen, nicht selbst ausführen

**Nicht lesen / nicht umsetzen:** `03-backlog/` und `../_archiv/` – das ist die spätere finale Version (Astro, Archiv, RSS …). Nur öffnen, wenn ausdrücklich darum gebeten.

## Regeln

- Website nur im Ordner `docs/` (GitHub Pages veröffentlicht `/docs`). Kein Framework, kein npm-Build, keine GitHub Action.
- Startseite optisch wie D3 (Abschnitte laut Spez), Farben nur aus den Tokens der Spez.
- **Nichts erfinden.** Fehlt etwas (leeres Feld im Fragebogen): HTML-Kommentar `<!-- FEHLT: … -->`, Element ausblenden oder neutraler Ersatz.
- Datenschutz: keine Cookies, kein Tracking, keine Requests an fremde Hosts beim Seitenaufruf, Schriften lokal, Player nur per 2-Klick.
- Barrierefreiheit WCAG 2.2 AA, `prefers-reduced-motion` respektieren.
- Solange Impressum oder Datenschutz fehlen: `noindex` + `robots.txt Disallow: /`.
- Deutsch, Du-Ansprache, typografische Anführungszeichen. Commits auf Deutsch.

## Wenn Manuel den Fragebogen später aktualisiert

Geänderte Werte in `docs/` übernehmen, erledigte `FEHLT`-Kommentare entfernen, Liste der noch offenen Punkte ausgeben. Nichts dazuerfinden.
