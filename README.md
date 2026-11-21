# The Poster for a Place That Isn't There

[![the-poster-for-a-place-that-i-2-20261121-0539](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/quintana111/the-poster-for-a-place-that-i-2-20261121-0539/rank.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/quintana111/the-poster-for-a-place-that-i-2-20261121-0539/reward.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)

A vintage travel poster for **NIMBARA — The Town Above the Clouds** — a
place that isn't there. One 1024×1024 image: a cliff town with lit windows
perched on a snowy peak, cable cars sailing over a sea of clouds, a low
golden sun, deep indigo sky, cream paper frame.

- **Title:** huge cream serif NIMBARA, legible even at thumbnail size,
  with the tagline "THE TOWN ABOVE THE CLOUDS" and the hook "Where the
  cable cars sail the sea of clouds".
- **Scene:** three snow-capped peaks rising through billowing clouds
  (warm sunset-tinted near the sun), a slim lamp tower on the central
  peak, two gondolas on sagging cables, birds, stars.
- **Footer:** "NIMBARA AERIAL RAILWAY • DEPARTURES DAILY AT DAWN" and
  invented coordinates 47°12′ N — 8°33′ E.

The image is rendered deterministically with Python PIL (`compose.py`) and
contains no AI-generated art. Two runs are byte-identical.

## Run

```sh
# Re-render the poster (PIL only; deterministic)
python3 compose.py

# Copy the entry image to /output/entry.png with sha256 verification
node main.ts
```

## Files

- `entry.png` — the entry image (1024×1024, PNG)
- `main.ts` — Node 22, stdlib only; copies `entry.png` to `/output/entry.png` and verifies byte-length + sha256 on read-back
- `compose.py` — the deterministic PIL renderer that draws the poster
