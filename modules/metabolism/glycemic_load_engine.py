# ==========================================================
# SCANIX AI
# SYSTEM 3 – METABOLIC INTELLIGENCE (GLYCEMIC LOAD ENGINE)
# ELITE PRODUCTION GRADE – FINAL VERSION
# ==========================================================


from __future__ import annotations


from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple


# ==========================================================
# CONSTANTS
# ==========================================================


DEFAULT_GI_BASELINE = 55.0

MAX_GI_BOOST = 20.0

MAX_GI_REDUCTION = 15.0

MIN_GI = 20.0

MAX_GI = 100.0

SUGAR_GI_BOOST_FACTOR = 0.8

FIBER_GI_REDUCTION_FACTOR = 1.5

GLYCEMIC_LOAD_CATEGORIES = {

    "LOW": 10,
    "MODERATE": 20,
    "HIGH": 999,

}

GLYCEMIC_LOAD_SCORES = {

    "LOW": 90,
    "MODERATE": 65,
    "HIGH": 25,

}

GLYCEMIC_LOAD_BURDEN_MULTIPLIER = 4.0

INSULIN_TRIGGER_MULTIPLIER = 3.5

CONFIDENCE_FULL_DATA = 100

CONFIDENCE_PARTIAL_DATA = 40

DEFAULT_CARBS_BY_CATEGORY = {

    "chips": 53,
    "crisps": 53,
    "snack": 53,
    "biscuit": 70,
    "cookie": 70,
    "cereal": 75,
    "breakfast cereal": 75,
    "soft drink": 11,
    "soda": 11,

}

CATEGORY_FIBER_DEFAULTS = {

    "chips": 3,
    "crisps": 3,
    "snack": 3,

}


# ==========================================================
# GLYCEMIC LOAD ENGINE
# ==========================================================


class GlycemicLoadEngine:
    """
    Production Glycemic Load Engine for System 3.

    Calculates estimated glycemic load based on:
    - Carbohydrates
    - Fiber (reduces available carbs)
    - Sugar (increases GI estimate)

    Inputs:
        carbohydrates (g/100g)
        fiber (g/100g)
        sugar (g/100g)
        category (optional, for fallback values)

    Outputs:
        glycemic_load: Estimated glycemic load value
        estimated_gi: Estimated glycemic index (20-100)
        available_carbs: Net carbohydrates (carbs - fiber)
        category: LOW (<10), MODERATE (10-20), HIGH (>20)
        score: Health score (90, 65, or 25)
        blood_sugar_burden: 0-100 scale
        insulin_trigger: 0-100 scale
        confidence: Data confidence percentage
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

    def _get_default_carbs_by_category(
        self,
        product_category: str,
    ) -> Tuple[float, float]:
        """
        Get default carbohydrate and fiber values based on product category.

        Args:
            product_category: Product category string

        Returns:
            Tuple of (default_carbs, default_fiber)
        """

        category_lower = product_category.lower()

        default_fiber = 0.0

        for key, value in DEFAULT_CARBS_BY_CATEGORY.items():

            if key in category_lower:

                if key in CATEGORY_FIBER_DEFAULTS:

                    default_fiber = CATEGORY_FIBER_DEFAULTS[key]

                return float(value), default_fiber

        return 0.0, 0.0

    def _estimate_gi(
        self,
        sugar: float,
        fiber: float,
    ) -> float:
        """
        Estimate glycemic index based on sugar and fiber content.

        Formula:
        Baseline GI (55) + sugar boost - fiber reduction

        Args:
            sugar: Sugar content in grams
            fiber: Fiber content in grams

        Returns:
            Estimated GI between 20 and 100
        """

        gi = DEFAULT_GI_BASELINE

        # Sugar increases GI (up to +20)
        gi += min(
            MAX_GI_BOOST,
            sugar * SUGAR_GI_BOOST_FACTOR,
        )

        # Fiber decreases GI (up to -15)
        gi -= min(
            MAX_GI_REDUCTION,
            fiber * FIBER_GI_REDUCTION_FACTOR,
        )

        # Clamp to valid range
        gi = max(
            MIN_GI,
            min(
                MAX_GI,
                gi,
            ),
        )

        return gi

    def _get_glycemic_load_category(
        self,
        glycemic_load: float,
    ) -> str:
        """
        Get category based on glycemic load value.

        Args:
            glycemic_load: Calculated glycemic load

        Returns:
            Category string (LOW, MODERATE, or HIGH)
        """

        if glycemic_load < GLYCEMIC_LOAD_CATEGORIES["LOW"]:

            return "LOW"

        if glycemic_load < GLYCEMIC_LOAD_CATEGORIES["MODERATE"]:

            return "MODERATE"

        return "HIGH"

    def _get_glycemic_load_score(
        self,
        category: str,
    ) -> int:
        """
        Get health score based on glycemic load category.

        Args:
            category: LOW, MODERATE, or HIGH

        Returns:
            Health score (90, 65, or 25)
        """

        return GLYCEMIC_LOAD_SCORES.get(
            category,
            GLYCEMIC_LOAD_SCORES["MODERATE"],
        )

    def _calculate_blood_sugar_burden(
        self,
        glycemic_load: float,
    ) -> float:
        """
        Calculate blood sugar burden (0-100 scale).

        Args:
            glycemic_load: Calculated glycemic load

        Returns:
            Blood sugar burden score
        """

        burden = glycemic_load * GLYCEMIC_LOAD_BURDEN_MULTIPLIER

        return round(
            min(
                100.0,
                burden,
            ),
            2,
        )

    def _calculate_insulin_trigger(
        self,
        glycemic_load: float,
    ) -> float:
        """
        Calculate insulin trigger score (0-100 scale).

        Args:
            glycemic_load: Calculated glycemic load

        Returns:
            Insulin trigger score
        """

        trigger = glycemic_load * INSULIN_TRIGGER_MULTIPLIER

        return round(
            min(
                100.0,
                trigger,
            ),
            2,
        )

    def _calculate_confidence(
        self,
        has_carbs: bool,
    ) -> int:
        """
        Calculate confidence score based on data completeness.

        Args:
            has_carbs: Whether carbohydrate data is available

        Returns:
            Confidence score (100 or 40)
        """

        if has_carbs:

            return CONFIDENCE_FULL_DATA

        return CONFIDENCE_PARTIAL_DATA

    def analyze(
        self,
        nutrition: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Analyze glycemic load for a food product.

        Args:
            nutrition: Nutrition data containing:
                - carbohydrates (g)
                - protein (g)
                - fiber (g)
                - sugar (g)
                - category (optional)

        Returns:
            Glycemic load analysis with all metrics
        """

        # Extract nutrition values
        carbs = self._safe_float(
            nutrition.get(
                "carbohydrates",
                0,
            )
        )

        sugar = self._safe_float(
            nutrition.get(
                "sugar",
                0,
            )
        )

        fiber = self._safe_float(
            nutrition.get(
                "fiber",
                0,
            )
        )

        product_category = str(

            nutrition.get(
                "category",
                "",
            )

        ).lower()

        has_carbs = False

        # Handle missing carbs using category defaults
        if carbs <= 0:

            default_carbs, default_fiber = self._get_default_carbs_by_category(
                product_category
            )

            if default_carbs > 0:

                carbs = default_carbs

                if fiber <= 0 and default_fiber > 0:

                    fiber = default_fiber

                has_carbs = True

            elif sugar > 0:

                carbs = sugar * 1.5

                has_carbs = False

            else:

                has_carbs = False

        else:

            has_carbs = True

        # Calculate available carbs (net of fiber)
        available_carbs = max(
            0.0,
            carbs - fiber,
        )

        # Estimate glycemic index
        estimated_gi = self._estimate_gi(
            sugar=sugar,
            fiber=fiber,
        )

        # Calculate glycemic load
        glycemic_load = round(

            (
                estimated_gi
                *
                available_carbs
            )
            / 100,

            2,
        )

        # Determine category
        category = self._get_glycemic_load_category(
            glycemic_load,
        )

        # Get health score
        score = self._get_glycemic_load_score(
            category,
        )

        # Calculate derived metrics
        blood_sugar_burden = self._calculate_blood_sugar_burden(
            glycemic_load,
        )

        insulin_trigger = self._calculate_insulin_trigger(
            glycemic_load,
        )

        # Calculate confidence
        confidence = self._calculate_confidence(
            has_carbs,
        )

        return {

            "glycemic_load":
            glycemic_load,

            "estimated_gi":
            round(
                estimated_gi,
                2,
            ),

            "available_carbs":
            round(
                available_carbs,
                2,
            ),

            "category":
            category,

            "score":
            score,

            "blood_sugar_burden":
            blood_sugar_burden,

            "insulin_trigger":
            insulin_trigger,

            "confidence":
            confidence,

        }


# ==========================================================
# SINGLETON INSTANCE
# ==========================================================


glycemic_load_engine = GlycemicLoadEngine()


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [

    "GlycemicLoadEngine",
    "glycemic_load_engine",

]


# ==========================================================
# END OF FILE – glycemic_load_engine.py
# ==========================================================