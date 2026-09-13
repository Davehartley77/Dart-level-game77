#!/bin/bash
# Records extra caller phrases (key|text lines on stdin) into every existing voice set.
set -e
cd "$(dirname "$0")/.."
LINES=$(cat)
for dir in sounds/voice/*/; do
  slug=$(basename "$dir")
  case "$slug" in serena) VOICE="Serena (Enhanced)";; daniel) VOICE="Daniel";; *) continue;; esac
  TMP=$(mktemp -d)
  while IFS='|' read -r key text; do
    [ -z "$key" ] && continue
    say -v "$VOICE" -o "$TMP/$key.aiff" "$text"
    afconvert -f m4af -d aac -b 56000 "$TMP/$key.aiff" "$dir/$key.m4a" >/dev/null
    grep -qx "$key" "$dir/manifest.txt" || echo "$key" >> "$dir/manifest.txt"
  done <<< "$LINES"
  rm -rf "$TMP"; echo "$slug: $(ls "$dir" | wc -l | tr -d ' ') files"
done
