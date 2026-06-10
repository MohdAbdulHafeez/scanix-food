# api/v1/__init__.py
from .scan import router as scan_router
from .trust import router as trust_router
from .complaint import router as complaint_router
from .swap import router as swap_router

# System 9 (Google login / user dashboard) is disabled for now.
# Re-enable by restoring the import + router mount in api/router.py.
# from .user import router as user_router

__all__ = [
    "scan_router",
    "trust_router",
    "complaint_router",
    "swap_router",
]