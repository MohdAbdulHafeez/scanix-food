# Scanix AI — frontend

A Next.js (App Router, TypeScript) app for Scanix AI. Hand-written CSS, no UI
framework — the look is bespoke ("warm forensic": a dark instrument panel read
by a turmeric-marigold light, with a rotating **verdict seal** as the signature).

## Run

```bash
npm install
npm run dev          # http://localhost:3000
```

Requests to `/api/*` are proxied to the FastAPI backend (`http://localhost:8000`
by default — override with `BACKEND_ORIGIN`). The scan page also ships a sample
dossier (`/scan#sample`) so you can explore the UI before the backend is live.

## Map

```
app/
  layout.tsx       fonts (Bricolage Grotesque / Hanken Grotesk / Space Mono) + metadata
  globals.css      design tokens + home/marketing styles
  dossier.css      scan flow + product dossier styles
  page.tsx         home — hero, manifesto, 9-system pipeline, trust, swaps, CTA
  scan/page.tsx    upload → scan → dossier
components/
  Nav, Footer, Reveal, VerdictSeal (signature), Dossier, icons
lib/
  api.ts           scanProduct() → POST /api/v1/scan
  types.ts         response shapes
  sample.ts        sample dossier
```
