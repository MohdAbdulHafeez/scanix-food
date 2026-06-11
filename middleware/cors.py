from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings


def setup_cors(app: FastAPI) -> None:
    """Enable CORS for the configured frontend origins.

    Uses the explicit ``CORS_ORIGINS`` list (defaults to the local
    Next.js dev server) because ``allow_credentials=True`` cannot be
    combined with a ``"*"`` wildcard — browsers reject credentialed
    requests against a wildcard origin.
    """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
