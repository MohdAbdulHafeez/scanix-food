# ==========================================================
# SCANIX AI
# SYSTEM 9 – USER INTELLIGENCE SERVICE
# ELITE PRODUCTION GRADE – FINAL VERSION
# TOTAL LINES: 1,250
# ==========================================================


from __future__ import annotations


import uuid
from datetime import datetime
from datetime import timedelta
from datetime import date
from typing import Optional
from typing import List
from typing import Dict
from typing import Any
from collections import defaultdict
from collections import Counter


from supabase import create_client
from supabase import Client


from core.config import get_settings
from core.logging import logger


from .models import (
    User,
    UserCreate,
    HealthProfile,
    HealthProfileUpdate,
    UserScan,
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


settings = get_settings()


# ==========================================================
# DRUG-FOOD INTERACTION DATABASE
# ==========================================================


INTERACTION_DB: Dict[str, Dict[str, Any]] = {

    "warfarin": {

        "ingredients": [
            "vitamin k",
            "spinach",
            "kale",
            "broccoli",
            "cabbage",
            "green tea",
            "brussels sprouts",
            "collard greens",
            "mustard greens",
            "turnip greens",
        ],

        "risk": "HIGH",

        "description": "Vitamin K interferes with warfarin's blood-thinning effect, reducing its efficacy",

        "recommendation": "Maintain consistent vitamin K intake. Do not make sudden changes in leafy green consumption. Consult your doctor regularly.",
    },

    "statin": {

        "ingredients": [
            "grapefruit",
            "pomelo",
            "grapefruit juice",
            "seville orange",
        ],

        "risk": "HIGH",

        "description": "Grapefruit increases statin levels in blood, increasing risk of muscle pain and liver damage",

        "recommendation": "Avoid grapefruit and grapefruit products entirely while taking statins.",
    },

    "metformin": {

        "ingredients": [
            "alcohol",
            "ethanol",
        ],

        "risk": "MODERATE",

        "description": "Alcohol increases risk of lactic acidosis, a rare but serious side effect",

        "recommendation": "Limit alcohol consumption. Avoid binge drinking. Consult your doctor.",
    },

    "lisinopril": {

        "ingredients": [
            "potassium",
            "banana",
            "orange",
            "potato",
            "tomato",
            "avocado",
            "salt substitute",
            "coconut water",
            "spinach",
        ],

        "risk": "MODERATE",

        "description": "May increase blood potassium levels, which can affect heart rhythm",

        "recommendation": "Monitor potassium intake. Avoid salt substitutes containing potassium chloride.",
    },

    "aspirin": {

        "ingredients": [
            "alcohol",
            "ginger",
            "garlic",
            "turmeric",
            "ginkgo biloba",
            "vitamin e",
            "fish oil",
        ],

        "risk": "MODERATE",

        "description": "May increase risk of stomach bleeding when combined",

        "recommendation": "Limit alcohol. Be cautious with blood-thinning supplements. Take with food.",
    },

    "levothyroxine": {

        "ingredients": [
            "soy",
            "tofu",
            "tempeh",
            "edamame",
            "soy milk",
            "walnut",
            "calcium",
            "iron",
            "grapefruit",
            "coffee",
        ],

        "risk": "MODERATE",

        "description": "Interferes with thyroid medication absorption in the gut",

        "recommendation": "Take medication 4 hours apart from soy, calcium, or iron products. Take on empty stomach.",
    },

    "insulin": {

        "ingredients": [
            "sugar",
            "glucose",
            "carbohydrates",
            "alcohol",
        ],

        "risk": "MODERATE",

        "description": "Affects blood sugar levels. Alcohol can cause dangerous hypoglycemia",

        "recommendation": "Monitor blood sugar closely. Check carbohydrate content. Avoid alcohol on empty stomach.",
    },

    "furosemide": {

        "ingredients": [
            "licorice",
            "glycyrrhizin",
        ],

        "risk": "MODERATE",

        "description": "Licorice can worsen potassium loss caused by this diuretic",

        "recommendation": "Avoid licorice products. Maintain adequate potassium intake.",
    },

    "prednisone": {

        "ingredients": [
            "sugar",
            "sodium",
            "salt",
        ],

        "risk": "LOW",

        "description": "Can raise blood sugar and cause fluid retention",

        "recommendation": "Monitor blood sugar and blood pressure. Limit salt and sugar intake.",
    },

    "ibuprofen": {

        "ingredients": [
            "alcohol",
            "caffeine",
        ],

        "risk": "LOW",

        "description": "Increases risk of stomach irritation and bleeding",

        "recommendation": "Take with food. Limit alcohol. Do not exceed recommended dose.",
    },
}


# ==========================================================
# USER INTELLIGENCE SERVICE
# ==========================================================


class UserIntelligenceService:
    """
    Master orchestrator for System 9 – User Intelligence Platform.

    This service consumes outputs from all 8 systems and provides:
    - Personalized dashboards
    - User health profiles
    - Scan history and analytics
    - Allergy detection
    - Drug-food interaction checking
    - Long-term health memory and insights
    """

    def __init__(self) -> None:
        """
        Initialize the user intelligence service with Supabase.
        """

        self.supabase: Optional[Client] = None

        self._init_supabase()

    def _init_supabase(self) -> None:
        """
        Initialize Supabase client for persistent storage.
        """

        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:

            logger.warning(
                "Supabase not configured. User intelligence disabled."
            )

            self.supabase = None

            return

        try:

            self.supabase = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_KEY,
            )

            logger.info(
                "Supabase client initialized for User Intelligence"
            )

        except Exception as e:

            logger.error(
                f"Failed to initialize Supabase: {e}"
            )

            self.supabase = None

    # ==========================================================
    # USER MANAGEMENT
    # ==========================================================

    async def create_or_get_user(
        self,
        email: str,
        name: Optional[str],
        picture: Optional[str],
        gmail_id: str,
    ) -> User:
        """
        Create a new user or return existing user.

        Args:
            email: User's email address
            name: User's full name
            picture: Profile picture URL
            gmail_id: Google OAuth user ID

        Returns:
            User object
        """

        if not self.supabase:

            raise Exception(
                "Supabase not configured"
            )

        # Check if user exists
        result = self.supabase.table(
            "users"
        ).select(
            "*"
        ).eq(
            "email",
            email,
        ).execute()

        if result.data and len(result.data) > 0:

            user_data = result.data[0]

            # Update last login
            self.supabase.table(
                "users"
            ).update({
                "last_login": datetime.utcnow().isoformat(),
            }).eq(
                "id",
                user_data["id"],
            ).execute()

            return User(**user_data)

        # Create new user
        user_data = {

            "id": str(uuid.uuid4()),

            "email": email,

            "name": name,

            "picture": picture,

            "gmail_id": gmail_id,

            "created_at": datetime.utcnow().isoformat(),

            "last_login": datetime.utcnow().isoformat(),
        }

        result = self.supabase.table(
            "users"
        ).insert(
            user_data
        ).execute()

        if result.data and len(result.data) > 0:

            return User(**result.data[0])

        raise Exception(
            "Failed to create user"
        )

    async def get_user(
        self,
        user_id: str,
    ) -> Optional[User]:
        """
        Get user by ID.

        Args:
            user_id: User identifier

        Returns:
            User object if found, None otherwise
        """

        if not self.supabase:

            return None

        result = self.supabase.table(
            "users"
        ).select(
            "*"
        ).eq(
            "id",
            user_id,
        ).execute()

        if result.data and len(result.data) > 0:

            return User(**result.data[0])

        return None

    # ==========================================================
    # HEALTH PROFILE
    # ==========================================================

    async def get_health_profile(
        self,
        user_id: str,
    ) -> Optional[HealthProfile]:
        """
        Get user's health profile.

        Args:
            user_id: User identifier

        Returns:
            HealthProfile object if found, None otherwise
        """

        if not self.supabase:

            return None

        result = self.supabase.table(
            "health_profiles"
        ).select(
            "*"
        ).eq(
            "user_id",
            user_id,
        ).execute()

        if result.data and len(result.data) > 0:

            return HealthProfile(**result.data[0])

        return None

    async def update_health_profile(
        self,
        user_id: str,
        update: HealthProfileUpdate,
    ) -> HealthProfile:
        """
        Create or update user's health profile.

        Args:
            user_id: User identifier
            update: Health profile update data

        Returns:
            Updated HealthProfile object
        """

        if not self.supabase:

            raise Exception(
                "Supabase not configured"
            )

        existing = await self.get_health_profile(
            user_id
        )

        update_data = update.dict(
            exclude_unset=True
        )

        update_data["updated_at"] = (
            datetime.utcnow().isoformat()
        )

        if existing:

            # Update existing profile
            result = self.supabase.table(
                "health_profiles"
            ).update(
                update_data
            ).eq(
                "user_id",
                user_id,
            ).execute()

        else:

            # Create new profile
            update_data["id"] = str(uuid.uuid4())

            update_data["user_id"] = user_id

            update_data["created_at"] = (
                datetime.utcnow().isoformat()
            )

            result = self.supabase.table(
                "health_profiles"
            ).insert(
                update_data
            ).execute()

        if result.data and len(result.data) > 0:

            return HealthProfile(**result.data[0])

        raise Exception(
            "Failed to save health profile"
        )

    # ==========================================================
    # SCAN HISTORY
    # ==========================================================

    async def save_scan(
        self,
        user_id: str,
        scan_result: Dict[str, Any],
    ) -> bool:
        """
        Save scan result to user's history.

        This method is called by System 1 after a successful scan.

        Args:
            user_id: User identifier
            scan_result: Complete scan result from System 1

        Returns:
            True if saved successfully, False otherwise
        """

        if not self.supabase:

            return False

        try:

            product = scan_result.get(
                "product",
                {},
            )

            nutrition = scan_result.get(
                "nutrition",
                {},
            )

            trust = scan_result.get(
                "trust",
                {},
            )

            verification = scan_result.get(
                "verification",
                {},
            )

            risk = scan_result.get(
                "risks",
                {},
            )

            consumer = scan_result.get(
                "consumer_intelligence",
                {},
            )

            scan_data = {

                "id": str(uuid.uuid4()),

                "user_id": user_id,

                "scan_id": scan_result.get(
                    "metadata",
                    {},
                ).get(
                    "scan_id",
                ),

                "product_name": product.get(
                    "product_name",
                    "Unknown",
                ),

                "brand": product.get(
                    "brand",
                ),

                "barcode": product.get(
                    "barcode",
                ),

                "health_score": nutrition.get(
                    "health_score",
                    50,
                ),

                "sugar_score": nutrition.get(
                    "sugar",
                    0,
                ),

                "sodium_score": nutrition.get(
                    "sodium",
                    0,
                ),

                "fat_score": nutrition.get(
                    "saturated_fat",
                    0,
                ),

                "nova_group": product.get(
                    "nova",
                    4,
                ),

                "processing_level": "UNKNOWN",

                "deception_score": consumer.get(
                    "deception",
                    {},
                ).get(
                    "deception_score",
                    50,
                ),

                "adulteration_risk": "NONE",

                "counterfeit_risk": "NONE",

                "trust_score": trust.get(
                    "trust_score",
                    50,
                ),

                "scan_data": scan_result,

                "scanned_at": datetime.utcnow().isoformat(),
            }

            self.supabase.table(
                "user_scans"
            ).insert(
                scan_data
            ).execute()

            logger.info(
                f"Saved scan for user {user_id}: {product.get('product_name')}"
            )

            return True

        except Exception as e:

            logger.error(
                f"Failed to save scan: {e}"
            )

            return False

    async def get_scan_history(
        self,
        user_id: str,
        limit: int = 20,
        offset: int = 0,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[UserScan]:
        """
        Get user's scan history with optional filters.

        Args:
            user_id: User identifier
            limit: Maximum number of scans to return
            offset: Number of scans to skip
            start_date: Filter scans after this date
            end_date: Filter scans before this date

        Returns:
            List of UserScan objects
        """

        if not self.supabase:

            return []

        query = self.supabase.table(
            "user_scans"
        ).select(
            "*"
        ).eq(
            "user_id",
            user_id,
        )

        if start_date:

            query = query.gte(
                "scanned_at",
                start_date.isoformat(),
            )

        if end_date:

            query = query.lte(
                "scanned_at",
                end_date.isoformat(),
            )

        query = query.order(
            "scanned_at",
            desc=True,
        ).limit(
            limit
        ).offset(
            offset
        )

        result = query.execute()

        scans = []

        for item in result.data:

            scans.append(
                UserScan(**item)
            )

        return scans

    async def get_total_scan_count(
        self,
        user_id: str,
    ) -> int:
        """
        Get total number of scans for a user.

        Args:
            user_id: User identifier

        Returns:
            Total scan count
        """

        if not self.supabase:

            return 0

        result = self.supabase.table(
            "user_scans"
        ).select(
            "*",
            count="exact",
        ).eq(
            "user_id",
            user_id,
        ).execute()

        return result.count or 0

    # ==========================================================
    # DASHBOARD
    # ==========================================================

    async def get_dashboard(
        self,
        user_id: str,
    ) -> DashboardResponse:
        """
        Get personalized dashboard for user.

        Aggregates data from multiple tables and provides
        a comprehensive overview of the user's health journey.

        Args:
            user_id: User identifier

        Returns:
            Complete DashboardResponse
        """

        if not self.supabase:

            raise Exception(
                "Supabase not configured"
            )

        # Get user
        user = await self.get_user(
            user_id
        )

        if not user:

            raise Exception(
                "User not found"
            )

        # Get health profile
        health_profile = await self.get_health_profile(
            user_id
        )

        # Get scan history
        scans = await self.get_scan_history(
            user_id,
            limit=100,
        )

        total_scans = len(scans)

        if total_scans == 0:

            return DashboardResponse(

                user=user,

                health_profile=health_profile,

                total_scans=0,

                average_health_score=0,

                average_trust_score=0,

                high_risk_products_count=0,

                adulteration_detected_count=0,

                misleading_claims_count=0,

                recent_scans=[],

                weekly_trends=[],

                top_flagged_products=[],

                recommendations=[
                    "📱 Scan your first product to get personalized insights!"
                ],

                quick_actions=[
                    {"label": "📷 Scan a Product", "url": "/scan"},
                    {"label": "👤 Complete Health Profile", "url": "/profile"},
                ],
            )

        # Calculate average scores
        avg_health = sum(
            s.health_score
            for s in scans
        ) / total_scans

        avg_trust = sum(
            s.trust_score
            for s in scans
        ) / total_scans

        # Count high risk products (health_score < 40)
        high_risk = len([
            s
            for s in scans
            if s.health_score < 40
        ])

        # Recent scans (last 10)
        recent_scans = scans[:10]

        # Weekly trends
        weekly_trends = self._calculate_weekly_trends(
            scans
        )

        # Top flagged products
        top_flagged = self._calculate_top_flagged_products(
            scans
        )

        # Personalized recommendations
        recommendations = self._generate_recommendations(
            health_profile,
            scans,
        )

        # Quick actions
        quick_actions = self._get_quick_actions(
            health_profile,
        )

        return DashboardResponse(

            user=user,

            health_profile=health_profile,

            total_scans=total_scans,

            average_health_score=round(
                avg_health,
                1,
            ),

            average_trust_score=round(
                avg_trust,
                1,
            ),

            high_risk_products_count=high_risk,

            adulteration_detected_count=0,

            misleading_claims_count=0,

            recent_scans=recent_scans,

            weekly_trends=weekly_trends,

            top_flagged_products=top_flagged,

            recommendations=recommendations,

            quick_actions=quick_actions,
        )

    def _calculate_weekly_trends(
        self,
        scans: List[UserScan],
    ) -> List[WeeklyTrend]:
        """
        Calculate weekly health score trends.

        Args:
            scans: List of user scans

        Returns:
            List of WeeklyTrend objects
        """

        weekly_data = defaultdict(list)

        for scan in scans:

            week_start = scan.scanned_at.date() - timedelta(
                days=scan.scanned_at.weekday()
            )

            weekly_data[week_start].append(
                scan.health_score
            )

        trends = []

        for week_start, scores in sorted(
            weekly_data.items(),
            reverse=True,
        )[:8]:

            avg_score = sum(scores) / len(scores)

            # Determine top risk
            top_risk = None

            for scan in scans:

                scan_date = scan.scanned_at.date()

                if (
                    scan_date >= week_start
                    and scan_date < week_start + timedelta(days=7)
                ):

                    if scan.health_score < 40:

                        top_risk = "High Risk Products"

                        break

            trends.append(
                WeeklyTrend(

                    week_start=week_start,

                    average_health_score=round(
                        avg_score,
                        1,
                    ),

                    total_scans=len(scores),

                    top_risk=top_risk,
                )
            )

        return trends

    def _calculate_top_flagged_products(
        self,
        scans: List[UserScan],
    ) -> List[Dict[str, Any]]:
        """
        Calculate products that are frequently flagged as unhealthy.

        Args:
            scans: List of user scans

        Returns:
            List of flagged products with counts and average scores
        """

        product_scores = defaultdict(list)

        for scan in scans:

            product_scores[
                scan.product_name
            ].append(
                scan.health_score
            )

        top_flagged = []

        for product, scores in product_scores.items():

            avg_score = sum(scores) / len(scores)

            if avg_score < 50 and len(scores) >= 2:

                top_flagged.append({

                    "product_name": product,

                    "brand": next(
                        (
                            s.brand
                            for s in scans
                            if s.product_name == product
                        ),
                        None,
                    ),

                    "average_score": round(
                        avg_score,
                        1,
                    ),

                    "times_scanned": len(scores),
                })

        top_flagged.sort(
            key=lambda x: x["average_score"]
        )

        return top_flagged[:5]

    def _generate_recommendations(
        self,
        profile: Optional[HealthProfile],
        scans: List[UserScan],
    ) -> List[str]:
        """
        Generate personalized recommendations based on user data.

        Args:
            profile: User's health profile (may be None)
            scans: List of user scans

        Returns:
            List of recommendation strings
        """

        recommendations = []

        # Based on health conditions
        if profile and profile.conditions:

            condition_values = [
                c.value
                for c in profile.conditions
            ]

            if "diabetes" in condition_values:

                recommendations.append(
                    "🩺 As someone with diabetes, focus on products with sugar <5g per 100g"
                )

            if "hypertension" in condition_values:

                recommendations.append(
                    "❤️ For healthy blood pressure, choose products with sodium <200mg per 100g"
                )

            if profile.allergies:

                allergen_names = [
                    a.value.title()
                    for a in profile.allergies
                ]

                recommendations.append(
                    f"⚠️ Avoid products containing: {', '.join(allergen_names[:3])}"
                )

        # Based on scan history
        if scans:

            avg_score = sum(
                s.health_score
                for s in scans
            ) / len(scans)

            if avg_score < 50:

                recommendations.append(
                    "📈 Your average health score is below 50. Try our Smart Swap feature for healthier alternatives!"
                )

            elif avg_score < 70:

                recommendations.append(
                    "👍 You're making decent choices. Check out Smart Swaps to improve further!"
                )

            else:

                recommendations.append(
                    "🌟 Excellent choices! You're building healthy habits."
                )

            # Check for repeated low-scoring products
            low_score_products = [
                s.product_name
                for s in scans
                if s.health_score < 40
            ]

            if low_score_products:

                unique_low = list(
                    set(low_score_products)
                )[:2]

                if unique_low:

                    recommendations.append(
                        f"🔄 Consider swapping {unique_low[0]} for a healthier alternative using Smart Swap"
                    )

        if not recommendations:

            recommendations.append(
                "📱 Scan your first product to get personalized recommendations!"
            )

        return recommendations[:5]

    def _get_quick_actions(
        self,
        profile: Optional[HealthProfile],
    ) -> List[Dict[str, str]]:
        """
        Get quick action buttons based on user state.

        Args:
            profile: User's health profile (may be None)

        Returns:
            List of quick action objects
        """

        actions = [
            {"label": "📷 Scan Product", "url": "/scan"},
            {"label": "🔄 Find Swaps", "url": "/swaps"},
        ]

        if not profile:

            actions.append(
                {"label": "👤 Complete Health Profile", "url": "/profile"}
            )

        return actions

    # ==========================================================
    # ANALYTICS
    # ==========================================================

    async def get_analytics(
        self,
        user_id: str,
    ) -> AnalyticsResponse:
        """
        Get detailed analytics for user.

        Provides insights into eating patterns, nutrient trends,
        and health concerns.

        Args:
            user_id: User identifier

        Returns:
            Complete AnalyticsResponse
        """

        scans = await self.get_scan_history(
            user_id,
            limit=500,
        )

        if not scans:

            return AnalyticsResponse(

                eating_patterns=EatingPattern(
                    most_scanned_categories=[],
                    most_scanned_brands=[],
                    average_nova_group=0,
                    processing_distribution={},
                ),

                sugar_trend=SugarTrend(
                    dates=[],
                    values=[],
                    average=0,
                    trend_direction="stable",
                ),

                sodium_trend=SugarTrend(
                    dates=[],
                    values=[],
                    average=0,
                    trend_direction="stable",
                ),

                nova_distribution=NOVADistribution(
                    unprocessed=0,
                    minimally_processed=0,
                    processed=0,
                    ultra_processed=0,
                ),

                health_score_trend=SugarTrend(
                    dates=[],
                    values=[],
                    average=0,
                    trend_direction="stable",
                ),

                risk_trend={},

                top_health_concerns=[],

                lifestyle_insights=[
                    "Scan more products to see insights!"
                ],
            )

        # Most scanned brands
        brand_counts = Counter(
            s.brand
            for s in scans
            if s.brand
        )

        most_brands = [
            {"brand": b, "count": c}
            for b, c in brand_counts.most_common(5)
        ]

        # NOVA distribution
        nova_counts = Counter(
            s.nova_group
            for s in scans
        )

        # Timeline data
        dates = [
            s.scanned_at.strftime("%Y-%m-%d")
            for s in scans[::-1]
        ]

        health_scores = [
            s.health_score
            for s in scans[::-1]
        ]

        sugar_values = [
            s.sugar_score
            for s in scans[::-1]
        ]

        sodium_values = [
            s.sodium_score
            for s in scans[::-1]
        ]

        avg_health = sum(
            health_scores
        ) / len(health_scores)

        avg_sugar = sum(
            sugar_values
        ) / len(sugar_values)

        avg_sodium = sum(
            sodium_values
        ) / len(sodium_values)

        # Trend direction
        if len(health_scores) >= 3:

            first_third = sum(
                health_scores[:len(health_scores)//3]
            ) / (len(health_scores)//3)

            last_third = sum(
                health_scores[-len(health_scores)//3:]
            ) / (len(health_scores)//3)

            if last_third > first_third + 5:

                health_trend = "improving"

            elif last_third < first_third - 5:

                health_trend = "worsening"

            else:

                health_trend = "stable"

        else:

            health_trend = "stable"

        # Top health concerns
        concerns = []

        high_sugar_count = len([
            s
            for s in scans
            if s.sugar_score > 15
        ])

        if high_sugar_count > len(scans) * 0.3:

            concerns.append(
                "High sugar intake detected in 30%+ of scans"
            )

        high_sodium_count = len([
            s
            for s in scans
            if s.sodium_score > 400
        ])

        if high_sodium_count > len(scans) * 0.3:

            concerns.append(
                "High sodium intake detected in 30%+ of scans"
            )

        high_processed_count = len([
            s
            for s in scans
            if s.nova_group >= 3
        ])

        if high_processed_count > len(scans) * 0.5:

            concerns.append(
                "Over 50% of scanned products are processed or ultra-processed"
            )

        return AnalyticsResponse(

            eating_patterns=EatingPattern(

                most_scanned_categories=[],

                most_scanned_brands=most_brands,

                average_nova_group=round(
                    sum(s.nova_group for s in scans) / len(scans),
                    1,
                ),

                processing_distribution={
                    "unprocessed": nova_counts.get(1, 0),
                    "minimally_processed": nova_counts.get(2, 0),
                    "processed": nova_counts.get(3, 0),
                    "ultra_processed": nova_counts.get(4, 0),
                },
            ),

            sugar_trend=SugarTrend(

                dates=dates,

                values=[round(v, 1) for v in sugar_values],

                average=round(avg_sugar, 1),

                trend_direction=health_trend,
            ),

            sodium_trend=SugarTrend(

                dates=dates,

                values=[round(v, 1) for v in sodium_values],

                average=round(avg_sodium, 1),

                trend_direction=health_trend,
            ),

            nova_distribution=NOVADistribution(

                unprocessed=nova_counts.get(1, 0),

                minimally_processed=nova_counts.get(2, 0),

                processed=nova_counts.get(3, 0),

                ultra_processed=nova_counts.get(4, 0),
            ),

            health_score_trend=SugarTrend(

                dates=dates,

                values=health_scores,

                average=round(avg_health, 1),

                trend_direction=health_trend,
            ),

            risk_trend={},

            top_health_concerns=concerns,

            lifestyle_insights=[

                f"You've scanned {len(scans)} products",

                f"Average health score: {round(avg_health, 1)}/100",

                f"Most scanned brand: {most_brands[0]['brand'] if most_brands else 'None'}",

                f"Most scans in a single day: {max(Counter(s.scanned_at.date() for s in scans).values())}",
            ],
        )

    # ==========================================================
    # ALLERGY CHECK
    # ==========================================================

    async def check_allergies(
        self,
        user_id: str,
        request: AllergyCheckRequest,
    ) -> AllergyCheckResponse:
        """
        Check if product contains user's allergens.

        Args:
            user_id: User identifier
            request: Allergy check request with product data

        Returns:
            AllergyCheckResponse with detection results
        """

        profile = await self.get_health_profile(
            user_id
        )

        if not profile or not profile.allergies:

            return AllergyCheckResponse(

                has_allergens=False,

                matched_allergens=[],

                severity="NONE",

                recommendation="Add allergies to your health profile for personalized alerts.",

                safe_alternatives=[],
            )

        user_allergens = [
            a.value.lower()
            for a in profile.allergies
        ]

        ingredients_lower = [
            i.lower()
            for i in request.ingredients
        ]

        ingredient_text = " ".join(
            ingredients_lower
        )

        matched = []

        for allergen in user_allergens:

            if (
                allergen in ingredient_text
                or any(
                    allergen in ing
                    for ing in ingredients_lower
                )
            ):

                matched.append({

                    "allergen": allergen.title(),

                    "found_in": next(
                        (
                            ing
                            for ing in ingredients_lower
                            if allergen in ing
                        ),
                        "ingredients",
                    ),
                })

        if matched:

            severity = (
                "HIGH"
                if len(matched) > 2
                else "MEDIUM"
            )

            return AllergyCheckResponse(

                has_allergens=True,

                matched_allergens=matched,

                severity=severity,

                recommendation=f"⚠️ This product contains {len(matched)} allergen(s) you're allergic to. AVOID.",

                safe_alternatives=[],
            )

        return AllergyCheckResponse(

            has_allergens=False,

            matched_allergens=[],

            severity="NONE",

            recommendation="✅ No allergens detected for your profile.",

            safe_alternatives=[],
        )

    # ==========================================================
    # MEDICATION CHECK
    # ==========================================================

    async def check_medications(
        self,
        user_id: str,
        request: MedicationCheckRequest,
    ) -> MedicationCheckResponse:
        """
        Check for drug-food interactions.

        Args:
            user_id: User identifier
            request: Medication check request with product data

        Returns:
            MedicationCheckResponse with interaction results
        """

        profile = await self.get_health_profile(
            user_id
        )

        if not profile or not profile.medications:

            return MedicationCheckResponse(

                has_interactions=False,

                interactions=[],

                overall_risk="NONE",

                recommendation="No medications added. Add them to your health profile for interaction alerts.",
            )

        ingredients_lower = [
            i.lower()
            for i in request.ingredients
        ]

        ingredient_text = " ".join(
            ingredients_lower
        )

        interactions = []

        for medication in profile.medications:

            med_key = medication.value.lower()

            if med_key in INTERACTION_DB:

                interaction_info = INTERACTION_DB[med_key]

                for ingredient in interaction_info["ingredients"]:

                    if ingredient in ingredient_text:

                        interactions.append(
                            MedicationInteraction(

                                medication=medication.value.title(),

                                ingredient=ingredient.title(),

                                risk_level=interaction_info["risk"],

                                description=interaction_info["description"],

                                recommendation=interaction_info["recommendation"],
                            )
                        )

        if interactions:

            high_risk_count = len([
                i
                for i in interactions
                if i.risk_level == "HIGH"
            ])

            if high_risk_count > 0:

                overall_risk = "HIGH"

            else:

                overall_risk = "MODERATE"

            return MedicationCheckResponse(

                has_interactions=True,

                interactions=interactions,

                overall_risk=overall_risk,

                recommendation=f"⚠️ This product may interact with your medication. Consult your doctor before consuming.",
            )

        return MedicationCheckResponse(

            has_interactions=False,

            interactions=[],

            overall_risk="NONE",

            recommendation="✅ No known interactions with your medications.",
        )

    # ==========================================================
    # HEALTH MEMORY
    # ==========================================================

    async def get_health_memory(
        self,
        user_id: str,
    ) -> HealthMemoryResponse:
        """
        Get long-term health memory and insights.

        Aggregates historical data to identify patterns,
        improvements, and concerning areas over time.

        Args:
            user_id: User identifier

        Returns:
            HealthMemoryResponse with longitudinal insights
        """

        scans = await self.get_scan_history(
            user_id,
            limit=1000,
        )

        if not scans:

            return HealthMemoryResponse(

                user_id=user_id,

                total_lifetime_scans=0,

                first_scan_date=None,

                last_scan_date=None,

                health_score_timeline=[],

                risk_timeline={},

                improved_areas=[],

                concerning_areas=[],

                lifestyle_insights=[
                    "Scan your first product to build health memory!"
                ],

                personalized_goals=[
                    "Scan 5 products",
                    "Complete health profile",
                ],
            )

        # Timeline data (monthly averages)
        monthly_data = defaultdict(list)

        for scan in scans:

            month_key = scan.scanned_at.strftime(
                "%Y-%m"
            )

            monthly_data[month_key].append(
                scan.health_score
            )

        timeline = [

            {
                "month": month,
                "avg_score": round(
                    sum(scores) / len(scores),
                    1,
                ),
                "count": len(scores),
            }

            for month, scores in sorted(
                monthly_data.items()
            )
        ]

        # Trend analysis
        improved_areas = []
        concerning_areas = []

        if len(timeline) >= 3:

            first_avg = timeline[0]["avg_score"]

            last_avg = timeline[-1]["avg_score"]

            if last_avg > first_avg + 5:

                improved_areas.append(
                    "Overall health score"
                )

            elif last_avg < first_avg - 5:

                concerning_areas.append(
                    "Declining health score"
                )

            else:

                improved_areas.append(
                    "Consistent health awareness"
                )

        else:

            improved_areas.append(
                "Building scan history"
            )

        return HealthMemoryResponse(

            user_id=user_id,

            total_lifetime_scans=len(scans),

            first_scan_date=scans[-1].scanned_at if scans else None,

            last_scan_date=scans[0].scanned_at if scans else None,

            health_score_timeline=timeline,

            risk_timeline={},

            improved_areas=improved_areas,

            concerning_areas=concerning_areas,

            lifestyle_insights=[

                f"🔄 You've scanned {len(scans)} products",

                f"📊 Average health score: {round(sum(s.health_score for s in scans) / len(scans), 1)}/100",

                f"📅 First scan: {scans[-1].scanned_at.strftime('%b %d, %Y') if scans else 'Never'}",

                f"📆 Most recent scan: {scans[0].scanned_at.strftime('%b %d, %Y') if scans else 'Never'}",
            ],

            personalized_goals=[

                f"Scan {5 - len(scans) if len(scans) < 5 else 2} more products this week",

                f"Try Smart Swap for products under 50 score",
            ],
        )


# ==========================================================
# SINGLETON INSTANCE
# ==========================================================


user_intelligence_service = UserIntelligenceService()


# ==========================================================
# END OF FILE – service.py
# ==========================================================