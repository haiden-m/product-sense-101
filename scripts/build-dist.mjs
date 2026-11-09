#!/usr/bin/env node
/**
 * Minify all course HTML into dist/ for deployment (smaller, fewer bytes over the wire).
 */
import { mkdir, readFile, writeFile, cp, readdir, rm } from "node:fs/promises";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { minify } from "html-minifier-terser";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const dist = join(root, "dist");

const minifyOptions = {
  collapseWhitespace: true,
  conservativeCollapse: true,
  removeComments: true,
  removeRedundantAttributes: true,
  removeScriptTypeAttributes: true,
  removeStyleLinkTypeAttributes: true,
  useShortDoctype: true,
  minifyCSS: true,
  minifyJS: true,
  keepClosingSlash: true,
  // Quizzes and scenario textareas must keep user-facing whitespace where it matters
  ignoreCustomFragments: [/\{\{[\s\S]*?\}\}/],
};

async function main() {
  await rm(dist, { recursive: true, force: true });
  await mkdir(dist, { recursive: true });

  const htmlFiles = (await readdir(root))
    .filter((f) => f.endsWith(".html"))
    .sort();

  let totalIn = 0;
  let totalOut = 0;

  for (const file of htmlFiles) {
    const src = join(root, file);
    const raw = await readFile(src, "utf8");
    totalIn += Buffer.byteLength(raw, "utf8");
    const out = await minify(raw, minifyOptions);
    totalOut += Buffer.byteLength(out, "utf8");
    await writeFile(join(dist, file), out, "utf8");
  }

  await cp(join(root, "vercel.json"), join(dist, "vercel.json"));
  await writeFile(
    join(dist, "package.json"),
    JSON.stringify(
      {
        name: "product-sense-101",
        private: true,
        description: "Product Sense 101 — static dist (built)",
      },
      null,
      2,
    ) + "\n",
    "utf8",
  );

  const saved =
    totalIn > 0 ? Math.round((1 - totalOut / totalIn) * 100) : 0;
  console.log(
    `dist: ${htmlFiles.length} HTML files, ${totalIn} → ${totalOut} bytes (~${saved}% smaller)`,
  );
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
