// Entry program for news-image-20261123.
//
// The front page is drawn in code by draw_frontpage.py (PIL) at build time
// and shipped in this repo as entry.png. This program copies that file to
// the directory the harness reads: $MAKEFUN_OUTPUT_DIR/entry.png
// (default /output). No network, no dependencies beyond Node's stdlib.
// Deterministic: the same bytes are written on every run.

import { mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const bytes = readFileSync(join(here, "entry.png"));

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");
writeFileSync(target, bytes);
console.log(`entry.png -> ${target} (${statSync(target).size} bytes)`);
