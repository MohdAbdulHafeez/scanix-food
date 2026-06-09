# ==========================================================
# SCANIX AI
# SYSTEM 9 – USER INTELLIGENCE MODELS
# ELITE PRODUCTION GRADE – FINAL VERSION
# TOTAL LINES: 650
# ==========================================================


from __future__ import annotations


from datetime import datetime
from datetime import date
from typing import Optional
from typing import List
from typing import Dict
from typing import Any
from enum import Enum


from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import EmailStr
from pydantic import field_validator


# ==========================================================
# ENUMS – HEALTH CONDITIONS
# ==========================================================


class HealthCondition(str, Enum):
    """
    Health conditions that affect food recommendations.
    """

    DIABETES = "diabetes"
    HYPERTENSION = "hypertension"
    HEART_DISEASE = "heart_disease"
    KIDNEY_DISEASE = "kidney_disease"
    CELIAC = "celiac"
    LACTOSE_INTOLERANT = "lactose_intolerant"
    OBESITY = "obesity"
    THYROID = "thyroid"
    PCOS = "pcos"
    GOUT = "gout"
    ANEMIA = "anemia"
    PREGNANCY = "pregnancy"


class Medication(str, Enum):
    """
    Medications with known food interactions.
    """

    WARFARIN = "warfarin"
    STATIN = "statin"
    METFORMIN = "metformin"
    INSULIN = "insulin"
    LISINOPRIL = "lisinopril"
    ASPIRIN = "aspirin"
    LEVOTHYROXINE = "levothyroxine"
    FUROSEMIDE = "furosemide"
    PREDNISONE = "prednisone"
    IBUPROFEN = "ibuprofen"


class Allergy(str, Enum):
    """
    Common food allergies.
    """

    PEANUTS = "peanuts"
    TREE_NUTS = "tree_nuts"
    MILK = "milk"
    EGGS = "eggs"
    WHEAT = "wheat"
    SOY = "soy"
    FISH = "fish"
    SHELLFISH = "shellfish"
    GLUTEN = "gluten"
    LACTOSE = "lactose"
    SESAME = "sesame"
    MUSTARD = "mustard"
    SULPHITES = "sulphites"


# ==========================================================
# USER MODELS
# ==========================================================


class User(BaseModel):
    """
    User account information.
    """

    model_config = ConfigDict(extra="forbid")

    id: str = Field(
        ...,
        description="Unique user identifier",
    )

    email: EmailStr = Field(
        ...,
        description="User's email address",
    )

    name: Optional[str] = Field(
        default=None,
        description="User's full name",
    )

    picture: Optional[str] = Field(
        default=None,
        description="Profile picture URL",
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Account creation timestamp",
    )

    last_login: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last login timestamp",
    )


class UserCreate(BaseModel):
    """
    Request model for creating a new user.
    """

    model_config = ConfigDict(extra="forbid")

    email: EmailStr = Field(
        ...,
        description="User's email address",
    )

    name: Optional[str] = Field(
        default=None,
        description="User's full name",
    )

    picture: Optional[str] = Field(
        default=None,
        description="Profile picture URL",
    )

    gmail_id: str = Field(
        ...,
        description="Google OAuth user ID",
    )


# ==========================================================
# HEALTH PROFILE MODELS
# ==========================================================


class HealthProfile(BaseModel):
    """
    User's complete health profile for personalization.
    """

    model_config = ConfigDict(extra="forbid")

    id: str = Field(
        ...,
        description="Unique profile identifier",
    )

    user_id: str = Field(
        ...,
        description="Associated user ID",
    )

    age: Optional[int] = Field(
        default=None,
        ge=0,
        le=120,
        description="Age in years",
    )

    gender: Optional[str] = Field(
        default=None,
        description="Gender identity",
    )

    weight_kg: Optional[float] = Field(
        default=None,
        ge=0,
        le=500,
        description="Weight in kilograms",
    )

    height_cm: Optional[float] = Field(
        default=None,
        ge=0,
        le=300,
        description="Height in centimeters",
    )

    conditions: List[HealthCondition] = Field(
        default_factory=list,
        description="Medical conditions",
    )

    medications: List[Medication] = Field(
        default_factory=list,
        description="Current medications",
    )

    allergies: List[Allergy] = Field(
        default_factory=list,
        description="Food allergies",
    )

    dietary_preferences: List[str] = Field(
        default_factory=list,
        description="Dietary preferences (vegetarian, vegan, etc.)",
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Profile creation timestamp",
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp",
    )

    @property
    def bmi(self) -> Optional[float]:
        """
        Calculate Body Mass Index.
        """

        if self.weight_kg and self.height_cm:

            height_m = self.height_cm / 100

            return round(
                self.weight_kg / (height_m ** 2),
                1,
            )

        return None

    @property
    def bmi_category(self) -> Optional[str]:
        """
        Get BMI category.
        """

        bmi = self.bmi

        if bmi is None:

            return None

        if bmi < 18.5:

            return "UNDERWEIGHT"

        if bmi < 25:

            return "NORMAL"

        if bmi < 30:

            return "OVERWEIGHT"

        return "OBESE"


class HealthProfileUpdate(BaseModel):
    """
    Request model for updating health profile.
    """

    model_config = ConfigDict(extra="forbid")

    age: Optional[int] = Field(
        default=None,
        ge=0,
        le=120,
        description="Age in years",
    )

    gender: Optional[str] = Field(
        default=None,
        description="Gender identity",
    )

    weight_kg: Optional[float] = Field(
        default=None,
        ge=0,
        le=500,
        description="Weight in kilograms",
    )

    height_cm: Optional[float] = Field(
        default=None,
        ge=0,
        le=300,
        description="Height in centimeters",
    )

    conditions: Optional[List[HealthCondition]] = Field(
        default=None,
        description="Medical conditions",
    )

    medications: Optional[List[Medication]] = Field(
        default=None,
        description="Current medications",
    )

    allergies: Optional[List[Allergy]] = Field(
        default=None,
        description="Food allergies",
    )

    dietary_preferences: Optional[List[str]] = Field(
        default=None,
        description="Dietary preferences",
    )


# ==========================================================
# USER SCAN MODELS
# ==========================================================


class UserScan(BaseModel):
    """
    Record of a single product scan by a user.
    """

    model_config = ConfigDict(extra="forbid")

    id: str = Field(
        ...,
        description="Unique scan record ID",
    )

    user_id: str = Field(
        ...,
        description="Associated user ID",
    )

    scan_id: str = Field(
        ...,
        description="Original scan ID from System 1",
    )

    product_name: str = Field(
        ...,
        description="Name of the scanned product",
    )

    brand: Optional[str] = Field(
        default=None,
        description="Product brand",
    )

    barcode: Optional[str] = Field(
        default=None,
        description="Product barcode",
    )

    health_score: int = Field(
        default=0,
        ge=0,
        le=100,
        description="Overall health score (0-100)",
    )

    sugar_score: float = Field(
        default=0,
        description="Sugar content in grams",
    )

    sodium_score: float = Field(
        default=0,
        description="Sodium content in mg",
    )

    fat_score: float = Field(
        default=0,
        description="Saturated fat content in grams",
    )

    nova_group: int = Field(
        default=4,
        ge=1,
        le=4,
        description="NOVA processing group",
    )

    processing_level: str = Field(
        default="UNKNOWN",
        description="Processing level",
    )

    deception_score: int = Field(
        default=0,
        ge=0,
        le=100,
        description="Deception score (0-100)",
    )

    adulteration_risk: str = Field(
        default="NONE",
        description="Adulteration risk level",
    )

    counterfeit_risk: str = Field(
        default="NONE",
        description="Counterfeit risk level",
    )

    trust_score: int = Field(
        default=0,
        ge=0,
        le=100,
        description="Trust score (0-100)",
    )

    scan_data: Dict[str, Any] = Field(
        default_factory=dict,
        description="Complete scan data from System 1",
    )

    scanned_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the scan occurred",
    )


class ScanHistoryResponse(BaseModel):
    """
    Response model for scan history endpoint.
    """

    model_config = ConfigDict(extra="forbid")

    total_scans: int = Field(
        ...,
        description="Total number of scans",
    )

    scans: List[UserScan] = Field(
        default_factory=list,
        description="List of scans",
    )

    has_more: bool = Field(
        default=False,
        description="Whether more scans exist",
    )


# ==========================================================
# DASHBOARD MODELS
# ==========================================================


class WeeklyTrend(BaseModel):
    """
    Weekly health score trend for dashboard.
    """

    model_config = ConfigDict(extra="forbid")

    week_start: date = Field(
        ...,
        description="Start date of the week",
    )

    average_health_score: float = Field(
        ...,
        description="Average health score for the week",
    )

    total_scans: int = Field(
        ...,
        description="Number of scans in the week",
    )

    top_risk: Optional[str] = Field(
        default=None,
        description="Most common risk detected",
    )


class DashboardResponse(BaseModel):
    """
    Complete dashboard response for a user.
    """

    model_config = ConfigDict(extra="forbid")

    user: User = Field(
        ...,
        description="User information",
    )

    health_profile: Optional[HealthProfile] = Field(
        default=None,
        description="User's health profile",
    )

    total_scans: int = Field(
        default=0,
        description="Total number of scans",
    )

    average_health_score: float = Field(
        default=0,
        description="Average health score across all scans",
    )

    average_trust_score: float = Field(
        default=0,
        description="Average trust score across all scans",
    )

    high_risk_products_count: int = Field(
        default=0,
        description="Number of high-risk products scanned",
    )

    adulteration_detected_count: int = Field(
        default=0,
        description="Number of adulteration detections",
    )

    misleading_claims_count: int = Field(
        default=0,
        description="Number of misleading claim detections",
    )

    recent_scans: List[UserScan] = Field(
        default_factory=list,
        description="Most recent scans",
    )

    weekly_trends: List[WeeklyTrend] = Field(
        default_factory=list,
        description="Weekly health score trends",
    )

    top_flagged_products: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Most frequently flagged products",
    )

    recommendations: List[str] = Field(
        default_factory=list,
        description="Personalized recommendations",
    )

    quick_actions: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Quick action buttons",
    )


# ==========================================================
# ANALYTICS MODELS
# ==========================================================


class EatingPattern(BaseModel):
    """
    Analysis of user's eating patterns.
    """

    model_config = ConfigDict(extra="forbid")

    most_scanned_categories: List[Dict[str, int]] = Field(
        default_factory=list,
        description="Most scanned product categories",
    )

    most_scanned_brands: List[Dict[str, int]] = Field(
        default_factory=list,
        description="Most scanned brands",
    )

    average_nova_group: float = Field(
        default=0,
        description="Average NOVA group across scans",
    )

    processing_distribution: Dict[str, int] = Field(
        default_factory=dict,
        description="Distribution of processing levels",
    )


class SugarTrend(BaseModel):
    """
    Trend analysis for a specific nutrient.
    """

    model_config = ConfigDict(extra="forbid")

    dates: List[str] = Field(
        default_factory=list,
        description="Dates for the trend line",
    )

    values: List[float] = Field(
        default_factory=list,
        description="Values for the trend line",
    )

    average: float = Field(
        default=0,
        description="Average value",
    )

    trend_direction: str = Field(
        default="stable",
        description="Direction of trend (improving/worsening/stable)",
    )


class NOVADistribution(BaseModel):
    """
    Distribution of NOVA processing groups.
    """

    model_config = ConfigDict(extra="forbid")

    unprocessed: int = Field(
        default=0,
        description="NOVA 1 count",
    )

    minimally_processed: int = Field(
        default=0,
        description="NOVA 2 count",
    )

    processed: int = Field(
        default=0,
        description="NOVA 3 count",
    )

    ultra_processed: int = Field(
        default=0,
        description="NOVA 4 count",
    )


class AnalyticsResponse(BaseModel):
    """
    Complete analytics response for a user.
    """

    model_config = ConfigDict(extra="forbid")

    eating_patterns: EatingPattern = Field(
        ...,
        description="Eating pattern analysis",
    )

    sugar_trend: SugarTrend = Field(
        ...,
        description="Sugar consumption trend",
    )

    sodium_trend: SugarTrend = Field(
        ...,
        description="Sodium consumption trend",
    )

    nova_distribution: NOVADistribution = Field(
        ...,
        description="NOVA group distribution",
    )

    health_score_trend: SugarTrend = Field(
        ...,
        description="Health score trend",
    )

    risk_trend: Dict[str, List[int]] = Field(
        default_factory=dict,
        description="Risk trends over time",
    )

    top_health_concerns: List[str] = Field(
        default_factory=list,
        description="Top health concerns",
    )

    lifestyle_insights: List[str] = Field(
        default_factory=list,
        description="Lifestyle insights",
    )


# ==========================================================
# ALLERGY CHECK MODELS
# ==========================================================


class AllergyCheckRequest(BaseModel):
    """
    Request model for allergy checking.
    """

    model_config = ConfigDict(extra="forbid")

    product_name: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Name of the product",
    )

    ingredients: List[str] = Field(
        ...,
        description="List of ingredients",
    )

    scan_id: Optional[str] = Field(
        default=None,
        description="Associated scan ID",
    )


class AllergyCheckResponse(BaseModel):
    """
    Response model for allergy checking.
    """

    model_config = ConfigDict(extra="forbid")

    has_allergens: bool = Field(
        default=False,
        description="Whether allergens were found",
    )

    matched_allergens: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Matched allergens with details",
    )

    severity: str = Field(
        default="NONE",
        description="Severity level (HIGH/MEDIUM/LOW/NONE)",
    )

    recommendation: str = Field(
        default="",
        description="Recommended action",
    )

    safe_alternatives: List[str] = Field(
        default_factory=list,
        description="Safe alternative products",
    )


# ==========================================================
# MEDICATION CHECK MODELS
# ==========================================================


class MedicationInteraction(BaseModel):
    """
    Individual drug-food interaction.
    """

    model_config = ConfigDict(extra="forbid")

    medication: str = Field(
        ...,
        description="Name of the medication",
    )

    ingredient: str = Field(
        ...,
        description="Interacting ingredient",
    )

    risk_level: str = Field(
        ...,
        description="Risk level (HIGH/MODERATE/LOW)",
    )

    description: str = Field(
        ...,
        description="Description of the interaction",
    )

    recommendation: str = Field(
        ...,
        description="Recommended action",
    )


class MedicationCheckRequest(BaseModel):
    """
    Request model for medication checking.
    """

    model_config = ConfigDict(extra="forbid")

    product_name: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Name of the product",
    )

    ingredients: List[str] = Field(
        ...,
        description="List of ingredients",
    )

    nutrients: Dict[str, float] = Field(
        default_factory=dict,
        description="Nutritional information",
    )

    scan_id: Optional[str] = Field(
        default=None,
        description="Associated scan ID",
    )


class MedicationCheckResponse(BaseModel):
    """
    Response model for medication checking.
    """

    model_config = ConfigDict(extra="forbid")

    has_interactions: bool = Field(
        default=False,
        description="Whether interactions were found",
    )

    interactions: List[MedicationInteraction] = Field(
        default_factory=list,
        description="List of interactions",
    )

    overall_risk: str = Field(
        default="NONE",
        description="Overall risk level",
    )

    recommendation: str = Field(
        default="",
        description="Recommended action",
    )


# ==========================================================
# HEALTH MEMORY MODELS
# ==========================================================


class HealthMemoryResponse(BaseModel):
    """
    Long-term health memory and insights.
    """

    model_config = ConfigDict(extra="forbid")

    user_id: str = Field(
        ...,
        description="User identifier",
    )

    total_lifetime_scans: int = Field(
        default=0,
        description="Total scans in user's history",
    )

    first_scan_date: Optional[datetime] = Field(
        default=None,
        description="Date of first scan",
    )

    last_scan_date: Optional[datetime] = Field(
        default=None,
        description="Date of most recent scan",
    )

    health_score_timeline: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Health score over time",
    )

    risk_timeline: Dict[str, List[Dict[str, Any]]] = Field(
        default_factory=dict,
        description="Risks over time",
    )

    improved_areas: List[str] = Field(
        default_factory=list,
        description="Areas showing improvement",
    )

    concerning_areas: List[str] = Field(
        default_factory=list,
        description="Areas needing attention",
    )

    lifestyle_insights: List[str] = Field(
        default_factory=list,
        description="Lifestyle insights",
    )

    personalized_goals: List[str] = Field(
        default_factory=list,
        description="Personalized health goals",
    )


# ==========================================================
# USER PREFERENCES MODELS
# ==========================================================


class UserPreferences(BaseModel):
    """
    User preferences for personalized experience.
    """

    model_config = ConfigDict(extra="forbid")

    favorite_brands: List[str] = Field(
        default_factory=list,
        description="User's favorite brands",
    )

    avoided_ingredients: List[str] = Field(
        default_factory=list,
        description="Ingredients the user avoids",
    )

    preferred_categories: List[str] = Field(
        default_factory=list,
        description="Preferred product categories",
    )

    price_sensitivity: str = Field(
        default="MEDIUM",
        description="Price sensitivity (LOW/MEDIUM/HIGH)",
    )


class UserPreferencesUpdate(BaseModel):
    """
    Request model for updating preferences.
    """

    model_config = ConfigDict(extra="forbid")

    favorite_brands: Optional[List[str]] = Field(
        default=None,
        description="User's favorite brands",
    )

    avoided_ingredients: Optional[List[str]] = Field(
        default=None,
        description="Ingredients the user avoids",
    )

    preferred_categories: Optional[List[str]] = Field(
        default=None,
        description="Preferred product categories",
    )

    price_sensitivity: Optional[str] = Field(
        default=None,
        description="Price sensitivity (LOW/MEDIUM/HIGH)",
    )


# ==========================================================
# END OF FILE – models.py
# ==========================================================