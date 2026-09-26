#!/usr/bin/env bash
# Startet Claude Code im Projektordner mit dem MVP-Prompt (Mac/Linux).
cd "$(dirname "$0")" || exit 1
command -v claude >/dev/null || { echo "Claude Code (claude) nicht gefunden – bitte installieren oder PROMPT-MVP.md manuell einfügen."; exit 1; }
ls 01-von-manuel/*.docx >/dev/null 2>&1 || echo "Hinweis: kein Fragebogen in 01-von-manuel/ gefunden."
PROMPT="$(sed -n '/^---$/,$p' PROMPT-MVP.md | tail -n +2)"
exec claude "$PROMPT"
