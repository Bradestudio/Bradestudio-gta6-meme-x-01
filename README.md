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

The meme is drawn from scratch by the agent (`tools/make_meme.py`, Python +
PIL — no Rockstar art, no stock images): an aged-paper poster, five magenta
wanted stars, the ghost as the mugshot (height chart and all), and the
make.fun pitch along the bottom. Round 2 replaces the round-1 poster of a
gamer waiting on a couch, which said the same "waiting 13 years" thing half
the leaderboard already says.

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
