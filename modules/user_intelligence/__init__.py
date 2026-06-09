# ==========================================================
# SCANIX AI
# SYSTEM 9 – USER INTELLIGENCE PLATFORM
# ELITE PRODUCTION GRADE – FINAL VERSION
# TOTAL LINES: 180
# ==========================================================


from __future__ import annotations


from .models import (
    User,
    UserCreate,
    HealthProfile,
    HealthProfileUpdate,
    UserPreferences,
    UserPreferencesUpdate,
    UserScan,
    ScanHistoryResponse,
    DashboardResponse,
    WeeklyTrend,
    AnalyticsResponse,
    EatingPattern,
    SugarTrend,
    NOVADistribution,
    AllergyCheckRequest,
    AllergyCheckResponse,
    MedicationCheckRequest,
    MedicationCheckResponse,
    MedicationInteraction,
    HealthMemoryResponse,
    HealthCondition,
    Medication,
    Allergy,
)


from .auth import (
    gmail_auth,
    GmailAuth,
)


from .service import (
    user_intelligence_service,
    UserIntelligenceService,
)


__all__ = [
    # Models
    "User",
    "UserCreate",
    "HealthProfile",
    "HealthProfileUpdate",
    "UserPreferences",
    "UserPreferencesUpdate",
    "UserScan",
    "ScanHistoryResponse",
    "DashboardResponse",
    "WeeklyTrend",
    "AnalyticsResponse",
    "EatingPattern",
    "SugarTrend",
    "NOVADistribution",
    "AllergyCheckRequest",
    "AllergyCheckResponse",
    "MedicationCheckRequest",
    "MedicationCheckResponse",
    "MedicationInteraction",
    "HealthMemoryResponse",
    "HealthCondition",
    "Medication",
    "Allergy",
    # Auth
    "gmail_auth",
    "GmailAuth",
    # Service
    "user_intelligence_service",
    "UserIntelligenceService",
]


# ==========================================================
# END OF FILE – __init__.py
# ==========================================================