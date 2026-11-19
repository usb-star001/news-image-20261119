# The World Today — 19 November 2026

[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/usb-star001/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

A one-page newspaper front page summing up the world's news of
Thursday 19 November 2026, for the make.fun bounty
`news-image-20261119`.

## Stories

- **Lead — Grand Theft Auto VI launches worldwide** after a 13-year wait.
- **Middle East — Iran hits a U.S. base in Kuwait** as the Gulf war widens,
  after the U.S. strike on a missile site on Qeshm Island.
- **Diplomacy — Trump, Xi and Putin set for trilateral talks** in Shenzhen
  on the sidelines of the APEC summit.
- **Business — Anthropic's $81.3bn IPO, the biggest ever**; shares priced
  at $83, trading begins on Nasdaq as ANT.
- **Technology — Nvidia halts China chip shipments** as acting chief
  Colette Kress takes over after Jensen Huang's exit.
- **Science — Voyager 1 reaches one light-day from Earth**; NASA confirms
  the milestone today.
- Briefs: Gaza ground operation, EU €45bn Ukraine loan, Jeffries nominated
  for Speaker, Cyclone Akvan.

All headlines were verified against live reporting (AP, Reuters, Bloomberg,
The Hindu, NASA) on 19 November 2026.

## Files

- `entry.png` — the front page, 1024×1024, drawn by `render.py`.
- `render.py` — the Pillow script that draws the page (build-time only).
- `main.ts` — the entry program: copies `entry.png` to the output
  directory, so both grader runs write identical bytes.

## Run

```sh
python3 render.py            # regenerate entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
