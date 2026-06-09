from dotenv import load_dotenv

load_dotenv()


from fastapi import APIRouter, FastAPI

from api.router import api_router

from middleware.cors import (
    setup_cors,
)

from middleware.exception_handler import (
    setup_exception_handlers,
)

from middleware.request_logger import (
    RequestLoggerMiddleware,
)


from core.config import settings


app = FastAPI(

    title=settings.APP_NAME,

    version=settings.VERSION,

)


# ==========================================================
# MIDDLEWARE
# ==========================================================

setup_cors(app)

setup_exception_handlers(app)

app.add_middleware(
    RequestLoggerMiddleware
)


# ==========================================================
# API ROUTES
# ==========================================================

app.include_router(
    api_router,
    prefix="/api/v1",
)

# ==========================================================
# ROOT
# ==========================================================

@app.get("/")
async def root():

    return {

        "message": "Welcome to Scanix AI",

        "version": settings.VERSION,

        "status": "running",

    }