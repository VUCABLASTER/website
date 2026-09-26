# Backlog – nach dem MVP

Alles hier ist **für den MVP nicht relevant**. Grundlage für die finale Version: `BRIEF-final.md` (Spezifikation) und `INHALTE-final.md` (Ausfüllformular).
Priorität: **P1** direkt nach dem MVP · **P2** finale Version · **P3** irgendwann.

## Technik

| Prio | Thema | Notiz |
|---|---|---|
| P1 | Umstieg auf Astro | statischer Build, Tokens/CSS aus dem MVP übernehmen, URLs `/impressum/` `/datenschutz/` bleiben |
| P1 | RSS-Import der Folgen | Feed `https://evjjod.podcaster.de/VUCABlaster.rss` (bestätigen), Build-Zeit-Import mit Ersatzkopie, täglicher Neubau per GitHub Action |
| P1 | Aktuelle Folge automatisch | ersetzt den manuellen Wechsel aus `NEUE-FOLGE.md` |
| P2 | Deploy per GitHub Actions statt Branch | nötig für Astro |
| P2 | Automatische Tests | Playwright: Smoke, axe, Reduced Motion, keine Fremd-Requests |
| P2 | SEO-Ausbau | JSON-LD PodcastSeries/Episode, Sitemap, OG-Bild pro Folge |
| P2 | Performance-Ziele | Lighthouse ≥ 95 / 100 / 100 / 100 |
| P3 | Formular-Pflege (CMS) | z. B. Pages CMS, falls YAML im Browser zu fummelig |

## Seiten und Funktionen

| Prio | Thema | Notiz |
|---|---|---|
| P1 | Archiv `/folgen/` | alle Folgen, Filter nach Staffel, Wert, Jahr |
| P1 | Folgenseiten `/folgen/<slug>/` | eigener Player, Shownotes, Key Learnings |
| P1 | Kurzlinks `/62/` | für LinkedIn |
| P2 | Staffel-Abschnitt + Seite (Kanban „Staffel Mut 4/8“, Magnete, „Halbzeit!“) | in D3 schon gestaltet |
| P2 | Werte-Cluster + Themenseiten `/themen/<wert>/` | in D3 schon gestaltet, Leerzustand für Werte ohne Staffel |
| P2 | Archiv-Abschnitt (Flipchart „Protokoll 2020 bis 2025“) | in D3 schon gestaltet |
| P2 | Seite „Für Gäste“ | Ablauf, was wir brauchen, Gäste-Wand |
| P2 | Eigene Seite „Über uns“ | ausführliche Bios, „Warum wir das machen“ |
| P2 | Weitere Animationen | Haftnotizen, Magnete, Seitenwechsel (BRIEF Kap. 8) |
| P3 | Video-Player (YouTube, 2-Klick) | nur falls es Video gibt |
| P3 | Suche im Archiv | |

## Inhalte, die später gebraucht werden

- Links: Deezer, Amazon Music, podcast.de (bekannter Link war nicht erreichbar), YouTube falls vorhanden
- Deep-Links je Folge (Spotify, Apple)
- Folgennummern ohne `#` im Titel bestätigen – vermutet: Hoppe #58, Wendland #59, Maas #60, Koch #55
- Staffel Optimismus: Anzahl Folgen, dritte Folge (Hoppe?), Beschreibung
- Staffel Mut: Beschreibung, dürfen kommende Gäste (5–8) vorab genannt werden?
- Staffel/Werte-Zuordnung, Gast-Rollen, Fotos und Key Learnings für #61 und ältere Folgen
- Texte zu den fünf Werten (Vorschläge in `INHALTE-final.md`, nicht bestätigt)
- Für Gäste: Ablauf, Dauer, Aufnahmeort/-tool, Freigabe, was Gäste bekommen
- Archiv: Themen 2020–2025 bestätigen, Lieblingsfolgen aus dem Archiv
- Ausführliche Host-Bios, „Warum wir das machen“, Zielgruppe
- podcast.de nennt „Manuel & Ricardo“ – ehemaliger Co-Host? Erwähnen?
- Rhythmus „alle zwei Wochen“ bestätigen
- Nutzungsrechte für Gastfotos klären (schriftlich)
- Eigene E-Mail-Adresse @vucablaster.de?
