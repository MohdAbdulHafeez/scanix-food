# ==========================================================
# SCANIX AI
# SYSTEM 1 – SCAN INTELLIGENCE MODELS
# ELITE PRODUCTION GRADE
# ==========================================================


from __future__ import annotations


from enum import Enum
from typing import Any
from typing import Dict
from typing import List
from typing import Optional


from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


# ==========================================================
# ENUMS
# ==========================================================


class RiskLevel(str, Enum):
    """
    Risk level for health and safety assessments.
    """

    NONE = "NONE"

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"

    CRITICAL = "CRITICAL"


class VerificationLevel(str, Enum):
    """
    Verification level for data sources.
    """

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"

    VERIFIED = "VERIFIED"


class ProductGrade(str, Enum):
    """
    Overall product grade based on health score.
    """

    A_PLUS = "A+"

    A = "A"

    B = "B"

    C = "C"

    D = "D"

    F = "F"


class RecommendationType(str, Enum):
    """
    Consumption recommendation level.
    """

    DAILY = "DAILY"

    WEEKLY = "WEEKLY"

    OCCASIONAL = "OCCASIONAL"

    AVOID = "AVOID"


# ==========================================================
# PRODUCT INTELLIGENCE
# ==========================================================


class ProductIntelligence(BaseModel):
    """
    Product identification and basic information.
    """

    model_config = ConfigDict(extra="forbid")

    product_name: Optional[str] = None

    brand: Optional[str] = None

    category: Optional[str] = None

    barcode: Optional[str] = None

    image_url: Optional[str] = None

    identity_confidence: int = 0

    image_match_confidence: int = 0

    matched_by: List[str] = Field(
        default_factory=list
    )


# ==========================================================
# OCR INTELLIGENCE
# ==========================================================


class OCRIntelligence(BaseModel):
    """
    OCR extraction results and quality metrics.
    """

    model_config = ConfigDict(extra="forbid")

    extracted_text: str = ""

    blocks: List[str] = Field(
        default_factory=list
    )

    confidence_values: List[float] = Field(
        default_factory=list
    )

    average_confidence: float = 0.0

    text_density_score: int = 0

    readability_score: int = 0

    ocr_quality_score: int = 0


# ==========================================================
# SCAN QUALITY
# ==========================================================


class ScanQualityIntelligence(BaseModel):
    """
    Overall scan quality assessment.
    """

    model_config = ConfigDict(extra="forbid")

    image_quality_score: int = 0

    coverage_score: int = 0

    completeness_score: int = 0

    scan_quality_score: int = 0

    scan_reliability_score: int = 0


# ==========================================================
# INGREDIENT INTELLIGENCE
# ==========================================================


class IngredientIntelligence(BaseModel):
    """
    Comprehensive ingredient analysis from System 2.
    """

    model_config = ConfigDict(extra="forbid")

    ingredient_count: int = 0

    additive_count: int = 0

    preservative_count: int = 0

    artificial_count: int = 0

    additive_candidate_count: int = 0

    processing_level: Optional[str] = None

    processing_confidence: int = 0

    hidden_sugar_count: int = 0

    hidden_fat_count: int = 0

    quality_score: int = 0

    quality_grade: str = "C"

    clean_label_score: int = 0

    complexity_score: int = 0

    e_numbers: List[str] = Field(
        default_factory=list
    )

    allergens: List[str] = Field(
        default_factory=list
    )

    contains_palm_oil: bool = False

    contains_msg: bool = False

    overall_risk_level: Optional[str] = None

    ingredients: List[str] = Field(
        default_factory=list
    )


# ==========================================================
# POSITIVE INSIGHTS
# ==========================================================


class PositiveInsight(BaseModel):
    """
    Positive nutritional insights.
    """

    model_config = ConfigDict(extra="forbid")

    title: str

    value: Optional[str] = None

    reason: str


# ==========================================================
# NEGATIVE INSIGHTS
# ==========================================================


class NegativeInsight(BaseModel):
    """
    Negative nutritional insights.
    """

    model_config = ConfigDict(extra="forbid")

    title: str

    reason: str

    severity: RiskLevel


# ==========================================================
# ALLERGEN INSIGHTS
# ==========================================================


class AllergenInsight(BaseModel):
    """
    Detected allergens.
    """

    model_config = ConfigDict(extra="forbid")

    allergen: str

    severity: RiskLevel


# ==========================================================
# CLAIM INTELLIGENCE
# ==========================================================


class ClaimIntelligence(BaseModel):
    """
    Marketing claims detected on packaging.
    """

    model_config = ConfigDict(extra="forbid")

    claims_detected: List[str] = Field(
        default_factory=list
    )

    claim_details: Optional[List[Dict[str, Any]]] = None


# ==========================================================
# SECTION INTELLIGENCE
# ==========================================================


class SectionIntelligence(BaseModel):
    """
    Label sections detected via OCR.
    """

    model_config = ConfigDict(extra="forbid")

    nutrition_table: bool = False

    ingredients_section: bool = False

    barcode_section: bool = False

    claims_section: bool = False

    front_label_section: bool = False


# ==========================================================
# RISK INTELLIGENCE
# ==========================================================


class RiskIntelligence(BaseModel):
    """
    Health risk assessment.
    """

    model_config = ConfigDict(extra="forbid")

    risks: List[str] = Field(
        default_factory=list
    )

    hidden_sugars: Optional[List[str]] = None

    overall_risk: RiskLevel = RiskLevel.LOW


# ==========================================================
# TRUST INTELLIGENCE
# ==========================================================


class TrustIntelligence(BaseModel):
    """
    Data trust and reliability scores.
    """

    model_config = ConfigDict(extra="forbid")

    trust_score: int = 0

    source_reliability: int = 0

    evidence_strength: int = 0

    data_confidence: int = 0


# ==========================================================
# VERIFICATION INTELLIGENCE
# ==========================================================


class VerificationIntelligence(BaseModel):
    """
    Data source verification status.
    """

    model_config = ConfigDict(extra="forbid")

    barcode_verified: bool = False

    ocr_verified: bool = False

    source_verified: bool = False

    verification_level: VerificationLevel = (
        VerificationLevel.LOW
    )


# ==========================================================
# NUTRITION SNAPSHOT
# ==========================================================


class NutritionSnapshot(BaseModel):
    """
    Extracted nutritional information.
    """

    model_config = ConfigDict(extra="forbid")

    calories: Optional[float] = None

    protein: Optional[float] = None

    fat: Optional[float] = None

    saturated_fat: Optional[float] = None

    trans_fat: Optional[float] = None

    sugar: Optional[float] = None

    sodium: Optional[float] = None

    carbohydrates: Optional[float] = None

    fiber: Optional[float] = None

    caffeine: Optional[float] = None

    nutriscore: Optional[str] = None

    nova: Optional[int] = None

    category: Optional[str] = None

    # Derived scores
    health_score: int = 0

    sugar_risk_score: int = 0

    sodium_risk_score: int = 0

    fat_risk_score: int = 0

    nutrition_detected: bool = False

    nutrition_completeness: int = 0

    nutrition_confidence: int = 0

    # Health flags
    is_high_protein: bool = False

    is_high_fiber: bool = False

    is_low_sugar: bool = False

    is_low_sodium: bool = False

    is_heart_healthy: bool = False

    is_diabetic_friendly: bool = False


# ==========================================================
# RECOMMENDATION
# ==========================================================


class RecommendationInsight(BaseModel):
    """
    Final product recommendation.
    """

    model_config = ConfigDict(extra="forbid")

    recommendation: RecommendationType

    reason: str

    best_for: List[str] = Field(
        default_factory=list
    )


# ==========================================================
# CONSUMER INTELLIGENCE
# ==========================================================


class ConsumerIntelligence(BaseModel):
    """
    Consumer-facing intelligence from System 4.
    """

    model_config = ConfigDict(extra="forbid")

    data: Dict[str, Any] = Field(
        default_factory=dict
    )


# ==========================================================
# METADATA
# ==========================================================


class ScanMetadata(BaseModel):
    """
    Scan execution metadata.
    """

    model_config = ConfigDict(extra="forbid")

    scan_id: str

    timestamp: str

    source: str

    api_version: str = "2.0"

    overall_scan_confidence: int = 0

    processing_time_ms: Optional[int] = None

    audit_trail: Optional[Dict[str, Any]] = None


# ==========================================================
# MASTER RESPONSE
# ==========================================================


class ScanResponse(BaseModel):
    """
    Complete scan response from System 1.
    Consumed by Systems 2-9.
    """

    model_config = ConfigDict(extra="forbid")

    success: bool = True

    hash: Optional[str] = None

    metadata: ScanMetadata

    product: ProductIntelligence

    ocr: OCRIntelligence

    scan_quality: ScanQualityIntelligence

    ingredients: IngredientIntelligence

    claims: ClaimIntelligence

    sections: SectionIntelligence

    positives: List[PositiveInsight] = Field(
        default_factory=list
    )

    negatives: List[NegativeInsight] = Field(
        default_factory=list
    )

    allergens: List[AllergenInsight] = Field(
        default_factory=list
    )

    risks: RiskIntelligence

    trust: TrustIntelligence

    verification: VerificationIntelligence

    nutrition: NutritionSnapshot

    recommendation: RecommendationInsight

    # System 3
    metabolic_intelligence: Optional[Dict[str, Any]] = None

    # System 4
    consumer_intelligence: Optional[ConsumerIntelligence] = None

    # System 5
    digital_twin: Optional[Dict[str, Any]] = None

    # System 6
    food_explainer: Optional[Dict[str, Any]] = None

    nutritionist: Optional[Dict[str, Any]] = None

    # System 7
    smart_swaps: Optional[Dict[str, Any]] = None

    # System 8
    trust_intelligence: Optional[Dict[str, Any]] = None

    # System 9
    saved_to_history: bool = False

    # Analytics
    analytics: Optional[Dict[str, Any]] = None

    duplicate: Optional[Dict[str, Any]] = None


# ==========================================================
# FAVORITES
# ==========================================================


class FavoriteRequest(BaseModel):
    """
    Request model for adding product to favorites.
    """

    model_config = ConfigDict(extra="forbid")

    brand: str

    product_name: Optional[str] = None


# ==========================================================
# MANUAL SEARCH
# ==========================================================


class ManualSearchRequest(BaseModel):
    """
    Request model for manual product search.
    """

    model_config = ConfigDict(extra="forbid")

    query: str = Field(
        min_length=2,
        max_length=200,
    )


# ==========================================================
# END OF FILE – scan_intelligence.py
# ==========================================================