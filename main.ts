// news-image-20261123 entry (Node 22, standard library only): the program
// copies the front-page image beside it to /output/entry.png. The image
// was drawn by generator.py in this session from the day's news — 12
// featured stories and 38 briefs from Monday 23 November 2026, laid out
// as a classic broadsheet front page (masthead, lead, secondaries,
// featured grid, briefs). The render is deterministic: two runs of the
// generator write byte-identical PNGs.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
