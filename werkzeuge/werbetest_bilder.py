"""Lädt die Unsplash-Fotos des Werbetests einmalig herunter und schneidet sie zu (3:2 in 1200 und 600 px, quadratisch 320 px, WebP + JPG).

  python3 werkzeuge/werbetest_bilder.py            # nur fehlende Dateien
  python3 werkzeuge/werbetest_bilder.py --neu      # alle neu erzeugen

Quelle: inhalte/werbetest.json → "bilder" (Unsplash-ID, Fokus = waagrechter Bildschwerpunkt 0–1).
Ergebnis: docs/assets/img/werbetest/<name>-1200.webp|jpg und -600.webp|jpg. Die Website lädt die Fotos von dort,
beim Seitenaufruf geht keine Anfrage an Unsplash. Lizenz: Unsplash-Lizenz (kostenlose Nutzung)."""
import io, json, sys, urllib.request
from pathlib import Path
from PIL import Image, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parent))
from layout import REPO

ZIEL = REPO / 'docs' / 'assets' / 'img' / 'werbetest'


def main():
    neu = '--neu' in sys.argv
    bilder = json.loads((REPO / 'inhalte' / 'werbetest.json').read_text(encoding='utf-8'))['bilder']
    ZIEL.mkdir(parents=True, exist_ok=True)
    for name, b in bilder.items():
        if not neu and (ZIEL / f'{name}-q.webp').exists():
            continue
        url = f'https://images.unsplash.com/{b["unsplash"]}?w=2000&q=90&fm=jpg'
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'vucablaster.de'}), timeout=60) as r:
            im = Image.open(io.BytesIO(r.read())).convert('RGB')
        for breite in (1200, 600):
            zug = ImageOps.fit(im, (breite, breite * 2 // 3), Image.LANCZOS, centering=(b.get('fokus', 0.5), 0.5))
            zug.save(ZIEL / f'{name}-{breite}.webp', 'WEBP', quality=72, method=6)
            zug.save(ZIEL / f'{name}-{breite}.jpg', 'JPEG', quality=76, optimize=True, progressive=True)
        quadrat = ImageOps.fit(im, (320, 320), Image.LANCZOS, centering=(b.get('fokus', 0.5), 0.5))  # dezente Banner (V2)
        quadrat.save(ZIEL / f'{name}-q.webp', 'WEBP', quality=74, method=6)
        quadrat.save(ZIEL / f'{name}-q.jpg', 'JPEG', quality=78, optimize=True, progressive=True)
        print(name, 'ok')


if __name__ == '__main__':
    main()
