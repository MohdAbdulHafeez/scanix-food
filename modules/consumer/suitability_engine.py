# ==========================================================
# SCANIX AI
# SYSTEM 4 – CONSUMER INTELLIGENCE (SUITABILITY ENGINE)
# ELITE PRODUCTION GRADE – FINAL VERSION
# ==========================================================


from __future__ import annotations


from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple


# ==========================================================
# CONSTANTS
# ==========================================================


DEFAULT_SCORE = 50
DEFAULT_CONFIDENCE = 50
DEFAULT_PERCENTAGE = 50

SUGAR_HIGH_THRESHOLD = 15
SODIUM_HIGH_THRESHOLD = 600

PROTEIN_HIGH_THRESHOLD = 10
FIBER_HIGH_THRESHOLD = 5

CARBOHYDRATE_HIGH_THRESHOLD = 20
CARBOHYDRATE_VERY_HIGH_THRESHOLD = 40

FAT_HIGH_THRESHOLD = 15

ADDITIVE_COUNT_HIGH_THRESHOLD = 3
ADDITIVE_COUNT_VERY_HIGH_THRESHOLD = 5
ADDITIVE_COUNT_EXTREME_THRESHOLD = 6

DECEPTION_HIGH_THRESHOLD = 50
COMPLIANCE_LOW_THRESHOLD = 70

DIABETIC_RISK_HIGH_THRESHOLD = 70
HEART_RISK_HIGH_THRESHOLD = 60

PROCESSING_ULTRA = "ULTRA_PROCESSED"

KETO_SCORE_BASE = 100
KETO_CARBS_THRESHOLDS = {

    40: 80,
    20: 60,
    10: 40,
    5: 20,

}
KETO_SUGAR_THRESHOLD = 5

SCORE_LABEL_THRESHOLDS = {

    "EXCELLENT": 85,
    "GOOD": 70,
    "MODERATE": 55,
    "POOR": 40,
    "AVOID": 0,

}

GRADE_THRESHOLDS = {

    "A+": 90,
    "A": 80,
    "B": 70,
    "C": 55,
    "D": 40,
    "F": 0,

}

BUY_DECISION_THRESHOLDS = {

    "STRONGLY_RECOMMENDED": 85,
    "RECOMMENDED": 70,
    "BUY_OCCASIONALLY": 55,
    "LIMIT_CONSUMPTION": 40,
    "AVOID": 0,

}

FREQUENCY_THRESHOLDS = {

    "DAILY": 10,
    "SEVERAL_TIMES_PER_WEEK": 5,
    "OCCASIONALLY": 2,
    "RARELY": 0,

}

DIABETIC_SCORE_PENALTIES = {

    "ULTRA_PROCESSED": 25,
    "ADDITIVE_COUNT": 10,
    "SUGAR_HIGH": 15,
    "CARBS_HIGH": 20,

}

HEART_SCORE_PENALTIES = {

    "SODIUM_HIGH": 15,
    "SODIUM_VERY_HIGH": 15,
    "PALM_OIL": 15,
    "ULTRA_PROCESSED": 20,

}

HYPERTENSION_PENALTIES = {

    "SODIUM_200": 10,
    "SODIUM_400": 20,
    "SODIUM_600": 25,
    "SODIUM_800": 20,
    "ULTRA_PROCESSED": 10,
    "ADDITIVE_COUNT": 5,

}

METABOLIC_SYNDROME_PENALTIES = {

    "SUGAR_HIGH": 15,
    "FAT_HIGH": 15,
    "ULTRA_PROCESSED": 20,
    "ADDITIVE_COUNT_HIGH": 10,

}

CHILDREN_SCORE_PENALTIES = {

    "SUGAR_VERY_HIGH": 25,
    "SUGAR_HIGH": 15,
    "SODIUM_HIGH": 15,
    "SODIUM_VERY_HIGH": 15,
    "ADDITIVE_COUNT": 15,
    "ADDITIVE_COUNT_HIGH": 10,
    "ULTRA_PROCESSED": 20,
    "PALM_OIL": 5,
    "DIABETIC_RISK": 10,
    "HEART_RISK": 10,
    "DECEPTION": 10,

}

ADULT_SCORE_PENALTIES = {

    "SUGAR_HIGH": 15,
    "SODIUM_HIGH": 15,
    "ADDITIVE_COUNT_HIGH": 10,

}

ELDERLY_PENALTIES = {

    "SODIUM_HIGH": 20,
    "SUGAR_HIGH": 15,
    "ULTRA_PROCESSED": 15,
    "ADDITIVE_COUNT": 10,

}

PREGNANCY_PENALTIES = {

    "SODIUM_HIGH": 15,
    "ADDITIVE_COUNT": 15,
    "ULTRA_PROCESSED": 15,

}

KETO_PENALTIES = {

    "CARBS_VERY_HIGH": 80,
    "CARBS_HIGH": 60,
    "CARBS_MODERATE": 40,
    "CARBS_LOW": 20,
    "SUGAR_HIGH": 30,

}

WORKOUT_BONUSES = {

    "PRE_CALORIES": 15,
    "PRE_PROTEIN": 15,
    "PRE_LOW_SUGAR": 10,
    "PRE_HIGH_FAT": -15,

    "POST_PROTEIN_HIGH": 30,
    "POST_PROTEIN_MODERATE": 15,
    "POST_CALORIES": 10,
    "POST_SUGAR_HIGH": -10,

}

RECOVERY_BONUSES = {

    "PROTEIN_HIGH": 20,
    "FIBER_HIGH": 10,
    "ULTRA_PROCESSED": -15,

}

OFFICE_SNACK_PENALTIES = {

    "SUGAR_HIGH": 20,
    "SODIUM_HIGH": 15,
    "ULTRA_PROCESSED": 15,

}

LATE_NIGHT_PENALTIES = {

    "CALORIES_HIGH": 20,
    "SUGAR_HIGH": 20,
    "FAT_HIGH": 15,

}

TRAVEL_FOOD_PENALTIES = {

    "SODIUM_VERY_HIGH": 15,
    "ADDITIVE_COUNT_EXTREME": 10,

}

DAILY_LIMIT_BASE = 3
DAILY_LIMIT_ULTRA = 1
DAILY_LIMIT_SUGAR = 1
DAILY_LIMIT_SODIUM = 1

WEEKLY_LIMIT_BASE = 14
WEEKLY_LIMIT_ULTRA = 3
WEEKLY_LIMIT_SUGAR = 4
WEEKLY_LIMIT_SODIUM = 3
WEEKLY_LIMIT_ADDITIVES = 2


# ==========================================================
# SUITABILITY ENGINE
# ==========================================================


class SuitabilityEngine:
    """
    Suitability Engine for System 4 – Consumer Intelligence.

    Evaluates product suitability across:
    - Health goals (weight loss, muscle gain, keto, etc.)
    - Health conditions (diabetic, heart, hypertension, metabolic syndrome)
    - Demographics (children, teenagers, adults, elderly, pregnancy)
    - Lifestyles (pre/post workout, office snack, late night, cheat meal, travel)
    - Overall score, grade, buy decision, and consumption frequency
    """

    def _safe_float(
        self,
        value: Any,
        default: float = 0.0,
    ) -> float:
        """
        Safely convert value to float.

        Args:
            value: Value to convert
            default: Default value if conversion fails

        Returns:
            Float value or default
        """

        try:

            if value is None:

                return default

            return float(value)

        except Exception:

            return default

    def _safe_int(
        self,
        value: Any,
        default: int = 0,
    ) -> int:
        """
        Safely convert value to integer.

        Args:
            value: Value to convert
            default: Default value if conversion fails

        Returns:
            Integer value or default
        """

        try:

            if value is None:

                return default

            return int(value)

        except Exception:

            return default

    def _normalize_score(
        self,
        score: float,
        max_score: int = 100,
        min_score: int = 0,
    ) -> int:
        """
        Normalize score to specified range.

        Args:
            score: Raw score
            max_score: Maximum allowed value
            min_score: Minimum allowed value

        Returns:
            Normalized score
        """

        return max(
            min_score,
            min(
                max_score,
                self._safe_int(score),
            ),
        )

    def _get_label(
        self,
        score: int,
    ) -> str:
        """
        Get label based on score.

        Args:
            score: Score (0-100)

        Returns:
            Label string (EXCELLENT, GOOD, MODERATE, POOR, AVOID, or UNKNOWN)
        """

        if score >= SCORE_LABEL_THRESHOLDS["EXCELLENT"]:
            return "EXCELLENT"
        if score >= SCORE_LABEL_THRESHOLDS["GOOD"]:
            return "GOOD"
        if score >= SCORE_LABEL_THRESHOLDS["MODERATE"]:
            return "MODERATE"
        if score >= SCORE_LABEL_THRESHOLDS["POOR"]:
            return "POOR"
        return "AVOID"

    def _get_grade(
        self,
        score: int,
    ) -> str:
        """
        Get letter grade based on score.

        Args:
            score: Score (0-100)

        Returns:
            Letter grade (A+, A, B, C, D, or F)
        """

        if score >= GRADE_THRESHOLDS["A+"]:
            return "A+"
        if score >= GRADE_THRESHOLDS["A"]:
            return "A"
        if score >= GRADE_THRESHOLDS["B"]:
            return "B"
        if score >= GRADE_THRESHOLDS["C"]:
            return "C"
        if score >= GRADE_THRESHOLDS["D"]:
            return "D"
        return "F"

    def _get_buy_decision(
        self,
        score: int,
    ) -> str:
        """
        Get buy decision based on score.

        Args:
            score: Score (0-100)

        Returns:
            Buy decision string
        """

        if score >= BUY_DECISION_THRESHOLDS["STRONGLY_RECOMMENDED"]:
            return "STRONGLY_RECOMMENDED"
        if score >= BUY_DECISION_THRESHOLDS["RECOMMENDED"]:
            return "RECOMMENDED"
        if score >= BUY_DECISION_THRESHOLDS["BUY_OCCASIONALLY"]:
            return "BUY_OCCASIONALLY"
        if score >= BUY_DECISION_THRESHOLDS["LIMIT_CONSUMPTION"]:
            return "LIMIT_CONSUMPTION"
        return "AVOID"

    def _get_frequency(
        self,
        weekly_limit: int,
    ) -> str:
        """
        Get consumption frequency based on weekly limit.

        Args:
            weekly_limit: Weekly consumption limit

        Returns:
            Frequency string
        """

        if weekly_limit >= FREQUENCY_THRESHOLDS["DAILY"]:
            return "DAILY"
        if weekly_limit >= FREQUENCY_THRESHOLDS["SEVERAL_TIMES_PER_WEEK"]:
            return "SEVERAL_TIMES_PER_WEEK"
        if weekly_limit >= FREQUENCY_THRESHOLDS["OCCASIONALLY"]:
            return "OCCASIONALLY"
        return "RARELY"

    def _unique_sorted(
        self,
        items: List[str],
    ) -> List[str]:
        """
        Return unique sorted list.

        Args:
            items: List of items

        Returns:
            Unique sorted list
        """

        return sorted(
            list(
                set(items)
            )
        )

    def analyze(
        self,
        nutrition: Dict[str, Any],
        ingredient_intelligence: Dict[str, Any],
        metabolic_intelligence: Dict[str, Any],
        impact_result: Dict[str, Any],
        compliance: Dict[str, Any],
        deception: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Master analysis method for suitability.

        Args:
            nutrition: Nutrition data (per 100g)
            ingredient_intelligence: Ingredient analysis from System 2
            metabolic_intelligence: Metabolic analysis from System 3
            impact_result: Impact analysis from System 3
            compliance: Compliance analysis from System 4
            deception: Deception analysis from System 8

        Returns:
            Complete suitability analysis
        """

        nutrition = nutrition or {}

        nutrition_confidence = self._safe_float(
            nutrition.get(
                "nutrition_confidence",
                0,
            )
        )

        sugar = self._safe_float(
            nutrition.get(
                "sugar",
                0,
            )
        )

        protein = self._safe_float(
            nutrition.get(
                "protein",
                0,
            )
        )

        fiber = self._safe_float(
            nutrition.get(
                "fiber",
                0,
            )
        )

        fat = self._safe_float(
            nutrition.get(
                "fat",
                0,
            )
        )

        sodium = self._safe_float(
            nutrition.get(
                "sodium",
                0,
            )
        )

        calories = self._safe_float(
            nutrition.get(
                "calories",
                0,
            )
        )

        carbohydrates = self._safe_float(
            nutrition.get(
                "carbohydrates",
                0,
            )
        )

        processing_level = (

            ingredient_intelligence
            .get(
                "processing_analysis",
                {},
            )
            .get(
                "processing_level",
                "UNKNOWN",
            )

        )

        additive_count = self._safe_int(

            ingredient_intelligence
            .get(
                "ingredient_summary",
                {},
            )
            .get(
                "additive_candidates",
                ingredient_intelligence.get("additive_count", 0),
            )

        )

        deception_score = self._safe_int(

            deception.get(
                "deception_score",
                deception.get("overall_score", 0),
            )

        )

        compliance_score = self._safe_int(

            compliance.get(
                "compliance_score",
                compliance.get("fssai_score", DEFAULT_SCORE),
            )

        )

        satiety_score = self._safe_int(

            metabolic_intelligence
            .get(
                "satiety",
                {},
            )
            .get(
                "score",
                DEFAULT_SCORE,
            )

        )

        metabolic_load_score = self._safe_int(

            metabolic_intelligence
            .get(
                "metabolic_load",
                {},
            )
            .get(
                "score",
                DEFAULT_SCORE,
            )

        )

        metabolic_score = self._normalize_score(

            (satiety_score + (100 - metabolic_load_score)) // 2

        )

        positive_signals: List[str] = []
        negative_signals: List[str] = []
        risk_flags: List[str] = []

        personas = impact_result.get(
            "personas",
            {},
        )

        # =====================================================
        # WEIGHT LOSS
        # =====================================================

        weight_loss_score = self._safe_int(

            personas.get(
                "weight_loss",
                {},
            )
            .get(
                "score",
                DEFAULT_SCORE,
            )

        )

        if fiber >= FIBER_HIGH_THRESHOLD:
            positive_signals.append("HIGH_FIBER")

        if protein >= PROTEIN_HIGH_THRESHOLD:
            positive_signals.append("HIGH_PROTEIN")

        if processing_level == PROCESSING_ULTRA:
            risk_flags.append("ULTRA_PROCESSED")

        # =====================================================
        # FAT LOSS
        # =====================================================

        fat_loss_score = weight_loss_score

        if sodium > 500:
            fat_loss_score -= 10

        fat_loss_score = self._normalize_score(fat_loss_score)

        # =====================================================
        # MUSCLE GAIN
        # =====================================================

        muscle_gain_score = self._safe_int(

            personas.get(
                "muscle_building",
                {},
            )
            .get(
                "score",
                DEFAULT_SCORE,
            )

        )

        # =====================================================
        # LEAN BULK
        # =====================================================

        lean_bulk_score = muscle_gain_score

        if fat > FAT_HIGH_THRESHOLD:
            lean_bulk_score -= 10

        if sugar > SUGAR_HIGH_THRESHOLD:
            lean_bulk_score -= 10

        lean_bulk_score = self._normalize_score(lean_bulk_score)

        # =====================================================
        # DIABETIC
        # =====================================================

        diabetic_risk_score = self._safe_int(

            personas.get(
                "diabetic",
                {},
            )
            .get(
                "risk_score",
                DEFAULT_SCORE,
            )

        )

        diabetic_score = max(
            0,
            100 - diabetic_risk_score,
        )

        if processing_level == PROCESSING_ULTRA:
            diabetic_score -= DIABETIC_SCORE_PENALTIES["ULTRA_PROCESSED"]

        if additive_count >= ADDITIVE_COUNT_HIGH_THRESHOLD:
            diabetic_score -= DIABETIC_SCORE_PENALTIES["ADDITIVE_COUNT"]

        if sugar > SUGAR_HIGH_THRESHOLD:
            diabetic_score -= DIABETIC_SCORE_PENALTIES["SUGAR_HIGH"]

        if carbohydrates > CARBOHYDRATE_HIGH_THRESHOLD:
            diabetic_score -= DIABETIC_SCORE_PENALTIES["CARBS_HIGH"]

        diabetic_score = self._normalize_score(diabetic_score)

        # =====================================================
        # HEART HEALTH
        # =====================================================

        heart_risk_score = self._safe_int(

            personas.get(
                "heart",
                {},
            )
            .get(
                "risk_score",
                DEFAULT_SCORE,
            )

        )

        heart_score = max(
            0,
            100 - heart_risk_score,
        )

        contains_palm = (

            ingredient_intelligence
            .get(
                "ingredient_profile",
                {},
            )
            .get(
                "contains_palm_oil",
                False,
            )

        )

        if sodium > 400:
            heart_score -= HEART_SCORE_PENALTIES["SODIUM_HIGH"]

        if sodium > 700:
            heart_score -= HEART_SCORE_PENALTIES["SODIUM_VERY_HIGH"]

        if contains_palm:
            heart_score -= HEART_SCORE_PENALTIES["PALM_OIL"]

        if processing_level == PROCESSING_ULTRA:
            heart_score -= HEART_SCORE_PENALTIES["ULTRA_PROCESSED"]

        heart_score = self._normalize_score(heart_score)

        # =====================================================
        # HYPERTENSION
        # =====================================================

        hypertension_score = 100

        if sodium >= 200:
            hypertension_score -= HYPERTENSION_PENALTIES["SODIUM_200"]

        if sodium >= 400:
            hypertension_score -= HYPERTENSION_PENALTIES["SODIUM_400"]

        if sodium >= 600:
            hypertension_score -= HYPERTENSION_PENALTIES["SODIUM_600"]

        if sodium >= 800:
            hypertension_score -= HYPERTENSION_PENALTIES["SODIUM_800"]

        if processing_level == PROCESSING_ULTRA:
            hypertension_score -= HYPERTENSION_PENALTIES["ULTRA_PROCESSED"]

        if additive_count >= ADDITIVE_COUNT_HIGH_THRESHOLD:
            hypertension_score -= HYPERTENSION_PENALTIES["ADDITIVE_COUNT"]

        hypertension_score = self._normalize_score(hypertension_score)

        # =====================================================
        # METABOLIC SYNDROME
        # =====================================================

        metabolic_syndrome_score = 100

        if sugar > SUGAR_HIGH_THRESHOLD:
            metabolic_syndrome_score -= METABOLIC_SYNDROME_PENALTIES["SUGAR_HIGH"]

        if fat > FAT_HIGH_THRESHOLD:
            metabolic_syndrome_score -= METABOLIC_SYNDROME_PENALTIES["FAT_HIGH"]

        if processing_level == PROCESSING_ULTRA:
            metabolic_syndrome_score -= METABOLIC_SYNDROME_PENALTIES["ULTRA_PROCESSED"]

        if additive_count >= ADDITIVE_COUNT_VERY_HIGH_THRESHOLD:
            metabolic_syndrome_score -= METABOLIC_SYNDROME_PENALTIES["ADDITIVE_COUNT_HIGH"]

        metabolic_syndrome_score = self._normalize_score(metabolic_syndrome_score)

        # =====================================================
        # KETO
        # =====================================================

        if nutrition_confidence < 50 or carbohydrates <= 0:

            keto_score = DEFAULT_SCORE
            keto_label = "UNKNOWN"

        else:

            keto_score = KETO_SCORE_BASE

            if carbohydrates > CARBOHYDRATE_VERY_HIGH_THRESHOLD:
                keto_score -= KETO_PENALTIES["CARBS_VERY_HIGH"]

            elif carbohydrates > CARBOHYDRATE_HIGH_THRESHOLD:
                keto_score -= KETO_PENALTIES["CARBS_HIGH"]

            elif carbohydrates > 10:
                keto_score -= KETO_PENALTIES["CARBS_MODERATE"]

            elif carbohydrates > 5:
                keto_score -= KETO_PENALTIES["CARBS_LOW"]

            if sugar > KETO_SUGAR_THRESHOLD:
                keto_score -= KETO_PENALTIES["SUGAR_HIGH"]

            keto_score = self._normalize_score(keto_score)
            keto_label = self._get_label(keto_score)

        # =====================================================
        # SYSTEM INTELLIGENCE FLAGS
        # =====================================================

        if deception_score >= DECEPTION_HIGH_THRESHOLD:
            risk_flags.append("HIGH_DECEPTION")

        if compliance_score < COMPLIANCE_LOW_THRESHOLD:
            risk_flags.append("LOW_COMPLIANCE")

        if additive_count >= ADDITIVE_COUNT_VERY_HIGH_THRESHOLD:
            risk_flags.append("HIGH_ADDITIVES")

        if sugar > SUGAR_HIGH_THRESHOLD:
            negative_signals.append("HIGH_SUGAR")

        if sodium > SODIUM_HIGH_THRESHOLD:
            negative_signals.append("HIGH_SODIUM")

        # =====================================================
        # CHILDREN SUITABILITY
        # =====================================================

        if nutrition_confidence < 50:

            children_score = DEFAULT_SCORE
            children_label = "UNKNOWN"

        else:

            children_score = 100

            diabetic_risk = self._safe_int(
                personas.get(
                    "diabetic",
                    {},
                )
                .get(
                    "risk_score",
                    DEFAULT_SCORE,
                )
            )

            heart_risk = self._safe_int(
                personas.get(
                    "heart",
                    {},
                )
                .get(
                    "risk_score",
                    DEFAULT_SCORE,
                )
            )

            contains_palm = (
                ingredient_intelligence
                .get(
                    "ingredient_profile",
                    {},
                )
                .get(
                    "contains_palm_oil",
                    False,
                )
            )

            if sugar > 20:
                children_score -= CHILDREN_SCORE_PENALTIES["SUGAR_VERY_HIGH"]

            elif sugar > SUGAR_HIGH_THRESHOLD:
                children_score -= CHILDREN_SCORE_PENALTIES["SUGAR_HIGH"]

            if sodium > 400:
                children_score -= CHILDREN_SCORE_PENALTIES["SODIUM_HIGH"]

            if sodium > 700:
                children_score -= CHILDREN_SCORE_PENALTIES["SODIUM_VERY_HIGH"]

            if additive_count >= ADDITIVE_COUNT_HIGH_THRESHOLD:
                children_score -= CHILDREN_SCORE_PENALTIES["ADDITIVE_COUNT"]

            if additive_count >= ADDITIVE_COUNT_VERY_HIGH_THRESHOLD:
                children_score -= CHILDREN_SCORE_PENALTIES["ADDITIVE_COUNT_HIGH"]

            if processing_level == PROCESSING_ULTRA:
                children_score -= CHILDREN_SCORE_PENALTIES["ULTRA_PROCESSED"]

            if contains_palm:
                children_score -= CHILDREN_SCORE_PENALTIES["PALM_OIL"]

            if diabetic_risk >= DIABETIC_RISK_HIGH_THRESHOLD:
                children_score -= CHILDREN_SCORE_PENALTIES["DIABETIC_RISK"]

            if heart_risk >= HEART_RISK_HIGH_THRESHOLD:
                children_score -= CHILDREN_SCORE_PENALTIES["HEART_RISK"]

            if deception_score >= DECEPTION_HIGH_THRESHOLD:
                children_score -= CHILDREN_SCORE_PENALTIES["DECEPTION"]

            children_score = self._normalize_score(children_score)
            children_label = self._get_label(children_score)

        # =====================================================
        # TEENAGERS SUITABILITY
        # =====================================================

        teenager_score = 100

        if protein >= PROTEIN_HIGH_THRESHOLD:
            teenager_score += 5

        if sugar > SUGAR_HIGH_THRESHOLD:
            teenager_score -= 15

        if sodium > SODIUM_HIGH_THRESHOLD:
            teenager_score -= 15

        if processing_level == PROCESSING_ULTRA:
            teenager_score -= 15

        teenager_score = self._normalize_score(teenager_score)

        # =====================================================
        # ADULT SUITABILITY
        # =====================================================

        adult_score = 100

        if sugar > SUGAR_HIGH_THRESHOLD:
            adult_score -= ADULT_SCORE_PENALTIES["SUGAR_HIGH"]

        if sodium > SODIUM_HIGH_THRESHOLD:
            adult_score -= ADULT_SCORE_PENALTIES["SODIUM_HIGH"]

        if additive_count >= ADDITIVE_COUNT_VERY_HIGH_THRESHOLD:
            adult_score -= ADULT_SCORE_PENALTIES["ADDITIVE_COUNT_HIGH"]

        adult_score = self._normalize_score(adult_score)

        # =====================================================
        # ELDERLY SUITABILITY
        # =====================================================

        elderly_score = 100

        if sodium > 400:
            elderly_score -= ELDERLY_PENALTIES["SODIUM_HIGH"]

        if sugar > SUGAR_HIGH_THRESHOLD:
            elderly_score -= ELDERLY_PENALTIES["SUGAR_HIGH"]

        if processing_level == PROCESSING_ULTRA:
            elderly_score -= ELDERLY_PENALTIES["ULTRA_PROCESSED"]

        if additive_count >= ADDITIVE_COUNT_HIGH_THRESHOLD:
            elderly_score -= ELDERLY_PENALTIES["ADDITIVE_COUNT"]

        elderly_score = self._normalize_score(elderly_score)

        # =====================================================
        # PREGNANCY SUITABILITY
        # =====================================================

        pregnancy_score = 100

        if sodium > 500:
            pregnancy_score -= PREGNANCY_PENALTIES["SODIUM_HIGH"]

        if additive_count >= 4:
            pregnancy_score -= PREGNANCY_PENALTIES["ADDITIVE_COUNT"]

        if processing_level == PROCESSING_ULTRA:
            pregnancy_score -= PREGNANCY_PENALTIES["ULTRA_PROCESSED"]

        pregnancy_score = self._normalize_score(pregnancy_score)

        # =====================================================
        # PRE WORKOUT
        # =====================================================

        pre_workout_score = 50

        if calories >= 150:
            pre_workout_score += WORKOUT_BONUSES["PRE_CALORIES"]

        if protein >= PROTEIN_HIGH_THRESHOLD:
            pre_workout_score += WORKOUT_BONUSES["PRE_PROTEIN"]

        if sugar <= SUGAR_HIGH_THRESHOLD:
            pre_workout_score += WORKOUT_BONUSES["PRE_LOW_SUGAR"]

        if fat > FAT_HIGH_THRESHOLD:
            pre_workout_score += WORKOUT_BONUSES["PRE_HIGH_FAT"]

        pre_workout_score = self._normalize_score(pre_workout_score)

        # =====================================================
        # POST WORKOUT
        # =====================================================

        post_workout_score = 50

        if protein >= 20:
            post_workout_score += WORKOUT_BONUSES["POST_PROTEIN_HIGH"]

        elif protein >= PROTEIN_HIGH_THRESHOLD:
            post_workout_score += WORKOUT_BONUSES["POST_PROTEIN_MODERATE"]

        if calories >= 150:
            post_workout_score += WORKOUT_BONUSES["POST_CALORIES"]

        if sugar > 20:
            post_workout_score += WORKOUT_BONUSES["POST_SUGAR_HIGH"]

        post_workout_score = self._normalize_score(post_workout_score)

        # =====================================================
        # RECOVERY FOOD
        # =====================================================

        recovery_score = 50

        if protein >= 15:
            recovery_score += RECOVERY_BONUSES["PROTEIN_HIGH"]

        if fiber >= FIBER_HIGH_THRESHOLD:
            recovery_score += RECOVERY_BONUSES["FIBER_HIGH"]

        if processing_level == PROCESSING_ULTRA:
            recovery_score += RECOVERY_BONUSES["ULTRA_PROCESSED"]

        recovery_score = self._normalize_score(recovery_score)

        # =====================================================
        # OFFICE SNACK
        # =====================================================

        office_snack_score = 100

        if sugar > SUGAR_HIGH_THRESHOLD:
            office_snack_score -= OFFICE_SNACK_PENALTIES["SUGAR_HIGH"]

        if sodium > 500:
            office_snack_score -= OFFICE_SNACK_PENALTIES["SODIUM_HIGH"]

        if processing_level == PROCESSING_ULTRA:
            office_snack_score -= OFFICE_SNACK_PENALTIES["ULTRA_PROCESSED"]

        office_snack_score = self._normalize_score(office_snack_score)

        # =====================================================
        # LATE NIGHT
        # =====================================================

        late_night_score = 100

        if calories > 250:
            late_night_score -= LATE_NIGHT_PENALTIES["CALORIES_HIGH"]

        if sugar > SUGAR_HIGH_THRESHOLD:
            late_night_score -= LATE_NIGHT_PENALTIES["SUGAR_HIGH"]

        if fat > FAT_HIGH_THRESHOLD:
            late_night_score -= LATE_NIGHT_PENALTIES["FAT_HIGH"]

        late_night_score = self._normalize_score(late_night_score)

        # =====================================================
        # CHEAT MEAL
        # =====================================================

        cheat_meal_score = 100

        if processing_level == PROCESSING_ULTRA:
            cheat_meal_score -= 10

        if deception_score >= DECEPTION_HIGH_THRESHOLD:
            cheat_meal_score -= 10

        cheat_meal_score = self._normalize_score(cheat_meal_score)

        # =====================================================
        # TRAVEL FOOD
        # =====================================================

        travel_food_score = 100

        if sodium > 1000:
            travel_food_score -= TRAVEL_FOOD_PENALTIES["SODIUM_VERY_HIGH"]

        if additive_count >= ADDITIVE_COUNT_EXTREME_THRESHOLD:
            travel_food_score -= TRAVEL_FOOD_PENALTIES["ADDITIVE_COUNT_EXTREME"]

        travel_food_score = self._normalize_score(travel_food_score)

        # =====================================================
        # DAILY LIMIT
        # =====================================================

        daily_limit = DAILY_LIMIT_BASE

        if processing_level == PROCESSING_ULTRA:
            daily_limit = min(
                daily_limit,
                DAILY_LIMIT_ULTRA,
            )

        if sugar >= SUGAR_HIGH_THRESHOLD:
            daily_limit -= DAILY_LIMIT_SUGAR

        if sodium >= SODIUM_HIGH_THRESHOLD:
            daily_limit -= DAILY_LIMIT_SODIUM

        if processing_level == PROCESSING_ULTRA:
            daily_limit -= DAILY_LIMIT_ULTRA

        daily_limit = max(
            0,
            daily_limit,
        )

        # =====================================================
        # WEEKLY LIMIT
        # =====================================================

        weekly_limit = WEEKLY_LIMIT_BASE

        if processing_level == PROCESSING_ULTRA:
            weekly_limit = min(
                weekly_limit,
                WEEKLY_LIMIT_ULTRA,
            )

        if sugar >= SUGAR_HIGH_THRESHOLD:
            weekly_limit -= WEEKLY_LIMIT_SUGAR

        if sodium >= SODIUM_HIGH_THRESHOLD:
            weekly_limit -= WEEKLY_LIMIT_SODIUM

        if additive_count >= ADDITIVE_COUNT_VERY_HIGH_THRESHOLD:
            weekly_limit -= WEEKLY_LIMIT_ADDITIVES

        if processing_level == PROCESSING_ULTRA:
            weekly_limit -= WEEKLY_LIMIT_ULTRA

        weekly_limit = max(
            1,
            weekly_limit,
        )

        # =====================================================
        # CONSUMPTION FREQUENCY
        # =====================================================

        frequency = self._get_frequency(
            weekly_limit
        )

        # =====================================================
        # OVERALL SUITABILITY SCORE
        # =====================================================

        core_scores = [

            weight_loss_score,
            fat_loss_score,
            muscle_gain_score,
            lean_bulk_score,
            diabetic_score,
            heart_score,
            hypertension_score,
            metabolic_syndrome_score,
            children_score,
            teenager_score,
            adult_score,
            elderly_score,
            pregnancy_score,
            pre_workout_score,
            post_workout_score,
            recovery_score,
            office_snack_score,
            late_night_score,
            cheat_meal_score,
            travel_food_score,

        ]

        suitability_score = round(
            sum(core_scores) / len(core_scores)
        )

        suitability_score += (compliance_score - 50) * 0.10
        suitability_score -= (deception_score * 0.15)
        suitability_score += (metabolic_score - 50) * 0.10

        suitability_score = self._normalize_score(
            suitability_score
        )

        # =====================================================
        # SUITABILITY GRADE
        # =====================================================

        suitability_grade = self._get_grade(
            suitability_score
        )

        # =====================================================
        # BUY DECISION
        # =====================================================

        buy_decision = self._get_buy_decision(
            suitability_score
        )

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        recommendations: List[str] = []

        if protein >= PROTEIN_HIGH_THRESHOLD:
            recommendations.append("Good protein source")

        if fiber >= FIBER_HIGH_THRESHOLD:
            recommendations.append("Supports satiety")

        if sugar >= SUGAR_HIGH_THRESHOLD:
            recommendations.append("Reduce consumption frequency")

        if sodium >= SODIUM_HIGH_THRESHOLD:
            recommendations.append("Monitor sodium intake")

        if processing_level == PROCESSING_ULTRA:
            recommendations.append("Prefer minimally processed alternatives")

        if deception_score >= DECEPTION_HIGH_THRESHOLD:
            recommendations.append("Marketing claims require caution")

        if not recommendations:
            recommendations.append("Consume in moderation")

        # =====================================================
        # PERSONALIZED VERDICT REASONS
        # =====================================================

        verdict_reasons: List[str] = []

        if weight_loss_score >= 75:
            verdict_reasons.append("Weight loss friendly")

        if muscle_gain_score >= 75:
            verdict_reasons.append("Supports muscle gain")

        if diabetic_score < 50:
            verdict_reasons.append("Poor diabetic suitability")

        if heart_score < 50:
            verdict_reasons.append("Heart health concerns")

        if deception_score >= DECEPTION_HIGH_THRESHOLD:
            verdict_reasons.append("High deception indicators")

        # =====================================================
        # SUMMARY
        # =====================================================

        summary = {

            "daily_limit": daily_limit,
            "weekly_limit": weekly_limit,
            "frequency": frequency,
            "buy_decision": buy_decision,
            "grade": suitability_grade,

        }

        # =====================================================
        # FINAL RETURN
        # =====================================================

        return {

            "weight_loss": {
                "score": weight_loss_score,
                "label": self._get_label(weight_loss_score),
            },

            "fat_loss": {
                "score": fat_loss_score,
                "label": self._get_label(fat_loss_score),
            },

            "muscle_gain": {
                "score": muscle_gain_score,
                "label": self._get_label(muscle_gain_score),
            },

            "lean_bulk": {
                "score": lean_bulk_score,
                "label": self._get_label(lean_bulk_score),
            },

            "diabetic": {
                "score": diabetic_score,
                "label": self._get_label(diabetic_score),
            },

            "heart_health": {
                "score": heart_score,
                "label": self._get_label(heart_score),
            },

            "hypertension": {
                "score": hypertension_score,
                "label": self._get_label(hypertension_score),
            },

            "metabolic_syndrome": {
                "score": metabolic_syndrome_score,
                "label": self._get_label(metabolic_syndrome_score),
            },

            "keto": {
                "score": keto_score,
                "label": keto_label,
            },

            "positive_signals": self._unique_sorted(positive_signals),
            "negative_signals": self._unique_sorted(negative_signals),
            "risk_flags": self._unique_sorted(risk_flags),

            "system_scores": {
                "metabolic": metabolic_score,
                "compliance": compliance_score,
                "deception": deception_score,
            },

            "children": {
                "score": children_score,
                "label": children_label,
            },

            "teenagers": {
                "score": teenager_score,
                "label": self._get_label(teenager_score),
            },

            "adults": {
                "score": adult_score,
                "label": self._get_label(adult_score),
            },

            "elderly": {
                "score": elderly_score,
                "label": self._get_label(elderly_score),
            },

            "pregnancy": {
                "score": pregnancy_score,
                "label": self._get_label(pregnancy_score),
            },

            "pre_workout": {
                "score": pre_workout_score,
                "label": self._get_label(pre_workout_score),
            },

            "post_workout": {
                "score": post_workout_score,
                "label": self._get_label(post_workout_score),
            },

            "recovery": {
                "score": recovery_score,
                "label": self._get_label(recovery_score),
            },

            "office_snack": {
                "score": office_snack_score,
                "label": self._get_label(office_snack_score),
            },

            "late_night": {
                "score": late_night_score,
                "label": self._get_label(late_night_score),
            },

            "cheat_meal": {
                "score": cheat_meal_score,
                "label": self._get_label(cheat_meal_score),
            },

            "travel_food": {
                "score": travel_food_score,
                "label": self._get_label(travel_food_score),
            },

            "overall_score": suitability_score,
            "overall_grade": suitability_grade,
            "buy_decision": buy_decision,
            "daily_limit": daily_limit,
            "weekly_limit": weekly_limit,
            "consumption_frequency": frequency,
            "recommendations": recommendations,
            "verdict_reasons": verdict_reasons,
            "summary": summary,

        }


# ==========================================================
# SINGLETON INSTANCE
# ==========================================================


suitability_engine = SuitabilityEngine()


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [

    "SuitabilityEngine",
    "suitability_engine",

]


# ==========================================================
# END OF FILE – suitability_engine.py
# ==========================================================