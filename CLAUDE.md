# Saved by the Bull — project guide

The owner doesn't code. Explain changes in plain English, keep the project tidy, and say so when an idea is a bad one.

## What this is
A darts scoring app for a few friends: **Saved by the Bull** (the main game, rules in `RULES.md`), **501** with checkout suggestions, and **Killer**. You can play against mates or against **Bully**, the bull mascot and Dart Bot (15 skill levels). A voice caller reads out scores. It installs on a phone as an app (PWA) and works offline.

## Where things are
| Path | What it is |
|------|------------|
| `index.html` | **The whole game**: styles, logic and the Bully drawings in one file. Sections are marked `// ---------- name ----------` (rules, 501 checkout chart, Bully, Dart Bot, caller, voice control, render, game flow for each mode). |
| `RULES.md` | The Saved by the Bull rules. Keep this in step with the `LEVELS` table in `index.html`. |
| `manifest.json`, `sw.js` | Make it installable and offline. **Run `tools/stamp.sh` before publishing** so installed phones pick up the new version. |
| `images/` | App icons. |
| `sounds/voice/<voice>/` | Recorded caller clips (`.m4a`) plus `manifest.txt` and `names.txt` listing them. **George** (the default caller) is the free Kokoro AI voice, brisk with no echo (the owner disliked echo and slow delivery), made by `tools/build-george.py`; Serena and Daniel are Mac voices. |
| `tools/` | Mac-only scripts: `build-voice.sh` records a full voice set, `add-phrases.sh` adds new caller lines, `stamp.sh` bumps the app version. They use macOS `say`/`afconvert`, so they won't run in a Linux cloud session. |
| `design/mascot-draft.html` | Bully's character sheet (poses). |
| `old/` | Earlier Python/React attempts. Not used by the game; kept for reference only. |

## How it's published
- A Claude artifact page (the `index.html` page plus files) for quick previews.
- **Live site: GitHub Pages**, built from the `main` branch: https://davehartley77.github.io/Dart-level-game77/. Every push to `main` goes live in about a minute (the "pages build and deployment" run in GitHub Actions). Only push to `main` once the owner has said to make it live.

## Working notes
- Develop on the session branch, then merge to `main`.
- Adding a new caller phrase: add it to `TOKEN_TEXT` in `index.html`, then run `tools/build-george.py` (works in a cloud session) for George, and `tools/add-phrases.sh` on the Mac for Serena and Daniel. Unknown phrases are skipped, not spoken, so a missing clip makes the caller go quiet for that line.
- Keep it working on iPhone Safari. It's the main device, including the silent-switch audio trick and the installed home-screen app.
