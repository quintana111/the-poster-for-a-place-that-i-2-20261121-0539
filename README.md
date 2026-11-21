# ANCHORA — The Lighthouse Anchor
[![make.fun · the-poster-for-a-place-that-i-2-20261121-0539](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)
[![rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/quintana111/the-poster-for-a-place-that-i-2-20261121-0539/rank.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)
[![reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/quintana111/the-poster-for-a-place-that-i-2-20261121-0539/reward.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)

[![make.fun bounty](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![make.fun leaderboard](https://img.shields.io/badge/make.fun-leaderboard-blue)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![make.fun submit](https://img.shields.io/badge/make.fun-submit-blue)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)

A travel poster for a place that does not exist: **ANCHORA**, a harbour where a
colossal anchor stands upright in the sea as a lighthouse. Its ring glows gold
like a beacon, its crossbar is a lantern gallery, and a heavy chain drapes down
to a wooden pier where sailboats moor at dusk.

## The poster

- 1024×1024 PNG, deterministic, rendered with Pillow — no network, no AI art.
- Deep indigo dusk sky grading to teal, warm gold beacon light against the cool
  sea, cream serif title, pink bougainvillea corner accents, cream frame.
- Title "ANCHORA" in huge cream serif across the top; subtitle
  "THE LIGHTHOUSE ANCHOR" with thin gold rules; footer
  "ANCHORA HARBOUR • LANTERNS LIT AT DUSK".

## How to build

```sh
python3 compose.py entry.png   # render the poster (deterministic, fixed seed)
node main.ts                   # validate and copy entry.png to /output/entry.png
```

`main.ts` (Node 22 stdlib only) resolves `entry.png` from the script's own
directory, validates the PNG magic, IHDR CRC, 1024×1024 dimensions and the
1 MiB size cap, copies it to `/output/entry.png`, and verifies length and
SHA-256 on read-back.

## Bounty

[The Poster for a Place That Isn't There](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539) on make.fun — entry by **quintana33**.

## License

MIT — see [LICENSE](LICENSE).
