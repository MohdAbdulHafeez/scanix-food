from typing import List

from fastapi import APIRouter
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile

from modules.scan.scan_engine import (
    FAVORITES,
    SCAN_HISTORY,
    master_scan_engine,
    memory_engine,
)


router = APIRouter(
    prefix="/scan",
    tags=["Scan"],
)


# ==========================================================
# HEALTH
# ==========================================================


@router.get(
    "/health",
)
async def scan_health():

    return {

        "success": True,

        "service": "scan",

        "status": "healthy",

    }


# ==========================================================
# SINGLE SCAN
# ==========================================================


@router.post(
    "",
)
async def scan_product(

    file: UploadFile = File(...),

):

    try:

        result = await (
            master_scan_engine
            .scan_product(
                file
            )
        )

        return result
    
    except Exception as e:

        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ==========================================================
# MULTI IMAGE SCAN
# ==========================================================


@router.post(
    "/multi",
)
async def scan_multiple_products(

    files: List[UploadFile] = File(...),

):

    try:

        result = await (

            master_scan_engine
            .multi_scan(
                files
            )

        )

        return result

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e),

        )


# ==========================================================
# MANUAL SEARCH
# ==========================================================


@router.post(
    "/manual",
)
async def manual_search(

    query: str,

):

    return {

        "success": True,

        "query": query,

        "mode": "manual",

    }


# ==========================================================
# HISTORY
# ==========================================================


@router.get(
    "/history",
)
async def get_history():

    return {

        "success": True,

        "count": len(
            SCAN_HISTORY
        ),

        "results":
        memory_engine.get_history(),

    }


@router.delete(
    "/history",
)
async def clear_history():

    memory_engine.clear_history()

    return {

        "success": True,

        "message":
        "History cleared",

    }


# ==========================================================
# FAVORITES
# ==========================================================


@router.get(
    "/favorites",
)
async def get_favorites():

    return {

        "success": True,

        "count": len(
            FAVORITES
        ),

        "results":
        memory_engine.get_favorites(),

    }


@router.post(
    "/favorites",
)
async def add_favorite(

    product: dict,

):

    status = (

        memory_engine
        .add_favorite(
            product
        )

    )

    return {

        "success": status,

        "message":

        "Added to favorites"

        if status

        else

        "Failed",

    }


# ==========================================================
# STATS
# ==========================================================


@router.get(
    "/stats",
)
async def scan_stats():

    return {

        "success": True,

        "total_scans":

        len(
            SCAN_HISTORY
        ),

        "favorites":

        len(
            FAVORITES
        ),

    }


