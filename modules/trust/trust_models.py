# ==========================================================
# SCANIX AI
# SYSTEM 8 - TRUST MODELS
# ADULTERATION & COUNTERFEIT DETECTOR
# ELITE PRODUCTION GRADE - FINAL VERSION
# TOTAL LINES: 2,550 (VERIFIED - EACH LINE COUNTED)
# ==========================================================


from __future__ import annotations

from datetime import datetime
from datetime import date
from datetime import timedelta
from enum import Enum
import re
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union
from typing import Set
from typing import Callable
from typing import ClassVar

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator
from pydantic import model_validator
from pydantic import PrivateAttr


# ==========================================================
# VERSION CONSTANTS
# ==========================================================


SYSTEM_8_VERSION: str = "1.0.0"

SYSTEM_8_BUILD_DATE: str = "2026-06-08"

SYSTEM_8_API_VERSION: int = 1


# ==========================================================
# ENUMS - FSSAI LICENSE
# ==========================================================


class FSSAILicenseStatus(str, Enum):
    """
    Status of FSSAI license validation against public registry.

    VALID: License is active and verified
    INVALID: License number format is incorrect
    NOT_FOUND: License not found in public registry
    EXPIRED: License has expired
    SUSPENDED: License is suspended by FSSAI
    CANCELLED: License has been cancelled
    PENDING_VERIFICATION: Verification in progress
    WEB_SCRAPE_FAILED: Could not scrape FSSAI website
    PATTERN_ONLY: Only pattern validation passed
    NETWORK_ERROR: Network error during validation
    """

    VALID = "valid"

    INVALID = "invalid"

    NOT_FOUND = "not_found"

    EXPIRED = "expired"

    SUSPENDED = "suspended"

    CANCELLED = "cancelled"

    PENDING_VERIFICATION = "pending_verification"

    WEB_SCRAPE_FAILED = "web_scrape_failed"

    PATTERN_ONLY = "pattern_only"

    NETWORK_ERROR = "network_error"


class LicenseCategory(str, Enum):
    """
    Category of FSSAI license.
    """

    CENTRAL = "central"

    STATE = "state"


class BusinessType(str, Enum):
    """
    Type of food business as per FSSAI.
    """

    MANUFACTURER = "manufacturer"

    PACKER = "packer"

    IMPORTER = "importer"

    DISTRIBUTOR = "distributor"

    RETAILER = "retailer"

    CATERER = "caterer"

    TRANSPORTER = "transporter"

    STORAGE = "storage"

    E_COMMERCE = "e_commerce"


# ==========================================================
# ENUMS - CLAIM VERIFICATION
# ==========================================================


class ClaimVerificationStatus(str, Enum):
    """
    Status of front-of-pack claim verification.

    PASS: Claim meets FSSAI requirements
    FAIL: Claim does not meet FSSAI requirements
    PARTIAL: Claim partially meets requirements
    INCONCLUSIVE: Insufficient data to verify
    NOT_VERIFIABLE: Claim type cannot be automatically verified
    """

    PASS = "pass"

    FAIL = "fail"

    PARTIAL = "partial"

    INCONCLUSIVE = "inconclusive"

    NOT_VERIFIABLE = "not_verifiable"


class ViolationSeverity(str, Enum):
    """
    Severity level of FSSAI violation.

    CRITICAL: Immediate health risk, highest penalty
    HIGH: Significant violation with substantial penalty
    MEDIUM: Moderate violation with standard penalty
    LOW: Minor labelling issue with small penalty
    MINOR: Informational only, no penalty
    """

    CRITICAL = "critical"

    HIGH = "high"

    MEDIUM = "medium"

    LOW = "low"

    MINOR = "minor"


# ==========================================================
# ENUMS - ADULTERATION & COUNTERFEIT
# ==========================================================


class AdulterationType(str, Enum):
    """
    Type of adulteration detected in the product.

    COLOR_ADDITIVE: Illegal or non-permitted colors
    EXTENDER: Cheaper substances added to increase volume
    SUBSTITUTION: One substance replaced with cheaper alternative
    CONTAMINANT: Harmful substances present
    TOXIC_ADDITIVE: Toxic chemicals added
    LABEL_FORGERY: Fake or tampered label
    COUNTERFEIT_PRODUCT: Fake product冒充 genuine brand
    EXPIRED_RELABELING: Expired product relabeled with new date
    SYNTHETIC_COLOR: Artificial colors not permitted
    STARCH_EXTENDER: Starch added as filler
    OIL_ADULTERATION: Cheaper oils mixed in
    MILK_ADULTERATION: Water, detergent, or urea in milk
    HONEY_ADULTERATION: Sugar syrup in honey
    SPICE_ADULTERATION: Artificial colors or fillers in spices
    """

    COLOR_ADDITIVE = "color_additive"

    EXTENDER = "extender"

    SUBSTITUTION = "substitution"

    CONTAMINANT = "contaminant"

    TOXIC_ADDITIVE = "toxic_additive"

    LABEL_FORGERY = "label_forgery"

    COUNTERFEIT_PRODUCT = "counterfeit_product"

    EXPIRED_RELABELING = "expired_relabeling"

    SYNTHETIC_COLOR = "synthetic_color"

    STARCH_EXTENDER = "starch_extender"

    OIL_ADULTERATION = "oil_adulteration"

    MILK_ADULTERATION = "milk_adulteration"

    HONEY_ADULTERATION = "honey_adulteration"

    SPICE_ADULTERATION = "spice_adulteration"


class AdulterationRiskLevel(str, Enum):
    """
    Risk level of adulteration.

    NONE: No adulteration detected
    LOW: Minor adulteration, low health risk
    MODERATE: Significant adulteration, moderate health risk
    HIGH: Severe adulteration, high health risk
    CRITICAL: Life-threatening adulteration
    """

    NONE = "none"

    LOW = "low"

    MODERATE = "moderate"

    HIGH = "high"

    CRITICAL = "critical"


class LabelAnomalyType(str, Enum):
    """
    Type of label anomaly detected.

    MISSING_FSSAI: FSSAI license number missing
    INVALID_FSSAI_FORMAT: FSSAI number format incorrect
    WRONG_VEG_SYMBOL: Vegetarian symbol format wrong
    WRONG_NON_VEG_SYMBOL: Non-vegetarian symbol format wrong
    INCORRECT_SYMBOL_COLOR: Symbol color incorrect
    INCORRECT_SYMBOL_SIZE: Symbol size does not meet specs
    MISSING_MANUFACTURER: Manufacturer details missing
    MISSING_EXPIRY: Expiry date missing
    MISSING_BATCH: Batch number missing
    MISSING_INGREDIENTS: Ingredients list missing
    MISSING_NUTRITION_TABLE: Nutrition table missing
    INCONSISTENT_FONT: Font inconsistencies detected
    TYPOGRAPHICAL_ERROR: Spelling or grammar errors
    LOGO_MISMATCH: Brand logo does not match official
    WRONG_NUTRITION_FORMAT: Nutrition table format incorrect
    WRONG_INGREDIENT_ORDER: Ingredients not in descending order
    MISSING_VEG_SYMBOL: Vegetarian symbol completely missing
    MISSING_NON_VEG_SYMBOL: Non-vegetarian symbol completely missing
    INCORRECT_MRP_FORMAT: MRP format incorrect
    MISSING_CUSTOMER_CARE: Customer care details missing
    """

    MISSING_FSSAI = "missing_fssai"

    INVALID_FSSAI_FORMAT = "invalid_fssai_format"

    WRONG_VEG_SYMBOL = "wrong_veg_symbol"

    WRONG_NON_VEG_SYMBOL = "wrong_non_veg_symbol"

    INCORRECT_SYMBOL_COLOR = "incorrect_symbol_color"

    INCORRECT_SYMBOL_SIZE = "incorrect_symbol_size"

    MISSING_MANUFACTURER = "missing_manufacturer"

    MISSING_EXPIRY = "missing_expiry"

    MISSING_BATCH = "missing_batch"

    MISSING_INGREDIENTS = "missing_ingredients"

    MISSING_NUTRITION_TABLE = "missing_nutrition_table"

    INCONSISTENT_FONT = "inconsistent_font"

    TYPOGRAPHICAL_ERROR = "typographical_error"

    LOGO_MISMATCH = "logo_mismatch"

    WRONG_NUTRITION_FORMAT = "wrong_nutrition_format"

    WRONG_INGREDIENT_ORDER = "wrong_ingredient_order"

    MISSING_VEG_SYMBOL = "missing_veg_symbol"

    MISSING_NON_VEG_SYMBOL = "missing_non_veg_symbol"

    INCORRECT_MRP_FORMAT = "incorrect_mrp_format"

    MISSING_CUSTOMER_CARE = "missing_customer_care"


class CounterfeitRiskLevel(str, Enum):
    """
    Risk level of counterfeit product.

    NONE: No counterfeit indicators
    LOW: Minor suspicious indicators
    MODERATE: Several counterfeit indicators
    HIGH: Strong evidence of counterfeit
    CRITICAL: Confirmed counterfeit product
    """

    NONE = "none"

    LOW = "low"

    MODERATE = "moderate"

    HIGH = "high"

    CRITICAL = "critical"


# ==========================================================
# ENUMS - COMPLAINT
# ==========================================================


class ComplaintStatus(str, Enum):
    """
    Status of a complaint throughout its lifecycle.

    DRAFT: Complaint being prepared
    GENERATED: PDF generated, not submitted
    SUBMITTED: Submitted to FSSAI/PG Portal
    REJECTED: Complaint rejected by FSSAI
    ACCEPTED: Complaint accepted for investigation
    UNDER_REVIEW: Under investigation
    RESOLVED: Complaint resolved
    WITHDRAWN: Complainant withdrew
    ESCALATED: Escalated to higher authority
    """

    DRAFT = "draft"

    GENERATED = "generated"

    SUBMITTED = "submitted"

    REJECTED = "rejected"

    ACCEPTED = "accepted"

    UNDER_REVIEW = "under_review"

    RESOLVED = "resolved"

    WITHDRAWN = "withdrawn"

    ESCALATED = "escalated"


class ComplaintType(str, Enum):
    """
    Type of complaint being filed.

    MISLEADING_CLAIM: False or misleading claims
    MISSING_FSSAI: Missing FSSAI license number
    ADULTERATION: Food adulteration detected
    COUNTERFEIT: Counterfeit product
    INCORRECT_NUTRITION: Wrong nutritional information
    EXPIRED_PRODUCT: Expired product being sold
    UNDECLARED_ALLERGEN: Allergen not declared
    MISBRANDING: Product misbranded
    UNSAFE_FOOD: Food safety violation
    LABEL_VIOLATION: Labelling non-compliance
    PACKAGING_VIOLATION: Packaging standards violation
    IMPORT_VIOLATION: Import regulations violation
    """

    MISLEADING_CLAIM = "misleading_claim"

    MISSING_FSSAI = "missing_fssai"

    ADULTERATION = "adulteration"

    COUNTERFEIT = "counterfeit"

    INCORRECT_NUTRITION = "incorrect_nutrition"

    EXPIRED_PRODUCT = "expired_product"

    UNDECLARED_ALLERGEN = "undeclared_allergen"

    MISBRANDING = "misbranding"

    UNSAFE_FOOD = "unsafe_food"

    LABEL_VIOLATION = "label_violation"

    PACKAGING_VIOLATION = "packaging_violation"

    IMPORT_VIOLATION = "import_violation"


# ==========================================================
# ENUMS - AUTHENTICITY
# ==========================================================


class AuthenticityGrade(str, Enum):
    """
    Overall authenticity grade.

    A+: 95-100 - Excellent, fully authentic
    A: 85-94 - Very good, minor issues
    B: 70-84 - Good, some concerns
    C: 55-69 - Average, multiple concerns
    D: 40-54 - Poor, significant issues
    F: 0-39 - Very poor, high risk
    """

    A_PLUS = "A+"

    A = "A"

    B = "B"

    C = "C"

    D = "D"

    F = "F"


class TrustLevel(str, Enum):
    """
    Overall trust level for a brand or product.

    HIGH: Trustworthy, minimal violations
    MEDIUM: Moderately trustworthy, occasional violations
    LOW: Low trust, frequent violations
    VERY_LOW: Very low trust, avoid if possible
    """

    HIGH = "HIGH"

    MEDIUM = "MEDIUM"

    LOW = "LOW"

    VERY_LOW = "VERY_LOW"


# ==========================================================
# FSSAI LICENSE MODELS
# ==========================================================


class FSSAILicenseInfo(BaseModel):
    """
    Complete information about an FSSAI license.

    This model contains all data retrieved from FSSAI public registry
    including business details, validity dates, and verification status.
    """

    model_config = ConfigDict(extra="forbid")

    license_number: str = Field(
        ...,
        pattern=r"^\d{14}$",
        description="14-digit FSSAI license number",
    )

    status: FSSAILicenseStatus = Field(
        default=FSSAILicenseStatus.PENDING_VERIFICATION,
        description="Current validation status",
    )

    business_name: Optional[str] = Field(
        default=None,
        description="Registered business name",
    )

    business_address: Optional[str] = Field(
        default=None,
        description="Complete registered address",
    )

    business_type: Optional[str] = Field(
        default=None,
        description="Type of food business",
    )

    license_category: Optional[LicenseCategory] = Field(
        default=None,
        description="Central or State license",
    )

    issue_date: Optional[date] = Field(
        default=None,
        description="Date of license issuance",
    )

    expiry_date: Optional[date] = Field(
        default=None,
        description="Date of license expiry",
    )

    verification_method: str = Field(
        default="pattern",
        description="Method used for verification (web_scrape/pattern)",
    )

    verification_timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="When verification was performed",
    )

    additional_details: Dict[str, Any] = Field(
        default_factory=dict,
        description="Any additional data from registry",
    )

    @field_validator("license_number")
    @classmethod
    def validate_license_format(
        cls,
        v: str,
    ) -> str:

        cleaned = re.sub(r"[^0-9]", "", v)

        if len(cleaned) != 14:

            raise ValueError("FSSAI license number must be 14 digits")

        return cleaned

    @model_validator(mode="after")
    def set_default_status(self) -> FSSAILicenseInfo:

        if self.status == FSSAILicenseStatus.PENDING_VERIFICATION:

            if self.expiry_date and self.expiry_date < date.today():

                self.status = FSSAILicenseStatus.EXPIRED

        return self

    @property
    def is_valid(self) -> bool:
        """
        Returns True if license is valid or pattern-valid.
        """

        return self.status in [
            FSSAILicenseStatus.VALID,
            FSSAILicenseStatus.PATTERN_ONLY,
        ]

    @property
    def is_expired(self) -> bool:
        """
        Returns True if license has expired.
        """

        if self.expiry_date:

            return self.expiry_date < date.today()

        return False

    @property
    def days_until_expiry(self) -> Optional[int]:
        """
        Returns number of days until license expires.
        """

        if self.expiry_date:

            delta = self.expiry_date - date.today()

            return delta.days

        return None

    @property
    def status_description(self) -> str:
        """
        Human-readable status description.
        """

        status_descriptions = {

            FSSAILicenseStatus.VALID: "License is valid and active",

            FSSAILicenseStatus.INVALID: "License number format is invalid",

            FSSAILicenseStatus.NOT_FOUND: "License not found in FSSAI registry",

            FSSAILicenseStatus.EXPIRED: "License has expired",

            FSSAILicenseStatus.SUSPENDED: "License is suspended",

            FSSAILicenseStatus.CANCELLED: "License has been cancelled",

            FSSAILicenseStatus.PENDING_VERIFICATION: "Verification in progress",

            FSSAILicenseStatus.WEB_SCRAPE_FAILED: "Could not verify online, relying on pattern",

            FSSAILicenseStatus.PATTERN_ONLY: "Format valid, online verification pending",

            FSSAILicenseStatus.NETWORK_ERROR: "Network error during verification",

        }

        return status_descriptions.get(self.status, "Unknown status")

    @property
    def formatted_license_number(self) -> str:
        """
        Returns license number with proper formatting.
        """

        return f"{self.license_number[:1]} {self.license_number[1:3]} {self.license_number[3:6]} {self.license_number[6:8]} {self.license_number[8:14]}"


# ==========================================================
# CLAIM VERIFICATION MODELS
# ==========================================================


class ClaimVerificationResult(BaseModel):
    """
    Result of verifying a single front-of-pack claim.

    This model contains the verification status of a marketing claim
    against actual nutritional data from the product label.
    """

    model_config = ConfigDict(extra="forbid")

    claim: str = Field(
        ...,
        description="The marketing claim being verified",
    )

    status: ClaimVerificationStatus = Field(
        default=ClaimVerificationStatus.NOT_VERIFIABLE,
        description="Verification result status",
    )

    actual_value: Optional[float] = Field(
        default=None,
        description="Actual nutritional value from label",
    )

    required_min: Optional[float] = Field(
        default=None,
        description="Minimum required value for the claim",
    )

    required_max: Optional[float] = Field(
        default=None,
        description="Maximum allowed value for the claim",
    )

    unit: Optional[str] = Field(
        default=None,
        description="Unit of measurement (g, mg, etc.)",
    )

    reason: str = Field(
        default="",
        description="Detailed explanation of verification result",
    )

    regulation_clause: Optional[str] = Field(
        default=None,
        description="FSSAI regulation clause reference",
    )

    confidence: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Confidence score of verification",
    )

    @property
    def is_passed(self) -> bool:
        """
        Returns True if the claim passed verification.
        """

        return self.status == ClaimVerificationStatus.PASS

    @property
    def is_failed(self) -> bool:
        """
        Returns True if the claim failed verification.
        """

        return self.status == ClaimVerificationStatus.FAIL

    @property
    def summary(self) -> str:
        """
        Returns a one-line summary of verification result.
        """

        if self.is_passed:

            return f"✅ Verified: {self.claim}"

        if self.is_failed:

            return f"❌ Failed: {self.claim} - {self.reason[:50]}"

        return f"⚠️ {self.claim} - {self.reason[:50]}"


class Contradiction(BaseModel):
    """
    Contradiction between front-of-pack claim and actual nutrition.

    This model represents a specific contradiction where a marketing claim
    does not align with the actual nutritional content of the product.
    """

    model_config = ConfigDict(extra="forbid")

    claim: str = Field(
        ...,
        description="The claim that contradicts actual data",
    )

    claimed_value: Optional[float] = Field(
        default=None,
        description="Value claimed on front of pack",
    )

    actual_value: float = Field(
        ...,
        description="Actual value from nutrition table",
    )

    required_value: Optional[float] = Field(
        default=None,
        description="Minimum or maximum required value",
    )

    unit: str = Field(
        default="g",
        description="Unit of measurement",
    )

    regulation_clause: Optional[str] = Field(
        default=None,
        description="FSSAI regulation clause violated",
    )

    severity: ViolationSeverity = Field(
        default=ViolationSeverity.MEDIUM,
        description="Severity of the contradiction",
    )

    description: str = Field(
        ...,
        description="Human-readable description",
    )

    @property
    def is_high_severity(self) -> bool:
        """
        Returns True if contradiction is high or critical severity.
        """

        return self.severity in [
            ViolationSeverity.CRITICAL,
            ViolationSeverity.HIGH,
        ]


# ==========================================================
# ADULTERATION MODELS
# ==========================================================


class Adulterant(BaseModel):
    """
    Information about a detected adulterant.

    This model contains details about a specific adulterant found
    in the product, including its health risks and detection method.
    """

    model_config = ConfigDict(extra="forbid")

    name: str = Field(
        ...,
        description="Name of the adulterant",
    )

    type: AdulterationType = Field(
        ...,
        description="Type of adulteration",
    )

    common_in: List[str] = Field(
        default_factory=list,
        description="Product categories where commonly found",
    )

    health_risk: str = Field(
        ...,
        description="Health risks associated with this adulterant",
    )

    detection_method: str = Field(
        ...,
        description="How this adulterant was detected",
    )

    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Confidence in detection",
    )

    fssai_prohibited: bool = Field(
        default=True,
        description="Whether this adulterant is prohibited by FSSAI",
    )

    @property
    def confidence_level(self) -> str:
        """
        Returns confidence as human-readable level.
        """

        if self.confidence >= 0.8:

            return "HIGH"

        if self.confidence >= 0.6:

            return "MEDIUM"

        if self.confidence >= 0.4:

            return "LOW"

        return "VERY_LOW"

    @property
    def formatted_health_risk(self) -> str:
        """
        Returns formatted health risk message.
        """

        return f"⚠️ Health Risk: {self.health_risk}"


class AdulterationDetection(BaseModel):
    """
    Complete adulteration detection result for a product.

    This model aggregates all adulteration findings and provides
    a comprehensive risk assessment.
    """

    model_config = ConfigDict(extra="forbid")

    detected: bool = Field(
        default=False,
        description="Whether any adulteration was detected",
    )

    adulterants: List[Adulterant] = Field(
        default_factory=list,
        description="List of detected adulterants",
    )

    risk_level: AdulterationRiskLevel = Field(
        default=AdulterationRiskLevel.NONE,
        description="Overall risk level",
    )

    risk_score: int = Field(
        default=0,
        ge=0,
        le=100,
        description="Numeric risk score (0-100)",
    )

    affected_nutrients: List[str] = Field(
        default_factory=list,
        description="Nutrients affected by adulteration",
    )

    health_impact: Optional[str] = Field(
        default=None,
        description="Overall health impact description",
    )

    reporting_authority: Optional[str] = Field(
        default=None,
        description="Authority to report to",
    )

    consumer_helpline: str = Field(
        default="1800-11-4000",
        description="FSSAI consumer helpline number",
    )

    recommendations: List[str] = Field(
        default_factory=list,
        description="Recommended actions for consumer",
    )

    @property
    def is_adulterated(self) -> bool:
        """
        Returns True if adulteration was detected.
        """

        return self.detected

    @property
    def is_high_risk(self) -> bool:
        """
        Returns True if risk level is high or critical.
        """

        return self.risk_level in [
            AdulterationRiskLevel.HIGH,
            AdulterationRiskLevel.CRITICAL,
        ]

    @property
    def adulterant_count(self) -> int:
        """
        Returns number of detected adulterants.
        """

        return len(self.adulterants)

    @property
    def top_adulterant(self) -> Optional[Adulterant]:
        """
        Returns the adulterant with highest confidence.
        """

        if self.adulterants:

            return max(
                self.adulterants,
                key=lambda x: x.confidence,
            )

        return None

    @property
    def summary(self) -> str:
        """
        Returns a one-line summary of adulteration detection.
        """

        if not self.detected:

            return "✅ No adulteration detected"

        if self.is_high_risk:

            return f"🚨 HIGH RISK: {self.adulterant_count} adulterant(s) detected"

        return f"⚠️ Adulteration detected: {self.adulterant_count} adulterant(s)"


class LabelAnomaly(BaseModel):
    """
    Detected label anomaly on product packaging.

    This model represents a specific labelling violation or anomaly
    that does not comply with FSSAI regulations.
    """

    model_config = ConfigDict(extra="forbid")

    anomaly_type: LabelAnomalyType = Field(
        ...,
        description="Type of label anomaly",
    )

    description: str = Field(
        ...,
        description="Detailed description of the anomaly",
    )

    severity: ViolationSeverity = Field(
        default=ViolationSeverity.MEDIUM,
        description="Severity of the anomaly",
    )

    fssai_requirement: Optional[str] = Field(
        default=None,
        description="FSSAI regulation requirement",
    )

    suggested_correction: Optional[str] = Field(
        default=None,
        description="How to correct the anomaly",
    )

    @property
    def is_critical(self) -> bool:
        """
        Returns True if anomaly is critical severity.
        """

        return self.severity == ViolationSeverity.CRITICAL

    @property
    def is_high_severity(self) -> bool:
        """
        Returns True if severity is high or critical.
        """

        return self.severity in [
            ViolationSeverity.CRITICAL,
            ViolationSeverity.HIGH,
        ]


# ==========================================================
# COUNTERFEIT MODELS
# ==========================================================


class CounterfeitIndicator(BaseModel):
    """
    Individual indicator of counterfeit product.

    This model represents a single piece of evidence suggesting
    the product may be counterfeit.
    """

    model_config = ConfigDict(extra="forbid")

    name: str = Field(
        ...,
        description="Name of the indicator",
    )

    description: str = Field(
        ...,
        description="Detailed description",
    )

    weight: float = Field(
        default=1.0,
        ge=0.0,
        le=10.0,
        description="Weight/importance of this indicator",
    )

    detected: bool = Field(
        default=False,
        description="Whether this indicator was detected",
    )


class CounterfeitDetection(BaseModel):
    """
    Counterfeit product detection result.

    This model aggregates all counterfeit indicators and provides
    a comprehensive risk assessment for counterfeit products.
    """

    model_config = ConfigDict(extra="forbid")

    is_counterfeit: bool = Field(
        default=False,
        description="Whether product is likely counterfeit",
    )

    risk_level: CounterfeitRiskLevel = Field(
        default=CounterfeitRiskLevel.NONE,
        description="Risk level of counterfeit",
    )

    risk_score: int = Field(
        default=0,
        ge=0,
        le=100,
        description="Numeric risk score (0-100)",
    )

    indicators: List[str] = Field(
        default_factory=list,
        description="Detected counterfeit indicators",
    )

    brand_mismatch: bool = Field(
        default=False,
        description="Brand information mismatch detected",
    )

    logo_anomaly: bool = Field(
        default=False,
        description="Logo anomaly detected",
    )

    price_anomaly: bool = Field(
        default=False,
        description="Price anomaly detected",
    )

    source_anomaly: bool = Field(
        default=False,
        description="Source/seller anomaly detected",
    )

    recommendations: List[str] = Field(
        default_factory=list,
        description="Recommended actions for consumer",
    )

    @property
    def is_high_risk(self) -> bool:
        """
        Returns True if risk level is high or critical.
        """

        return self.risk_level in [
            CounterfeitRiskLevel.HIGH,
            CounterfeitRiskLevel.CRITICAL,
        ]

    @property
    def summary(self) -> str:
        """
        Returns a one-line summary of counterfeit detection.
        """

        if not self.is_counterfeit:

            return "✅ No counterfeit indicators detected"

        if self.is_high_risk:

            return "🚨 HIGH RISK: Product appears counterfeit"

        return f"⚠️ Counterfeit risk detected: {len(self.indicators)} indicator(s)"


# ==========================================================
# AUTHENTICITY MODELS
# ==========================================================


class AuthenticityScore(BaseModel):
    """
    Overall authenticity score for a product.

    This model combines all trust metrics into a single authenticity
    score with grade and detailed component scores.
    """

    model_config = ConfigDict(extra="forbid")

    overall_score: int = Field(
        default=0,
        ge=0,
        le=100,
        description="Overall authenticity score (0-100)",
    )

    fssai_validity_score: int = Field(
        default=0,
        ge=0,
        le=100,
        description="Score based on FSSAI license validity",
    )

    label_format_score: int = Field(
        default=0,
        ge=0,
        le=100,
        description="Score based on label format compliance",
    )

    adulteration_risk_score: int = Field(
        default=0,
        ge=0,
        le=100,
        description="Score based on adulteration risk (lower is better)",
    )

    counterfeiting_risk_score: int = Field(
        default=0,
        ge=0,
        le=100,
        description="Score based on counterfeit risk (lower is better)",
    )

    claim_verification_score: int = Field(
        default=0,
        ge=0,
        le=100,
        description="Score based on claim verification results",
    )

    @property
    def is_authentic(self) -> bool:
        """
        Returns True if product is likely authentic.
        """

        return self.overall_score >= 70

    @property
    def is_high_risk(self) -> bool:
        """
        Returns True if product has high risk.
        """

        return self.overall_score < 40

    @property
    def grade(self) -> str:
        """
        Returns letter grade based on overall score.
        """

        if self.overall_score >= 95:

            return "A+"

        if self.overall_score >= 85:

            return "A"

        if self.overall_score >= 70:

            return "B"

        if self.overall_score >= 55:

            return "C"

        if self.overall_score >= 40:

            return "D"

        return "F"

    @property
    def grade_color(self) -> str:
        """
        Returns color code for the grade.
        """

        grade_colors = {

            "A+": "#1B5E20",

            "A": "#2ECC71",

            "B": "#27AE60",

            "C": "#F39C12",

            "D": "#E67E22",

            "F": "#E74C3C",

        }

        return grade_colors.get(self.grade, "#95A5A6")

    @property
    def recommendation(self) -> str:
        """
        Returns recommendation based on authenticity score.
        """

        if self.overall_score >= 85:

            return "Product appears authentic. Safe to consume."

        if self.overall_score >= 70:

            return "Product is likely authentic but has minor concerns."

        if self.overall_score >= 50:

            return "Exercise caution. Multiple authenticity concerns detected."

        return "HIGH RISK. Avoid purchasing this product."


# ==========================================================
# BRAND TRUST MODELS
# ==========================================================


class BrandTrustScore(BaseModel):
    """
    Trust score for a brand based on aggregated scan data.

    This model tracks brand performance over time based on
    user scans and detected violations.
    """

    model_config = ConfigDict(extra="forbid")

    brand_name: str = Field(
        ...,
        description="Name of the brand",
    )

    trust_score: int = Field(
        default=50,
        ge=0,
        le=100,
        description="Overall trust score (0-100)",
    )

    total_scans: int = Field(
        default=0,
        description="Total number of scans for this brand",
    )

    violation_count: int = Field(
        default=0,
        description="Total violations detected",
    )

    adulteration_count: int = Field(
        default=0,
        description="Adulteration incidents detected",
    )

    counterfeit_count: int = Field(
        default=0,
        description="Counterfeit products detected",
    )

    complaint_count: int = Field(
        default=0,
        description="Complaints filed against brand",
    )

    average_authenticity_score: float = Field(
        default=0.0,
        description="Average authenticity score across scans",
    )

    rank_in_category: Optional[int] = Field(
        default=None,
        description="Rank within product category",
    )

    percentile: Optional[float] = Field(
        default=None,
        description="Percentile in category",
    )

    last_assessed: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="Last assessment timestamp",
    )

    @property
    def trust_level(self) -> str:
        """
        Returns trust level based on score.
        """

        if self.trust_score >= 80:

            return "HIGH"

        if self.trust_score >= 60:

            return "MEDIUM"

        if self.trust_score >= 40:

            return "LOW"

        return "VERY_LOW"

    @property
    def trust_color(self) -> str:
        """
        Returns color code for trust level.
        """

        if self.trust_score >= 80:

            return "#2ECC71"

        if self.trust_score >= 60:

            return "#F39C12"

        if self.trust_score >= 40:

            return "#E67E22"

        return "#E74C3C"

    @property
    def recommendation(self) -> str:
        """
        Returns recommendation based on trust level.
        """

        if self.trust_score >= 80:

            return "Highly trustworthy brand. Products are generally authentic."

        if self.trust_score >= 60:

            return "Generally reliable brand. Occasional minor issues detected."

        if self.trust_score >= 40:

            return "Exercise caution with this brand. Multiple violations detected."

        return "Avoid this brand. High risk of adulteration and counterfeit products."

    @property
    def is_high_trust(self) -> bool:
        """
        Returns True if trust level is HIGH.
        """

        return self.trust_level == "HIGH"

    @property
    def is_low_trust(self) -> bool:
        """
        Returns True if trust level is LOW or VERY_LOW.
        """

        return self.trust_level in ["LOW", "VERY_LOW"]


# ==========================================================
# COMPLAINT MODELS
# ==========================================================


class Violation(BaseModel):
    """
    Detected FSSAI violation for complaint generation.

    This model represents a specific violation that can be included
    in an FSSAI complaint document.
    """

    model_config = ConfigDict(extra="forbid")

    violation_type: str = Field(
        ...,
        description="Type of violation",
    )

    title: str = Field(
        ...,
        description="Short title of the violation",
    )

    description: str = Field(
        ...,
        description="Detailed description of the violation",
    )

    regulation_act: Optional[str] = Field(
        default=None,
        description="FSSAI Act reference",
    )

    regulation_section: Optional[str] = Field(
        default=None,
        description="Section number",
    )

    regulation_clause: Optional[str] = Field(
        default=None,
        description="Specific clause",
    )

    penalty_amount: Optional[int] = Field(
        default=None,
        description="Maximum penalty in rupees",
    )

    severity: ViolationSeverity = Field(
        default=ViolationSeverity.MEDIUM,
        description="Severity of violation",
    )

    evidence: Dict[str, Any] = Field(
        default_factory=dict,
        description="Evidence supporting this violation",
    )

    @property
    def formatted_regulation(self) -> str:
        """
        Returns formatted regulation reference.
        """

        parts = []

        if self.regulation_act:

            parts.append(self.regulation_act)

        if self.regulation_section:

            parts.append(f"Section {self.regulation_section}")

        if self.regulation_clause:

            parts.append(f"Clause {self.regulation_clause}")

        return " - ".join(parts)


class ComplaintRequest(BaseModel):
    """
    Request model for generating FSSAI complaint.

    This model contains all information needed to generate
    a formal FSSAI complaint PDF document.
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

    violations: List[Violation] = Field(
        default_factory=list,
        description="List of violations detected",
    )

    consumer_name: str = Field(
        default="Consumer",
        max_length=100,
        description="Name of the complainant",
    )

    consumer_email: str = Field(
        default="",
        max_length=100,
        description="Email address",
    )

    consumer_phone: str = Field(
        default="",
        max_length=15,
        description="Phone number",
    )

    consumer_address: str = Field(
        default="",
        max_length=500,
        description="Complete address",
    )

    additional_notes: str = Field(
        default="",
        max_length=2000,
        description="Additional observations",
    )

    include_scan_image: bool = Field(
        default=False,
        description="Include scanned label image as evidence",
    )

    scan_image_base64: Optional[str] = Field(
        default=None,
        description="Base64 encoded scan image",
    )

    @property
    def has_valid_consumer_info(self) -> bool:
        """
        Returns True if consumer has provided contact info.
        """

        return bool(self.consumer_name and self.consumer_email)


class ComplaintResponse(BaseModel):
    """
    Response from complaint generation.

    This model contains the generated complaint data including
    PDF download link and submission instructions.
    """

    model_config = ConfigDict(extra="forbid")

    success: bool = True

    complaint_id: str = Field(
        ...,
        description="Unique complaint identifier",
    )

    generated_at: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="Generation timestamp",
    )

    violations_count: int = Field(
        ...,
        description="Number of violations included",
    )

    severity_summary: Dict[str, int] = Field(
        ...,
        description="Counts by severity level",
    )

    pdf_size_bytes: int = Field(
        ...,
        description="PDF file size in bytes",
    )

    qr_code_size_bytes: int = Field(
        ...,
        description="QR code image size in bytes",
    )

    submission_portal_url: str = Field(
        default="https://pgportal.gov.in/",
        description="PG Portal submission URL",
    )

    submission_text: str = Field(
        ...,
        description="Formatted submission text",
    )

    instructions: List[str] = Field(
        default_factory=list,
        description="Submission instructions",
    )


# ==========================================================
# TRUST INTELLIGENCE REQUEST/RESPONSE
# ==========================================================


class TrustIntelligenceRequest(BaseModel):
    """
    Request model for trust intelligence analysis.

    This model accepts all product data needed to perform
    comprehensive trust analysis.
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

    image_url: Optional[str] = Field(
        default=None,
        description="URL of scanned product image",
    )

    barcode: Optional[str] = Field(
        default=None,
        description="Product barcode",
    )

    @property
    def has_complete_data(self) -> bool:
        """
        Returns True if all required data is present.
        """

        return bool(
            self.product_name
            and self.brand
            and self.nutrition_data
        )


class TrustIntelligenceResponse(BaseModel):
    """
    Complete response from trust intelligence system.

    This model aggregates all analysis results into a single
    comprehensive response.
    """

    model_config = ConfigDict(extra="forbid")

    success: bool = True

    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="Response timestamp",
    )

    processing_time_ms: int = Field(
        default=0,
        description="Processing time in milliseconds",
    )

    fssai_validation: Optional[FSSAILicenseInfo] = Field(
        default=None,
        description="FSSAI license validation result",
    )

    is_fssai_valid: bool = Field(
        default=False,
        description="Whether FSSAI license is valid",
    )

    claim_verifications: List[ClaimVerificationResult] = Field(
        default_factory=list,
        description="Results of claim verification",
    )

    contradictions: List[Contradiction] = Field(
        default_factory=list,
        description="Detected contradictions",
    )

    has_contradictions: bool = Field(
        default=False,
        description="Whether any contradictions were found",
    )

    adulteration_detection: Optional[AdulterationDetection] = Field(
        default=None,
        description="Adulteration detection results",
    )

    label_anomalies: List[LabelAnomaly] = Field(
        default_factory=list,
        description="Detected label anomalies",
    )

    counterfeit_detection: Optional[CounterfeitDetection] = Field(
        default=None,
        description="Counterfeit detection results",
    )

    authenticity_score: Optional[AuthenticityScore] = Field(
        default=None,
        description="Overall authenticity score",
    )

    brand_trust: Optional[BrandTrustScore] = Field(
        default=None,
        description="Brand trust score",
    )

    overall_trust_score: int = Field(
        default=0,
        ge=0,
        le=100,
        description="Overall trust score (0-100)",
    )

    overall_trust_level: str = Field(
        default="UNKNOWN",
        description="Overall trust level",
    )

    warnings: List[str] = Field(
        default_factory=list,
        description="Important warnings for consumer",
    )

    recommendations: List[str] = Field(
        default_factory=list,
        description="Recommended actions",
    )

    @property
    def is_trustworthy(self) -> bool:
        """
        Returns True if product is considered trustworthy.
        """

        return self.overall_trust_score >= 60

    @property
    def is_high_risk(self) -> bool:
        """
        Returns True if product has high risk.
        """

        return self.overall_trust_score < 40


# ==========================================================
# ADULTERATION PATTERNS DATABASE
# ==========================================================


ADULTERATION_PATTERNS: Dict[str, List[Dict[str, Any]]] = {

    "chilli_powder": [

        {

            "adulterant": "Sudan Red I/II",

            "type": AdulterationType.COLOR_ADDITIVE,

            "detection": "E-number scan detects illegal synthetic colors",

            "health_risk": "Carcinogenic - banned by FSSAI",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

        {

            "adulterant": "Brick Dust",

            "type": AdulterationType.EXTENDER,

            "detection": "High ash content, gritty texture",

            "health_risk": "Silica particles damage digestive tract",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

        {

            "adulterant": "Metanil Yellow",

            "type": AdulterationType.COLOR_ADDITIVE,

            "detection": "Non-permitted color detected",

            "health_risk": "Neurotoxic, causes stomach disorders",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

        {

            "adulterant": "Rice Flour",

            "type": AdulterationType.EXTENDER,

            "detection": "Starch test positive",

            "health_risk": "Reduced nutritional value",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

    ],

    "turmeric_powder": [

        {

            "adulterant": "Metanil Yellow",

            "type": AdulterationType.COLOR_ADDITIVE,

            "detection": "Artificial color detected",

            "health_risk": "Neurotoxic, banned for food use",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

        {

            "adulterant": "Lead Chromate",

            "type": AdulterationType.TOXIC_ADDITIVE,

            "detection": "High lead content detected",

            "health_risk": "Lead poisoning, kidney damage",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

        {

            "adulterant": "Starch",

            "type": AdulterationType.EXTENDER,

            "detection": "Iodine test positive for starch",

            "health_risk": "Reduced nutritional value",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

        {

            "adulterant": "Yellow Clay",

            "type": AdulterationType.EXTENDER,

            "detection": "High insoluble ash content",

            "health_risk": "Digestive issues",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

    ],

    "milk": [

        {

            "adulterant": "Water",

            "type": AdulterationType.EXTENDER,

            "detection": "Low SNF, low specific gravity",

            "health_risk": "Reduced nutritional value",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

        {

            "adulterant": "Detergent",

            "type": AdulterationType.CONTAMINANT,

            "detection": "Foaming test positive",

            "health_risk": "Gastrointestinal issues, diarrhea",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

        {

            "adulterant": "Urea",

            "type": AdulterationType.CONTAMINANT,

            "detection": "High nitrogen content",

            "health_risk": "Kidney damage, digestive issues",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

        {

            "adulterant": "Starch",

            "type": AdulterationType.EXTENDER,

            "detection": "Iodine test positive",

            "health_risk": "Reduced nutritional value",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

        {

            "adulterant": "Synthetic Milk",

            "type": AdulterationType.SUBSTITUTION,

            "detection": "Low protein, presence of urea",

            "health_risk": "Severe health issues",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

    ],

    "honey": [

        {

            "adulterant": "Sugar Syrup",

            "type": AdulterationType.EXTENDER,

            "detection": "Low C4 sugar content, high fructose/glucose ratio",

            "health_risk": "Reduced medicinal properties, diabetes risk",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

        {

            "adulterant": "Jaggery Syrup",

            "type": AdulterationType.SUBSTITUTION,

            "detection": "Non-permitted sugar detected",

            "health_risk": "No nutritional benefits of real honey",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

        {

            "adulterant": "Corn Syrup",

            "type": AdulterationType.EXTENDER,

            "detection": "High fructose content",

            "health_risk": "Increased diabetes risk",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

    ],

    "ghee": [

        {

            "adulterant": "Vegetable Oil",

            "type": AdulterationType.SUBSTITUTION,

            "detection": "Low butyric acid, presence of plant sterols",

            "health_risk": "Trans fats, reduced nutritional value",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

        {

            "adulterant": "Vanaspati",

            "type": AdulterationType.SUBSTITUTION,

            "detection": "Presence of trans fats, higher melting point",

            "health_risk": "Heart disease, cholesterol issues",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

        {

            "adulterant": "Animal Fat",

            "type": AdulterationType.SUBSTITUTION,

            "detection": "Fatty acid profile mismatch",

            "health_risk": "Religious/ethical concerns, health risks",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

    ],

    "paneer": [

        {

            "adulterant": "Starch",

            "type": AdulterationType.EXTENDER,

            "detection": "Iodine test positive",

            "health_risk": "Reduced protein content",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

        {

            "adulterant": "Urea",

            "type": AdulterationType.CONTAMINANT,

            "detection": "High nitrogen content",

            "health_risk": "Kidney damage",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

        {

            "adulterant": "Palm Oil",

            "type": AdulterationType.SUBSTITUTION,

            "detection": "Fatty acid profile mismatch",

            "health_risk": "Increased saturated fat",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

    ],

    "coffee_powder": [

        {

            "adulterant": "Chicory",

            "type": AdulterationType.EXTENDER,

            "detection": "Low caffeine content, presence of inulin",

            "health_risk": "Reduced caffeine content, different taste",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

        {

            "adulterant": "Tamarind Seeds",

            "type": AdulterationType.SUBSTITUTION,

            "detection": "Microscopic examination",

            "health_risk": "No health benefits of real coffee",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

        {

            "adulterant": "Roasted Gram",

            "type": AdulterationType.EXTENDER,

            "detection": "Microscopic examination",

            "health_risk": "Reduced caffeine content",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

    ],

    "olive_oil": [

        {

            "adulterant": "Cheaper Vegetable Oils",

            "type": AdulterationType.SUBSTITUTION,

            "detection": "Fatty acid profile mismatch",

            "health_risk": "Loss of olive oil health benefits",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

        {

            "adulterant": "Palm Oil",

            "type": AdulterationType.SUBSTITUTION,

            "detection": "High saturated fat content",

            "health_risk": "Increased cholesterol risk",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

    ],

    "juice": [

        {

            "adulterant": "Sugar Syrup",

            "type": AdulterationType.EXTENDER,

            "detection": "Low fruit content, high sugar",

            "health_risk": "Diabetes risk, empty calories",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

        {

            "adulterant": "Synthetic Colors",

            "type": AdulterationType.COLOR_ADDITIVE,

            "detection": "Artificial colors detected",

            "health_risk": "Allergic reactions, hyperactivity in children",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

        {

            "adulterant": "Water",

            "type": AdulterationType.EXTENDER,

            "detection": "Low Brix value",

            "health_risk": "Reduced nutritional value",

            "reporting": "FSSAI consumer helpline 1800-11-4000",

        },

    ],

}


# ==========================================================
# COUNTERFEIT INDICATORS DATABASE
# ==========================================================


COUNTERFEIT_INDICATORS: Dict[str, List[Dict[str, Any]]] = {

    "fssai_mismatch": [

        {

            "indicator": "FSSAI license number format appears invalid",

            "weight": 8.0,

            "description": "The 14-digit FSSAI number does not follow standard format",

        },

        {

            "indicator": "FSSAI license not registered for this product category",

            "weight": 10.0,

            "description": "License exists but not for this type of product",

        },

        {

            "indicator": "FSSAI license expired or suspended",

            "weight": 9.0,

            "description": "License is not active/valid",

        },

    ],

    "logo_anomaly": [

        {

            "indicator": "Brand logo size/position differs from standard",

            "weight": 7.0,

            "description": "Logo placement does not match official brand guidelines",

        },

        {

            "indicator": "Logo quality appears pixelated or distorted",

            "weight": 8.0,

            "description": "Poor quality logo indicates counterfeit printing",

        },

        {

            "indicator": "Missing registered trademark symbol",

            "weight": 5.0,

            "description": "® or ™ symbol missing from brand name",

        },

        {

            "indicator": "FSSAI logo format incorrect",

            "weight": 9.0,

            "description": "Official FSSAI logo not displayed correctly",

        },

    ],

    "label_anomaly": [

        {

            "indicator": "Vegetarian/Non-vegetarian symbol format incorrect",

            "weight": 7.0,

            "description": "Green/Brown dot not as per FSSAI specifications",

        },

        {

            "indicator": "Font inconsistencies across label",

            "weight": 6.0,

            "description": "Different fonts used indicating tampering",

        },

        {

            "indicator": "Missing mandatory information fields",

            "weight": 8.0,

            "description": "Required information not present on label",

        },

        {

            "indicator": "Batch number format inconsistent",

            "weight": 6.0,

            "description": "Batch/lot number format differs from brand standard",

        },

    ],

    "price_anomaly": [

        {

            "indicator": "Price significantly lower than market average",

            "weight": 7.0,

            "description": "Unusually low price indicates counterfeit",

        },

        {

            "indicator": "Price too high for reported MRP",

            "weight": 5.0,

            "description": "Price exceeds MRP significantly",

        },

        {

            "indicator": "Unusually large discount without reason",

            "weight": 6.0,

            "description": "Deep discount suggests counterfeit",

        },

    ],

    "source_anomaly": [

        {

            "indicator": "Unknown or suspicious seller",

            "weight": 8.0,

            "description": "Seller not authorized by brand",

        },

        {

            "indicator": "Multiple sellers with same product at varying prices",

            "weight": 5.0,

            "description": "Inconsistent pricing across sellers",

        },

        {

            "indicator": "Product not available on official channels",

            "weight": 7.0,

            "description": "Product missing from brand's official website",

        },

    ],

}


# ==========================================================
# FSSAI REGULATIONS DATABASE
# ==========================================================


class FSSAIRegulation(BaseModel):
    """
    FSSAI regulation clause with complete legal details.
    """

    model_config = ConfigDict(extra="forbid")

    act: str

    section: str

    regulation: str

    clause: Optional[str] = None

    sub_clause: Optional[str] = None

    title: str

    description: str

    penalty_amount: Optional[int] = None

    penalty_description: Optional[str] = None

    severity: ViolationSeverity = ViolationSeverity.MEDIUM


FSSAI_REGULATIONS: Dict[str, FSSAIRegulation] = {

    "missing_fssai": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="31",

        regulation="Food Safety and Standards (Licensing and Registration of Food Businesses) Regulations, 2011",

        clause="3.1",

        title="Missing FSSAI License Number",

        description="Food product does not display mandatory FSSAI license number on packaging.",

        penalty_amount=500000,

        penalty_description="Penalty up to ₹5,00,000 under Section 53",

        severity=ViolationSeverity.HIGH,

    ),

    "invalid_fssai": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="31",

        regulation="Food Safety and Standards (Licensing and Registration of Food Businesses) Regulations, 2011",

        clause="3.2",

        title="Invalid FSSAI License Number",

        description="Displayed FSSAI license number is invalid or does not match registered business.",

        penalty_amount=500000,

        penalty_description="Penalty up to ₹5,00,000 under Section 53",

        severity=ViolationSeverity.CRITICAL,

    ),

    "adulteration": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="26",

        regulation="Food Safety and Standards (Prohibition and Restrictions on Sales) Regulations, 2011",

        clause="Regulation 2.1",

        title="Food Adulteration",

        description="Product contains adulterants not permitted under FSSAI standards.",

        penalty_amount=500000,

        penalty_description="Penalty up to ₹5,00,000 under Section 53",

        severity=ViolationSeverity.CRITICAL,

    ),

    "misleading_claim": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="24",

        regulation="Food Safety and Standards (Advertising and Claims) Regulations, 2018",

        clause="Regulation 3.1",

        title="Misleading Claim",

        description="Product makes misleading or false claims not supported by nutritional facts.",

        penalty_amount=250000,

        penalty_description="Penalty under Section 52 for misleading advertisement",

        severity=ViolationSeverity.HIGH,

    ),

    "label_violation": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="23",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Regulation 2.1",

        title="Labelling Violation",

        description="Product label does not comply with mandatory labelling requirements.",

        penalty_amount=100000,

        penalty_description="Penalty for non-compliance with labelling regulations",

        severity=ViolationSeverity.MEDIUM,

    ),

    "counterfeit": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="52",

        regulation="Food Safety and Standards (Offences and Penalties) Regulations, 2011",

        clause="3.1",

        title="Counterfeit Product",

        description="Product appears to be counterfeit or tampered.",

        penalty_amount=500000,

        penalty_description="Penalty up to ₹5,00,000 under Section 52",

        severity=ViolationSeverity.CRITICAL,

    ),

    "vegetarian_symbol_missing": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="23",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Regulation 2.5.1",

        title="Missing Vegetarian/Non-Vegetarian Symbol",

        description="Product does not display mandatory green or brown circle symbol.",

        penalty_amount=100000,

        penalty_description="Penalty for labelling non-compliance",

        severity=ViolationSeverity.MEDIUM,

    ),

    "ingredients_list_missing": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="23",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Regulation 2.2.1",

        title="Missing Ingredients List",

        description="Product packaging does not display mandatory ingredients list.",

        penalty_amount=100000,

        penalty_description="Penalty for labelling non-compliance",

        severity=ViolationSeverity.MEDIUM,

    ),

    "nutrition_table_missing": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="23",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Regulation 2.3.1",

        title="Missing Nutrition Information",

        description="Product packaging does not display mandatory nutrition information.",

        penalty_amount=100000,

        penalty_description="Penalty for labelling non-compliance",

        severity=ViolationSeverity.MEDIUM,

    ),

    "expired_product": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="26",

        regulation="Food Safety and Standards (Prohibition and Restrictions on Sales) Regulations, 2011",

        clause="Regulation 2.1",

        title="Sale of Expired Product",

        description="Product being sold past its expiry date.",

        penalty_amount=500000,

        penalty_description="Penalty up to ₹5,00,000 under Section 53",

        severity=ViolationSeverity.CRITICAL,

    ),

}


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [

    "SYSTEM_8_VERSION",
    "SYSTEM_8_BUILD_DATE",
    "SYSTEM_8_API_VERSION",

    "FSSAILicenseStatus",
    "LicenseCategory",
    "BusinessType",
    "ClaimVerificationStatus",
    "ViolationSeverity",
    "AdulterationType",
    "AdulterationRiskLevel",
    "LabelAnomalyType",
    "CounterfeitRiskLevel",
    "ComplaintStatus",
    "ComplaintType",
    "AuthenticityGrade",
    "TrustLevel",

    "FSSAILicenseInfo",
    "ClaimVerificationResult",
    "Contradiction",
    "Adulterant",
    "AdulterationDetection",
    "LabelAnomaly",
    "CounterfeitIndicator",
    "CounterfeitDetection",
    "AuthenticityScore",
    "BrandTrustScore",
    "Violation",
    "ComplaintRequest",
    "ComplaintResponse",
    "TrustIntelligenceRequest",
    "TrustIntelligenceResponse",

    "ADULTERATION_PATTERNS",
    "COUNTERFEIT_INDICATORS",
    "FSSAIRegulation",
    "FSSAI_REGULATIONS",

]


# ==========================================================
# END OF FILE - trust_models.py
# TOTAL LINES: 2,550 (VERIFIED)
# ==========================================================