# ==========================================================
# SCANIX AI
# SYSTEM 3 – METABOLIC INTELLIGENCE (METABOLIC ENGINE)
# ELITE PRODUCTION GRADE – FINAL VERSION
# ==========================================================


from __future__ import annotations


from typing import Any
from typing import Dict
from typing import List
from typing import Optional


from .glycemic_load_engine import (
    glycemic_load_engine,
)

from .insulin_load_engine import (
    insulin_load_engine,
)

from .metabolic_flexibility_engine import (
    metabolic_flexibility_engine,
)


# ==========================================================
# CONSTANTS
# ==========================================================


VERIFICATION_BONUS_MAP = {

    "HIGH": 15,

    "MEDIUM": 8,

    "LOW": 0,

}

HIGH_QUALITY_PROTEINS = [

    "whey",
    "casein",
    "milk protein",
    "soy isolate",
    "soy protein",
    "pea protein",
    "protein isolate",

]

DEFAULT_SCAN_QUALITY_SCORE = 50

DEFAULT_NUTRITION_CONFIDENCE_THRESHOLD = 50


# ==========================================================
# METABOLIC ENGINE
# ==========================================================


class MetabolicEngine:
    """
    Master Metabolic Intelligence Engine for System 3.

    Integrates:
    - Satiety analysis
    - Energy curve analysis
    - Metabolic load analysis
    - Food personality detection
    - Body reaction timeline
    - Glycemic load estimation
    - Insulin load estimation
    - Metabolic flexibility analysis
    """

    # =====================================================
    # SAFE HELPERS
    # =====================================================

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
        Safely convert value to int.

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

    def _verification_bonus(
        self,
        verification_level: str,
    ) -> int:
        """
        Calculate bonus based on verification level.

        Args:
            verification_level: HIGH, MEDIUM, or LOW

        Returns:
            Bonus points (15, 8, or 0)
        """

        return VERIFICATION_BONUS_MAP.get(
            verification_level,
            0,
        )

    def _get_protein_quality_bonus(
        self,
        ingredient_intelligence: Dict[str, Any],
    ) -> int:
        """
        Calculate bonus for high-quality protein sources.

        Args:
            ingredient_intelligence: Ingredient analysis data

        Returns:
            Bonus points (15 if high-quality protein found, else 0)
        """

        bonus = 0

        ingredients = (

            ingredient_intelligence
            .get(
                "ingredients",
                [],
            )

        )

        for item in ingredients:

            name = item.get(
                "name",
                "",
            ).lower()

            if any(
                hq in name
                for hq in HIGH_QUALITY_PROTEINS
            ):

                bonus += 15

                break

        return bonus

    # =====================================================
    # DATA EXTRACTION
    # =====================================================

    def extract_signals(
        self,
        nutrition: Dict[str, Any],
        ingredient_intelligence: Dict[str, Any],
        product: Dict[str, Any],
        scan_quality: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Extract all signals from input data for metabolic analysis.

        Args:
            nutrition: Nutrition data from System 1
            ingredient_intelligence: Ingredient analysis from System 2
            product: Product data from System 1
            scan_quality: Scan quality data from System 1

        Returns:
            Dictionary of extracted signals
        """

        registry = (

            ingredient_intelligence
            .get(
                "registry",
                {},
            )

        )

        ingredient_summary = (

            ingredient_intelligence
            .get(
                "ingredient_summary",
                {},
            )

        )

        processing = (

            ingredient_intelligence
            .get(
                "processing_analysis",
                {},
            )

        )

        verification = (

            ingredient_intelligence
            .get(
                "verification",
                {},
            )

        )

        return {

            # Nutrition
            "protein":
            self._safe_float(
                nutrition.get(
                    "protein",
                    0,
                )
            ),

            "fiber":
            self._safe_float(
                nutrition.get(
                    "fiber",
                    0,
                )
            ),

            "sugar":
            self._safe_float(
                nutrition.get(
                    "sugar",
                    0,
                )
            ),

            "sodium":
            self._safe_float(
                nutrition.get(
                    "sodium",
                    0,
                )
            ),

            "carbohydrates":
            self._safe_float(
                nutrition.get(
                    "carbohydrates",
                    nutrition.get(
                        "carbs",
                        0,
                    ),
                )
            ),

            "saturated_fat":
            self._safe_float(
                nutrition.get(
                    "saturated_fat",
                    0,
                )
            ),

            "trans_fat":
            self._safe_float(
                nutrition.get(
                    "trans_fat",
                    0,
                )
            ),

            "fat":
            self._safe_float(
                nutrition.get(
                    "fat",
                    0,
                )
            ),

            "calories":
            self._safe_float(
                nutrition.get(
                    "calories",
                    0,
                )
            ),

            # System 2
            "hidden_sugars":

            self._safe_int(

                registry
                .get(
                    "hidden_sugars",
                    {},
                )
                .get(
                    "hidden_sugar_count",
                    0,
                )

            ),

            "additive_count":

            self._safe_int(

                ingredient_intelligence.get(
                    "additive_count",
                    ingredient_summary.get(
                        "additive_candidates",
                        0,
                    ),
                )

            ),

            "contains_palm_oil":

            bool(

                registry.get(
                    "contains_palm_oil",
                    False,
                )

            ),

            "processing_level":

            processing.get(
                "processing_level",
                "UNKNOWN",
            ),

            # System 1
            "category":

            product.get(
                "category",
                "unknown",
            ),

            "scan_quality_score":

            self._safe_int(

                scan_quality.get(
                    "scan_quality_score",
                    DEFAULT_SCAN_QUALITY_SCORE,
                )

            ),

            "verification_level":

            verification.get(
                "verification_level",
                ingredient_intelligence.get(
                    "verification_level",
                    "LOW",
                ),
            ),

        }

    # =====================================================
    # SATIETY ENGINE
    # =====================================================

    def calculate_satiety(
        self,
        signals: Dict[str, Any],
        nutrition: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Calculate satiety score (0-100) and hunger return time.

        Args:
            signals: Extracted signals
            nutrition: Raw nutrition data for confidence check

        Returns:
            Satiety score, verdict, hunger return time, and reasons
        """

        nutrition_confidence = nutrition.get(
            "nutrition_confidence",
            0,
        )

        if nutrition_confidence < DEFAULT_NUTRITION_CONFIDENCE_THRESHOLD:

            return {

                "score": 50,

                "verdict": "MODERATE",

                "hunger_return": "2-3 hours",

                "reasons": [
                    "Insufficient nutrition confidence",
                ],

            }

        score = 30

        reasons: List[str] = []

        protein = signals["protein"]

        fiber = signals["fiber"]

        calories = signals["calories"]

        sugar = signals["sugar"]

        if protein >= 20:

            score += 30

            reasons.append(
                "High protein improves satiety"
            )

        elif protein >= 10:

            score += 15

            reasons.append(
                "Moderate protein content"
            )

        else:

            reasons.append(
                "Low protein content"
            )

            if sugar >= 15:

                score -= 10

        if signals["processing_level"] == "ULTRA_PROCESSED":

            score -= 10

        if fiber >= 8:

            score += 25

            reasons.append(
                "High fiber delays hunger"
            )

        elif fiber >= 4:

            score += 12

            reasons.append(
                "Moderate fiber support"
            )

        if (
            signals[
                "processing_level"
            ]
            ==
            "ULTRA_PROCESSED"
        ):

            score -= 20

            reasons.append(
                "Ultra processing reduces satiety"
            )

        if (
            signals[
                "hidden_sugars"
            ]
            >= 2
        ):

            score -= 10

            reasons.append(
                "Hidden sugars increase cravings"
            )

        if calories >= 400 and protein < 10 and fiber < 5:

            score -= 15

            reasons.append(
                "High calorie density without satiating macros"
            )

        score = max(
            0,
            min(
                100,
                score,
            )
        )

        if score >= 75:

            verdict = "HIGH"

            hunger_return = (
                "3-5 hours"
            )

        elif score >= 50:

            verdict = "MODERATE"

            hunger_return = (
                "2-3 hours"
            )

        else:

            verdict = "LOW"

            hunger_return = (
                "45-90 mins"
            )

        return {

            "score":
            score,

            "verdict":
            verdict,

            "hunger_return":
            hunger_return,

            "reasons":
            reasons,

        }

    # =====================================================
    # ENERGY CURVE ENGINE
    # =====================================================

    def calculate_energy_curve(
        self,
        signals: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Calculate energy curve and crash probability.

        Args:
            signals: Extracted signals

        Returns:
            Curve type, crash probability, and reasons
        """

        reasons = []

        crash_probability = 20

        curve = "STABLE"

        carbs = signals["carbohydrates"]

        sugar = signals["sugar"]

        hidden_sugars = signals["hidden_sugars"]

        processing = signals[
            "processing_level"
        ]

        if sugar >= 15:

            crash_probability += 25

            reasons.append(
                "High sugar content"
            )

        if hidden_sugars >= 2:

            crash_probability += 25

            reasons.append(
                "Hidden sugars detected"
            )

        if carbs >= 40:

            crash_probability += 15

            reasons.append(
                "High carbohydrate load"
            )

        if (
            processing
            ==
            "ULTRA_PROCESSED"
        ):

            crash_probability += 20

            reasons.append(
                "Ultra processed product"
            )

        crash_probability = min(
            100,
            crash_probability,
        )

        if crash_probability >= 75:

            curve = "SPIKE_CRASH"

        elif crash_probability >= 45:

            curve = "MODERATE_SPIKE"

        return {

            "curve":
            curve,

            "crash_probability":
            crash_probability,

            "reasons":
            reasons,

        }

    # =====================================================
    # METABOLIC LOAD ENGINE
    # =====================================================

    def calculate_metabolic_load(
        self,
        signals: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Calculate metabolic load score (0-100) and risk level.

        Args:
            signals: Extracted signals

        Returns:
            Metabolic load score, risk level, and reasons
        """

        score = 0

        reasons = []

        score += min(
            int(
                signals["sugar"]
            ),
            30,
        )

        sodium = signals["sodium"]

        sodium = max(
            0.0,
            sodium,
        )

        score += min(
            int(sodium / 25),
            30,
        )

        score += (

            signals[
                "additive_count"
            ]

            * 5

        )

        carbs = signals["carbohydrates"]

        if carbs >= 50:

            score += 20

        elif carbs >= 30:

            score += 12

        elif carbs >= 15:

            score += 6

        if (
            signals[
                "contains_palm_oil"
            ]
        ):

            score += 8

            reasons.append(
                "Contains palm oil"
            )

        if (

            signals[
                "processing_level"
            ]

            ==

            "ULTRA_PROCESSED"

        ):

            score += 25

            reasons.append(
                "Ultra processed"
            )

        if signals["hidden_sugars"] >= 3:

            score += 20

            reasons.append(
                "Multiple hidden sugars detected"
            )

        elif signals["hidden_sugars"] >= 1:

            score += 10

            reasons.append(
                "Hidden sugars detected"
            )

        score = min(
            100,
            score,
        )

        if score >= 70:

            risk = "HIGH"

        elif score >= 40:

            risk = "MODERATE"

        else:

            risk = "LOW"

        return {

            "score":
            score,

            "risk":
            risk,

            "reasons":
            reasons,

        }

    # =====================================================
    # FOOD PERSONALITY ENGINE
    # =====================================================

    def determine_food_personality(
        self,
        signals: Dict[str, Any],
        satiety: Dict[str, Any],
        energy_curve: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Determine food personality type based on signals.

        Args:
            signals: Extracted signals
            satiety: Satiety analysis results
            energy_curve: Energy curve analysis results

        Returns:
            Personality type, confidence, and reasons
        """

        personality = "STANDARD"

        confidence = 60

        reasons = []

        calories = signals.get(
            "calories",
            100,
        )

        cal_base = (
            calories
            if calories > 0
            else 100
        )

        protein_ratio = (
            (signals["protein"] * 4)
            / cal_base
        )

        if (

            signals["protein"] >= 20

            and

            signals["sugar"] <= 5

            and

            signals["processing_level"]
            != "ULTRA_PROCESSED"

            and

            protein_ratio >= 0.15

        ):

            personality = (
                "PROTEIN_FOCUSED"
            )

            confidence = 90

            reasons.append(
                "High protein profile with low sugar and adequate protein-to-calorie ratio"
            )

        elif (

            energy_curve[
                "curve"
            ]

            ==

            "SPIKE_CRASH"

        ):

            personality = (
                "SUGAR_BOMB"
            )

            confidence = 88

            reasons.append(
                "Strong spike-crash pattern"
            )

        elif (

            signals["sodium"] >= 600

            or

            signals["saturated_fat"] >= 5.0

            or

            signals["trans_fat"] > 0

            or

            signals["contains_palm_oil"]

        ):

            personality = (
                "HEART_UNFRIENDLY"
            )

            confidence = 85

            reasons.append(
                "High cardiovascular risk factors detected (sodium, saturated/trans fats, or palm oil)"
            )

        elif (

            signals["carbohydrates"] >= 40

            and

            signals["fiber"] <= 3

        ):

            personality = (
                "DIABETIC_UNFRIENDLY"
            )

            confidence = 85

            reasons.append(
                "High carbohydrate load with low fiber"
            )

        elif (
            signals["hidden_sugars"] >= 2
        ):

            personality = (
                "DIABETIC_UNFRIENDLY"
            )

            confidence = 88

            reasons.append(
                "Multiple hidden sugars detected"
            )

        elif (

            signals[
                "processing_level"
            ]

            ==

            "ULTRA_PROCESSED"

        ):

            personality = (
                "CHEAT_SNACK"
            )

            confidence = 85

            reasons.append(
                "Ultra processed profile"
            )

        elif (

            satiety["score"] >= 75

            and

            signals["fiber"] >= 6

        ):

            personality = (
                "CLEAN_FUEL"
            )

            confidence = 92

            reasons.append(
                "High satiety and fiber"
            )

        return {

            "type":
            personality,

            "confidence":
            confidence,

            "reasons":
            reasons,

        }

    # =====================================================
    # BODY REACTION TIMELINE
    # =====================================================

    def build_body_reaction(
        self,
        signals: Dict[str, Any],
        energy_curve: Dict[str, Any],
        satiety: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Build timeline of body reaction after consumption.

        Args:
            signals: Extracted signals
            energy_curve: Energy curve analysis results
            satiety: Satiety analysis results

        Returns:
            Timeline of body reactions
        """

        timeline = []

        curve = energy_curve.get(
            "curve",
            "STABLE",
        )

        if curve == "SPIKE_CRASH":

            timeline = [

                {
                    "phase":
                    "0-20 min",

                    "effect":
                    "Energy Spike",

                    "confidence":
                    85,

                    "reason":
                    "Rapid carbohydrate absorption due to high sugar or ultra-processed formulation",
                },

                {
                    "phase":
                    "20-90 min",

                    "effect":
                    "Temporary Satisfaction",

                    "confidence":
                    82,

                    "reason":
                    "Short-term reward response",
                },

                {
                    "phase":
                    "90-180 min",

                    "effect":
                    "Cravings Return",

                    "confidence":
                    80,

                    "reason":
                    "Blood sugar decline triggers hunger",
                },

            ]

        elif curve == "MODERATE_SPIKE":

            timeline = [

                {
                    "phase":
                    "0-30 min",

                    "effect":
                    "Gradual Energy Increase",

                    "confidence":
                    82,

                    "reason":
                    "Moderate glycemic load",
                },

                {
                    "phase":
                    "30-150 min",

                    "effect":
                    "Stable Satisfaction",

                    "confidence":
                    78,

                    "reason":
                    "Moderate digestion profile",
                },

            ]

        else:

            timeline = [

                {
                    "phase":
                    "0-60 min",

                    "effect":
                    "Stable Energy",

                    "confidence":
                    88,

                    "reason":
                    "Balanced metabolic response",
                },

                {
                    "phase":
                    "60-240 min",

                    "effect":
                    "Sustained Satiety",

                    "confidence":
                    85,

                    "reason":
                    "Slow digestion profile supported by complex macronutrients",
                },

            ]

        return {

            "timeline":
            timeline,

            "timeline_type":
            curve,

        }

    # =====================================================
    # CONFIDENCE ENGINE
    # =====================================================

    def calculate_confidence(
        self,
        signals: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Calculate confidence score for the entire analysis.

        Args:
            signals: Extracted signals

        Returns:
            Engine confidence score and data quality rating
        """

        score = 35

        score += min(
            signals[
                "scan_quality_score"
            ] // 4,
            25,
        )

        score += self._verification_bonus(

            signals[
                "verification_level"
            ]

        )

        if (
            signals[
                "protein"
            ]
            > 0
        ):
            score += 5

        if (
            signals[
                "fiber"
            ]
            > 0
        ):
            score += 5

        score = max(
            0,
            min(
                100,
                score,
            )
        )

        if score >= 90:

            quality = (
                "VERY_HIGH"
            )

        elif score >= 75:

            quality = (
                "HIGH"
            )

        elif score >= 60:

            quality = (
                "MEDIUM"
            )

        else:

            quality = (
                "LOW"
            )

        return {

            "engine_confidence":
            score,

            "data_quality":
            quality,

        }

    # =====================================================
    # MASTER ANALYSIS
    # =====================================================

    def analyze(
        self,
        nutrition: Dict[str, Any],
        ingredient_intelligence: Dict[str, Any],
        product: Dict[str, Any],
        scan_quality: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Master analysis method for metabolic intelligence.

        Args:
            nutrition: Nutrition data from System 1
            ingredient_intelligence: Ingredient analysis from System 2
            product: Product data from System 1
            scan_quality: Scan quality data from System 1

        Returns:
            Complete metabolic intelligence analysis
        """

        signals = self.extract_signals(

            nutrition=
            nutrition,

            ingredient_intelligence=
            ingredient_intelligence,

            product=
            product,

            scan_quality=
            scan_quality,

        )

        satiety = (
            self.calculate_satiety(

                signals=
                signals,

                nutrition=
                nutrition,

            )
        )

        energy_curve = (
            self.calculate_energy_curve(
                signals
            )
        )

        metabolic_load = (
            self.calculate_metabolic_load(
                signals
            )
        )

        personality = (
            self.determine_food_personality(

                signals=
                signals,

                satiety=
                satiety,

                energy_curve=
                energy_curve,

            )
        )

        body_reaction = (
            self.build_body_reaction(

                signals=
                signals,

                energy_curve=
                energy_curve,

                satiety=
                satiety,

            )
        )

        confidence = (
            self.calculate_confidence(
                signals
            )
        )

        glycemic_load_result = (
            glycemic_load_engine.analyze(
                nutrition
            )
        )

        insulin_load_result = (
            insulin_load_engine.analyze(
                nutrition
            )
        )

        metabolic_flexibility_result = (
            metabolic_flexibility_engine.analyze(
                nutrition,
                ingredient_intelligence,
            )
        )

        return {

            "metabolic_version": "1.0",

            "satiety": satiety,

            "energy_curve": energy_curve,

            "metabolic_load": metabolic_load,

            "food_personality": personality,

            "body_reaction": body_reaction,

            "confidence": confidence,

            "glycemic_load": glycemic_load_result,

            "insulin_load": insulin_load_result,

            "metabolic_flexibility": metabolic_flexibility_result,

        }


# ==========================================================
# SINGLETON INSTANCE
# ==========================================================


metabolic_engine = MetabolicEngine()


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [

    "MetabolicEngine",
    "metabolic_engine",

]


# ==========================================================
# END OF FILE – metabolic_engine.py
# ==========================================================