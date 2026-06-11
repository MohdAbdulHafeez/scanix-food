# ==========================================================
# SCANIX AI
# SYSTEM 8 - TRUST INTELLIGENCE + FSSAI COMPLAINT
# MODULE INITIALIZATION
# ==========================================================
#
# Re-exports the public surface of System 8 so callers can do
# `from modules.trust import trust_service, AuthenticityScore, ...`.
# Names are pulled from the submodule that actually defines them.

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

from .trust_models import (
    FSSAILicenseInfo,
    AuthenticityScore,
    BrandTrustScore,
    AdulterationDetection,
    CounterfeitDetection,
    TrustIntelligenceRequest,
    TrustIntelligenceResponse,
    ADULTERATION_PATTERNS,
    COUNTERFEIT_INDICATORS,
)

from .trust_service import (
    TrustIntelligenceService,
    trust_service,
    get_adulteration_patterns_for_category,
    get_all_adulteration_categories,
    get_counterfeit_indicators,
    get_fssai_regulations,
    get_claim_thresholds,
    CVLabelAuthenticityScorer,
)

__all__ = [
    # complaint_service
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
    # trust_models
    "FSSAILicenseInfo",
    "AuthenticityScore",
    "BrandTrustScore",
    "AdulterationDetection",
    "CounterfeitDetection",
    "TrustIntelligenceRequest",
    "TrustIntelligenceResponse",
    "ADULTERATION_PATTERNS",
    "COUNTERFEIT_INDICATORS",
    # trust_service
    "TrustIntelligenceService",
    "trust_service",
    "get_adulteration_patterns_for_category",
    "get_all_adulteration_categories",
    "get_counterfeit_indicators",
    "get_fssai_regulations",
    "get_claim_thresholds",
    "CVLabelAuthenticityScorer",
]
