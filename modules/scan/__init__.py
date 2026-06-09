# ==========================================================
# SCANIX AI
# SYSTEM 1 – SCAN INTELLIGENCE MODULE
# ELITE PRODUCTION GRADE – FINAL VERSION
# ==========================================================


from __future__ import annotations


from .constants import (
    MAX_UPLOAD_MB,

    MAX_SCAN_IMAGES,

    SUPPORTED_IMAGE_TYPES,

    MIN_OCR_CONFIDENCE,

    GOOD_OCR_CONFIDENCE,

    EXCELLENT_OCR_CONFIDENCE,

    HIGH_QUALITY_SCORE,

    MEDIUM_QUALITY_SCORE,

    LOW_QUALITY_SCORE,

    E_NUMBER_PATTERN,

    OCR_CORRECTIONS,

    BRANDS,

    INDIAN_BRANDS,

    CATEGORY_KEYWORDS,

    CATEGORY_MAPPINGS,

    POSITIVE_INGREDIENTS,

    NEGATIVE_INGREDIENTS,

    PALM_OIL_KEYWORDS,

    ULTRA_PROCESSED_KEYWORDS,

    PROCESSING_LEVEL_KEYWORDS,

    NOVA_GROUP_KEYWORDS,

    PRESERVATIVES,

    ADDITIVES,

    HIGH_RISK_E_NUMBERS,

    HIGH_RISK_E_NUMBERS_LIST,

    ARTIFICIAL_INGREDIENTS,

    ALLERGENS,

    ALLERGEN_ALIASES,

    HIDDEN_SUGARS,

    HIDDEN_FATS,

    RISK_KEYWORDS,

    MARKETING_CLAIMS,

    SECTION_KEYWORDS,

    PRODUCT_IMAGES,

    NUTRISCORE_THRESHOLDS,

    RECOMMENDATION_RULES,

    HEALTH_SCORE_WEIGHTS,

    HEALTH_SCORE_THRESHOLDS,
)


from .scan_intelligence import (
    RiskLevel,

    VerificationLevel,

    ProductGrade,

    RecommendationType,

    ProductIntelligence,

    OCRIntelligence,

    ScanQualityIntelligence,

    IngredientIntelligence,

    PositiveInsight,

    NegativeInsight,

    AllergenInsight,

    ClaimIntelligence,

    SectionIntelligence,

    RiskIntelligence,

    TrustIntelligence,

    VerificationIntelligence,

    NutritionSnapshot,

    RecommendationInsight,

    ConsumerIntelligence,

    ScanMetadata,

    ScanResponse,

    FavoriteRequest,

    ManualSearchRequest,
)


from .scan_engine import (
    ScanUtils,

    MemoryEngine,

    OCRCorrectionEngine,

    OCREngine,

    BarcodeEngine,

    ProductEngine,

    ProductFusionEngine,

    ImageQualityEngine,

    OpenFoodFactsEngine,

    TrustEngine,

    VerificationEngine,

    ProductEnrichmentEngine,

    ProductFusionV2,

    ENumberExtractorEngine,

    PositiveEngine,

    NegativeEngine,

    AllergenEngine,

    ClaimEngine,

    RiskEngine,

    SectionEngine,

    CoverageEngine,

    ScanQualityEngine,

    RecommendationEngine,

    ClaimVerificationEngine,

    ProductBadgeEngine,

    TrustClassificationEngine,

    NutritionSnapshotEngine,

    MemoryAnalyticsEngine,

    DuplicateIntelligenceEngine,

    ConsumerProfileEngine,

    MultiImageFusionEngine,

    MasterScanEngine,

    ocr_correction_engine,

    ocr_engine,

    memory_engine,

    barcode_engine,

    product_engine,

    fusion_engine,

    image_quality_engine,

    openfoodfacts_engine,

    trust_engine,

    verification_engine,

    enrichment_engine,

    fusion_v2,

    enumber_extractor_engine,

    positive_engine,

    negative_engine,

    allergen_engine,

    claim_engine,

    risk_engine,

    section_engine,

    coverage_engine,

    scan_quality_engine,

    recommendation_engine,

    claim_verification_engine,

    product_badge_engine,

    trust_classification_engine,

    nutrition_snapshot_engine,

    memory_analytics_engine,

    duplicate_intelligence_engine,

    consumer_profile_engine,

    multi_image_fusion_engine,

    master_scan_engine,
)


__all__ = [
    # Constants
    "MAX_UPLOAD_MB",

    "MAX_SCAN_IMAGES",

    "SUPPORTED_IMAGE_TYPES",

    "MIN_OCR_CONFIDENCE",

    "GOOD_OCR_CONFIDENCE",

    "EXCELLENT_OCR_CONFIDENCE",

    "HIGH_QUALITY_SCORE",

    "MEDIUM_QUALITY_SCORE",

    "LOW_QUALITY_SCORE",

    "E_NUMBER_PATTERN",

    "OCR_CORRECTIONS",

    "BRANDS",

    "INDIAN_BRANDS",

    "CATEGORY_KEYWORDS",

    "CATEGORY_MAPPINGS",

    "POSITIVE_INGREDIENTS",

    "NEGATIVE_INGREDIENTS",

    "PALM_OIL_KEYWORDS",

    "ULTRA_PROCESSED_KEYWORDS",

    "PROCESSING_LEVEL_KEYWORDS",

    "NOVA_GROUP_KEYWORDS",

    "PRESERVATIVES",

    "ADDITIVES",

    "HIGH_RISK_E_NUMBERS",

    "HIGH_RISK_E_NUMBERS_LIST",

    "ARTIFICIAL_INGREDIENTS",

    "ALLERGENS",

    "ALLERGEN_ALIASES",

    "HIDDEN_SUGARS",

    "HIDDEN_FATS",

    "RISK_KEYWORDS",

    "MARKETING_CLAIMS",

    "SECTION_KEYWORDS",

    "PRODUCT_IMAGES",

    "NUTRISCORE_THRESHOLDS",

    "RECOMMENDATION_RULES",

    "HEALTH_SCORE_WEIGHTS",

    "HEALTH_SCORE_THRESHOLDS",

    # Models
    "RiskLevel",

    "VerificationLevel",

    "ProductGrade",

    "RecommendationType",

    "ProductIntelligence",

    "OCRIntelligence",

    "ScanQualityIntelligence",

    "IngredientIntelligence",

    "PositiveInsight",

    "NegativeInsight",

    "AllergenInsight",

    "ClaimIntelligence",

    "SectionIntelligence",

    "RiskIntelligence",

    "TrustIntelligence",

    "VerificationIntelligence",

    "NutritionSnapshot",

    "RecommendationInsight",

    "ConsumerIntelligence",

    "ScanMetadata",

    "ScanResponse",

    "FavoriteRequest",

    "ManualSearchRequest",

    # Engines
    "ScanUtils",

    "MemoryEngine",

    "OCRCorrectionEngine",

    "OCREngine",

    "BarcodeEngine",

    "ProductEngine",

    "ProductFusionEngine",

    "ImageQualityEngine",

    "OpenFoodFactsEngine",

    "TrustEngine",

    "VerificationEngine",

    "ProductEnrichmentEngine",

    "ProductFusionV2",

    "ENumberExtractorEngine",

    "PositiveEngine",

    "NegativeEngine",

    "AllergenEngine",

    "ClaimEngine",

    "RiskEngine",

    "SectionEngine",

    "CoverageEngine",

    "ScanQualityEngine",

    "RecommendationEngine",

    "ClaimVerificationEngine",

    "ProductBadgeEngine",

    "TrustClassificationEngine",

    "NutritionSnapshotEngine",

    "MemoryAnalyticsEngine",

    "DuplicateIntelligenceEngine",

    "ConsumerProfileEngine",

    "MultiImageFusionEngine",

    "MasterScanEngine",

    # Singletons
    "ocr_correction_engine",

    "ocr_engine",

    "memory_engine",

    "barcode_engine",

    "product_engine",

    "fusion_engine",

    "image_quality_engine",

    "openfoodfacts_engine",

    "trust_engine",

    "verification_engine",

    "enrichment_engine",

    "fusion_v2",

    "enumber_extractor_engine",

    "positive_engine",

    "negative_engine",

    "allergen_engine",

    "claim_engine",

    "risk_engine",

    "section_engine",

    "coverage_engine",

    "scan_quality_engine",

    "recommendation_engine",

    "claim_verification_engine",

    "product_badge_engine",

    "trust_classification_engine",

    "nutrition_snapshot_engine",

    "memory_analytics_engine",

    "duplicate_intelligence_engine",

    "consumer_profile_engine",

    "multi_image_fusion_engine",

    "master_scan_engine",
]


# ==========================================================
# MODULE INITIALIZATION LOG
# ==========================================================


from core.logging import log


log.info(
    "System 1 – Scan Intelligence module initialized",
    constants_loaded=len(__all__),
    brands_count=len(BRANDS) + len(INDIAN_BRANDS),
    categories_count=len(CATEGORY_KEYWORDS),
    allergens_count=len(ALLERGENS),
    e_numbers_risk_count=len(HIGH_RISK_E_NUMBERS),
)


# ==========================================================
# END OF FILE – __init__.py
# ==========================================================