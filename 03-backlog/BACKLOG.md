# Backlog – nach dem MVP

Stand: 28.09.2026. Der MVP ist live (Startseite, Impressum, Datenschutz, 404, Gewinnspiel `/worccamp/`).
**29.–30.09.2026 (WORCamp): Live-Seite nicht anfassen.** Arbeiten nur auf dem Branch `relaunch` – GitHub Pages veröffentlicht nur `main`.

Priorität: **P0** direkt nach dem Event · **P1** nächster Ausbau (Archiv) · **P2** danach · **P3** irgendwann.

## Leitlinien für den Ausbau

- **Übergabe an Manuel ist das Ziel.** Er muss alles selbst betreuen können, ohne Code.
- **Gehört wird auf den Plattformen.** Archiv und Folgenseiten verlinken auf Apple Podcasts und Spotify, damit Abrufe und Bewertungen dort zählen. Eingebettet bleibt nur die aktuelle Folge (2-Klick).
- **So viel automatisch wie möglich.** Manuel pflegt Folgen und Bilder weiter bei podcaster.de. Die Website holt sich die Daten selbst.
- **Nur das Nötigste von Hand:** pro Folge Gast-Rolle, Key Learnings, Werte, Staffel.

## Ergebnis der Machbarkeitsprüfung (28.09.2026)

| Quelle | Liefert automatisch | Befund |
|---|---|---|
| RSS-Feed `https://evjjod.podcaster.de/VUCABlaster.rss` | Nummer, Titel, Datum, Dauer, Folgenbild, MP3, Beschreibung (HTML), Link | Erreichbar, alle 62 Folgen. 1 Folge ohne `itunes:episode`-Nummer. |
| Apple Lookup-API (`itunes.apple.com/lookup?id=1541461336&entity=podcastEpisode`) | Direktlink zu jeder Folge bei Apple Podcasts | Öffentlich, ohne Schlüssel. 62/62 Folgen per GUID eindeutig zugeordnet. |
| Spotify Web API | Direktlink zu jeder Folge bei Spotify | Nur mit (kostenlosem) Spotify-Entwicklerkonto. Sonst Link auf die Show. |

## Vorschlag Architektur (ersetzt „Umstieg auf Astro“)

- **Hosting bleibt GitHub Pages.** Kostenlos, live, DNS und HTTPS laufen. Ein Wechsel (Netlify, Cloudflare) brächte vor allem neue Konten.
- **Kein großes Framework.** Ein kleines Build-Skript (Node, z. B. Eleventy) erzeugt aus Feed, Apple-Links und den Folgen-Infos statisches HTML im bestehenden D3-Design.
- **GitHub Action, täglich + auf Knopfdruck:** Feed lesen → Folgenseiten, Archiv, Kurzlinks, aktuelle Folge auf der Startseite und Suchindex neu erzeugen → veröffentlichen. Neue Folge bei podcaster.de = spätestens am nächsten Tag auf der Website.
- **Pflege für Manuel:** pro Folge eine kleine Datei mit Gast-Rolle, Key Learnings, Werten und Staffel. Die Action legt sie für neue Folgen vorausgefüllt an. Bearbeiten über ein Browser-Formular (Pages CMS, Login mit GitHub, nichts zu hosten) oder zur Not direkt im GitHub-Webeditor.
- **Suche und Filter im Browser:** Suchindex als JSON (62 Folgen sind klein), Volltext über Titel, Gast, Beschreibung und Key Learnings, Filter nach Wert, Staffel und Jahr. Ohne externe Dienste.

## P0 – direkt nach dem Event (ab 01.10.2026)

| Thema | Notiz |
|---|---|
| Gewinnspiel beenden | Gewinnspiel-Leiste entfernen (`GEWINNSPIEL-LEISTE:START/ENDE` in `docs/index.html`, `impressum/`, `datenschutz/`, `404.html`). `/worccamp/` offline nehmen oder als „Gewinnspiel beendet“ kennzeichnen. |
| Datenschutz nachziehen | Abschnitt 8 (Gewinnspiel) nach Abschluss und Versand entfernen oder als abgeschlossen kennzeichnen. Teilnehmerdaten löschen (Postfach hello@). |
| Branch `relaunch` einspielen | Nur Backlog/Planung, keine Seitenänderung. |

## P1 – Archiv und Automatik

| Thema | Notiz |
|---|---|
| Feed-Import + Apple-Links | Build-Skript liest Feed und Apple-API, Ersatzkopie im Repo, falls ein Dienst nicht erreichbar ist. |
| Archiv `/folgen/` | Alle Folgen, Volltextsuche, Filter nach Wert, Staffel, Jahr. Links zu Apple (direkt) und Spotify. |
| Folgenseiten `/folgen/<nr>-<slug>/` | Folgenbild, Beschreibung aus dem Feed, Gast + Rolle, Key Learnings, Werte, Plattform-Buttons. Kein eingebetteter Player (Abrufe sollen auf den Plattformen zählen). |
| Kurzlinks `/62/` | Weiterleitung auf die Folgenseite, für LinkedIn-Posts. |
| Aktuelle Folge automatisch | Ersetzt den manuellen Wechsel aus `NEUE-FOLGE.md`. |
| Folgen-Infos pflegen | Eine Datei pro Folge, Pflegeformular (Pages CMS) oder GitHub-Webeditor. |
| Deploy per GitHub Action | Nötig für den Build. Pages-Quelle von „Branch /docs“ auf „GitHub Actions“ umstellen. |
| Übergabe-Doku `PFLEGE.md` | Neue Folge, Folgen-Infos ergänzen, Bild tauschen, Build neu anstoßen, Fehler lesen – jeweils im Browser und mit Claude Code. |

## P2 – danach

| Thema | Notiz |
|---|---|
| Seite „Für Gäste“ | Ablauf für Gäste (Vorgespräch, Aufnahme, Dauer, Tool/Ort, Freigabe, Veröffentlichung), Kontakt per Mail. Inhalte von Manuel nötig. |
| Staffel-Abschnitt + Staffelseiten | In D3 gestaltet („Staffel Mut 4/8“, Magnete, „Halbzeit!“). |
| Werte-Cluster + Themenseiten `/themen/<wert>/` | In D3 gestaltet; nutzen dieselben Folgen-Infos wie der Filter. |
| Spotify-Direktlinks | Braucht kostenloses Spotify-Entwicklerkonto (Client-ID/Secret als GitHub-Secret). |
| SEO | JSON-LD PodcastSeries/Episode, Sitemap, OG-Bild pro Folge (Folgenbild). |
| Automatische Tests | Link-Check, Barrierefreiheit, keine Fremd-Requests. |
| Eigene Seite „Über uns“ | Ausführliche Bios, „Warum wir das machen“. |

## P3 – irgendwann

| Thema | Notiz |
|---|---|
| Video (YouTube, 2-Klick) | Nur falls es Video gibt. |
| Weitere Animationen | Haftnotizen, Magnete (BRIEF Kap. 8). |

## Inhalte, die später gebraucht werden

- Pro Folge: Gast-Rolle, Key Learnings, Hauptwert/Nebenwerte, Staffel (für den Filter). Rest kommt aus dem Feed.
- Staffel Optimismus und Mut: Beschreibung; dürfen kommende Gäste (5–8) vorab genannt werden?
- Texte zu den fünf Werten (Vorschläge in `INHALTE-final.md`, nicht bestätigt).
- Für Gäste: Ablauf, Dauer, Aufnahmeort/-tool, Freigabe, was Gäste bekommen.
- Links: Deezer, Amazon Music, podcast.de, YouTube falls vorhanden.
- Nutzungsrechte für Gastfotos (die Folgenbilder aus dem Feed sind eigene Grafiken – prüfen, ob Gastfotos darin freigegeben sind).
- podcast.de nennt „Manuel & Ricardo“ – ehemaliger Co-Host? Erwähnen?
- Folgenbild #61 „Mut ohne Überwindung“ liegt schon in `01-von-manuel/bilder/` (kommt künftig ohnehin aus dem Feed).

## Überholt

- Umstieg auf Astro (ersetzt durch Build-Skript, siehe oben).
- Rhythmus „alle zwei Wochen“ – geklärt: unregelmäßig.
- Impressum, Datenschutz, Kontakt-E-Mail, Host-Fotos – mit dem MVP erledigt.
