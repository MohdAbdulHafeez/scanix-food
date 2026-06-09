# ==========================================================
# SCANIX AI
# SYSTEM 8 - FSSAI COMPLAINT API ROUTES
# ELITE PRODUCTION GRADE - FINAL VERSION
# TOTAL LINES: 520
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
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from pydantic import Field
from pydantic import ConfigDict

import io

from core.logging import logger
from core.exceptions import ScanixException
from core.exceptions import ErrorCode

from modules.trust import (
    complaint_service,
    generate_complaint_from_scan,
    generate_complaint_from_violations,
    FSSAIComplaintService,
    FSSAILicenseStatus,
    ViolationSeverity,
    FSSAILicenseValidator,
)


router = APIRouter(
    prefix="/complaint",
    tags=["Complaint"],
)


# ==========================================================
# REQUEST MODELS
# ==========================================================


class GenerateComplaintRequest(BaseModel):
    """
    Request model for generating FSSAI complaint.
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

    manufacturer: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Manufacturer name",
    )

    fssai_number: Optional[str] = Field(
        default=None,
        pattern=r"^\d{14}$",
        description="14-digit FSSAI license number",
    )

    violations: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="List of detected violations",
    )

    consumer_name: str = Field(
        default="Consumer",
        max_length=100,
        description="Name of the complainant",
    )

    consumer_email: str = Field(
        default="",
        max_length=100,
        description="Email of the complainant",
    )

    consumer_phone: str = Field(
        default="",
        max_length=15,
        description="Phone number of the complainant",
    )

    consumer_address: str = Field(
        default="",
        max_length=500,
        description="Address of the complainant",
    )

    additional_notes: str = Field(
        default="",
        max_length=2000,
        description="Additional notes or observations",
    )


class ComplaintFromScanRequest(BaseModel):
    """
    Request model for generating complaint from scan result.
    """

    model_config = ConfigDict(extra="forbid")

    scan_result: Dict[str, Any] = Field(
        ...,
        description="Complete scan result from System 1-6",
    )

    consumer_name: str = Field(
        default="Consumer",
        max_length=100,
        description="Name of the complainant",
    )

    consumer_email: str = Field(
        default="",
        max_length=100,
        description="Email of the complainant",
    )

    consumer_phone: str = Field(
        default="",
        max_length=15,
        description="Phone number of the complainant",
    )


# ==========================================================
# RESPONSE MODELS
# ==========================================================


class ComplaintResponse(BaseModel):
    """
    Response model for FSSAI complaint generation.
    """

    model_config = ConfigDict(extra="forbid")

    success: bool = True

    complaint_id: str

    generated_at: str

    violations_count: int

    severity_summary: Dict[str, int]

    pdf_size_bytes: int

    qr_code_size_bytes: int

    submission_portal_url: str


class FSSAILicenseValidationResponse(BaseModel):
    """
    Response model for FSSAI license validation.
    """

    model_config = ConfigDict(extra="forbid")

    success: bool = True

    license_number: str

    status: str

    is_valid: bool

    details: Dict[str, Any]


# ==========================================================
# API ENDPOINTS
# ==========================================================


@router.post(
    "/generate",
    response_model=ComplaintResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate FSSAI complaint",
    description="Generate a formal FSSAI complaint document from product details.",
)
async def generate_complaint(
    request: GenerateComplaintRequest,
) -> ComplaintResponse:
    """
    Generate FSSAI complaint from product details and violations.
    """

    try:

        logger.info(
            f"Generating FSSAI complaint for product: {request.product_name}"
        )

        result = await complaint_service.generate_complaint(

            product_name=request.product_name,

            brand=request.brand,

            manufacturer=request.manufacturer,

            fssai_number=request.fssai_number,

            violations_data=request.violations,

            consumer_name=request.consumer_name,

            consumer_email=request.consumer_email,

            consumer_phone=request.consumer_phone,

            consumer_address=request.consumer_address,

            additional_notes=request.additional_notes,

        )

        return ComplaintResponse(

            success=True,

            complaint_id=result["complaint_id"],

            generated_at=result["generated_at"],

            violations_count=result["violations_count"],

            severity_summary=result["severity_summary"],

            pdf_size_bytes=result["pdf"]["size_bytes"],

            qr_code_size_bytes=result["qr_code"]["size_bytes"],

            submission_portal_url=result["submission"]["portal_url"],

        )

    except ScanixException as e:

        logger.error(f"ScanixException in generate_complaint: {e}")

        raise HTTPException(

            status_code=e.status_code,

            detail={

                "error_code": e.error_code,

                "message": e.message,

                "details": e.details,

            },

        )

    except Exception as e:

        logger.exception(f"Unexpected error in generate_complaint: {e}")

        raise HTTPException(

            status_code=500,

            detail={

                "error_code": ErrorCode.UNKNOWN_ERROR,

                "message": str(e),

            },

        )


@router.post(
    "/from-scan",
    response_model=ComplaintResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate complaint from scan result",
    description="Generate FSSAI complaint directly from System 1-6 scan output.",
)
async def generate_complaint_from_scan_result(
    request: ComplaintFromScanRequest,
    background_tasks: BackgroundTasks,
) -> ComplaintResponse:
    """
    Generate FSSAI complaint from existing scan result.
    """

    try:

        logger.info("Generating FSSAI complaint from scan result")

        result = await generate_complaint_from_scan(

            scan_result=request.scan_result,

            consumer_name=request.consumer_name,

            consumer_email=request.consumer_email,

            consumer_phone=request.consumer_phone,

        )

        return ComplaintResponse(

            success=True,

            complaint_id=result["complaint_id"],

            generated_at=result["generated_at"],

            violations_count=result["violations_count"],

            severity_summary=result["severity_summary"],

            pdf_size_bytes=result["pdf"]["size_bytes"],

            qr_code_size_bytes=result["qr_code"]["size_bytes"],

            submission_portal_url=result["submission"]["portal_url"],

        )

    except ScanixException as e:

        logger.error(f"ScanixException in generate_complaint_from_scan_result: {e}")

        raise HTTPException(

            status_code=e.status_code,

            detail={

                "error_code": e.error_code,

                "message": e.message,

                "details": e.details,

            },

        )

    except Exception as e:

        logger.exception(f"Unexpected error in generate_complaint_from_scan_result: {e}")

        raise HTTPException(

            status_code=500,

            detail={

                "error_code": ErrorCode.UNKNOWN_ERROR,

                "message": str(e),

            },

        )


@router.post(
    "/validate-fssai",
    response_model=FSSAILicenseValidationResponse,
    status_code=status.HTTP_200_OK,
    summary="Validate FSSAI license",
    description="Validate a 14-digit FSSAI license number.",
)
async def validate_fssai_license(
    license_number: str = Query(
        ...,
        pattern=r"^\d{14}$",
        description="14-digit FSSAI license number",
    ),
) -> FSSAILicenseValidationResponse:
    """
    Validate FSSAI license number.
    """

    try:

        logger.info(f"Validating FSSAI license: {license_number}")

        validator = FSSAILicenseValidator()

        result = await validator.validate(license_number)

        # Handle both tuple return and object return
        if isinstance(result, tuple):
            status_val, details = result
            is_valid = status_val in [
                FSSAILicenseStatus.VALID,
                FSSAILicenseStatus.PATTERN_ONLY,
            ]
            status_str = status_val.value if hasattr(status_val, 'value') else str(status_val)
        else:
            is_valid = result.is_valid
            status_str = result.status.value if hasattr(result.status, 'value') else str(result.status)
            details = result.additional_details if hasattr(result, 'additional_details') else {}

        return FSSAILicenseValidationResponse(

            success=True,

            license_number=license_number,

            status=status_str,

            is_valid=is_valid,

            details=details,

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


@router.get(
    "/download/{complaint_id}",
    status_code=status.HTTP_200_OK,
    summary="Download complaint PDF",
    description="Download the generated FSSAI complaint PDF.",
)
async def download_complaint_pdf(
    complaint_id: str,
):
    """
    Download complaint PDF by complaint ID from Supabase storage.
    """
    try:
        # Get PDF from storage
        pdf_bytes = await complaint_service.download_pdf(complaint_id)
        
        if not pdf_bytes:
            raise HTTPException(
                status_code=404,
                detail={
                    "error_code": "PDF_NOT_FOUND",
                    "message": f"PDF for complaint {complaint_id} not found. Please check the complaint ID or generate the complaint first.",
                },
            )
        
        # Return as downloadable file
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=fssai_complaint_{complaint_id}.pdf"},
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error downloading PDF: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error_code": ErrorCode.UNKNOWN_ERROR,
                "message": str(e),
            },
        )


@router.get(
    "/status/{complaint_id}",
    status_code=status.HTTP_200_OK,
    summary="Get complaint status",
    description="Get the status of a submitted complaint.",
)
async def get_complaint_status(
    complaint_id: str,
) -> Dict[str, Any]:
    """
    Get status of a complaint by ID from database.
    """
    try:
        status_data = await complaint_service.get_complaint_status(complaint_id)
        
        return {
            "success": True,
            "complaint_id": complaint_id,
            "status": status_data.get("status", "unknown"),
            "submitted_at": status_data.get("submitted_at"),
            "updated_at": status_data.get("updated_at"),
            "product_name": status_data.get("product_name"),
            "pdf_url": status_data.get("pdf_url"),
        }
        
    except Exception as e:
        logger.exception(f"Error getting complaint status: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error_code": ErrorCode.UNKNOWN_ERROR,
                "message": str(e),
            },
        )


# ==========================================================
# HEALTH CHECK
# ==========================================================


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Complaint service health check",
)
async def complaint_health() -> Dict[str, Any]:
    """
    Health check endpoint for complaint service.
    """

    return {

        "success": True,

        "service": "FSSAI Complaint Generator",

        "version": "2.0.0",

        "status": "healthy",

    }


# ==========================================================
# END OF FILE - complaint.py
# TOTAL LINES: 520
# ==========================================================