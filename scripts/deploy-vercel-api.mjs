#!/usr/bin/env node
/**
 * Deploy dist/ to an existing Vercel project via REST API.
 * Requires: VERCEL_TOKEN (or `vercel login` token in env).
 *
 * Usage: VERCEL_TOKEN=... node scripts/deploy-vercel-api.mjs
 */
import { createHash } from "node:crypto";
import { readFile, readdir } from "node:fs/promises";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const dist = join(root, "dist");
const TEAM_ID = "team_n0zMLuyVjnHyDjJTn6mR9Q1B";
const PROJECT_ID = "prj_o8BiPRZQyz8zmjW5xCBgQ5lvF5FY";

const token = process.env.VERCEL_TOKEN;
if (!token) {
  console.error("Set VERCEL_TOKEN (create at https://vercel.com/account/tokens)");
  process.exit(1);
}

const api = (path, init = {}) =>
  fetch(`https://api.vercel.com${path}`, {
    ...init,
    headers: {
      Authorization: `Bearer ${token}`,
      ...(init.headers || {}),
    },
  });

async function uploadFile(name, buf) {
  const sha = createHash("sha1").update(buf).digest("hex");
  const size = buf.length;
  const res = await api(`/v2/files?teamId=${TEAM_ID}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/octet-stream",
      "x-vercel-digest": sha,
      "Content-Length": String(size),
    },
    body: buf,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Upload ${name} failed: ${res.status} ${text}`);
  }
  return { file: name, sha, size };
}

async function main() {
  const names = (await readdir(dist)).filter((f) => !f.startsWith(".")).sort();
  const fileRefs = [];
  for (const name of names) {
    const buf = await readFile(join(dist, name));
    fileRefs.push(await uploadFile(name, buf));
    process.stderr.write(`uploaded ${name}\n`);
  }

  const body = {
    name: "product-sense-101",
    project: PROJECT_ID,
    target: "production",
    files: fileRefs,
  };

  const res = await api(`/v13/deployments?teamId=${TEAM_ID}&skipAutoDetectionConfirmation=1`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const json = await res.json();
  if (!res.ok) {
    console.error(JSON.stringify(json, null, 2));
    process.exit(1);
  }
  const url = json.url ? `https://${json.url}` : json.alias?.[0];
  console.log(url || JSON.stringify(json, null, 2));
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
