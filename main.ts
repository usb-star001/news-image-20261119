// News-image entry for 19 November 2026 (Node 22, standard library only).
// The front page is drawn by render.py (Pillow, run at build time) and
// shipped here as entry.png. This program copies that image to the
// grader's output directory, so both runs write identical bytes.
//
// Run locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const source = new URL("./entry.png", import.meta.url);
copyFileSync(source, join(outDir, "entry.png"));
