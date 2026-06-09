# ==========================================================
# SCANIX AI
# SYSTEM 9 – USER INTELLIGENCE API ROUTES
# ELITE PRODUCTION GRADE – FINAL VERSION
# TOTAL LINES: 550
# ==========================================================


from __future__ import annotations


from typing import Optional
from typing import Dict
from typing import Any


from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from fastapi import Depends
from fastapi import Query
from fastapi.responses import RedirectResponse


from core.logging import logger
from core.exceptions import ScanixException
from core.exceptions import ErrorCode


from modules.user_intelligence.service import (
    user_intelligence_service,
)

from modules.user_intelligence.auth import (
    gmail_auth,
    get_current_user,
)

from modules.user_intelligence.models import (
    HealthProfileUpdate,
    AllergyCheckRequest,
    AllergyCheckResponse,
    MedicationCheckRequest,
    MedicationCheckResponse,
    DashboardResponse,
    AnalyticsResponse,
    HealthMemoryResponse,
    UserScan,
)


router = APIRouter(
    prefix="/user",
    tags=["User Intelligence"],
)


# ==========================================================
# AUTHENTICATION ENDPOINTS
# ==========================================================


@router.get(
    "/auth/login",
    summary="Google OAuth Login",
    description="Redirect to Google login page",
)
async def login() -> RedirectResponse:
    """
    Initiate Google OAuth login flow.

    Returns:
        RedirectResponse to Google login page
    """

    login_url = gmail_auth.get_login_url()

    return RedirectResponse(
        url=login_url
    )


@router.get(
    "/auth/callback",
    summary="OAuth Callback",
    description="Handle Google OAuth callback",
)
async def auth_callback(
    code: str,
) -> RedirectResponse:
    """
    Handle Google OAuth callback and create session.

    Args:
        code: Authorization code from Google

    Returns:
        RedirectResponse to frontend dashboard
    """

    try:

        # Exchange code for tokens
        tokens = await gmail_auth.exchange_code(
            code
        )

        access_token = tokens.get(
            "access_token"
        )

        # Get user info
        user_info = await gmail_auth.get_user_info(
            access_token
        )

        email = user_info.get("email")

        name = user_info.get("name")

        picture = user_info.get("picture")

        gmail_id = user_info.get("id")

        if not email:

            raise HTTPException(
                status_code=400,
                detail="Email not found",
            )

        # Create or get user
        user = await user_intelligence_service.create_or_get_user(
            email,
            name,
            picture,
            gmail_id,
        )

        # Create session token
        session_token = gmail_auth.create_session_token(
            user.id,
            user.email,
        )

        # Redirect to frontend with cookie
        response = RedirectResponse(
            url="http://localhost:3000/dashboard",
        )

        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            max_age=604800,  # 7 days
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
        )

        return response

    except Exception as e:

        logger.error(
            f"Auth callback failed: {e}"
        )

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/auth/logout",
    summary="Logout",
    description="Clear session and logout",
)
async def logout() -> RedirectResponse:
    """
    Logout user by clearing session cookie.

    Returns:
        RedirectResponse to frontend home
    """

    return gmail_auth.create_logout_response(
        "http://localhost:3000"
    )


@router.get(
    "/auth/me",
    summary="Get Current User",
    description="Get authenticated user information",
)
async def get_me(
    user_id: str = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Get current authenticated user.

    Args:
        user_id: User ID from session token

    Returns:
        User information
    """

    if not user_id:

        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )

    user = await user_intelligence_service.get_user(
        user_id
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return {
        "success": True,
        "user": user.dict(),
    }


# ==========================================================
# DASHBOARD ENDPOINTS
# ==========================================================


@router.get(
    "/dashboard",
    response_model=DashboardResponse,
    summary="Get Dashboard",
    description="Get personalized dashboard with health insights",
)
async def get_dashboard(
    user_id: str = Depends(get_current_user),
) -> DashboardResponse:
    """
    Get personalized dashboard for authenticated user.

    Args:
        user_id: User ID from session token

    Returns:
        Complete dashboard with stats and recommendations
    """

    if not user_id:

        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )

    return await user_intelligence_service.get_dashboard(
        user_id
    )


@router.get(
    "/analytics",
    response_model=AnalyticsResponse,
    summary="Get Analytics",
    description="Get detailed health analytics and trends",
)
async def get_analytics(
    user_id: str = Depends(get_current_user),
) -> AnalyticsResponse:
    """
    Get detailed analytics for authenticated user.

    Args:
        user_id: User ID from session token

    Returns:
        Analytics with trends and insights
    """

    if not user_id:

        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )

    return await user_intelligence_service.get_analytics(
        user_id
    )


@router.get(
    "/health-memory",
    response_model=HealthMemoryResponse,
    summary="Get Health Memory",
    description="Get long-term health memory and insights",
)
async def get_health_memory(
    user_id: str = Depends(get_current_user),
) -> HealthMemoryResponse:
    """
    Get long-term health memory for authenticated user.

    Args:
        user_id: User ID from session token

    Returns:
        Health memory with longitudinal insights
    """

    if not user_id:

        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )

    return await user_intelligence_service.get_health_memory(
        user_id
    )


# ==========================================================
# HEALTH PROFILE ENDPOINTS
# ==========================================================


@router.get(
    "/profile",
    summary="Get Health Profile",
    description="Get user's health profile",
)
async def get_profile(
    user_id: str = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Get user's health profile.

    Args:
        user_id: User ID from session token

    Returns:
        Health profile data
    """

    if not user_id:

        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )

    profile = await user_intelligence_service.get_health_profile(
        user_id
    )

    return {
        "success": True,
        "profile": profile.dict() if profile else None,
    }


@router.put(
    "/profile",
    summary="Update Health Profile",
    description="Create or update user's health profile",
)
async def update_profile(
    update: HealthProfileUpdate,
    user_id: str = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Update user's health profile.

    Args:
        update: Health profile update data
        user_id: User ID from session token

    Returns:
        Updated health profile
    """

    if not user_id:

        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )

    profile = await user_intelligence_service.update_health_profile(
        user_id,
        update,
    )

    return {
        "success": True,
        "profile": profile.dict(),
    }


# ==========================================================
# SCAN HISTORY ENDPOINTS
# ==========================================================


@router.get(
    "/scans",
    summary="Get Scan History",
    description="Get user's scan history",
)
async def get_scans(
    limit: int = Query(
        20,
        ge=1,
        le=100,
        description="Number of scans to return",
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Number of scans to skip",
    ),
    user_id: str = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Get user's scan history.

    Args:
        limit: Maximum number of scans
        offset: Pagination offset
        user_id: User ID from session token

    Returns:
        List of scans
    """

    if not user_id:

        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )

    scans = await user_intelligence_service.get_scan_history(
        user_id,
        limit,
        offset,
    )

    total = await user_intelligence_service.get_total_scan_count(
        user_id
    )

    return {
        "success": True,
        "total": total,
        "returned": len(scans),
        "scans": [s.dict() for s in scans],
    }


# ==========================================================
# ALLERGY CHECK ENDPOINT
# ==========================================================


@router.post(
    "/check-allergies",
    response_model=AllergyCheckResponse,
    summary="Check Allergies",
    description="Check if product contains user's allergens",
)
async def check_allergies(
    request: AllergyCheckRequest,
    user_id: str = Depends(get_current_user),
) -> AllergyCheckResponse:
    """
    Check if product contains user's allergens.

    Args:
        request: Product data for allergy check
        user_id: User ID from session token

    Returns:
        Allergy detection results
    """

    if not user_id:

        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )

    return await user_intelligence_service.check_allergies(
        user_id,
        request,
    )


# ==========================================================
# MEDICATION CHECK ENDPOINT
# ==========================================================


@router.post(
    "/check-medications",
    response_model=MedicationCheckResponse,
    summary="Check Medications",
    description="Check for drug-food interactions",
)
async def check_medications(
    request: MedicationCheckRequest,
    user_id: str = Depends(get_current_user),
) -> MedicationCheckResponse:
    """
    Check for drug-food interactions.

    Args:
        request: Product data for medication check
        user_id: User ID from session token

    Returns:
        Interaction detection results
    """

    if not user_id:

        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )

    return await user_intelligence_service.check_medications(
        user_id,
        request,
    )


# ==========================================================
# INTEGRATION ENDPOINT (Called by System 1)
# ==========================================================


@router.post(
    "/save-scan",
    summary="Save Scan",
    description="Save scan result to user's history",
)
async def save_scan(
    scan_result: Dict[str, Any],
    user_id: str = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Save scan result to user's history.

    This endpoint is called by System 1 after a successful scan.

    Args:
        scan_result: Complete scan result from System 1
        user_id: User ID from session token

    Returns:
        Success status
    """

    if not user_id:

        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )

    success = await user_intelligence_service.save_scan(
        user_id,
        scan_result,
    )

    if success:

        return {
            "success": True,
            "message": "Scan saved to your history",
        }

    else:

        raise HTTPException(
            status_code=500,
            detail="Failed to save scan",
        )


# ==========================================================
# HEALTH CHECK
# ==========================================================


@router.get(
    "/health",
    summary="Health Check",
    description="Check if service is healthy",
)
async def user_health() -> Dict[str, Any]:
    """
    Health check endpoint for User Intelligence service.

    Returns:
        Service status
    """

    return {

        "success": True,

        "service": "User Intelligence Platform",

        "version": "1.0.0",

        "status": "healthy",

        "endpoints": [
            "GET /auth/login",
            "GET /auth/callback",
            "GET /auth/logout",
            "GET /auth/me",
            "GET /dashboard",
            "GET /analytics",
            "GET /health-memory",
            "GET /profile",
            "PUT /profile",
            "GET /scans",
            "POST /check-allergies",
            "POST /check-medications",
            "POST /save-scan",
        ],
    }


# ==========================================================
# END OF FILE – user.py
# ==========================================================