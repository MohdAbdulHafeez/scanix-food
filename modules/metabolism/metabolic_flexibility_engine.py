# ==========================================================
# SCANIX AI
# SYSTEM 3 – METABOLIC INTELLIGENCE (METABOLIC FLEXIBILITY ENGINE)
# ELITE PRODUCTION GRADE – FINAL VERSION
# ==========================================================


from __future__ import annotations


from typing import Any
from typing import Dict
from typing import Optional


# ==========================================================
# CONSTANTS
# ==========================================================


PROTEIN_BONUS_FACTOR = 2.0

FIBER_BONUS_FACTOR = 3.0

SUGAR_PENALTY_FACTOR = 1.5

ULTRA_PROCESSED_PENALTY = 20

PROCESSED_PENALTY = 10

DEFAULT_SCORE = 50

VERDICT_THRESHOLDS = {

    "EXCELLENT": 80,

    "GOOD": 65,

    "MODERATE": 50,

    "POOR": 0,

}


# ==========================================================
# METABOLIC FLEXIBILITY ENGINE
# ==========================================================


class MetabolicFlexibilityEngine:
    """
    Elite Metabolic Flexibility Engine for System 3.

    Measures the body's ability to switch between fuel sources
    (carbs vs fats) based on:
    - Protein content (supports metabolic health)
    - Fiber content (improves insulin sensitivity)
    - Sugar content (impairs flexibility)
    - Processing level (ultra-processed foods reduce flexibility)

    Higher score = better metabolic flexibility.
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

            return float(value)

        except Exception:

            return default

    def _calculate_base_score(
        self,
        protein: float,
        fiber: float,
        sugar: float,
    ) -> float:
        """
        Calculate base metabolic flexibility score.

        Formula:
        50 + (protein * 2) + (fiber * 3) - (sugar * 1.5)

        Args:
            protein: Protein content in grams
            fiber: Fiber content in grams
            sugar: Sugar content in grams

        Returns:
            Base score (0-100)
        """

        score = DEFAULT_SCORE

        score += protein * PROTEIN_BONUS_FACTOR

        score += fiber * FIBER_BONUS_FACTOR

        score -= sugar * SUGAR_PENALTY_FACTOR

        return score

    def _apply_processing_penalty(
        self,
        score: float,
        processing_level: str,
    ) -> float:
        """
        Apply penalty based on processing level.

        Args:
            score: Current score
            processing_level: Processing level (ULTRA_PROCESSED, PROCESSED, etc.)

        Returns:
            Score after applying penalty
        """

        if processing_level == "ULTRA_PROCESSED":

            score -= ULTRA_PROCESSED_PENALTY

        elif processing_level == "PROCESSED":

            score -= PROCESSED_PENALTY

        return score

    def _normalize_score(
        self,
        score: float,
    ) -> float:
        """
        Normalize score to 0-100 range.

        Args:
            score: Raw score

        Returns:
            Normalized score between 0 and 100
        """

        return max(
            0.0,
            min(
                100.0,
                score,
            ),
        )

    def _get_verdict(
        self,
        score: float,
    ) -> str:
        """
        Get verdict based on score.

        Args:
            score: Normalized score (0-100)

        Returns:
            Verdict string (EXCELLENT, GOOD, MODERATE, or POOR)
        """

        if score >= VERDICT_THRESHOLDS["EXCELLENT"]:

            return "EXCELLENT"

        if score >= VERDICT_THRESHOLDS["GOOD"]:

            return "GOOD"

        if score >= VERDICT_THRESHOLDS["MODERATE"]:

            return "MODERATE"

        return "POOR"

    def analyze(
        self,
        nutrition: Dict[str, Any],
        ingredient_intelligence: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Analyze metabolic flexibility of a food product.

        Args:
            nutrition: Nutrition data containing:
                - protein (g)
                - fiber (g)
                - sugar (g)
            ingredient_intelligence: Ingredient analysis for processing level

        Returns:
            Metabolic flexibility analysis with:
            - metabolic_flexibility: Score (0-100)
            - score: Same as metabolic_flexibility
            - verdict: EXCELLENT, GOOD, MODERATE, or POOR
            - fuel_switching: Same as score (ability to switch fuel sources)
            - metabolic_resilience: Same as score (ability to maintain metabolic health)
        """

        # Extract nutrient values
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

        sugar = self._safe_float(
            nutrition.get(
                "sugar",
                0,
            )
        )

        # Extract processing level
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

        # Calculate base score
        score = self._calculate_base_score(
            protein,
            fiber,
            sugar,
        )

        # Apply processing penalty
        score = self._apply_processing_penalty(
            score,
            processing_level,
        )

        # Normalize to 0-100 range
        score = self._normalize_score(
            score,
        )

        # Get verdict
        verdict = self._get_verdict(
            score,
        )

        return {

            "metabolic_flexibility":
            round(
                score,
                2,
            ),

            "score":
            round(
                score,
                2,
            ),

            "verdict":
            verdict,

            "fuel_switching":
            round(
                score,
                2,
            ),

            "metabolic_resilience":
            round(
                score,
                2,
            ),

        }


# ==========================================================
# SINGLETON INSTANCE
# ==========================================================


metabolic_flexibility_engine = MetabolicFlexibilityEngine()


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [

    "MetabolicFlexibilityEngine",
    "metabolic_flexibility_engine",

]


# ==========================================================
# END OF FILE – metabolic_flexibility_engine.py
# ==========================================================