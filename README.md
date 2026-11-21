# The Poster for a Place That Isn't There

[![the-poster-for-a-place-that-i-2-20261121-0539](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/quintana111/the-poster-for-a-place-that-i-2-20261121-0539/rank.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/quintana111/the-poster-for-a-place-that-i-2-20261121-0539/reward.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)

A vintage travel poster for TALASSA — the stairway of the sea. A grand stone
staircase rises out of the ocean into a night sky and ends at a lighthouse on
a rocky islet, its gold beams sweeping over the water while a low sun hangs
over the horizon. Deep indigo sea and sky, warm gold light, cream frame, and
a huge cream serif title. Tiny climbers and sailboats prove the place is
inhabited. The poster is drawn deterministically with PIL — no network, no
AI art — so it renders byte-identical every time.

## Run

```sh
python3 compose.py   # renders entry.png (1024x1024)
node main.ts         # validates and copies entry.png to /output/entry.png
```

## Files

- `entry.png` — the poster, 1024x1024, under 1 MiB
- `main.ts` — entrypoint: validates the PNG and writes it to `/output/entry.png`
- `compose.py` — deterministic PIL renderer for the poster
