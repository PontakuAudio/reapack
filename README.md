# Pontaku Audio — ReaPack repository

One ReaPack repository for every free REAPER script and extension from Pontaku Audio.
Register this single URL and new tools appear in ReaPack as they are released — no extra registrations.

Pontaku Audio の無料 REAPER スクリプト／拡張は、この1つのリポジトリにまとまっています。

## Add this repository to ReaPack

1. In REAPER, open **Extensions → ReaPack → Import repositories…**
2. Paste this URL:

   ```text
   https://github.com/PontakuAudio/reapack/raw/main/index.xml
   ```

3. Open **Extensions → ReaPack → Browse packages…** and install what you need.

## Packages

| Package | Category | Notes |
| --- | --- | --- |
| SoundPrep | Media Explorer | Audition sound effects through your FX chains in Media Explorer, then drag processed audio into Arrange. |
| Pitch Canvas Extension — Adaptive Precision | Extensions | Experimental. Helps VST3 instruments follow Pitch Canvas curves more closely. Install Pitch Canvas separately. |

## How this index is maintained

Each product keeps its own repository and its own generated `index.xml`.
`tools/merge_index.py` merges the indexes listed in `sources.txt` into the
`index.xml` at this repo's root. A GitHub Action re-runs the merge daily and
on demand, so product releases flow into this repository automatically.
The per-product indexes remain available, but this merged repository is the
recommended registration.
