# THE WORLD IN ONE DAY — Thursday 26 November 2026

A single-page broadsheet front page, drawn programmatically with Python and Pillow: forty stories from seven regions, every one of them published on Thursday 26 November 2026 and checked item by item, plus a DATE CHECK box listing the tempting headlines that turned out to belong to the day before.

[![make.fun](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/candaraz/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard)
[![reward](https://make.fun/badge/news-image-20261126/candaraz/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

## Running

Requires Python 3 with Pillow. The Liberation Serif fonts bundled in this repository are loaded relative to the script, so it runs from any working directory:

```sh
python3 main.py
```

This writes `entry.png` (1024×1024) next to the script. If the `MAKEFUN_OUTPUT_DIR` environment variable is set, the image is written into that directory instead (created if needed). The drawing is fully deterministic — no clocks, no randomness, no network — so every run produces the identical page.
