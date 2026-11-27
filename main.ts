// Hand-in program for the news-image-20261126 entry.
//
// The rendered front page ships inside this repository as entry.png.
// All this program does is deliver that file: it works out where it
// lives on disk from its own location, prepares the output directory
// the grader points at, and copies the PNG across untouched.

import { copyFileSync, mkdirSync, readdirSync, rmSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Every path below hangs off the folder holding this script, so the
// program behaves the same no matter where it is launched from.
const scriptDir = dirname(fileURLToPath(import.meta.url));
const sourcePng = join(scriptDir, "entry.png");

// The grader names the destination through the environment; fall back
// to a plain "output" folder beside the script when it is absent.
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? join(scriptDir, "output");

// Create the output directory when needed, then clear whatever a
// previous run left inside it. Only the contents go — the directory
// itself always stays in place.
function prepareOutputDir(dir: string): void {
  mkdirSync(dir, { recursive: true });
  for (const name of readdirSync(dir)) {
    rmSync(join(dir, name), { recursive: true, force: true });
  }
}

// Deliver the page: a straight byte-for-byte copy of the bundled PNG
// into the prepared output directory, under the name the grader
// expects to find there.
function deliverPage(): void {
  prepareOutputDir(outputDir);
  copyFileSync(sourcePng, join(outputDir, "entry.png"));
}

deliverPage();
