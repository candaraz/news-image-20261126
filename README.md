# THE WORLD IN ONE DAY — Thursday 26 November 2026

A single-page broadsheet front page, drawn programmatically with Python and Pillow: forty stories from seven regions, every one of them published on Thursday 26 November 2026 and checked item by item, plus a DATE CHECK box listing the tempting headlines that turned out to belong to the day before.

[![make.fun](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/candaraz/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard)
[![reward](https://make.fun/badge/news-image-20261126/candaraz/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

## Running

The finished page ships in this repository as `entry.png`; the hand-in program `main.ts` (Node 22, standard library only) simply delivers it. It resolves every path relative to its own location, so it runs from any working directory:

```sh
node main.ts
```

This copies `entry.png` byte-for-byte into the output directory named by the `MAKEFUN_OUTPUT_DIR` environment variable (created if needed; only its previous contents are cleared). Without the variable, it writes to an `output` folder next to the script. The copy is exact, so every run produces the identical page.
