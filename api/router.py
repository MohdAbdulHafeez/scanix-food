from fastapi import APIRouter

from api.v1 import scan, trust, complaint, user, swap


from api.v1.scan import (
    router as scan_router,
)


api_router = APIRouter()

api_router.include_router(
    scan_router,
)


from fastapi import APIRouter

from api.v1.scan import router as scan_router
from api.v1.complaint import router as complaint_router


api_router = APIRouter()

api_router.include_router(
    scan_router,
)

api_router.include_router(
    complaint_router,
)


api_router = APIRouter()
api_router.include_router(scan.router)
api_router.include_router(trust.router)
api_router.include_router(complaint.router)
api_router.include_router(user.router)
api_router.include_router(swap.router)  # System 7