# Product Sense 101

30-day static coaching course (one HTML lesson per day). Source lives in the repo root; production assets are built into `dist/`.

## Local preview

```bash
npm install
npm run dev          # source HTML
npm run build
npm run dev:dist     # minified build
```

## Deploy (Vercel)

**Git (recommended):** Connect [haiden-m/product-sense-101](https://github.com/haiden-m/product-sense-101) to the Vercel project `product-sense-101` on team **heyhaiden's projects**. Vercel runs `npm run build` and serves `dist/` (see `vercel.json`). Pushes to `main` deploy production; other branches get previews.

**CLI (manual):**

```bash
vercel login
npm run deploy
```

Local CLI link lives in `.vercel/` (not committed).
