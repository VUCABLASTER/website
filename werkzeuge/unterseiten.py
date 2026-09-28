"""Erzeugt Impressum, Datenschutz (aus 01-von-manuel/DATENSCHUTZ.md) und 404."""
import re, html
from layout import REPO, page

def linkify(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'(https?://[^\s)]+)', lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>', t)
    t = re.sub(r'\b([\w.+-]+@[\w-]+\.[\w.]+)\b', r'<a href="mailto:\1">\1</a>', t)
    t = re.sub(r'Telefon: (\d+)', r'Telefon: <a href="tel:\1">\1</a>', t)
    return t

def main(site):
    (site/"impressum").mkdir(exist_ok=True)
    (site/"datenschutz").mkdir(exist_ok=True)
    # ---- Impressum (1:1 aus dem Fragebogen, ohne interne Anmerkung) ----
    imp = '''  <div class="legal-body">
    <p>Immanuel Wyszynski<br>
    Kortumstraße 9<br>
    45130 Essen</p>
    <h2>Kontakt</h2>
    <p>Telefon: <a href="tel:017662512658">017662512658</a><br>
    E-Mail: <a href="mailto:manuel.wy@googlemail.com">manuel.wy@googlemail.com</a></p>
    <p>Quelle: <a href="https://www.e-recht24.de/impressum-generator.html">https://www.e-recht24.de/impressum-generator.html</a></p>
  </div>'''
    open(site/'impressum'/'index.html','w',encoding='utf-8').write(page(
      'Impressum – VUCA Blaster','<link rel="canonical" href="https://vucablaster.de/impressum/">\n','../','Impressum',
      ('', f'<section class="legal" aria-label="Impressum">\n{imp}\n</section>')))

    # ---- Datenschutz (1:1 aus DATENSCHUTZ.md) ----
    md = open(REPO/'01-von-manuel'/'DATENSCHUTZ.md', encoding='utf-8').read().strip().split('\n\n')
    assert md[0].startswith('# Datenschutzerklärung')
    out=[]
    for block in md[1:]:
        if block.startswith('## '):
            out.append(f'    <h2>{html.escape(block[3:], quote=False)}</h2>')
        else:
            lines=[linkify(l) for l in block.split('\n')]
            out.append('    <p>' + '<br>\n    '.join(lines) + '</p>')
    ds='  <div class="legal-body">\n' + '\n'.join(out) + '\n  </div>'
    open(site/'datenschutz'/'index.html','w',encoding='utf-8').write(page(
      'Datenschutzerklärung – VUCA Blaster','<link rel="canonical" href="https://vucablaster.de/datenschutz/">\n','../','Datenschutzerklärung',
      ('', f'<section class="legal" aria-label="Datenschutzerklärung">\n{ds}\n</section>')))

    # ---- 404 (absolute Pfade, weil GitHub sie unter jeder URL ausliefert) ----
    nf_board = '  <p class="notfound-note">Hier steht noch nichts.</p>\n'
    nf_body = '<div class="notfound-body"><a class="btn" href="/">Zur Startseite</a></div>'
    open(site/'404.html','w',encoding='utf-8').write(page(
      'Seite nicht gefunden – VUCA Blaster','','/','Seite nicht gefunden',(nf_board, nf_body)))


if __name__ == "__main__":
    main(REPO/"docs")
