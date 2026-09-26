# VUCA Blaster Website – START HIER

**Jetzt: MVP bis Dienstag, 29.09.2026. Nur GitHub Pages.**

## Wer macht was

| Wer | Was | Datei |
|---|---|---|
| **Manuel** | Infos ausfüllen, Bilder ablegen | `01-von-manuel/Fragebogen-Manuel-VUCA-Blaster-ausgefuellt.docx` ausfüllen, Fotos nach `01-von-manuel/bilder/` |
| **Manuel / wer DNS-Zugang hat** | Repo anlegen, DNS setzen (heute/morgen!) | `02-mvp/SETUP-GITHUB-DOMAIN.md` Schritte 1–3 |
| **Thomas** | Claude Code starten | `./start-mvp.sh` oder `PROMPT-MVP.md` einfügen |
| **Claude Code** | Website bauen in `docs/` | liest `CLAUDE.md` + `02-mvp/MVP-SPEZ.md` |
| **Thomas / Manuel** | Push, Pages + Domain einschalten | `02-mvp/SETUP-GITHUB-DOMAIN.md` Schritte 4–7 |

## Ordner

```
vuca-blaster-website/
├─ README.md                  ← du bist hier
├─ CLAUDE.md                  Regeln für Claude Code (MVP)
├─ PROMPT-MVP.md              Start-Prompt für Claude Code
├─ start-mvp.sh               startet Claude Code mit dem Prompt (Mac)
├─ 01-von-manuel/             ← HIER liefert Manuel
│  ├─ Fragebogen-Manuel-VUCA-Blaster.docx
│  └─ bilder/
├─ 02-mvp/                    Spezifikation, Design, Klick-Anleitung
│  ├─ MVP-SPEZ.md
│  ├─ SETUP-GITHUB-DOMAIN.md
│  └─ design/                 D3 Desktop, Mobile, Stilblatt (PNG + HTML)
├─ 03-backlog/                alles für später – im MVP ignorieren
│  ├─ BACKLOG.md
│  ├─ BRIEF-final.md          komplette Spezifikation der finalen Version
│  └─ INHALTE-final.md        Ausfüllformular für die finale Version
└─ docs/                      ← hier baut Claude Code die Website (wird veröffentlicht)
```

Alte Entwürfe, Prototypen und frühere Claude-Ausgaben liegen in `../_archiv/` – für das Projekt irrelevant.
