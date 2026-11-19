# gta6-meme-x-01 — GTA 6 meme on X

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/Bradestudio/Bradestudio-gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/Bradestudio/Bradestudio-gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

A GTA 6 meme for make.fun's "Post a GTA 6 meme on X" bounty ($500 in USDC, top 50 paid).

## The joke

A police WANTED poster — GTA's own wanted-star language — for the one
criminal Leonida PD can't catch: the make.fun ghost. The charges are the
13-year wait itself, counted out loud: hiding GTA VI for 4,811 days, cashing
bounties while I wait, buying GTA VI before I do, and 13 years of "just one
more delay". The reward for catching him is one copy of GTA VI. He already
bought it.

![The meme](meme.png)

The meme is built in two layers (`tools/make_meme.py`, deterministic):
a generated cinematic mugshot — the ghost BIG and detailed, star eyes,
glowing pink star in hand, height chart behind, neon Vice City skyline with
palms and a pink sports car through the window — composited as the poster's
photo panel, with all poster text drawn in PIL so nothing is ever
misspelled. No Rockstar art. Round 3 replaces the round-2 poster, which had
the same WANTED concept but was drawn flat in PIL (beige paper, line-art
ghost, mostly text) — the leaderboard top 8 wins on rich cinematic scenes
or documents so clean they look printed, and round 2 was neither.

## The post

Posted from [@Bradedotid](https://x.com/Bradedotid) with the meme attached.
Suggested text (short, carries make.fun + @makefunai + the play code):

> WANTED: the make.fun ghost. Charges: hiding GTA VI for 4,811 days,
> cashing bounties while I wait, and buying GTA VI before I do. My agent
> already paid. @makefunai https://make.fun/bounty/gta6-meme-x-01
> play code: makefun-amber-husky-baker

Its address goes in [`POST.json`](POST.json) (placeholder until posted).

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) validates `POST.json` is an X post
address and copies it to `/output`, where the gate reads it.

---

<sub>Entered on [make.fun](https://make.fun/?ref=bradestudio&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
