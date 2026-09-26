# Prompt für Claude Code – MVP bauen

Im Ordner `vuca-blaster-website` Claude Code starten und alles unterhalb der Linie einfügen (oder `./start-mvp.sh`).

---

Du baust den MVP der Website für den Podcast „VUCA Blaster“. Livegang: Dienstag, 29.09.2026, unter https://vucablaster.de über GitHub Pages.

ZIEL
Eine Startseite, die die Hosts in LinkedIn-Posts und bei Gastanfragen verlinken: aktuelle Folge #62 mit 2-Klick-Player, Beschreibung des Podcasts, Profile der beiden Hosts, Kontakt – plus Impressum, Datenschutz und 404. Design: Richtung D3 „Whiteboard nach dem Workshop“, unverändert. Reines HTML/CSS/minimales JS im Ordner docs/, kein Framework, kein Build.

LIES ZUERST, IN DIESER REIHENFOLGE
1. CLAUDE.md
2. 02-mvp/MVP-SPEZ.md – die Spezifikation, sie gilt vollständig
3. 01-von-manuel/Fragebogen-Manuel-VUCA-Blaster-ausgefuellt.docx – einzige Inhaltsquelle (lesen mit `textutil -convert txt -stdout <datei>` oder `pandoc -t plain <datei>`)
4. 01-von-manuel/ERGAENZUNGEN.md (Klarstellungen, gehen dem Fragebogen vor) und 01-von-manuel/DATENSCHUTZ.md (fertige Datenschutzerklärung)
5. 01-von-manuel/bilder/ – Fotos, falls vorhanden
6. 02-mvp/design/D3-Desktop.png, D3-Mobile.png, D3-Stil.png + gleichnamige .html (Maße inline; nur Referenz, keinen Code 1:1 übernehmen)
Ignoriere 03-backlog/ und ../_archiv/.

REGELN FÜR DEN FRAGEBOGEN
- Übernimm nur die eigentlichen Inhalte. Anmerkungen wie „– stimmt“, „(bitte bestätigen)“, „(Formulierung bitte mit Sebastian abstimmen)“, „Vor Veröffentlichung prüfen: …“ sind interne Notizen: nicht auf die Seite, sondern in deine Liste offener Punkte.
- Nicht angekreuzte vorausgefüllte Werte (Staffel, Werte, Key Learnings) gelten als bestätigt.
- Leere Felder = fehlt. Nichts erfinden.

BEKANNTE PUNKTE AUS DEM FRAGEBOGEN – SO UMSETZEN
- Datenschutz: Text aus 01-von-manuel/DATENSCHUTZ.md 1:1 als /datenschutz/ übernehmen (Überschriften als h2, URLs als Links).
- Impressum: Text aus dem Fragebogen 1:1 übernehmen (Immanuel Wyszynski, Kortumstraße 9, 45130 Essen, Telefon, manuel.wy@googlemail.com, Quellenhinweis e-recht24 als letzte Zeile). Ohne Zusätze, ohne die Anmerkung „Vor Veröffentlichung prüfen …“.
- Da Impressum und Datenschutz vollständig sind: KEINE Livegang-Sperre – kein noindex, robots.txt mit „Allow: /“.
- Rhythmus ist „unregelmäßig“: im Hero nur „62 Folgen seit 2020“ ohne Rhythmusangabe.
- Kontakt-E-Mail auf der Seite: hello@vucablaster.com (existiert, bestätigt).
- Folge #62: Datum 23.09.2026, MP3 https://evjjod.podcaster.de/vucablaster/media/VUCA_Blaster_Claudia_Jahn(1).mp3 – im HTML korrekt kodieren (Klammern als %28/%29) und in der Vorschau prüfen, ob die Datei lädt; Audio-Hoster „podcaster.de“.
- Hosts: Manuel Wyszynski (Host · Change Manager und Coach), Sebastian Oremek (Co-Host · Innovationsmanager) mit den Bios aus dem Fragebogen, ohne die Klammer-Anmerkungen. LinkedIn nur bei Sebastian: https://de.linkedin.com/in/sebastian-oremek (bestätigt).
- Fotos kommen erst nächste Woche: Foto-Abzüge für Hosts, Gast und Cover jetzt mit Schraffur ohne Beschriftung bauen, aber bereits auf die Dateinamen aus 01-von-manuel/bilder/LIESMICH.txt verdrahten (Pfade in docs/assets/img/), sodass später nur die Bilder abgelegt werden müssen. Fehlende Fotos sind KEIN Blocker.

VORGEHEN
1. Kurz auflisten: was im Fragebogen fehlt oder geklärt werden muss – getrennt nach „blockiert Livegang“ und „kann nachgereicht werden“. Dann ohne Rückfrage bauen.
2. Website nach MVP-SPEZ.md in docs/ bauen (Schriften lokal als woff2, niemals Google Fonts per CDN; keine externen Requests beim Laden).
3. Selbst prüfen: 320, 390, 768, 1024, 1440 px (Headless-Browser, falls verfügbar), 390 und 1440 mit den D3-PNGs vergleichen, Fokus sichtbar, Player lädt erst nach Klick, keine Requests an fremde Hosts. Abweichungen zu D3 in ABWEICHUNGEN.md im Projekt-Root notieren (nicht in docs/).
4. NEUE-FOLGE.md im Projekt-Root schreiben (Wechsel der aktuellen Folge per GitHub-Webeditor und per Claude-Code-Prompt).
5. Abschlussbericht:
   a) was fertig ist,
   b) offene Punkte (Blocker zuerst),
   c) welche Schritte aus 02-mvp/SETUP-GITHUB-DOMAIN.md noch offen sind,
   d) den ersten Push nach https://github.com/VUCABLASTER/website.git (Branch main) – erst ausführen, wenn ich es bestätige.
