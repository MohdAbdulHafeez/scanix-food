# api/v1/swap.py
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import Response
from pydantic import BaseModel

from modules.smart_food import (
    smart_swap_service,
    SwapRequest,
    SmartSwapResponse,
    SortByOption,
    export_swaps_to_csv,
    export_swaps_to_markdown,
    export_swaps_to_html,
    export_swaps_to_json,
    export_swaps_to_excel,
)

router = APIRouter(prefix="/swap", tags=["Smart Swap"])


class SwapRecommendationRequest(BaseModel):
    product_name: str
    brand: Optional[str] = None
    barcode: Optional[str] = None
    category: Optional[str] = None
    nutrition: Optional[dict] = None
    nova_group: int = 4
    processing_level: str = "ULTRA_PROCESSED"
    deception_score: int = 50
    metabolic_risk_score: int = 50
    organ_impact_score: int = 50
    additives_list: List[str] = []
    max_results: int = 6
    sort_by: str = "health_score"
    health_condition: Optional[str] = None


@router.post("/recommendations", response_model=SmartSwapResponse)
async def get_swap_recommendations(request: SwapRecommendationRequest):
    """Get healthier swap recommendations for a product."""
    try:
        swap_request = SwapRequest(
            product_name=request.product_name,
            brand=request.brand,
            barcode=request.barcode,
            category=request.category,
            nutrition=request.nutrition or {},
            nova_group=request.nova_group,
            processing_level=request.processing_level,
            deception_score=request.deception_score,
            metabolic_risk_score=request.metabolic_risk_score,
            organ_impact_score=request.organ_impact_score,
            additives_list=request.additives_list,
            max_results=request.max_results,
            sort_by=SortByOption(request.sort_by),
        )
        return await smart_swap_service.get_swaps(swap_request, health_condition=request.health_condition)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-barcode/{barcode}", response_model=SmartSwapResponse)
async def get_swap_by_barcode(
    barcode: str,
    max_results: int = 6,
    health_condition: Optional[str] = None,
):
    """Get swap recommendations by scanning a barcode."""
    try:
        return await smart_swap_service.get_swap_by_barcode(barcode, health_condition=health_condition)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export/csv")
async def export_csv(response: SmartSwapResponse):
    """Export swap recommendations as CSV."""
    return Response(
        content=export_swaps_to_csv(response),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=swaps.csv"}
    )


@router.get("/health")
async def swap_health():
    return {"success": True, "service": "Smart Swap", "status": "healthy"}