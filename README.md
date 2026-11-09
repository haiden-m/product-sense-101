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

```bash
vercel login
npm run deploy
```

Project is linked via `.vercel/` (not committed). Build output is uploaded from `dist/`.
