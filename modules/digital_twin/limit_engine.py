# ============================================================
# ELITE PART A
#
# LIMIT ENGINE FOUNDATION
#
# WHO CONSTANTS
# ICMR CONSTANTS
# FSSAI CONSTANTS
#
# SHARED EXPOSURE UTILITIES
# SHARED LIMIT HELPERS
# SHARED HEATMAP HELPERS
#
# Used By:
#
# WHO Sugar Engine
# WHO Sodium Engine
# WHO Fat Engine
#
# UPF Engine
# Additive Engine
#
# Weekly Engine
# Monthly Engine
#
# Safe Frequency Engine
# Health Debt Engine
#
# Regulatory Compliance Engine
# Consumption Safety Engine
#
# Final Aggregator
# ============================================================

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Any
from typing import Optional


# ============================================================
# REGULATORY CONSTANTS
# ============================================================

class LimitConstants:

    # --------------------------------------------------------
    # WHO DAILY LIMITS
    # --------------------------------------------------------

    WHO_SUGAR_LIMIT_G = 25.0

    WHO_SODIUM_LIMIT_MG = 2000.0

    WHO_SATURATED_FAT_LIMIT_G = 20.0

    WHO_TRANS_FAT_LIMIT_G = 2.0

    WHO_CALORIE_REFERENCE = 2000.0

    # --------------------------------------------------------
    # ICMR THRESHOLDS
    # --------------------------------------------------------

    ICMR_UPF_LOW = 30.0

    ICMR_UPF_MODERATE = 60.0

    ICMR_UPF_HIGH = 80.0

    # --------------------------------------------------------
    # ADDITIVE THRESHOLDS
    # --------------------------------------------------------

    ADDITIVE_LOW = 25.0

    ADDITIVE_MODERATE = 50.0

    ADDITIVE_HIGH = 75.0

    # --------------------------------------------------------
    # HEALTH DEBT THRESHOLDS
    # --------------------------------------------------------

    DEBT_LOW = 30.0

    DEBT_MODERATE = 60.0

    DEBT_HIGH = 80.0

    # --------------------------------------------------------
    # LIMIT SCORE THRESHOLDS
    # --------------------------------------------------------

    EXCELLENT_SCORE = 90.0

    GOOD_SCORE = 80.0

    MODERATE_SCORE = 65.0

    POOR_SCORE = 50.0


# ============================================================
# LIMIT MATH UTILITIES
# ============================================================

class LimitMath:

    @staticmethod
    def clamp(
        value: float,
        minimum: float = 0.0,
        maximum: float = 100.0
    ) -> float:

        return max(
            minimum,
            min(
                value,
                maximum
            )
        )

    @staticmethod
    def safe_divide(
        numerator: float,
        denominator: float
    ) -> float:

        if denominator == 0:
            return 0.0

        return numerator / denominator

    @staticmethod
    def percentage(
        value: float,
        limit: float
    ) -> float:

        if limit <= 0:
            return 0.0

        return (

            value

            /

            limit

        ) * 100

    @staticmethod
    def weighted_average(
        values: List[float],
        weights: List[float]
    ) -> float:

        if not values:
            return 0.0

        numerator = sum(

            value * weight

            for value, weight

            in zip(
                values,
                weights
            )

        )

        denominator = sum(weights)

        if denominator == 0:
            return 0.0

        return numerator / denominator


# ============================================================
# EXPOSURE MULTIPLIER ENGINE
# ============================================================

class ExposureMultiplierEngine:

    @staticmethod
    def weekly(
        daily_value: float
    ) -> float:

        return daily_value * 7

    @staticmethod
    def monthly(
        daily_value: float
    ) -> float:

        return daily_value * 30

    @staticmethod
    def yearly(
        daily_value: float
    ) -> float:

        return daily_value * 365


# ============================================================
# REGULATORY UTILITIES
# ============================================================

class RegulatoryUtils:

    @staticmethod
    def remaining_budget(
        current: float,
        limit: float
    ) -> float:

        return max(
            0,
            limit - current
        )

    @staticmethod
    def utilization_percent(
        current: float,
        limit: float
    ) -> float:

        return round(

            LimitMath.percentage(
                current,
                limit
            ),

            2
        )


# ============================================================
# EXPOSURE ZONE ENGINE
# ============================================================

class ExposureZoneEngine:

    @staticmethod
    def calculate(
        utilization_percent: float
    ) -> str:

        if utilization_percent >= 100:

            return "CRITICAL"

        if utilization_percent >= 80:

            return "HIGH"

        if utilization_percent >= 50:

            return "MODERATE"

        return "LOW"


# ============================================================
# HEATMAP ENGINE
# ============================================================

class ExposureHeatmapUtils:

    @staticmethod
    def zone(
        score: float
    ) -> str:

        if score >= 90:

            return "DARK_GREEN"

        if score >= 80:

            return "GREEN"

        if score >= 65:

            return "YELLOW"

        if score >= 50:

            return "ORANGE"

        return "RED"


# ============================================================
# HEALTH DEBT LEVEL ENGINE
# ============================================================

class HealthDebtLevelEngine:

    @staticmethod
    def calculate(
        debt_score: float
    ) -> str:

        if debt_score >= 80:

            return "SEVERE"

        if debt_score >= 60:

            return "HIGH"

        if debt_score >= 30:

            return "MODERATE"

        return "LOW"


# ============================================================
# SAFE FREQUENCY HELPER
# ============================================================

class SafeFrequencyHelper:

    @staticmethod
    def weekly_frequency(
        utilization_percent: float
    ) -> str:

        if utilization_percent >= 100:

            return "AVOID"

        if utilization_percent >= 80:

            return "1 TIME / WEEK"

        if utilization_percent >= 50:

            return "1-2 TIMES / WEEK"

        if utilization_percent >= 25:

            return "2-4 TIMES / WEEK"

        return "DAILY"


# ============================================================
# COMPLIANCE ENGINE
# ============================================================

class ComplianceEngine:

    @staticmethod
    def compliance(
        score: float
    ) -> str:

        if score >= 90:

            return "FULLY_COMPLIANT"

        if score >= 75:

            return "MOSTLY_COMPLIANT"

        if score >= 50:

            return "PARTIALLY_COMPLIANT"

        return "NON_COMPLIANT"


# ============================================================
# CONSUMPTION SAFETY ENGINE
# ============================================================

class ConsumptionSafetyEngine:

    @staticmethod
    def classify(
        overall_score: float
    ) -> str:

        if overall_score >= 85:

            return "SAFE"

        if overall_score >= 60:

            return "LIMIT"

        return "AVOID"


# ============================================================
# OUTPUT MODELS
# ============================================================

@dataclass
class ExposureResult:

    exposure: float

    limit_percent: float

    remaining_budget: float

    zone: str


@dataclass
class HealthDebtResult:

    score: float

    level: str


# ============================================================
# PART A REGISTRATION
# ============================================================

class LimitFoundation:

    def __init__(self):

        self.constants = (
            LimitConstants()
        )

        self.math = (
            LimitMath()
        )

        self.zone_engine = (
            ExposureZoneEngine()
        )

        self.heatmap = (
            ExposureHeatmapUtils()
        )

        self.compliance = (
            ComplianceEngine()
        )


        # ============================================================
# ELITE PART B
#
# WHO SUGAR EXPOSURE ENGINE
# WHO SODIUM EXPOSURE ENGINE
# WHO SATURATED FAT EXPOSURE ENGINE
#
# Depends On:
# - LimitConstants
# - LimitMath
# - ExposureMultiplierEngine
# - RegulatoryUtils
# - ExposureZoneEngine
# ============================================================


# ============================================================
# WHO SUGAR EXPOSURE ENGINE
# ============================================================

class WHOSugarExposureEngine:

    def calculate(
        self,
        sugar_per_serving_g: float,
        servings_per_day: float = 1.0
    ) -> Dict:
        
        servings_per_day = max(
    0,
    servings_per_day
)

        daily_sugar_intake = (

            sugar_per_serving_g
            *
            servings_per_day

        )

        weekly_sugar_intake = (

            ExposureMultiplierEngine
            .weekly(
                daily_sugar_intake
            )

        )

        monthly_sugar_intake = (

            ExposureMultiplierEngine
            .monthly(
                daily_sugar_intake
            )

        )

        who_sugar_limit_percent = (

            RegulatoryUtils
            .utilization_percent(

                daily_sugar_intake,

                LimitConstants
                .WHO_SUGAR_LIMIT_G

            )

        )

        remaining_sugar_budget = (

            RegulatoryUtils
            .remaining_budget(

                daily_sugar_intake,

                LimitConstants
                .WHO_SUGAR_LIMIT_G

            )

        )

        sugar_exposure_zone = (

            ExposureZoneEngine
            .calculate(
                who_sugar_limit_percent
            )

        )

        return {

            "daily_sugar_intake":
                round(
                    daily_sugar_intake,
                    2
                ),

            "weekly_sugar_intake":
                round(
                    weekly_sugar_intake,
                    2
                ),

            "monthly_sugar_intake":
                round(
                    monthly_sugar_intake,
                    2
                ),

            "who_sugar_limit_percent":
                round(
                    who_sugar_limit_percent,
                    2
                ),

            "remaining_sugar_budget":
                round(
                    remaining_sugar_budget,
                    2
                ),

            "sugar_exposure_zone":
                sugar_exposure_zone
        }


# ============================================================
# WHO SODIUM EXPOSURE ENGINE
# ============================================================

class WHOSodiumExposureEngine:

    def calculate(
        self,
        sodium_mg: float,
        servings_per_day: float = 1.0
    ) -> Dict:
        
        servings_per_day = max(
    0,
    servings_per_day
)
        
        daily_sodium_intake = (

            sodium_mg
            *
            servings_per_day

        )

        weekly_sodium_intake = (

            ExposureMultiplierEngine
            .weekly(
                daily_sodium_intake
            )

        )

        monthly_sodium_intake = (

            ExposureMultiplierEngine
            .monthly(
                daily_sodium_intake
            )

        )

        who_sodium_limit_percent = (

            RegulatoryUtils
            .utilization_percent(

                daily_sodium_intake,

                LimitConstants
                .WHO_SODIUM_LIMIT_MG

            )

        )

        remaining_sodium_budget = (

            RegulatoryUtils
            .remaining_budget(

                daily_sodium_intake,

                LimitConstants
                .WHO_SODIUM_LIMIT_MG

            )

        )

        sodium_exposure_zone = (

            ExposureZoneEngine
            .calculate(
                who_sodium_limit_percent
            )

        )

        return {

            "daily_sodium_intake":
                round(
                    daily_sodium_intake,
                    2
                ),

            "weekly_sodium_intake":
                round(
                    weekly_sodium_intake,
                    2
                ),

            "monthly_sodium_intake":
                round(
                    monthly_sodium_intake,
                    2
                ),

            "who_sodium_limit_percent":
                round(
                    who_sodium_limit_percent,
                    2
                ),

            "remaining_sodium_budget":
                round(
                    remaining_sodium_budget,
                    2
                ),

            "sodium_exposure_zone":
                sodium_exposure_zone
        }


# ============================================================
# SATURATED FAT BURDEN MODEL
# ============================================================

class SaturatedFatBurdenModel:

    @staticmethod
    def calculate(
        saturated_fat_g: float,
        trans_fat_g: float
    ) -> float:

        burden = (

            saturated_fat_g

            +

            (
                trans_fat_g * 5
            )

        )

        return burden


# ============================================================
# CARDIOVASCULAR FAT LOAD MODEL
# ============================================================

class CardiovascularFatLoadModel:

    @staticmethod
    def calculate(
        saturated_fat_g: float,
        trans_fat_g: float
    ) -> float:

        load = (

            saturated_fat_g * 2.0

            +

            trans_fat_g * 15.0

        )

        return LimitMath.clamp(
            load
        )


# ============================================================
# WHO SATURATED FAT ENGINE
# ============================================================

class WHOSaturatedFatExposureEngine:

    def calculate(
        self,
        saturated_fat_g: float,
        trans_fat_g: float,
        servings_per_day: float = 1.0
    ) -> Dict:

        servings_per_day = max(
            0,
            servings_per_day
        )

        daily_sat_fat = (
            saturated_fat_g
            *
            servings_per_day
        )

        daily_trans_fat = (
            trans_fat_g
            *
            servings_per_day
        )

        fat_exposure = (

            SaturatedFatBurdenModel
            .calculate(
                daily_sat_fat,
                daily_trans_fat
            )

        )

        fat_limit_percent = (

            RegulatoryUtils
            .utilization_percent(

                fat_exposure,

                LimitConstants
                .WHO_SATURATED_FAT_LIMIT_G

            )

        )

        cardiovascular_burden = (

            CardiovascularFatLoadModel
            .calculate(
                daily_sat_fat,
                daily_trans_fat
            )

        )

        fat_zone = (

            ExposureZoneEngine
            .calculate(
                fat_limit_percent
            )

        )

        return {

            "daily_saturated_fat":
                round(
                    daily_sat_fat,
                    2
                ),

            "daily_trans_fat":
                round(
                    daily_trans_fat,
                    2
                ),

            "fat_exposure":
                round(
                    fat_exposure,
                    2
                ),

            "fat_limit_percent":
                round(
                    fat_limit_percent,
                    2
                ),

            "cardiovascular_burden":
                round(
                    cardiovascular_burden,
                    2
                ),

            "fat_zone":
                fat_zone
        }


# ============================================================
# PART B REGISTRATION
# ============================================================

class WHOLimitLayer:

    def __init__(self):

        self.sugar = (
            WHOSugarExposureEngine()
        )

        self.sodium = (
            WHOSodiumExposureEngine()
        )

        self.fat = (
            WHOSaturatedFatExposureEngine()
        )


        # ============================================================
# ELITE PART C
#
# ICMR UPF EXPOSURE ENGINE
# ADDITIVE EXPOSURE ENGINE
#
# Depends On:
# - LimitConstants
# - LimitMath
# - ExposureZoneEngine
# ============================================================


# ============================================================
# ICMR UPF MODELS
# ============================================================

class UPFExposureModel:

    @staticmethod
    def calculate(
        processing_score: float,
        additive_score: float,
        emulsifier_score: float,
        artificial_ingredient_count: int
    ) -> float:

        upf_score = (

            processing_score * 0.45

            +

            additive_score * 0.25

            +

            emulsifier_score * 0.20

            +

            (
                artificial_ingredient_count * 2
            ) * 0.10

        )

        return LimitMath.clamp(
            upf_score
        )


class UPFRiskModel:

    @staticmethod
    def calculate(
        upf_score: float
    ) -> str:

        if upf_score >= LimitConstants.ICMR_UPF_HIGH:

            return "HIGH"

        if upf_score >= LimitConstants.ICMR_UPF_MODERATE:

            return "MODERATE"

        return "LOW"


class ICMRAlignmentModel:

    @staticmethod
    def calculate(
        upf_score: float
    ) -> float:

        alignment = (

            100 -
            upf_score

        )

        return LimitMath.clamp(
            alignment
        )


# ============================================================
# ICMR UPF EXPOSURE ENGINE
# ============================================================

class ICMRUPFExposureEngine:

    def calculate(
        self,
        processing_score: float,
        additive_score: float,
        emulsifier_score: float,
        artificial_ingredient_count: int
    ) -> Dict:

        artificial_ingredient_count = max(
            0,
            artificial_ingredient_count
        )

        upf_score = (

            UPFExposureModel
            .calculate(
                processing_score,
                additive_score,
                emulsifier_score,
                artificial_ingredient_count
            )

        )

        upf_risk = (

            UPFRiskModel
            .calculate(
                upf_score
            )

        )

        icmr_alignment = (

            ICMRAlignmentModel
            .calculate(
                upf_score
            )

        )

        if upf_score >= 80:

            upf_verdict = (
                "HIGHLY_ULTRA_PROCESSED"
            )

        elif upf_score >= 60:

            upf_verdict = (
                "ULTRA_PROCESSED"
            )

        elif upf_score >= 40:

            upf_verdict = (
                "MODERATELY_PROCESSED"
            )

        else:

            upf_verdict = (
                "MINIMALLY_PROCESSED"
            )

        return {

            "upf_score":
                round(
                    upf_score,
                    2
                ),

            "upf_risk":
                upf_risk,

            "icmr_alignment":
                round(
                    icmr_alignment,
                    2
                ),

            "upf_verdict":
                upf_verdict
        }


# ============================================================
# ADDITIVE MODELS
# ============================================================

class AdditiveLoadModel:

    @staticmethod
    def calculate(
        additive_count: int,
        servings_per_day: float
    ) -> float:

        additive_count = max(
            0,
            additive_count
        )

        return (

            additive_count

            *

            servings_per_day

        )


class RiskWeightedAdditiveModel:

    @staticmethod
    def calculate(
        low_risk_additives: int,
        moderate_risk_additives: int,
        high_risk_additives: int
    ) -> float:

        weighted_score = (

            low_risk_additives * 1

            +

            moderate_risk_additives * 3

            +

            high_risk_additives * 6

        )

        return weighted_score


class CumulativeAdditiveBurdenModel:

    @staticmethod
    def calculate(
        additive_load: float
    ) -> float:

        burden = (

            additive_load * 4

        )

        return LimitMath.clamp(
            burden
        )


# ============================================================
# ADDITIVE EXPOSURE ENGINE
# ============================================================

class AdditiveExposureEngine:

    def calculate(
        self,
        additive_count: int,
        low_risk_additives: int,
        moderate_risk_additives: int,
        high_risk_additives: int,
        servings_per_day: float = 1.0
    ) -> Dict:

        servings_per_day = max(
            0.0,
            servings_per_day
        )
        low_risk_additives = max(
            0,
            low_risk_additives
        )

        moderate_risk_additives = max(
            0,
            moderate_risk_additives
        )

        high_risk_additives = max(
            0,
            high_risk_additives
        )
        additive_load = (

            AdditiveLoadModel
            .calculate(
                additive_count,
                servings_per_day
            )

        )

        weighted_risk = (

            RiskWeightedAdditiveModel
            .calculate(
                low_risk_additives,
                moderate_risk_additives,
                high_risk_additives
            )

        )

        cumulative_additive_burden = (

            CumulativeAdditiveBurdenModel
            .calculate(

                additive_load

                +

                weighted_risk

            )

        )

        additive_exposure_score = (

            100

            -

            cumulative_additive_burden

        )

        additive_exposure_score = (
            LimitMath.clamp(
                additive_exposure_score
            )
        )

        if additive_exposure_score >= 80:

            exposure_zone = "LOW"

        elif additive_exposure_score >= 60:

            exposure_zone = "MODERATE"

        elif additive_exposure_score >= 40:

            exposure_zone = "HIGH"

        else:

            exposure_zone = "CRITICAL"

        return {

            "additive_load":
                round(
                    additive_load,
                    2
                ),

            "cumulative_additive_burden":
                round(
                    cumulative_additive_burden,
                    2
                ),

            "high_risk_additives":
                high_risk_additives,

            "additive_exposure_score":
                round(
                    additive_exposure_score,
                    2
                ),

            "additive_exposure_zone":
                exposure_zone
        }


# ============================================================
# PART C REGISTRATION
# ============================================================

class RegulatoryExposureLayer:

    def __init__(self):

        self.upf = (
            ICMRUPFExposureEngine()
        )

        self.additives = (
            AdditiveExposureEngine()
        )


        # ============================================================
# ELITE PART D
#
# WEEKLY EXPOSURE ENGINE
# MONTHLY EXPOSURE ENGINE
#
# Depends On:
# - LimitConstants
# - LimitMath
# - ExposureMultiplierEngine
# ============================================================


# ============================================================
# WEEKLY EXPOSURE MODELS
# ============================================================

class WeeklySugarExposureModel:

    @staticmethod
    def calculate(
        sugar_per_serving_g: float,
        servings_per_day: float
    ) -> float:

        daily_sugar = (

            sugar_per_serving_g
            *
            servings_per_day

        )

        return (

            ExposureMultiplierEngine
            .weekly(
                daily_sugar
            )

        )


class WeeklySodiumExposureModel:

    @staticmethod
    def calculate(
        sodium_mg: float,
        servings_per_day: float
    ) -> float:

        daily_sodium = (

            sodium_mg
            *
            servings_per_day

        )

        return (

            ExposureMultiplierEngine
            .weekly(
                daily_sodium
            )

        )


class WeeklyAdditiveExposureModel:

    @staticmethod
    def calculate(
        additive_count: int,
        servings_per_day: float
    ) -> float:

        daily_additives = (

            additive_count
            *
            servings_per_day

        )

        return (

            ExposureMultiplierEngine
            .weekly(
                daily_additives
            )

        )


class WeeklyRiskModel:

    @staticmethod
    def calculate(
        weekly_sugar: float,
        weekly_sodium: float,
        weekly_additives: float
    ) -> float:

        sugar_component = (

            weekly_sugar

            /

            (
                LimitConstants
                .WHO_SUGAR_LIMIT_G
                * 7
            )

        ) * 100

        sodium_component = (

            weekly_sodium

            /

            (
                LimitConstants
                .WHO_SODIUM_LIMIT_MG
                * 7
            )

        ) * 100

        additive_component = (

            weekly_additives * 2

        )

        risk = (

            sugar_component * 0.40

            +

            sodium_component * 0.35

            +

            additive_component * 0.25

        )

        return LimitMath.clamp(
            risk
        )


# ============================================================
# WEEKLY EXPOSURE ENGINE
# ============================================================

class WeeklyExposureEngine:

    def calculate(
        self,
        sugar_per_serving_g: float,
        sodium_mg: float,
        additive_count: int,
        servings_per_day: float = 1.0
    ) -> Dict:

        servings_per_day = max(
            0.0,
            servings_per_day
        )

        additive_count = max(
            0,
            additive_count
        )

        weekly_sugar = (

            WeeklySugarExposureModel
            .calculate(
                sugar_per_serving_g,
                servings_per_day
            )

        )

        weekly_sodium = (

            WeeklySodiumExposureModel
            .calculate(
                sodium_mg,
                servings_per_day
            )

        )

        weekly_additives = (

            WeeklyAdditiveExposureModel
            .calculate(
                additive_count,
                servings_per_day
            )

        )

        weekly_risk = (

            WeeklyRiskModel
            .calculate(
                weekly_sugar,
                weekly_sodium,
                weekly_additives
            )

        )

        simulation_profiles = {}

        for servings in [1, 2, 3]:

            profile_sugar = (
                sugar_per_serving_g
                *
                servings
                *
                7
            )

            profile_sodium = (
                sodium_mg
                *
                servings
                *
                7
            )

            profile_additives = (
                additive_count
                *
                servings
                *
                7
            )

            simulation_profiles[
                f"{servings}_per_day"
            ] = {

                "weekly_sugar":
                    round(
                        profile_sugar,
                        2
                    ),

                "weekly_sodium":
                    round(
                        profile_sodium,
                        2
                    ),

                "weekly_additives":
                    round(
                        profile_additives,
                        2
                    )
            }

        return {

            "weekly_sugar":
                round(
                    weekly_sugar,
                    2
                ),

            "weekly_sodium":
                round(
                    weekly_sodium,
                    2
                ),

            "weekly_additives":
                round(
                    weekly_additives,
                    2
                ),

            "weekly_risk":
                round(
                    weekly_risk,
                    2
                ),

            "simulation_profiles":
                simulation_profiles
        }

# ============================================================
# MONTHLY EXPOSURE MODELS
# ============================================================

class MonthlySugarExposureModel:

    @staticmethod
    def calculate(
        sugar_per_serving_g: float,
        servings_per_day: float
    ) -> float:

        return (

            sugar_per_serving_g

            *

            servings_per_day

            *

            30

        )


class MonthlySodiumExposureModel:

    @staticmethod
    def calculate(
        sodium_mg: float,
        servings_per_day: float
    ) -> float:

        return (

            sodium_mg

            *

            servings_per_day

            *

            30

        )


class MonthlyAdditiveExposureModel:

    @staticmethod
    def calculate(
        additive_count: int,
        servings_per_day: float
    ) -> float:

        return (

            additive_count

            *

            servings_per_day

            *

            30

        )


class MonthlyHealthBurdenModel:

    @staticmethod
    def calculate(
        monthly_sugar: float,
        monthly_sodium: float,
        monthly_additives: float
    ) -> float:

        sugar_burden = (

            monthly_sugar

            /

            (
                LimitConstants
                .WHO_SUGAR_LIMIT_G
                * 30
            )

        ) * 100

        sodium_burden = (

            monthly_sodium

            /

            (
                LimitConstants
                .WHO_SODIUM_LIMIT_MG
                * 30
            )

        ) * 100

        additive_burden = (

            monthly_additives * 1.5

        )

        burden = (

            sugar_burden * 0.40

            +

            sodium_burden * 0.35

            +

            additive_burden * 0.25

        )

        return LimitMath.clamp(
            burden
        )


# ============================================================
# MONTHLY EXPOSURE ENGINE
# ============================================================

class MonthlyExposureEngine:

    def calculate(
        self,
        sugar_per_serving_g: float,
        sodium_mg: float,
        additive_count: int,
        servings_per_day: float = 1.0
    ) -> Dict:

        servings_per_day = max(
            0.0,
            servings_per_day
        )

        additive_count = max(
            0,
            additive_count
        )

        monthly_sugar = (

            MonthlySugarExposureModel
            .calculate(
                sugar_per_serving_g,
                servings_per_day
            )

        )

        monthly_sodium = (

            MonthlySodiumExposureModel
            .calculate(
                sodium_mg,
                servings_per_day
            )

        )

        monthly_additives = (

            MonthlyAdditiveExposureModel
            .calculate(
                additive_count,
                servings_per_day
            )

        )

        monthly_health_burden = (

            MonthlyHealthBurdenModel
            .calculate(
                monthly_sugar,
                monthly_sodium,
                monthly_additives
            )

        )

        if monthly_health_burden >= 80:

            monthly_risk = "HIGH"

        elif monthly_health_burden >= 60:

            monthly_risk = "MODERATE"

        else:

            monthly_risk = "LOW"

        simulation_profiles = {}

        for servings in [1, 2, 3]:

            profile_sugar = (
                sugar_per_serving_g
                *
                servings
                *
                30
            )

            profile_sodium = (
                sodium_mg
                *
                servings
                *
                30
            )

            profile_additives = (
                additive_count
                *
                servings
                *
                30
            )

            simulation_profiles[
                f"{servings}_per_day"
            ] = {

                "monthly_sugar":
                    round(
                        profile_sugar,
                        2
                    ),

                "monthly_sodium":
                    round(
                        profile_sodium,
                        2
                    ),

                "monthly_additives":
                    round(
                        profile_additives,
                        2
                    )
            }

        return {

            "monthly_exposure": {

                "sugar":
                    round(
                        monthly_sugar,
                        2
                    ),

                "sodium":
                    round(
                        monthly_sodium,
                        2
                    ),

                "additives":
                    round(
                        monthly_additives,
                        2
                    )
            },

            "monthly_risk":
                monthly_risk,

            "monthly_health_burden":
                round(
                    monthly_health_burden,
                    2
                ),

            "simulation_profiles":
                simulation_profiles
        }
# ============================================================
# PART D REGISTRATION
# ============================================================

class LongTermExposureLayer:

    def __init__(self):

        self.weekly = (
            WeeklyExposureEngine()
        )

        self.monthly = (
            MonthlyExposureEngine()
        )


        # ============================================================
# ELITE PART E
#
# SAFE CONSUMPTION FREQUENCY ENGINE
# HEALTH DEBT ENGINE
#
# Depends On:
# - LimitConstants
# - LimitMath
# - HealthDebtLevelEngine
# - SafeFrequencyHelper
# ============================================================


# ============================================================
# SAFE CONSUMPTION MODELS
# ============================================================

class SugarFrequencyModel:

    @staticmethod
    def calculate(
        sugar_per_serving_g: float
    ) -> float:

        if sugar_per_serving_g <= 0:
            return 7.0

        return (

            LimitConstants.WHO_SUGAR_LIMIT_G

            /

            sugar_per_serving_g

        )


class SodiumFrequencyModel:

    @staticmethod
    def calculate(
        sodium_mg: float
    ) -> float:

        if sodium_mg <= 0:
            return 7.0

        return (

            LimitConstants.WHO_SODIUM_LIMIT_MG

            /

            sodium_mg

        )


class FrequencyRecommendationModel:

    @staticmethod
    def calculate(
        sugar_frequency: float,
        sodium_frequency: float,
        upf_score: float,
        additive_burden: float
    ) -> str:

        limiting_frequency = min(
            sugar_frequency,
            sodium_frequency
        )

        if upf_score >= 80:

            limiting_frequency *= 0.50

        elif upf_score >= 60:

            limiting_frequency *= 0.75

        if additive_burden >= 75:

            limiting_frequency *= 0.70

        if limiting_frequency >= 7:

            return "DAILY"

        if limiting_frequency >= 4:

            return "4-6 TIMES/WEEK"

        if limiting_frequency >= 2:

            return "1-3 TIMES/WEEK"

        if limiting_frequency >= 1:

            return "1 TIME/WEEK"

        return "OCCASIONAL ONLY"


# ============================================================
# SAFE CONSUMPTION FREQUENCY ENGINE
# ============================================================
class SafeConsumptionFrequencyEngine:

    def calculate(
        self,
        sugar_per_serving_g: float,
        sodium_mg: float,
        upf_score: float,
        additive_burden: float
    ) -> Dict:

        sugar_frequency = (

            SugarFrequencyModel
            .calculate(
                sugar_per_serving_g
            )

        )

        sodium_frequency = (

            SodiumFrequencyModel
            .calculate(
                sodium_mg
            )

        )

        safe_weekly = (

            FrequencyRecommendationModel
            .calculate(
                sugar_frequency,
                sodium_frequency,
                upf_score,
                additive_burden
            )

        )

        safe_frequency_score = min(
            sugar_frequency,
            sodium_frequency
        )

        return {

            "safe_daily":

                safe_weekly == "DAILY",

            "safe_weekly":
                safe_weekly,

            "safe_monthly":

                "OCCASIONAL ONLY"

                if safe_weekly
                in [
                    "1 TIME/WEEK"
                ]

                else

                "SAFE",

            "sugar_frequency_limit":
                round(
                    sugar_frequency,
                    2
                ),

            "sodium_frequency_limit":
                round(
                    sodium_frequency,
                    2
                ),

            "safe_frequency_score":
                round(
                    safe_frequency_score,
                    2
                )
        }


# ============================================================
# HEALTH DEBT MODELS
# ============================================================

class SugarDebtModel:

    @staticmethod
    def calculate(
        sugar_percent: float
    ) -> float:

        return LimitMath.clamp(
            sugar_percent
        )


class SodiumDebtModel:

    @staticmethod
    def calculate(
        sodium_percent: float
    ) -> float:

        return LimitMath.clamp(
            sodium_percent
        )


class UPFDebtModel:

    @staticmethod
    def calculate(
        upf_score: float
    ) -> float:

        return LimitMath.clamp(
            upf_score
        )


class AdditiveDebtModel:

    @staticmethod
    def calculate(
        additive_burden: float
    ) -> float:

        return LimitMath.clamp(
            additive_burden
        )


class HealthDebtScoreModel:

    @staticmethod
    def calculate(
        sugar_debt: float,
        sodium_debt: float,
        upf_debt: float,
        additive_debt: float
    ) -> float:

        score = (

            sugar_debt * 0.30

            +

            sodium_debt * 0.25

            +

            upf_debt * 0.25

            +

            additive_debt * 0.20

        )

        return LimitMath.clamp(
            score
        )


# ============================================================
# HEALTH DEBT ENGINE
# ============================================================

class HealthDebtEngine:

    def calculate(
        self,
        sugar_percent: float,
        sodium_percent: float,
        upf_score: float,
        additive_burden: float
    ) -> Dict:

        sugar_debt = (

            SugarDebtModel
            .calculate(
                sugar_percent
            )

        )

        sodium_debt = (

            SodiumDebtModel
            .calculate(
                sodium_percent
            )

        )

        upf_debt = (

            UPFDebtModel
            .calculate(
                upf_score
            )

        )

        additive_debt = (

            AdditiveDebtModel
            .calculate(
                additive_burden
            )

        )

        health_debt_score = (

            HealthDebtScoreModel
            .calculate(
                sugar_debt,
                sodium_debt,
                upf_debt,
                additive_debt
            )

        )

        health_debt_level = (

            HealthDebtLevelEngine
            .calculate(
                health_debt_score
            )

        )

        return {

            "sugar_debt":
                round(
                    sugar_debt,
                    2
                ),

            "sodium_debt":
                round(
                    sodium_debt,
                    2
                ),

            "upf_debt":
                round(
                    upf_debt,
                    2
                ),

            "additive_debt":
                round(
                    additive_debt,
                    2
                ),

            "health_debt_score":
                round(
                    health_debt_score,
                    2
                ),

            "health_debt_level":
                health_debt_level
        }


# ============================================================
# PART E REGISTRATION
# ============================================================

class ConsumptionIntelligenceLayer:

    def __init__(self):

        self.safe_frequency = (
            SafeConsumptionFrequencyEngine()
        )

        self.health_debt = (
            HealthDebtEngine()
        )


        # ============================================================
# ELITE PART F
#
# REGULATORY COMPLIANCE ENGINE
# CONSUMPTION SAFETY ENGINE
# EXPOSURE HEATMAP ENGINE
#
# Depends On:
# - LimitMath
# - ComplianceEngine
# - ConsumptionSafetyEngine
# - ExposureHeatmapUtils
# ============================================================


# ============================================================
# WHO COMPLIANCE MODEL
# ============================================================

class WHOComplianceModel:

    @staticmethod
    def calculate(
        sugar_percent: float,
        sodium_percent: float,
        fat_percent: float
    ) -> float:

        sugar_score = max(
            0,
            100 - sugar_percent
        )

        sodium_score = max(
            0,
            100 - sodium_percent
        )

        fat_score = max(
            0,
            100 - fat_percent
        )

        compliance = (

            sugar_score * 0.40

            +

            sodium_score * 0.35

            +

            fat_score * 0.25

        )

        return LimitMath.clamp(
            compliance
        )


# ============================================================
# ICMR COMPLIANCE MODEL
# ============================================================

class ICMRComplianceModel:

    @staticmethod
    def calculate(
        upf_score: float,
        additive_burden: float
    ) -> float:

        compliance = (

            (100 - upf_score) * 0.60

            +

            (100 - additive_burden) * 0.40

        )

        return LimitMath.clamp(
            compliance
        )


# ============================================================
# FSSAI ALIGNMENT MODEL
# ============================================================

class FSSAIAlignmentModel:

    @staticmethod
    def calculate(
        who_compliance: float,
        icmr_compliance: float
    ) -> float:

        alignment = (

            who_compliance * 0.55

            +

            icmr_compliance * 0.45

        )

        return LimitMath.clamp(
            alignment
        )


# ============================================================
# REGULATORY COMPLIANCE ENGINE
# ============================================================

class RegulatoryComplianceEngine:

    def calculate(
        self,
        sugar_percent: float,
        sodium_percent: float,
        fat_percent: float,
        upf_score: float,
        additive_burden: float
    ) -> Dict:

        who_compliance = (

            WHOComplianceModel
            .calculate(
                sugar_percent,
                sodium_percent,
                fat_percent
            )

        )

        icmr_compliance = (

            ICMRComplianceModel
            .calculate(
                upf_score,
                additive_burden
            )

        )

        fssai_alignment = (

            FSSAIAlignmentModel
            .calculate(
                who_compliance,
                icmr_compliance
            )

        )

        regulatory_score = (

            who_compliance * 0.40

            +

            icmr_compliance * 0.35

            +

            fssai_alignment * 0.25

        )

        regulatory_score = (
            LimitMath.clamp(
                regulatory_score
            )
        )

        regulatory_verdict = (

            ComplianceEngine
            .compliance(
                regulatory_score
            )

        )

        return {

            "who_compliance":
                round(
                    who_compliance,
                    2
                ),

            "icmr_compliance":
                round(
                    icmr_compliance,
                    2
                ),

            "fssai_alignment":
                round(
                    fssai_alignment,
                    2
                ),

            "regulatory_score":
                round(
                    regulatory_score,
                    2
                ),

                "compliance_gap":
    round(
        100 - regulatory_score,
        2
    ),

            "regulatory_verdict":
                regulatory_verdict
        }


# ============================================================
# CONSUMPTION SAFETY SCORE MODEL
# ============================================================

class ConsumptionSafetyScoreModel:

    @staticmethod
    def calculate(
        weekly_risk: float,
        monthly_health_burden: float,
        health_debt_score: float
    ) -> float:

        score = (

            (100 - weekly_risk) * 0.30

            +

            (100 - monthly_health_burden) * 0.40

            +

            (100 - health_debt_score) * 0.30

        )

        return LimitMath.clamp(
            score
        )


# ============================================================
# CONSUMPTION SAFETY ENGINE
# ============================================================

class ProductConsumptionSafetyEngine:

    def calculate(
        self,
        weekly_risk: float,
        monthly_health_burden: float,
        health_debt_score: float
    ) -> Dict:

        safety_score = (

            ConsumptionSafetyScoreModel
            .calculate(
                weekly_risk,
                monthly_health_burden,
                health_debt_score
            )

        )

        safety_verdict = (

            ConsumptionSafetyEngine
            .classify(
                safety_score
            )

        )

        return {

            "consumption_safety_score":
                round(
                    safety_score,
                    2
                ),

            "consumption_safety":
                safety_verdict
        }


# ============================================================
# EXPOSURE HEATMAP ENGINE
# ============================================================

class ExposureHeatmapEngine:

    def generate(
        self,
        sugar_percent: float,
        sodium_percent: float,
        fat_percent: float,
        additive_burden: float,
        upf_score: float
    ) -> Dict:

        sugar_score = max(
            0,
            100 - sugar_percent
        )

        sodium_score = max(
            0,
            100 - sodium_percent
        )

        fat_score = max(
            0,
            100 - fat_percent
        )

        additive_score = max(
            0,
            100 - additive_burden
        )

        upf_alignment = max(
            0,
            100 - upf_score
        )

        return {

            "sugar":

                ExposureHeatmapUtils
                .zone(
                    sugar_score
                ),

            "sodium":

                ExposureHeatmapUtils
                .zone(
                    sodium_score
                ),

            "fat":

                ExposureHeatmapUtils
                .zone(
                    fat_score
                ),

            "additives":

                ExposureHeatmapUtils
                .zone(
                    additive_score
                ),

            "upf":

                ExposureHeatmapUtils
                .zone(
                    upf_alignment
                )
        }


# ============================================================
# PART F REGISTRATION
# ============================================================

class RegulatorySafetyLayer:

    def __init__(self):

        self.compliance = (
            RegulatoryComplianceEngine()
        )

        self.safety = (
            ProductConsumptionSafetyEngine()
        )

        self.heatmap = (
            ExposureHeatmapEngine()
        )


        # ============================================================
# ELITE PART G
#
# OVERALL LIMIT SCORE ENGINE
# OVERALL LIMIT VERDICT ENGINE
#
# MASTER LIMIT ENGINE
#
# FINAL AGGREGATOR
# ============================================================


# ============================================================
# OVERALL LIMIT SCORE ENGINE
# ============================================================

class OverallLimitScoreEngine:

    @staticmethod
    def calculate(
        who_sugar_percent: float,
        who_sodium_percent: float,
        fat_percent: float,
        upf_score: float,
        additive_burden: float,
        health_debt_score: float,
        regulatory_score: float
    ) -> float:

        sugar_component = max(
            0,
            max(
    0,
    100 - who_sugar_percent
)
        )

        sodium_component = max(
            0,
            100 - who_sodium_percent
        )

        fat_component = max(
            0,
            100 - fat_percent
        )

        upf_component = max(
            0,
            100 - upf_score
        )

        additive_component = max(
            0,
            100 - additive_burden
        )

        debt_component = max(
            0,
            100 - health_debt_score
        )

        score = (

            sugar_component * 0.15

            +

            sodium_component * 0.15

            +

            fat_component * 0.10

            +

            upf_component * 0.15

            +

            additive_component * 0.10

            +

            debt_component * 0.15

            +

            regulatory_score * 0.20

        )

        return round(

            LimitMath.clamp(
                score
            ),

            2
        )


# ============================================================
# OVERALL LIMIT VERDICT ENGINE
# ============================================================

class OverallLimitVerdictEngine:

    @staticmethod
    def generate(
        score: float
    ) -> str:

        if score >= 90:

            return (
                "EXCELLENT"
            )

        if score >= 80:

            return (
                "GOOD"
            )

        if score >= 65:

            return (
                "MODERATE"
            )

        if score >= 50:

            return (
                "POOR"
            )

        return (
            "HIGH_RISK"
        )


# ============================================================
# MASTER LIMIT ENGINE
# ============================================================

class LimitEngine:

    def __init__(self):

        self.sugar_engine = (
            WHOSugarExposureEngine()
        )

        self.sodium_engine = (
            WHOSodiumExposureEngine()
        )

        self.fat_engine = (
            WHOSaturatedFatExposureEngine()
        )

        self.upf_engine = (
            ICMRUPFExposureEngine()
        )

        self.additive_engine = (
            AdditiveExposureEngine()
        )

        self.weekly_engine = (
            WeeklyExposureEngine()
        )

        self.monthly_engine = (
            MonthlyExposureEngine()
        )

        self.safe_frequency_engine = (
            SafeConsumptionFrequencyEngine()
        )

        self.health_debt_engine = (
            HealthDebtEngine()
        )

        self.regulatory_engine = (
            RegulatoryComplianceEngine()
        )

        self.safety_engine = (
            ProductConsumptionSafetyEngine()
        )

        self.heatmap_engine = (
            ExposureHeatmapEngine()
        )

    def analyze(
        self,
        limit_inputs: Dict
    ) -> Dict:

        # ====================================================
        # INPUT VALIDATION
        # ====================================================

        required_fields = [

            "sugar_per_serving_g",
            "sodium_mg",
            "saturated_fat_g",
            "trans_fat_g",

            "processing_score",
            "additive_score",
            "emulsifier_score",

            "artificial_ingredient_count",

            "additive_count",
            "low_risk_additives",
            "moderate_risk_additives",
            "high_risk_additives",

            "servings_per_day"
        ]

        missing = [

            field

            for field in required_fields

            if field not in limit_inputs

        ]

        if missing:

            raise ValueError(
                f"Missing limit inputs: {missing}"
            )

        # ====================================================
        # NUMERIC VALIDATION
        # ====================================================

        for field in required_fields:

            if limit_inputs[field] is None:

                raise ValueError(
                    f"{field} cannot be None"
                )

        # ====================================================
        # WHO ENGINES
        # ====================================================

        who_sugar = (

            self.sugar_engine
            .calculate(

                sugar_per_serving_g=
                    limit_inputs[
                        "sugar_per_serving_g"
                    ],

                servings_per_day=
                    limit_inputs[
                        "servings_per_day"
                    ]
            )
        )

        who_sodium = (

            self.sodium_engine
            .calculate(

                sodium_mg=
                    limit_inputs[
                        "sodium_mg"
                    ],

                servings_per_day=
                    limit_inputs[
                        "servings_per_day"
                    ]
            )
        )

        who_fat = (

            self.fat_engine
            .calculate(

                saturated_fat_g=
                    limit_inputs[
                        "saturated_fat_g"
                    ],

                trans_fat_g=
                    limit_inputs[
                        "trans_fat_g"
                    ],

                servings_per_day=
                    limit_inputs[
                        "servings_per_day"
                    ]
            )
        )

        # ====================================================
        # UPF
        # ====================================================

        upf = (

            self.upf_engine
            .calculate(

                processing_score=
                    limit_inputs[
                        "processing_score"
                    ],

                additive_score=
                    limit_inputs[
                        "additive_score"
                    ],

                emulsifier_score=
                    limit_inputs[
                        "emulsifier_score"
                    ],

                artificial_ingredient_count=
                    limit_inputs[
                        "artificial_ingredient_count"
                    ]
            )
        )

        # ====================================================
        # ADDITIVES
        # ====================================================

        additives = (

            self.additive_engine
            .calculate(

                additive_count=
                    limit_inputs[
                        "additive_count"
                    ],

                low_risk_additives=
                    limit_inputs[
                        "low_risk_additives"
                    ],

                moderate_risk_additives=
                    limit_inputs[
                        "moderate_risk_additives"
                    ],

                high_risk_additives=
                    limit_inputs[
                        "high_risk_additives"
                    ],

                servings_per_day=
                    limit_inputs[
                        "servings_per_day"
                    ]
            )
        )

        # ====================================================
        # WEEKLY
        # ====================================================

        weekly_exposure = (

            self.weekly_engine
            .calculate(

                sugar_per_serving_g=
                    limit_inputs[
                        "sugar_per_serving_g"
                    ],

                sodium_mg=
                    limit_inputs[
                        "sodium_mg"
                    ],

                additive_count=
                    limit_inputs[
                        "additive_count"
                    ],

                servings_per_day=
                    limit_inputs[
                        "servings_per_day"
                    ]
            )
        )

        # ====================================================
        # MONTHLY
        # ====================================================

        monthly_exposure = (

            self.monthly_engine
            .calculate(

                sugar_per_serving_g=
                    limit_inputs[
                        "sugar_per_serving_g"
                    ],

                sodium_mg=
                    limit_inputs[
                        "sodium_mg"
                    ],

                additive_count=
                    limit_inputs[
                        "additive_count"
                    ],

                servings_per_day=
                    limit_inputs[
                        "servings_per_day"
                    ]
            )
        )

        # ====================================================
        # SAFE FREQUENCY
        # ====================================================

        safe_frequency = (

            self.safe_frequency_engine
            .calculate(

                sugar_per_serving_g=
                    limit_inputs[
                        "sugar_per_serving_g"
                    ],

                sodium_mg=
                    limit_inputs[
                        "sodium_mg"
                    ],

                upf_score=
                    upf[
                        "upf_score"
                    ],

                additive_burden=
                    additives[
                        "cumulative_additive_burden"
                    ]
            )
        )

        # ====================================================
        # HEALTH DEBT
        # ====================================================

        health_debt = (

            self.health_debt_engine
            .calculate(

                sugar_percent=
                    who_sugar[
                        "who_sugar_limit_percent"
                    ],

                sodium_percent=
                    who_sodium[
                        "who_sodium_limit_percent"
                    ],

                upf_score=
                    upf[
                        "upf_score"
                    ],

                additive_burden=
                    additives[
                        "cumulative_additive_burden"
                    ]
            )
        )

        # ====================================================
        # REGULATORY
        # ====================================================

        regulatory = (

            self.regulatory_engine
            .calculate(

                sugar_percent=
                    who_sugar[
                        "who_sugar_limit_percent"
                    ],

                sodium_percent=
                    who_sodium[
                        "who_sodium_limit_percent"
                    ],

                fat_percent=
                    who_fat[
                        "fat_limit_percent"
                    ],

                upf_score=
                    upf[
                        "upf_score"
                    ],

                additive_burden=
                    additives[
                        "cumulative_additive_burden"
                    ]
            )
        )

        # ====================================================
        # SAFETY
        # ====================================================

        consumption_safety = (

            self.safety_engine
            .calculate(

                weekly_risk=
                    weekly_exposure[
                        "weekly_risk"
                    ],

                monthly_health_burden=
                    monthly_exposure[
                        "monthly_health_burden"
                    ],

                health_debt_score=
                    health_debt[
                        "health_debt_score"
                    ]
            )
        )

        # ====================================================
        # HEATMAP
        # ====================================================

        exposure_heatmap = (

            self.heatmap_engine
            .generate(

                sugar_percent=
                    who_sugar[
                        "who_sugar_limit_percent"
                    ],

                sodium_percent=
                    who_sodium[
                        "who_sodium_limit_percent"
                    ],

                fat_percent=
                    who_fat[
                        "fat_limit_percent"
                    ],

                additive_burden=
                    additives[
                        "cumulative_additive_burden"
                    ],

                upf_score=
                    upf[
                        "upf_score"
                    ]
            )
        )

        # ====================================================
        # FINAL SCORE
        # ====================================================

        overall_limit_score = (

            OverallLimitScoreEngine
            .calculate(

                who_sugar_percent=
                    who_sugar[
                        "who_sugar_limit_percent"
                    ],

                who_sodium_percent=
                    who_sodium[
                        "who_sodium_limit_percent"
                    ],

                fat_percent=
                    who_fat[
                        "fat_limit_percent"
                    ],

                upf_score=
                    upf[
                        "upf_score"
                    ],

                additive_burden=
                    additives[
                        "cumulative_additive_burden"
                    ],

                health_debt_score=
                    health_debt[
                        "health_debt_score"
                    ],

                regulatory_score=
                    regulatory[
                        "regulatory_score"
                    ]
            )
        )

        overall_limit_verdict = (

            OverallLimitVerdictEngine
            .generate(
                overall_limit_score
            )

        )

        # ====================================================
        # FINAL RESPONSE
        # ====================================================

        return {

            "who_sugar":
                who_sugar,

            "who_sodium":
                who_sodium,

            "who_fat":
                who_fat,

            "upf":
                upf,

            "additives":
                additives,

            "weekly_exposure":
                weekly_exposure,

            "monthly_exposure":
                monthly_exposure,

            "safe_frequency":
                safe_frequency,

            "health_debt":
                health_debt,

            "regulatory_compliance":
                regulatory,

            "consumption_safety":
                consumption_safety,

            "exposure_heatmap":
                exposure_heatmap,

            "overall_limit_score":
                overall_limit_score,

            "overall_limit_verdict":
                overall_limit_verdict,

            "engine_version":
                "1.0.0",

            "engine":
                "SCANIX_LIMIT_ENGINE"
        }


# ============================================================
# SINGLETON EXPORT
# ============================================================

limit_engine = (
    LimitEngine()
)