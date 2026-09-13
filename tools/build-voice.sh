#!/bin/bash
# Records every line the caller can say with a macOS voice, as small AAC clips the game plays on any device.
# usage: tools/build-voice.sh "Serena (Enhanced)" serena
set -e
VOICE="$1"; SLUG="$2"
cd "$(dirname "$0")/.."
OUT="sounds/voice/$SLUG"; mkdir -p "$OUT"
TMP=$(mktemp -d)
render() { # key, text
  say -v "$VOICE" -o "$TMP/$1.aiff" "$2"
  afconvert -f m4af -d aac -b 56000 "$TMP/$1.aiff" "$OUT/$1.m4a" >/dev/null
  rm -f "$TMP/$1.aiff"
}
for n in $(seq 0 180); do render "n-$n" "$n"; done
render "n-180" "One hundred and eighty!"
render "n-0" "No score."
while IFS='|' read -r key text; do [ -n "$key" ] && render "$key" "$text"; done <<'LINES'
you-require|you require
game-on|Game on!
game-shot|Game shot!
game-shot-match|Game, shot, and the match!
no-score-bust|No score! Bust.
bust|Bust.
treble|treble
double|double
single|single
bull|bull
outer-bull|outer bull
hit|Hit!
missed|Missed.
no-points-lost|No points lost.
saved|Saved by the bull!
checkout|Checkout
level|level
what-a-checkout|What a checkout!
yes|Yes!
wonderful-darts|Wonderful darts!
a-ton|A ton!
ton-forty|Ton forty!
ton-sixty|Ton sixty!
bed-and-breakfast|Twenty six. Bed and breakfast.
takes-leg|takes the leg.
the-big-fish|The big fish! One hundred and seventy! Game shot!
what-a-finish|What a finish!
voice-control-on|Voice control on. Say your score.
undone|Undone.
to-throw-again|to throw again.
points|points
has|has
minus|minus
wins|wins!
with|with
stays-on-level|stays on level
caller-on|Caller on.
player|Next player.
LINES
# names
: > "$OUT/names.txt"
for name in $(cat sounds/names.txt); do
  slug=$(echo "$name" | tr '[:upper:]' '[:lower:]' | tr -cd 'a-z0-9')
  render "name-$slug" "$name."
  echo "$slug" >> "$OUT/names.txt"
done
ls "$OUT" | sed 's/\.m4a$//' | grep -v '^names$' > "$OUT/manifest.txt"
rm -rf "$TMP"
echo "$SLUG: $(ls "$OUT" | wc -l | tr -d ' ') files, $(du -sh "$OUT" | cut -f1)"
