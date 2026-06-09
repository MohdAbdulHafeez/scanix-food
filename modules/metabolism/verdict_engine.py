# ==========================================================
# SCANIX AI
# SYSTEM 4 – CONSUMER INTELLIGENCE (VERDICT ENGINE)
# ELITE PRODUCTION GRADE – FINAL VERSION
# ==========================================================


from __future__ import annotations


from typing import Any
from typing import Dict
from typing import List
from typing import Optional


# ==========================================================
# CONSTANTS
# ==========================================================


DEFAULT_SCORE = 100

DEFAULT_SATIETY_SCORE = 50

DEFAULT_METABOLIC_LOAD = 50

DEFAULT_PERSONA_SCORE = 50

VERDICT_THRESHOLDS = {

    "EXCELLENT": 85,
    "GOOD": 70,
    "MODERATE": 50,
    "POOR": 30,
    "AVOID": 0,

}

PERSONALITY_PENALTIES = {

    "SUGAR_BOMB": 20,
    "HEART_UNFRIENDLY": 20,
    "DIABETIC_UNFRIENDLY": 20,
    "CHEAT_SNACK": 15,

}

DATA_QUALITY_PENALTIES = {

    "LOW": 25,
    "MEDIUM": 10,
    "HIGH": 0,

}

PROCESSING_PENALTIES = {

    "ULTRA_PROCESSED": 20,
    "PROCESSED": 10,
    "MINIMALLY_PROCESSED": 0,
    "UNPROCESSED": 0,

}

MUSCLE_BUILDING_BONUS_THRESHOLD = 80

MUSCLE_BUILDING_BONUS = 5

WEIGHT_LOSS_PENALTY_THRESHOLD = 40

WEIGHT_LOSS_PENALTY = 15

DIABETIC_RISK_PENALTY = 20

HEART_RISK_PENALTY = 20

METABOLIC_LOAD_PENALTY_THRESHOLD = 70

METABOLIC_LOAD_PENALTY = 25

SATIETY_PENALTY_THRESHOLD = 50

SATIETY_PENALTY = 15

BEST_FOR_THRESHOLD = 70

PERSONALITY_SUMMARY_MAP = {

    "SUGAR_BOMB": (
        "Rapid energy spike followed "
        "by increased crash potential."
    ),

    "CHEAT_SNACK": (
        "Highly processed food best "
        "reserved for occasional use."
    ),

    "PROTEIN_FOCUSED": (
        "Strong protein profile with "
        "better fitness compatibility."
    ),

    "CLEAN_FUEL": (
        "Balanced nutritional profile "
        "with favorable metabolic response."
    ),

}


# ==========================================================
# VERDICT ENGINE
# ==========================================================


class VerdictEngine:
    """
    Verdict Engine for System 4 – Consumer Intelligence.

    Synthesizes all metabolic and impact analyses into:
    - Overall verdict (EXCELLENT, GOOD, MODERATE, POOR, AVOID)
    - Best for recommendations
    - Avoid if warnings
    - Consumer-friendly summary
    """

    # =====================================================
    # OVERALL VERDICT
    # =====================================================

    def determine_overall_verdict(
        self,
        metabolic_result: Dict[str, Any],
        impact_result: Dict[str, Any],
        ingredient_intelligence: Dict[str, Any],
        confidence: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Determine overall product verdict based on all analyses.

        Args:
            metabolic_result: Results from metabolic engine
            impact_result: Results from impact engine
            ingredient_intelligence: Ingredient analysis data
            confidence: Confidence scores from analyses

        Returns:
            Overall verdict with score, verdict type, and reasons
        """

        score = DEFAULT_SCORE

        reasons: List[str] = []

        # Extract scores from metabolic result
        satiety_score = (

            metabolic_result
            .get(
                "satiety",
                {},
            )
            .get(
                "score",
                DEFAULT_SATIETY_SCORE,
            )

        )

        metabolic_load = (

            metabolic_result
            .get(
                "metabolic_load",
                {},
            )
            .get(
                "score",
                DEFAULT_METABOLIC_LOAD,
            )

        )

        food_personality = (

            metabolic_result
            .get(
                "food_personality",
                {},
            )
            .get(
                "type",
                "STANDARD",
            )

        )

        # Extract scores from impact result
        personas = (

            impact_result
            .get(
                "personas",
                {},
            )

        )

        weight_loss_score = (

            personas
            .get(
                "weight_loss",
                {},
            )
            .get(
                "score",
                DEFAULT_PERSONA_SCORE,
            )

        )

        muscle_score = (

            personas
            .get(
                "muscle_building",
                {},
            )
            .get(
                "score",
                DEFAULT_PERSONA_SCORE,
            )

        )

        diabetic_risk = (

            personas
            .get(
                "diabetic",
                {},
            )
            .get(
                "risk",
                "LOW",
            )

        )

        heart_risk = (

            personas
            .get(
                "heart",
                {},
            )
            .get(
                "risk",
                "LOW",
            )

        )

        # Apply food personality penalties
        if food_personality in PERSONALITY_PENALTIES:

            score -= PERSONALITY_PENALTIES[food_personality]

            if food_personality == "SUGAR_BOMB":

                reasons.append(
                    "High sugar spike risk"
                )

            elif food_personality == "HEART_UNFRIENDLY":

                reasons.append(
                    "Heart-unfriendly profile"
                )

            elif food_personality == "DIABETIC_UNFRIENDLY":

                reasons.append(
                    "Diabetic-unfriendly profile"
                )

            elif food_personality == "CHEAT_SNACK":

                reasons.append(
                    "Best kept as an occasional cheat snack"
                )

        # Apply metabolic load penalty
        if metabolic_load >= METABOLIC_LOAD_PENALTY_THRESHOLD:

            score -= METABOLIC_LOAD_PENALTY

            reasons.append(
                "High metabolic burden"
            )

        # Apply satiety penalty
        if satiety_score < SATIETY_PENALTY_THRESHOLD:

            score -= SATIETY_PENALTY

            reasons.append(
                "Low satiety profile"
            )

        # Apply weight loss penalty
        if weight_loss_score < WEIGHT_LOSS_PENALTY_THRESHOLD:

            score -= WEIGHT_LOSS_PENALTY

            reasons.append(
                "Poor weight loss compatibility"
            )

        # Apply muscle building bonus
        if muscle_score >= MUSCLE_BUILDING_BONUS_THRESHOLD:

            score += MUSCLE_BUILDING_BONUS

            reasons.append(
                "Excellent muscle-building support"
            )

        # Apply diabetic risk penalty
        if diabetic_risk == "HIGH":

            score -= DIABETIC_RISK_PENALTY

            reasons.append(
                "High diabetic impact"
            )

        # Apply heart risk penalty
        if heart_risk == "HIGH":

            score -= HEART_RISK_PENALTY

            reasons.append(
                "High cardiovascular impact"
            )

        # Apply data quality penalty
        data_quality = (

            confidence.get(
                "data_quality",
                "HIGH",
            )

        )

        if data_quality in DATA_QUALITY_PENALTIES:

            penalty = DATA_QUALITY_PENALTIES[data_quality]

            if penalty > 0:

                score -= penalty

                reasons.append(
                    f"{data_quality.capitalize()} data quality"
                )

        # Apply processing level penalty
        processing_level = (

            ingredient_intelligence
            .get(
                "processing_analysis",
                {},
            )
            .get(
                "processing_level",
                "UNPROCESSED",
            )

        )

        if processing_level in PROCESSING_PENALTIES:

            penalty = PROCESSING_PENALTIES[processing_level]

            if penalty > 0:

                score -= penalty

                reasons.append(
                    f"{processing_level.replace('_', ' ').lower()} ingredients detected"
                )

        # Normalize score to 0-100 range
        score = max(
            0,
            min(
                100,
                score,
            )
        )

        # Determine verdict based on score
        if score >= VERDICT_THRESHOLDS["EXCELLENT"]:

            verdict = "EXCELLENT"

        elif score >= VERDICT_THRESHOLDS["GOOD"]:

            verdict = "GOOD"

        elif score >= VERDICT_THRESHOLDS["MODERATE"]:

            verdict = "MODERATE"

        elif score >= VERDICT_THRESHOLDS["POOR"]:

            verdict = "POOR"

        else:

            verdict = "AVOID"

        return {

            "score":
            score,

            "verdict":
            verdict,

            "reasons":
            reasons,

        }

    # =====================================================
    # BEST FOR
    # =====================================================

    def determine_best_for(
        self,
        impact_result: Dict[str, Any],
    ) -> List[str]:
        """
        Determine which user personas this product is best for.

        Args:
            impact_result: Results from impact engine

        Returns:
            List of recommended user personas
        """

        best_for: List[str] = []

        personas = (

            impact_result
            .get(
                "personas",
                {},
            )

        )

        # Check muscle building suitability
        if (

            personas
            .get(
                "muscle_building",
                {},
            )
            .get(
                "score",
                0,
            )

            >=

            BEST_FOR_THRESHOLD

        ):

            best_for.append(
                "Muscle Building"
            )

        # Check weight loss suitability
        if (

            personas
            .get(
                "weight_loss",
                {},
            )
            .get(
                "score",
                0,
            )

            >=

            BEST_FOR_THRESHOLD

        ):

            best_for.append(
                "Weight Loss"
            )

        # Default recommendation if no specific personas match
        if not best_for:

            best_for.append(
                "Occasional Consumption"
            )

        return best_for

    # =====================================================
    # AVOID IF
    # =====================================================

    def determine_avoid_if(
        self,
        impact_result: Dict[str, Any],
    ) -> List[str]:
        """
        Determine which conditions should avoid this product.

        Args:
            impact_result: Results from impact engine

        Returns:
            List of conditions that should avoid this product
        """

        avoid_if: List[str] = []

        personas = (

            impact_result
            .get(
                "personas",
                {},
            )

        )

        diabetic_risk = (

            personas
            .get(
                "diabetic",
                {},
            )
            .get(
                "risk",
                "LOW",
            )

        )

        heart_risk = (

            personas
            .get(
                "heart",
                {},
            )
            .get(
                "risk",
                "LOW",
            )

        )

        # Check diabetic risk
        if diabetic_risk == "HIGH":

            avoid_if.append(
                "Diabetes"
            )

        # Check heart disease risk
        if heart_risk == "HIGH":

            avoid_if.append(
                "Heart Disease"
            )

        # Check weight loss compatibility
        if (

            personas
            .get(
                "weight_loss",
                {},
            )
            .get(
                "score",
                100,
            )

            <

            WEIGHT_LOSS_PENALTY_THRESHOLD

        ):

            avoid_if.append(
                "Weight Loss Diet"
            )

        return avoid_if

    # =====================================================
    # CONSUMER SUMMARY
    # =====================================================

    def build_summary(
        self,
        overall: Dict[str, Any],
        metabolic_result: Dict[str, Any],
    ) -> str:
        """
        Build a consumer-friendly summary of the product.

        Args:
            overall: Overall verdict results
            metabolic_result: Results from metabolic engine

        Returns:
            Human-readable summary string
        """

        personality = (

            metabolic_result
            .get(
                "food_personality",
                {},
            )
            .get(
                "type",
                "STANDARD",
            )

        )

        verdict = overall.get(
            "verdict",
            "MODERATE",
        )

        # Return personality-specific summary if available
        if personality in PERSONALITY_SUMMARY_MAP:

            return PERSONALITY_SUMMARY_MAP[personality]

        # Return verdict-based summary for poor/avoid ratings
        if verdict in {"POOR", "AVOID"}:

            return (
                "Frequent consumption is "
                "not recommended."
            )

        # Default summary
        return (
            "Moderate impact food with "
            "acceptable consumption profile."
        )

    # =====================================================
    # MASTER ANALYSIS
    # =====================================================

    def analyze(
        self,
        product: Dict[str, Any],
        ingredient_intelligence: Dict[str, Any],
        metabolic_result: Dict[str, Any],
        impact_result: Dict[str, Any],
        confidence: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Master analysis method for consumer verdict.

        Args:
            product: Product data from System 1
            ingredient_intelligence: Ingredient analysis from System 2
            metabolic_result: Results from metabolic engine
            impact_result: Results from impact engine
            confidence: Confidence scores from analyses

        Returns:
            Complete verdict analysis
        """

        if confidence is None:

            confidence = {}

        overall = self.determine_overall_verdict(

            metabolic_result=
            metabolic_result,

            impact_result=
            impact_result,

            ingredient_intelligence=
            ingredient_intelligence,

            confidence=
            confidence,

        )

        best_for = self.determine_best_for(
            impact_result
        )

        avoid_if = self.determine_avoid_if(
            impact_result
        )

        summary = self.build_summary(

            overall=
            overall,

            metabolic_result=
            metabolic_result,

        )

        return {

            "verdict_version":
            "1.0",

            "overall":
            overall,

            "food_personality":

            metabolic_result
            .get(
                "food_personality",
                {},
            ),

            "best_for":
            best_for,

            "avoid_if":
            avoid_if,

            "summary":
            summary,

        }


# ==========================================================
# SINGLETON INSTANCE
# ==========================================================


verdict_engine = VerdictEngine()


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [

    "VerdictEngine",
    "verdict_engine",

]


# ==========================================================
# END OF FILE – verdict_engine.py
# ==========================================================