// gta6-meme-x-01 entry program (Node 22, standard library only).
//
// The entry itself is the X post: a GTA 6 meme (meme.png in this repo) posted
// from @Bradedotid with make.fun and the play code in its text. This program
// only hands the post's address to the grader: it reads POST.json from the
// repository root, checks it is a real X post address, and copies it to the
// output directory where the gate reads it.
//
// Local run:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

// An X post address: https://x.com/<handle>/status/<digits> (or twitter.com).
const POST_URL = /^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/[^/]+\/status\/\d+$/;

const source = join(BOT_DIR, "POST.json");
const raw = readFileSync(source, "utf8");
if (raw.length > 16384) {
  console.error(`POST.json is ${raw.length} bytes, over the gate's 16384 cap`);
  process.exit(1);
}
const post = JSON.parse(raw);

if (typeof post !== "object" || post === null || Array.isArray(post)) {
  console.error("POST.json must be a JSON object with a url field");
  process.exit(1);
}
if (typeof post.url !== "string" || !POST_URL.test(post.url)) {
  console.error(`POST.json url is not an X post address: ${String(post.url)}`);
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
copyFileSync(source, join(OUTPUT_DIR, "POST.json"));
console.log(`POST.json copied to ${OUTPUT_DIR}: ${post.url}`);
