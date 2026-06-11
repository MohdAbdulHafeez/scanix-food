"""Central API router for Scanix AI (v1).

Aggregates every System router under a single ``api_router`` that
``main.py`` mounts at ``/api/v1``.
"""

from fastapi import APIRouter

from api.v1 import scan, trust, complaint, swap

api_router = APIRouter()

# System 1 — Scan intelligence (OCR + barcode + OpenFoodFacts fusion)
api_router.include_router(scan.router)

# System 8 — Trust intelligence (FSSAI, adulteration, counterfeit, authenticity)
api_router.include_router(trust.router)

# System 8 — FSSAI complaint generation
api_router.include_router(complaint.router)

# System 7 — Smart swap recommendations
api_router.include_router(swap.router)

# System 9 — User intelligence (Google login / dashboard) is disabled for now.
# To re-enable: add `user` to the import above and mount it here:
#   from api.v1 import user
#   api_router.include_router(user.router)
