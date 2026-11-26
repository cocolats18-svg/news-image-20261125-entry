# news-image-20261125 — The World in One Image

[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/cocolats18-svg/news-image-20261125-entry/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/cocolats18-svg/news-image-20261125-entry/reward.svg)](https://make.fun/bounty/news-image-20261125)

Entry for the make.fun bounty
[news-image-20261125](https://make.fun/bounty/news-image-20261125):
sum up 25 November 2026's world news in one image.

## The image

A flat-vector newspaper front page for **Wednesday 25 November 2026**,
drawn from scratch with Python + Pillow (`render.py`):

- **Lead — Strait of Hormuz:** Iran's IRGC says oil tankers struck naval
  mines, exploded and caught fire in the strait, on an unauthorised route.
- **Yemen / Saudi Arabia:** Houthis say they hit the Ras Tanura refinery;
  air defences intercepted four drones. A Riyadh strike injured 11.
- **Gaza:** Israel's military killed Mohammad Abuelouf, the Hamas colonel
  heading its interior security service, with his wife and two children.
- **Russia / Ukraine:** a Russian strike on the Odesa region killed 2 and
  injured 3, including a child; Kyiv was hit, 2 injured. Ukrainian drones
  set two Rosneft refineries ablaze; 1 killed.
- **Trade:** tariffs proposed on 14 economies, including China (+20%);
  none take effect before a 25 January hearing.
- **Courts:** a Brooklyn jury convicted Huawei on 10 of 12 counts.
- **Markets:** KOSPI −6.16%, Nikkei −2.78%, S&P 500 −2.2%, Nasdaq about
  −3.2%; the Dow closed above 50,000 for the first time (50,018.70).
- **Also today:** Shenzhou-24 docks with Tiangong carrying Pakistan's
  first astronaut; Colombia hostages freed after a 17-hour siege; the
  Australia–Solomon Islands treaty; RSF drone strikes in Sudan;
  Pope Leo XIV on the failure of the COP31 talks.

Every number on the image comes from the 25 November 2026 news slate;
no figures were invented. No photorealistic faces or real leaders'
likenesses — flags, maps, icons and short text only.

## Run

The entry program is `main.ts` (Node 22, standard library only): it copies
the finished `entry.png` to `$MAKEFUN_OUTPUT_DIR` (or `/output`).

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

To redraw the image from scratch:

```sh
python3 render.py entry.png
```

The render is deterministic: two runs produce byte-identical PNGs
(1024×1024, under 1 MiB).

## License

MIT — see [LICENSE](LICENSE).
