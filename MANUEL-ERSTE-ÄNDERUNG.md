# Manuel: Deine erste kleine Entwicklung

## Ziel
Du clonst das Repo, machst eine Test-Änderung, buildest lokal, checkst im Browser, pushst. Fertig.

## 1. Repo clonen
```bash
git clone git@github.com:VUCABLASTER/website.git
cd website
```

## 2. Python installieren (einmalig)
```bash
pip install pillow
```

Das war's. Mehr brauchst du für kleine Änderungen nicht.

## 3. Test-Änderung machen

Öffne `werkzeuge/layout.py` und ändere einen Text, z.B. Zeile 21:

**Vorher:**
```python
AMAZON = 'https://music.amazon.de/podcasts/3eb46224-be51-446b-a8b1-cc0ab2cd83b0/vuca-blaster'
```

**Nachher:**
```python
AMAZON = 'https://music.amazon.de/podcasts/3eb46224-be51-446b-a8b1-cc0ab2cd83b0/vuca-blaster'  # TEST MANUEL
```

Speichern.

## 4. Lokal bauen
```bash
python3 werkzeuge/build.py
```

Schau auf den Output:
- ✅ Wenn es mit `Fertig: X Folgen, X Bilder, X Transkripte.` endet → super
- ❌ Wenn ein Error kommt → kopier ihn, ask Langdock

## 5. Vorschau im Browser
```bash
open docs/index.html
```

Oder in Firefox/Chrome: `File → Open → docs/index.html`

- Sieht die Seite noch richtig aus?
- Kein roter Text / kein "FEHLER"?
- Dann: weiter zu Schritt 6

## 6. Pushen
```bash
git add -A
git commit -m "Test: kleine Änderung in layout.py"
git push
```

## 7. Live prüfen

Geh zu https://github.com/VUCABLASTER/website → **Actions**

Du siehst dort "Website aktualisieren" – der Workflow sollte grün werden nach 1–2 Minuten.

Nach ca. 2 Min: https://vucablaster.de öffnen → Deine Änderung ist live.

---

## Wenn was schiefgeht:

**Fehler beim Bauen?**
- Kopier den Error → Langdock zeigen

**Workflow rot (GitHub Actions)?**
- Actions-Tab → "Website aktualisieren" → auf den fehlgeschlagenen Run klicken → Log anschauen
- Error kopieren → Langdock

**Sonst immer unsicher?**
- Langdock fragen. Das ist genau sein Job.

---

Das war's. Du bist jetzt Developer. 🚀
