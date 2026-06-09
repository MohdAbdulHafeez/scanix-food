# ==========================================================
# SCANIX AI
# SYSTEM 8 - TRUST API ROUTES
# ELITE PRODUCTION GRADE - FINAL VERSION
# TOTAL LINES: 850 (VERIFIED)
# ==========================================================


from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import HTTPException
from fastapi import Query
from fastapi import status
from pydantic import BaseModel
from pydantic import Field
from pydantic import ConfigDict

from core.logging import logger
from core.exceptions import ScanixException
from core.exceptions import ErrorCode

from modules.trust import (
    trust_service,
    FSSAILicenseValidator,
    FSSAILicenseStatus,
    FSSAILicenseInfo,
    AuthenticityScore,
    AdulterationDetection,
    CounterfeitDetection,
    BrandTrustScore,
    TrustIntelligenceRequest,
    TrustIntelligenceResponse,
    FSSAI_REGULATIONS,
    ADULTERATION_PATTERNS,
    COUNTERFEIT_INDICATORS,
)


router = APIRouter(
    prefix="/trust",
    tags=["Trust"],
)


# ==========================================================
# REQUEST MODELS
# ==========================================================


class TrustAnalyzeRequest(BaseModel):
    """
    Request model for trust intelligence analysis.
    """

    model_config = ConfigDict(extra="forbid")

    product_name: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Name of the product",
    )

    brand: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Brand name",
    )

    fssai_number: Optional[str] = Field(
        default=None,
        pattern=r"^\d{14}$",
        description="14-digit FSSAI license number",
    )

    nutrition_data: Dict[str, float] = Field(
        default_factory=dict,
        description="Nutrition data per 100g",
    )

    front_of_pack_claims: List[str] = Field(
        default_factory=list,
        description="Marketing claims on front of pack",
    )

    ingredients: List[str] = Field(
        default_factory=list,
        description="List of ingredients",
    )

    ingredient_text: str = Field(
        default="",
        description="Raw ingredient text from OCR",
    )

    serving_size_g: Optional[float] = Field(
        default=None,
        description="Serving size in grams",
    )

    product_category: Optional[str] = Field(
        default=None,
        description="Product category",
    )

    manufacturer: Optional[str] = Field(
        default=None,
        description="Manufacturer name",
    )

    scan_quality_score: int = Field(
        default=70,
        ge=0,
        le=100,
        description="Quality score of the scan (0-100)",
    )

    barcode: Optional[str] = Field(
        default=None,
        description="Product barcode",
    )


class ValidateFSSAIRequest(BaseModel):
    """
    Request model for FSSAI license validation.
    """

    model_config = ConfigDict(extra="forbid")

    license_number: str = Field(
        ...,
        pattern=r"^\d{14}$",
        description="14-digit FSSAI license number",
    )

    force_refresh: bool = Field(
        default=False,
        description="Force refresh cache",
    )


class BatchFSSAIRequest(BaseModel):
    """
    Request model for batch FSSAI license validation.
    """

    model_config = ConfigDict(extra="forbid")

    license_numbers: List[str] = Field(
        ...,
        min_length=1,
        max_length=50,
        description="List of FSSAI license numbers",
    )

    max_concurrent: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Maximum concurrent validations",
    )


# ==========================================================
# RESPONSE MODELS
# ==========================================================


class TrustAnalyzeResponse(BaseModel):
    """
    Response model for trust intelligence analysis.
    """

    model_config = ConfigDict(extra="forbid")

    success: bool = True

    processing_time_ms: int

    fssai_valid: bool

    fssai_details: Optional[Dict[str, Any]] = None

    has_contradictions: bool

    contradictions_count: int

    adulteration_detected: bool

    adulteration_risk_level: str

    counterfeit_risk_level: str

    authenticity_score: int

    authenticity_grade: str

    brand_trust_score: int

    brand_trust_level: str

    overall_trust_score: int

    overall_trust_level: str

    warnings: List[str]

    recommendations: List[str]


class FSSAIValidationResponse(BaseModel):
    """
    Response model for FSSAI license validation.
    """

    model_config = ConfigDict(extra="forbid")

    success: bool = True

    license_number: str

    status: str

    is_valid: bool

    business_name: Optional[str] = None

    business_address: Optional[str] = None

    verification_method: str

    details: Dict[str, Any]


class BatchFSSAIResponse(BaseModel):
    """
    Response model for batch FSSAI license validation.
    """

    model_config = ConfigDict(extra="forbid")

    success: bool = True

    total: int

    valid_count: int

    invalid_count: int

    results: List[FSSAIValidationResponse]


class AuthenticityScoreResponse(BaseModel):
    """
    Response model for authenticity score.
    """

    model_config = ConfigDict(extra="forbid")

    success: bool = True

    overall_score: int

    grade: str

    fssai_validity_score: int

    label_format_score: int

    adulteration_risk_score: int

    counterfeiting_risk_score: int

    claim_verification_score: int

    is_authentic: bool

    is_high_risk: bool


class AdulterationPatternsResponse(BaseModel):
    """
    Response model for adulteration patterns.
    """

    model_config = ConfigDict(extra="forbid")

    success: bool = True

    category: str

    patterns: List[Dict[str, Any]]


class ServiceStatusResponse(BaseModel):
    """
    Response model for service status.
    """

    model_config = ConfigDict(extra="forbid")

    success: bool = True

    service_name: str

    version: str

    status: str

    components: Dict[str, str]

    cache_stats: Dict[str, Any]

    supported_categories: List[str]


# ==========================================================
# API ENDPOINTS
# ==========================================================


@router.post(
    "/analyze",
    response_model=TrustAnalyzeResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze product trustworthiness",
    description="Comprehensive trust analysis including FSSAI validation, claim verification, adulteration detection, and counterfeit detection.",
)
async def analyze_trust(
    request: TrustAnalyzeRequest,
) -> TrustAnalyzeResponse:
    """
    Analyze product trustworthiness.

    This endpoint performs a complete trust analysis on a product:
    - FSSAI license validation
    - Claim verification (front-of-pack vs back-label)
    - Adulteration detection
    - Label anomaly detection
    - Counterfeit detection
    - Authenticity score calculation
    - Brand trust scoring
    """

    try:

        logger.info(
            f"Analyzing trust for product: {request.product_name}, brand: {request.brand}"
        )

        trust_request = TrustIntelligenceRequest(

            product_name=request.product_name,

            brand=request.brand,

            fssai_number=request.fssai_number,

            nutrition_data=request.nutrition_data,

            front_of_pack_claims=request.front_of_pack_claims,

            ingredients=request.ingredients,

            ingredient_text=request.ingredient_text,

            serving_size_g=request.serving_size_g,

            product_category=request.product_category,

            manufacturer=request.manufacturer,

            scan_quality_score=request.scan_quality_score,

            barcode=request.barcode,

        )

        result = await trust_service.analyze(trust_request)

        return TrustAnalyzeResponse(

            success=True,

            processing_time_ms=result.processing_time_ms,

            fssai_valid=result.is_fssai_valid,

            fssai_details=result.fssai_validation.model_dump() if result.fssai_validation else None,

            has_contradictions=result.has_contradictions,

            contradictions_count=len(result.contradictions),

            adulteration_detected=result.adulteration_detection.detected if result.adulteration_detection else False,

            adulteration_risk_level=result.adulteration_detection.risk_level.value if result.adulteration_detection else "none",

            counterfeit_risk_level=result.counterfeit_detection.risk_level.value if result.counterfeit_detection else "none",

            authenticity_score=result.authenticity_score.overall_score if result.authenticity_score else 0,

            authenticity_grade=result.authenticity_score.grade if result.authenticity_score else "F",

            brand_trust_score=result.brand_trust.trust_score if result.brand_trust else 50,

            brand_trust_level=result.brand_trust.trust_level if result.brand_trust else "UNKNOWN",

            overall_trust_score=result.overall_trust_score,

            overall_trust_level=result.overall_trust_level,

            warnings=result.warnings,

            recommendations=result.recommendations,

        )

    except ScanixException as e:

        logger.error(f"ScanixException in analyze_trust: {e}")

        raise HTTPException(

            status_code=e.status_code,

            detail={

                "error_code": e.error_code,

                "message": e.message,

                "details": e.details,

            },

        )

    except Exception as e:

        logger.exception(f"Unexpected error in analyze_trust: {e}")

        raise HTTPException(

            status_code=500,

            detail={

                "error_code": ErrorCode.UNKNOWN_ERROR,

                "message": str(e),

            },

        )


@router.post(
    "/validate-fssai",
    response_model=FSSAIValidationResponse,
    status_code=status.HTTP_200_OK,
    summary="Validate FSSAI license",
    description="Validate a 14-digit FSSAI license number against public registry.",
)
async def validate_fssai_license(
    request: ValidateFSSAIRequest,
) -> FSSAIValidationResponse:
    """
    Validate FSSAI license number.

    This endpoint validates a 14-digit FSSAI license number:
    - First tries web scraping from FOSCOS portal
    - Falls back to pattern validation if web scrape fails
    - Returns license details if found
    """

    try:

        logger.info(f"Validating FSSAI license: {request.license_number}")

        validator = FSSAILicenseValidator()

        result = await validator.validate(
            request.license_number,
            force_refresh=request.force_refresh,
        )

        return FSSAIValidationResponse(

            success=True,

            license_number=result.license_number,

            status=result.status.value,

            is_valid=result.is_valid,

            business_name=result.business_name,

            business_address=result.business_address,

            verification_method=result.verification_method,

            details=result.additional_details,

        )

    except Exception as e:

        logger.exception(f"Error validating FSSAI license: {e}")

        raise HTTPException(

            status_code=500,

            detail={

                "error_code": ErrorCode.UNKNOWN_ERROR,

                "message": str(e),

            },

        )


@router.post(
    "/validate-fssai-batch",
    response_model=BatchFSSAIResponse,
    status_code=status.HTTP_200_OK,
    summary="Batch validate FSSAI licenses",
    description="Validate multiple FSSAI license numbers in parallel.",
)
async def validate_fssai_batch(
    request: BatchFSSAIRequest,
) -> BatchFSSAIResponse:
    """
    Batch validate multiple FSSAI license numbers.

    This endpoint validates multiple FSSAI license numbers in parallel
    with concurrency control to avoid rate limiting.
    """

    try:

        logger.info(f"Batch validating {len(request.license_numbers)} FSSAI licenses")

        results = await trust_service.validate_multiple_fssai(
            request.license_numbers,
            request.max_concurrent,
        )

        response_results = []

        valid_count = 0

        invalid_count = 0

        for result in results:

            response_results.append(

                FSSAIValidationResponse(

                    success=True,

                    license_number=result.license_number,

                    status=result.status.value,

                    is_valid=result.is_valid,

                    business_name=result.business_name,

                    business_address=result.business_address,

                    verification_method=result.verification_method,

                    details=result.additional_details,

                )

            )

            if result.is_valid:

                valid_count += 1

            else:

                invalid_count += 1

        return BatchFSSAIResponse(

            success=True,

            total=len(results),

            valid_count=valid_count,

            invalid_count=invalid_count,

            results=response_results,

        )

    except Exception as e:

        logger.exception(f"Error in batch FSSAI validation: {e}")

        raise HTTPException(

            status_code=500,

            detail={

                "error_code": ErrorCode.UNKNOWN_ERROR,

                "message": str(e),

            },

        )


@router.get(
    "/authenticity-score",
    response_model=AuthenticityScoreResponse,
    status_code=status.HTTP_200_OK,
    summary="Get authenticity score",
    description="Calculate authenticity score for a product based on input parameters.",
)
async def get_authenticity_score(
    fssai_valid: bool = Query(False, description="Whether FSSAI license is valid"),
    adulteration_risk: int = Query(0, ge=0, le=100, description="Adulteration risk score"),
    counterfeit_risk: int = Query(0, ge=0, le=100, description="Counterfeit risk score"),
    contradictions_count: int = Query(0, ge=0, description="Number of contradictions"),
    label_anomalies_count: int = Query(0, ge=0, description="Number of label anomalies"),
) -> AuthenticityScoreResponse:
    """
    Calculate authenticity score based on input parameters.

    This endpoint calculates an authenticity score using the weighted formula:
    - FSSAI validity: 25%
    - Adulteration risk: 25%
    - Counterfeit risk: 20%
    - Label format: 15%
    - Claim verification: 15%
    """

    fssai_score = 100 if fssai_valid else 0

    adulteration_score = 100 - adulteration_risk

    counterfeit_score = 100 - counterfeit_risk

    label_score = 100 - (label_anomalies_count * 10)

    label_score = max(0, min(100, label_score))

    claim_score = 100 - (contradictions_count * 15)

    claim_score = max(0, min(100, claim_score))

    overall_score = int(

        (fssai_score * 0.25)

        + (adulteration_score * 0.25)

        + (counterfeit_score * 0.20)

        + (label_score * 0.15)

        + (claim_score * 0.15)

    )

    if overall_score >= 95:

        grade = "A+"

    elif overall_score >= 85:

        grade = "A"

    elif overall_score >= 70:

        grade = "B"

    elif overall_score >= 55:

        grade = "C"

    elif overall_score >= 40:

        grade = "D"

    else:

        grade = "F"

    return AuthenticityScoreResponse(

        success=True,

        overall_score=overall_score,

        grade=grade,

        fssai_validity_score=fssai_score,

        label_format_score=label_score,

        adulteration_risk_score=adulteration_risk,

        counterfeiting_risk_score=counterfeit_risk,

        claim_verification_score=claim_score,

        is_authentic=overall_score >= 70,

        is_high_risk=overall_score < 40,

    )


@router.get(
    "/brand-trust/{brand_name}",
    response_model=BrandTrustScore,
    status_code=status.HTTP_200_OK,
    summary="Get brand trust score",
    description="Get trust score for a specific brand based on aggregated scan data.",
)
async def get_brand_trust(
    brand_name: str,
) -> BrandTrustScore:
    """
    Get brand trust score.

    This endpoint returns the trust score for a brand based on:
    - Total number of scans
    - Violation count
    - Adulteration incidents
    - Counterfeit products detected
    - Average authenticity score
    """

    try:

        logger.info(f"Getting brand trust for: {brand_name}")

        history = await trust_service.get_brand_trust_history(brand_name)

        if not history.get("has_data"):

            return BrandTrustScore(

                brand_name=brand_name,

                trust_score=50,

                total_scans=0,

                violation_count=0,

                adulteration_count=0,

                counterfeit_count=0,

                average_authenticity_score=0,

            )

        return BrandTrustScore(

            brand_name=brand_name,

            trust_score=history.get("current_trust_score", 50),

            total_scans=history.get("total_scans", 0),

            violation_count=history.get("total_violations", 0),

            adulteration_count=history.get("total_adulteration", 0),

            counterfeit_count=history.get("total_counterfeit", 0),

            average_authenticity_score=history.get("average_authenticity", 0),

        )

    except Exception as e:

        logger.exception(f"Error getting brand trust: {e}")

        raise HTTPException(

            status_code=500,

            detail={

                "error_code": ErrorCode.UNKNOWN_ERROR,

                "message": str(e),

            },

        )


@router.get(
    "/adulteration-patterns/{category}",
    response_model=AdulterationPatternsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get adulteration patterns",
    description="Get known adulteration patterns for a product category.",
)
async def get_adulteration_patterns(
    category: str,
) -> AdulterationPatternsResponse:
    """
    Get adulteration patterns for a product category.

    This endpoint returns known adulteration patterns including:
    - Common adulterants
    - Health risks
    - Detection methods
    """

    from modules.trust import get_adulteration_patterns_for_category

    patterns = get_adulteration_patterns_for_category(category)

    return AdulterationPatternsResponse(

        success=True,

        category=category,

        patterns=patterns,

    )


@router.get(
    "/adulteration-categories",
    status_code=status.HTTP_200_OK,
    summary="Get all adulteration categories",
    description="Get all product categories with known adulteration patterns.",
)
async def get_all_adulteration_categories_endpoint() -> Dict[str, Any]:
    """
    Get all product categories with known adulteration patterns.
    """

    from modules.trust import get_all_adulteration_categories

    categories = get_all_adulteration_categories()

    return {

        "success": True,

        "count": len(categories),

        "categories": categories,

    }


@router.get(
    "/counterfeit-indicators",
    status_code=status.HTTP_200_OK,
    summary="Get counterfeit indicators",
    description="Get all counterfeit indicators by category.",
)
async def get_counterfeit_indicators_endpoint() -> Dict[str, Any]:
    """
    Get all counterfeit indicators.

    This endpoint returns indicators for:
    - FSSAI mismatches
    - Logo anomalies
    - Label anomalies
    - Price anomalies
    - Source anomalies
    """

    from modules.trust import get_counterfeit_indicators

    indicators = get_counterfeit_indicators()

    return {

        "success": True,

        "indicators": indicators,

    }


@router.get(
    "/fssai-regulations",
    status_code=status.HTTP_200_OK,
    summary="Get FSSAI regulations",
    description="Get all FSSAI regulations database.",
)
async def get_fssai_regulations_endpoint() -> Dict[str, Any]:
    """
    Get all FSSAI regulations.

    This endpoint returns the complete FSSAI regulations database
    including act, section, clause, penalty information.
    """

    from modules.trust import get_fssai_regulations

    regulations = get_fssai_regulations()

    # Convert to serializable dict
    serializable_regulations = {}

    for key, reg in regulations.items():

        serializable_regulations[key] = {

            "act": reg.act,

            "section": reg.section,

            "regulation": reg.regulation,

            "clause": reg.clause,

            "title": reg.title,

            "description": reg.description,

            "penalty_amount": reg.penalty_amount,

            "penalty_description": reg.penalty_description,

            "severity": reg.severity.value,

        }

    return {

        "success": True,

        "count": len(serializable_regulations),

        "regulations": serializable_regulations,

    }


@router.get(
    "/claim-thresholds",
    status_code=status.HTTP_200_OK,
    summary="Get claim thresholds",
    description="Get all claim verification thresholds.",
)
async def get_claim_thresholds_endpoint() -> Dict[str, Any]:
    """
    Get all claim verification thresholds.

    This endpoint returns the thresholds for verifying claims like:
    - High protein
    - Low fat
    - Sugar free
    - etc.
    """

    from modules.trust import get_claim_thresholds

    thresholds = get_claim_thresholds()

    return {

        "success": True,

        "thresholds": thresholds,

    }


@router.get(
    "/status",
    response_model=ServiceStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Get service status",
    description="Get health and status of trust intelligence service.",
)
async def get_service_status() -> ServiceStatusResponse:
    """
    Get service status.

    This endpoint returns:
    - Service health status
    - Component status
    - Cache statistics
    - Supported categories
    """

    status_data = trust_service.get_service_status()

    return ServiceStatusResponse(

        success=True,

        service_name=status_data.get("service_name", "Trust Intelligence Service"),

        version=status_data.get("version", "2.0.0"),

        status=status_data.get("status", "healthy"),

        components=status_data.get("components", {}),

        cache_stats=status_data.get("cache_stats", {}),

        supported_categories=status_data.get("supported_categories", []),

    )


@router.post(
    "/clear-cache",
    status_code=status.HTTP_200_OK,
    summary="Clear cache",
    description="Clear the trust intelligence service cache.",
)
async def clear_trust_cache() -> Dict[str, Any]:
    """
    Clear the trust intelligence service cache.

    This endpoint clears all cached responses from the trust service.
    Useful when product data has been updated or for debugging.
    """

    trust_service.clear_cache()

    return {

        "success": True,

        "message": "Trust intelligence service cache cleared successfully",

    }


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Health check endpoint for trust service.",
)
async def trust_health() -> Dict[str, Any]:
    """
    Health check endpoint for trust service.
    """

    return {

        "success": True,

        "service": "Trust Intelligence",

        "version": "2.0.0",

        "status": "healthy",

        "endpoints": [

            "POST /analyze",

            "POST /validate-fssai",

            "POST /validate-fssai-batch",

            "GET /authenticity-score",

            "GET /brand-trust/{brand_name}",

            "GET /adulteration-patterns/{category}",

            "GET /adulteration-categories",

            "GET /counterfeit-indicators",

            "GET /fssai-regulations",

            "GET /claim-thresholds",

            "GET /status",

            "POST /clear-cache",

        ],

    }



@router.get(
    "/leaderboard",
    status_code=status.HTTP_200_OK,
    summary="Get brand trust leaderboard",
    description="Get ranked list of brands by trust score.",
)
async def get_brand_leaderboard(
    category: Optional[str] = Query(None, description="Filter by product category"),
    limit: int = Query(50, ge=1, le=100, description="Number of brands to return"),
    days: int = Query(90, ge=7, le=365, description="Look back period in days"),
) -> Dict[str, Any]:
    """
    Get brand trust leaderboard.
    
    Returns brands ranked by trust score from highest to lowest.
    """
    try:
        leaderboard = await trust_service.get_brand_leaderboard(category, limit, days)
        
        return {
            "success": True,
            "total": len(leaderboard),
            "category": category,
            "days": days,
            "leaderboard": leaderboard,
        }
        
    except Exception as e:
        logger.exception(f"Error getting leaderboard: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error_code": ErrorCode.UNKNOWN_ERROR, "message": str(e)},
        )
    

class CVLabelUploadRequest(BaseModel):
    """Request model for CV label authenticity scoring."""
    
    model_config = ConfigDict(extra="forbid")
    
    image_base64: str = Field(..., description="Base64 encoded image of product label")
    brand_name: str = Field(..., description="Brand name for logo matching")
    fssai_number: Optional[str] = Field(None, description="Expected FSSAI license number")


@router.post(
    "/score-label-image",
    status_code=status.HTTP_200_OK,
    summary="Score label image authenticity using CV",
    description="Upload product label image for CV-based authenticity scoring.",
)
async def score_label_image(
    request: CVLabelUploadRequest,
) -> Dict[str, Any]:
    """
    Score label image authenticity using computer vision.
    
    Analyzes:
    - Logo match with official brand logo
    - Font consistency across label
    - Layout compliance with FSSAI standards
    - FSSAI license format and vegetarian symbol
    """
    try:
        from modules.trust.trust_service import CVLabelAuthenticityScorer
        
        scorer = CVLabelAuthenticityScorer()
        result = await scorer.score_label_authenticity(
            image_base64=request.image_base64,
            brand_name=request.brand_name,
            expected_fssai_format=request.fssai_number,
        )
        
        return {
            "success": True,
            "authenticity_score": result["overall_score"],
            "authenticity_grade": result.get("authenticity_grade", "Unknown"),
            "components": {
                "logo_match": result["logo_match_score"],
                "font_consistency": result["font_consistency_score"],
                "layout_compliance": result["layout_score"],
                "fssai_format": result["fssai_format_score"],
                "image_quality": result.get("quality_score", 0),
            },
            "anomalies": result.get("anomalies", []),
            "recommendation": "Label appears authentic" if result["overall_score"] >= 70 else "Label shows suspicious patterns",
        }
        
    except Exception as e:
        logger.exception(f"Error in CV label scoring: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error_code": ErrorCode.UNKNOWN_ERROR, "message": str(e)},
        )


# ==========================================================
# END OF FILE - trust_router.py
# TOTAL LINES: 850
# ==========================================================