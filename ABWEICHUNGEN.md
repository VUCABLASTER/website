# Abweichungen zur Design-Referenz D3

Stand: 26.09.2026. Verglichen wurde die gebaute Startseite (`docs/index.html`) bei 390 und 1440 px mit `02-mvp/design/D3-Mobile.png` und `D3-Desktop.png`.

## Laut Spezifikation gewollt

| Stelle | D3 | MVP | Grund |
|---|---|---|---|
| Navigation | Folgen · Themen · Über uns · Für Gäste · Kontakt | Aktuelle Folge · Über uns · Für Gäste · Kontakt | MVP-SPEZ 5.1 |
| Navigation mobil | Menü-Button | Links als Zeile unter der Wortmarke, „Für Gäste“ rechts oben | MVP-SPEZ 5.1 |
| Plattform-Buttons | Spotify, Apple, Deezer, Amazon Music, podcast.de | nur Spotify und Apple Podcasts | MVP-SPEZ / Fragebogen F |
| Hero-Zeile | „62 Folgen seit 2020 · alle zwei Wochen neu“ | „62 Folgen seit 2020“ | Folgen erscheinen unregelmäßig |
| Player | Audio/Video-Umschalter, Text mit „[Anbieter]“ | kein Umschalter, Anbieter „podcaster.de“, ohne JavaScript Link „Folge direkt anhören (MP3)“ | MVP-SPEZ 6 |
| Werte-Labels | Links | ohne Link | MVP-SPEZ 5.1 |
| Staffel Mut, Fünf Werte, Archiv | vorhanden | entfallen | MVP-SPEZ 5.1 |
| Über uns, Hosts, Kontakt, Footer | nicht im Design | neu aus D3-Bausteinen gebaut (Lexikon-Karte, Foto-Abzüge mit Klebeband, schwarzer Button) | MVP-SPEZ 5.1 |
| Foto-Platzhalter | Schraffur mit Beschriftung „Foto-Platzhalter · …“ | Schraffur ohne Beschriftung | Vorgabe: Fotos folgen, kein sichtbarer Platzhaltertext |

## Eigene Entscheidungen (bitte kurz prüfen)

| Stelle | Abweichung | Grund |
|---|---|---|
| Aktuelle Folge, Meta-Zeile | Erscheinungsdatum ergänzt: „#62 · Staffel Mut, 4 von 8 · 23.09.2026“. Mobil dadurch zweizeilig (D3: „#62 · Mut 4/8“ einzeilig). | Datum steht im Fragebogen; D3 zeigt keins. Mobil einheitlich lange Form statt eigener Kurzform. |
| Über uns | Zusätzlicher Foto-Abzug mit dem Podcast-Cover neben der Lexikon-Karte (ab 1024 px rechts, mobil darunter) | Das Cover wird geliefert und hatte sonst keinen Platz; füllt die rechte Spalte wie in D3. |
| Lexikon-Karte | Kopfzeile „VUCA Blaster“ über „Substantiv“ (Spez: „Substantiv, der“). Definition im Blocksatz mit automatischer Silbentrennung (Spez: `hyphens: manual`) | Kopfzeile: Lexikon-Logik. Wortart und Blocksatz: Wunsch von Manuel, 27.09.2026. Silbentrennung nur in der Definition, sonst entstehen im Blocksatz mobil große Wortlücken. |
| Kontakt | Satz „Für Gastanfragen und Ideen zu neuen Folgen erreichst du uns per E-Mail.“, darunter die Adresse als Text | Spez verlangt einen Satz zu Gastanfragen; Adresse sichtbar, falls `mailto:` am Gerät nicht funktioniert. |
| 404 | h1 „Seite nicht gefunden“ zusätzlich zur Marker-Notiz | Jede Seite braucht genau eine h1. |
| Hero „hier reinhören!“ | Zwischen 390 und 1279 px Position wie D3-Mobile, ab 1280 px wie D3-Desktop; unter 380 px Notiz 20 px statt 24 px | Sonst überlappt die Notiz die Haftnotiz (1024–1279) oder ragt aus dem Bildschirm (320 px). |
| Hero-Buttons mobil | Innenabstand links/rechts 4 px statt 10 px | Sonst bricht „Apple Podcasts“ bei 390 px um; D3 zeigt es einzeilig. |
| Key Learnings 768–1023 px | Drei Haftnotizen nebeneinander, schmaler als D3-Desktop | D3 hat kein Tablet-Layout. |
| Markerleiste | Enthält den roten Marker, obwohl Rot laut Spez „nur für den Kringel“ ist | Exakt wie D3. |
| Favicon | Türkise Haftnotiz mit Magnet, ohne Text | Kein Favicon im Design; D3-Signatur, keine Schrift nötig. |
| OG-Bild | Board mit Wortmarke, Aussprache, Claim, Kringel und Haftnotiz „Podcast · 62 Folgen seit 2020“ | Spez: Board-Look mit Wortmarke und Claim. |
