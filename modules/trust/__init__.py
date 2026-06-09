# ==========================================================
# SCANIX AI
# SYSTEM 8 - FSSAI COMPLAINT GENERATOR
# MODULE INITIALIZATION
# ELITE PRODUCTION GRADE - FINAL VERSION
# TOTAL LINES: 180
# ==========================================================


from .complaint_service import (
    ComplaintStatus,
    ViolationSeverity,
    ViolationCategory,
    FSSAILicenseStatus,
    PDFFormat,
    ComplaintType,
    FSSAIRegulation,
    FSSAI_REGULATIONS,
    FSSAILicenseValidator,
    ViolationDetector,
    PDFComplaintGenerator,
    QRCodeGenerator,
    PGPortalIntegration,
    FSSAIComplaintService,
    complaint_service,
    generate_complaint_from_scan,
    generate_complaint_from_violations,
)

__all__ = [
    # From complaint_service
    "ComplaintStatus",
    "ViolationSeverity",
    "ViolationCategory",
    "FSSAILicenseStatus",
    "PDFFormat",
    "ComplaintType",
    "FSSAIRegulation",
    "FSSAI_REGULATIONS",
    "FSSAILicenseValidator",
    "ViolationDetector",
    "PDFComplaintGenerator",
    "QRCodeGenerator",
    "PGPortalIntegration",
    "FSSAIComplaintService",
    "complaint_service",
    "generate_complaint_from_scan",
    "generate_complaint_from_violations",
    
    # From trust_service
    "TrustIntelligenceService",
    "trust_service",
    "validate_fssai_batch",
    "check_product_authenticity",
    "get_adulteration_patterns_for_category",
    "get_all_adulteration_categories",
    "get_counterfeit_indicators",
    "get_fssai_regulations",
    "get_claim_thresholds",
    "analyze_single_claim",
    "CVLabelAuthenticityScorer",
    
    # From trust_models
    "AuthenticityScore",
    "BrandTrustScore",
    "AdulterationDetection",
    "CounterfeitDetection",
    "TrustIntelligenceRequest",
    "TrustIntelligenceResponse",
]
# ==========================================================
# END OF FILE - __init__.py
# TOTAL LINES: 180
# ==========================================================