// news-image-20261125 entry (Node 22, standard library only).
// The image is the entry.png beside this file, drawn from scratch by
// render.py (Python + Pillow, deterministic, no network); the program
// copies it byte for byte to /output/entry.png, so both grader runs
// write identical bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const source = new URL('./entry.png', import.meta.url);
mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, 'entry.png'));
