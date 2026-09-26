# Setup GitHub und Domain – das klickt Manuel bzw. Thomas

Fakten: GitHub-Organisation **VUCABLASTER**, Repo **https://github.com/VUCABLASTER/website** (öffentlich). Domains bei **IONOS**, DNS setzt **Manuel**.
Die Website läuft auf **vucablaster.de**. GitHub Pages kann pro Website nur **eine** Domain bedienen; .com, .store und .global leiten auf vucablaster.de um.

## Heute oder morgen – Manuel (DNS braucht bis zu 24 h)

- [ ] **1. Repo** – erledigt (VUCABLASTER/website). Thomas muss Schreibrechte haben: Repo → Settings → Collaborators and teams → Thomas mit Rolle *Write* oder *Maintain*.

- [ ] **2. DNS für vucablaster.de bei IONOS**
  IONOS → Domains & SSL → vucablaster.de → **DNS**. Vorhandene **A-, AAAA- und CNAME-Einträge für @ und www löschen** (meist die IONOS-Parkseite). **MX-, TXT- und SPF-Einträge nicht anfassen.** Dann anlegen:

  | Typ | Hostname | Wert |
  |---|---|---|
  | A | @ | 185.199.108.153 |
  | A | @ | 185.199.109.153 |
  | A | @ | 185.199.110.153 |
  | A | @ | 185.199.111.153 |
  | AAAA | @ | 2606:50c0:8000::153 |
  | AAAA | @ | 2606:50c0:8001::153 |
  | AAAA | @ | 2606:50c0:8002::153 |
  | AAAA | @ | 2606:50c0:8003::153 |
  | CNAME | www | vucablaster.github.io |

  Falls IONOS meldet, dass die Domain mit einem IONOS-Webspace verbunden ist: Domain zuerst unter „Verwendungsart“ auf **DNS-Einstellungen / Externer Server** umstellen.

- [ ] **3. Domain in GitHub verifizieren**
  github.com/VUCABLASTER → Settings → **Pages** (links unter „Code, planning, and automation“) → **Add a domain** → `vucablaster.de` → GitHub zeigt einen **TXT-Eintrag** (Name `_github-pages-challenge-VUCABLASTER`, Wert eine Zeichenkette) → bei IONOS als TXT bei vucablaster.de anlegen → in GitHub **Verify**.

- [ ] **4. Weitere Domains umleiten (IONOS)**
  vucablaster.store und vucablaster.global: IONOS → Domain → **Weiterleitung** → HTTP-Weiterleitung (301) auf `https://vucablaster.de`.
  **vucablaster.com:** ebenfalls Weiterleitung auf `https://vucablaster.de` – **aber die MX-Einträge (E-Mail hello@vucablaster.com) müssen bleiben.** Nach der Umstellung eine Test-Mail an hello@vucablaster.com schicken.
  Hinweis: Damit auch `https://vucablaster.com` sauber umleitet, braucht die .com bei IONOS ein SSL-Zertifikat (in vielen IONOS-Paketen kostenlos enthalten) – in IONOS unter „SSL“ prüfen. Nicht kritisch für Dienstag.

## Nach dem Bau (Mo/Di) – Thomas

- [ ] **5. Code ins Repo**
  Im Ordner `vuca-blaster-website`:
  ```
  git init
  git branch -M main
  git remote add origin https://github.com/VUCABLASTER/website.git
  git add .
  git commit -m "MVP Website"
  git push -u origin main
  ```
  (Oder Claude Code bitten, das zu tun.)

- [ ] **6. GitHub Pages einschalten**
  github.com/VUCABLASTER/website → Settings → Pages → Source **Deploy from a branch** → Branch `main`, Ordner **`/docs`** → Save.

- [ ] **7. Eigene Domain**
  Gleiche Seite → Custom domain `vucablaster.de` → Save → warten, bis „DNS check successful“ → **Enforce HTTPS** anhaken (Zertifikat kann bis zu einige Stunden dauern).

- [ ] **8. Prüfen – beide**
  `https://vucablaster.de` · `https://www.vucablaster.de` (muss umleiten) · Impressum und Datenschutz verlinkt · Player lädt erst nach Klick · LinkedIn Post Inspector (linkedin.com/post-inspector) mit der URL testen · Test-Mail an hello@vucablaster.com.
