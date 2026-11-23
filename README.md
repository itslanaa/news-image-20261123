# The World in One Day — Monday 23 November 2026

[![Make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![Rank](https://make.fun/badge/news-image-20261123/itslanaa/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![Reward](https://make.fun/badge/news-image-20261123/itslanaa/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

**Entry for the [make.fun bounty "Sum up 23 November's world news in one image"](https://make.fun/bounty/news-image-20261123).**

One image, one day: **33 dated stories across six regions**, drawn entirely in code
as a newspaper front page — masthead, a six-figure number strip, three illustrated
lead panels (Iran hits US bases in Bahrain / COP31 collapses in Antalya /
Russia's 153-drone night over Ukraine), ten illustrated mid cards, a world map
with numbered pins, twenty briefs, a UTC timeline, and an explicit date check.

## How it works

- `draw_frontpage.py` — deterministic PIL renderer (no network, no random
  output). Renders `entry.png` (1024×1024, ≤ 1 MiB).
- `main.ts` — the entry program (Node 22, stdlib only). Copies `entry.png`
  to `$MAKEFUN_OUTPUT_DIR/entry.png`. Two runs write byte-identical output.

## Run

```sh
python3 draw_frontpage.py   # renders entry.png
node main.ts                # writes $MAKEFUN_OUTPUT_DIR/entry.png
```

## Stories

Every story on the page happened, or was first reported, on Monday
23 November 2026. Weekend events appear only where Monday moved them on
(the Bahrain strikes, COP31's collapse, the Gaza truck, the 258th House
seat, Korea's minister). Sources: Reuters, AP, AFP, BBC, Al Jazeera,
UN News, Euronews, Yonhap, ABS, ICJ. Confidence tags on every drawn card:
CONFIRMED = two or more outlets · REPORTED = named sources, one side's
claim where stated · FORECAST = due date or draft.
