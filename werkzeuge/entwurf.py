"""Vorausgefüllte Angaben für neue Folgen, abgeleitet aus Titel und Shownotes (Feed).

Es wird nichts erfunden: Alles ist aus dem Wortlaut übernommen. Ist ein Muster nicht eindeutig, bleibt das Feld
leer. Die Einträge sind als ungeprüft markiert (geprueft: false) und tragen einen Hinweis für Manuel.
"""
import re

HOSTS = ('manuel', 'sebastian', 'wyszynski', 'oremek')
TEILE = {'van', 'von', 'der', 'den', 'de', 'zu', 'und', '&', 'la', 'le', 'el', 'ten', 'ter'}
TITEL = r'(?:Prof\.\s+Dr\.|Prof\.|Dr\.)'
# Wörter, die nach „mit“ vorkommen, aber keine Namen sind
KEIN_NAME = {'herz', 'verstand', 'empathie', 'begeisterung', 'leidenschaft', 'freude', 'humor', 'haltung', 'mut', 'ki',
             'energie', 'neugier', 'zuversicht', 'optimismus', 'wirkung', 'ruhe', 'fokus', 'ziel', 'ziele', 'kopf', 'bauch'}


def titel_ohne_nummer(titel_roh):
    return re.sub(r'^\s*#\s*\d+\s*[-–:]?\s*', '', titel_roh).strip()


def gast(titel_roh):
    """Name nach dem letzten „mit“ im Titel, wenn er wie ein Personenname aussieht."""
    t = titel_ohne_nummer(titel_roh)
    pos = t.lower().rfind(' mit ')
    if pos < 0:
        return ''
    name = t[pos + 5:].strip(' .–-')
    woerter = name.split()
    if not 2 <= len(woerter) <= 8:
        return ''
    if any(w.lower().strip('.,') in KEIN_NAME for w in woerter):
        return ''
    if any(h in name.lower() for h in HOSTS):
        return ''
    for w in woerter:
        if w.lower() in TEILE or re.match(rf'^{TITEL}$', w):
            continue
        if not re.match(r'^[A-ZÄÖÜ][\wäöüÄÖÜß.\-]*$', w):
            return ''
    return name


def _ohne_titel(name):
    return re.sub(rf'^(?:{TITEL}\s+)+', '', name).strip()


def rolle(text, name):
    """Berufsbezeichnung, wenn sie direkt vor oder nach dem Namen in den Shownotes steht."""
    if not name:
        return ''
    kern = re.escape(_ohne_titel(name.split(' und ')[0].split(' & ')[0]))
    muster = [
        # „Mit Schauspielerin, Sprecherin und Executive Coach Claudia Jahn“, „mit dem Generationenforscher Dr. Rüdiger Maas“
        rf'\b[Mm]it\s+(?:dem\s+|der\s+|den\s+)?(?P<r>[A-ZÄÖÜ][^.!?;:\n]{{2,90}}?)\s+(?:{TITEL}\s+)*{kern}\b',
        # „Dr. Maja Storch, Psychologin, Psychoanalytikerin und …“
        rf'(?:{TITEL}\s+)*{kern},\s+(?P<r>[A-ZÄÖÜ][^.!?;:\n]{{2,90}}?)(?:,?\s+(?:sprechen|spricht|spreche|erzählt|zeigt|teilt)\b|[.!?])',
    ]
    for m in muster:
        r = re.search(m, text)
        if r:
            wert = r.group('r').strip(' ,')
            if 3 <= len(wert) <= 90 and not re.search(r'\b(wir|ich|uns|unser\w*|Folge|Gast|Podcast)\b', wert):
                if re.match(r'(?i)mit\s+dem\s', r.group(0)) and ' ' not in wert and wert.endswith('en'):
                    wert = wert[:-1]  # „mit dem Psychologen“ → „Psychologe“
                return wert
    return ''


def teaser(text):
    """Ein bis zwei Sätze aus dem Anfang der Shownotes, wörtlich, höchstens rund 200 Zeichen."""
    t = re.sub(r'[^\w\s.,;:!?„“"\'’()\-–/&%€$äöüÄÖÜß@]', ' ', text)  # Emojis, Symbole
    t = re.sub(r'\s+', ' ', t).strip()
    saetze = re.split(r'(?<=[.!?])\s+(?=[A-ZÄÖÜ„"])', t)
    aus = ''
    for s in saetze:
        s = s.strip()
        if len(s.split()) < 5 or re.search(r'https?://|www\.|@\w', s):   # Überschriften, Zurufe, Sätze mit Link
            continue
        if re.search(r'viel spaß|hör doch|jetzt reinhören|abonnier|bewert', s, re.I):
            continue
        if not aus:
            aus = s
        elif len(aus) + 1 + len(s) <= 210:
            aus += ' ' + s
        else:
            break
        if len(aus) >= 110:
            break
    if len(aus) > 230:
        aus = aus[:230].rsplit(' ', 1)[0].rstrip(',;:') + ' …'
    return aus


STAEMME = {
    'mutig': r'(?<![a-zäöüß])mut(?!ter|maß)\w*|\w*[a-zäöüß]mut\b',
    'optimistisch': r'optimis|zuversicht',
    'neugierig': r'neugier',
    'authentisch': r'authentisch|authentizität|echtheit',
    'verbindend': r'verbind|zusammenarbeit|gemeinsam|brücke',
}


def werte(titel_roh, text, transkript=''):
    """Hauptwert = Wert mit den meisten Schlüsselwort-Treffern. Titel zählt vierfach, Shownotes einfach, das Transkript
    (falls vorhanden) nach Dichte (Treffer je 2.000 Wörter). Leer nur, wenn kein Schlüsselwort vorkommt."""
    t, n = titel_roh.lower(), text.lower()
    woerter = max(len(transkript.split()), 1)
    punkte = {}
    for w, p in STAEMME.items():
        punkte[w] = 4 * len(re.findall(p, t)) + len(re.findall(p, n))
        if transkript:
            punkte[w] += len(re.findall(p, transkript.lower())) * 2000 / woerter
    w1, n1 = max(punkte.items(), key=lambda x: x[1])
    return w1 if n1 > 0 else ''


def entwurf(f, transkript=''):
    """f: Folge mit titel_roh und text (Shownotes als Klartext). Liefert nur gefüllte Felder."""
    out = {}
    g = gast(f['titel_roh'])
    if g:
        out['gast'] = g
        r = rolle(f['text'], g)
        if r:
            out['rolle'] = r
    t = teaser(f['text'])
    if t:
        out['teaser'] = t
    w = werte(f['titel_roh'], f['text'], transkript)
    if w:
        out['hauptwert'] = w
    if out:
        out['hinweis'] = 'Automatischer Entwurf aus Titel und Shownotes. Bitte prüfen und ergänzen (Rolle, Werte, Key Learnings).'
    return out
