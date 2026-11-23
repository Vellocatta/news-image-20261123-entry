# news-image-20261123-entry

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Vellocatta/news-image-20261123-entry/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Vellocatta/news-image-20261123-entry/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

Monday 23 November 2026: 50 stories, one front page. One image summing up the world news of Monday 23 November 2026.

## The image

A front page, "The World Today", with a lead story (Trump vows to sink Iranian ships after a US strike on a tanker), three secondaries (COP31 collapses, the AI rout, the Russian frigate Merkury sinking off Libya), 8 more featured stories (each with a headline and a deck), and 38 one-line briefs — 50 stories in all:

1. **The Gulf · Iran** — Trump vows to sink Iranian ships after a US tanker strike
2. **Antalya · Climate** — COP31 collapses with no climate deal
3. **Seoul · Markets** — AI rout: shares dive 5% as futures rebound
4. **Benghazi · War at sea** — Russian frigate sinks off Libya in a drone attack
5. **Washington · Politics** — Democrats win biggest House majority since 1992
6. **Riyadh · The Gulf** — Houthis claim strikes on a Saudi oil refinery
7. **Kyiv · Ukraine** — Boy, 7, pulled alive from the rubble
8. **Port Vila · Pacific** — Magnitude 6.5 quake strikes off Vanuatu
9. **London · Football** — UK set to host the 2035 Women's World Cup
10. **Taipei · Cyber** — Chinese hackers "used AI" to hit universities
11. **Paris · France** — French rivals both cool on Ukraine aid
12. **New Delhi · Asia** — India and China open talks to ease border strain

Plus 38 briefs, from South Korea's exports topping $1 trillion to the Mets' record $450m signing of Tarik Skubal.

## How it was made

`generator.py` (Python 3, Pillow) draws the page from `stories.py`: masthead, lead story with drawn hero art, three secondary stories, an 8-story featured grid, and 38 one-line briefs in three columns. Ten candidate variants were generated (five palettes, five lead stories) and judged in a local pairwise tournament; the winner is `v1-navy-iran` — see `tournament.md`. The winning render is byte-identical across two runs. `main.ts` copies `entry.png` to `/output/entry.png`.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
