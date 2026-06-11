# Scanix AI

Point your camera at any packaged-food label and Scanix reads it the way a
food inspector, a lab, and a nutritionist would — then hands back one honest
verdict: **eat daily, eat occasionally, or avoid.**

It is built for the Indian packaged-food market: FSSAI compliance, adulteration
and counterfeit checks, metabolic impact, an organ-level "digital twin", and
healthier swaps you can actually buy.

---

## Repository layout

```
scanix-food/
├── main.py                  # FastAPI app entrypoint (mounts /api/v1)
├── requirements.txt         # Backend dependencies
│
├── api/                     # HTTP layer
│   ├── router.py            # Aggregates every System router
│   └── v1/
│       ├── scan.py          # System 1  — scan a label image
│       ├── swap.py          # System 7  — healthier swap recommendations
│       ├── trust.py         # System 8  — FSSAI / adulteration / authenticity
│       ├── complaint.py     # System 8  — generate an FSSAI complaint (PDF)
│       └── user.py          # System 9  — auth, dashboard, health profile
│
├── core/                    # Config, logging, security, exceptions
├── middleware/              # CORS, rate-limit, request logging, error handler
├── database/                # SQLAlchemy models + session
│
├── modules/                 # The intelligence "Systems"
│   ├── scan/                # System 1 — OCR + barcode + OpenFoodFacts fusion
│   ├── ingredients/         # System 2 — additives, E-numbers, risk profiles
│   ├── metabolism/          # System 3 — glycemic / insulin / metabolic verdict
│   ├── consumer/            # System 4 — deception, FSSAI compliance, alerts
│   ├── digital_twin/        # System 5 — organ impact + body simulation
│   ├── ai/                  # System 6 — food explainer (RAG) + nutritionist
│   ├── smart_food/          # System 7 — smart swaps
│   ├── trust/               # System 8 — trust + FSSAI complaint generator
│   └── user_intelligence/   # System 9 — accounts, health memory, analytics
│
└── frontend/                # Next.js customer-facing app (see frontend/README.md)
```

A single scan runs Systems 1→9 and returns one rich JSON document; the frontend
renders it as a readable **product dossier**.

---

## Running it

### 1. Backend (FastAPI)

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (use: source .venv/bin/activate on macOS/Linux)
pip install -r requirements.txt
cp .env.example .env            # then fill in the keys you have
uvicorn main:app --reload --port 8000
```

- API root: <http://localhost:8000>
- Interactive docs (Swagger): <http://localhost:8000/docs>

> The scan pipeline needs `easyocr` + `opencv` (CPU is fine, first run downloads
> OCR models). AI explainer / nutritionist features need a `GEMINI_API_KEY`;
> without one they degrade gracefully and the rest of the scan still works.

### 2. Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev                     # http://localhost:3000
```

The frontend proxies `/api/*` to the backend (`http://localhost:8000` by
default), so no CORS setup is required in development. Override with
`NEXT_PUBLIC_API_BASE` if your backend runs elsewhere. The scan page also ships
a **sample dossier** so you can explore the UI before the backend is live.

---

## The nine systems

| # | System | What it answers |
|---|--------|-----------------|
| 1 | Scan | What product is this? (OCR + barcode + OpenFoodFacts) |
| 2 | Ingredients | What's actually inside, and which additives matter? |
| 3 | Metabolism | What will this do to my blood sugar and energy? |
| 4 | Consumer | Is the marketing honest? Is it FSSAI-compliant? |
| 5 | Digital Twin | How does this hit my liver, heart, pancreas, kidneys? |
| 6 | AI | Explain it like a nutritionist would, with sources. |
| 7 | Smart Swap | What healthier product should I buy instead? |
| 8 | Trust | Is it authentic — or adulterated / counterfeit? |
| 9 | User | Remember my allergies, meds, and scan history. |
