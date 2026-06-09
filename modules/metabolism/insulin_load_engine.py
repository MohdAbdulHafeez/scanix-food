# ==========================================================
# SCANIX AI
# SYSTEM 3 – METABOLIC INTELLIGENCE (INSULIN LOAD ENGINE)
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

INSULIN_LOAD_THRESHOLDS = {

    "LOW": 15,
    "MODERATE": 30,
    "HIGH": 999,

}

PANCREATIC_STRESS_MULTIPLIER = 3.0

BETA_CELL_BURDEN_MULTIPLIER = 2.5

PROTEIN_INSULIN_FACTOR = 0.56

SUGAR_INSULIN_FACTOR = 0.35

CONFIDENCE_FULL_DATA = 100

CONFIDENCE_PARTIAL_DATA = 40


# ==========================================================
# INSULIN LOAD ENGINE
# ==========================================================


class InsulinLoadEngine:
    """
    Elite Insulin Load Engine for System 3.

    Calculates estimated insulin load based on:
    - Carbohydrates (net of fiber)
    - Protein (modest insulin response)
    - Sugar (higher glycemic impact)

    Provides pancreatic stress and beta-cell burden estimates.
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

    def _get_default_carbs_by_category(
        self,
        product_category: str,
    ) -> float:
        """
        Get default carbohydrate value based on product category.

        Args:
            product_category: Product category string

        Returns:
            Default carbs value or 0.0
        """

        category_lower = product_category.lower()

        for key, value in DEFAULT_CARBS_BY_CATEGORY.items():

            if key in category_lower:

                return float(value)

        return 0.0

    def _calculate_insulin_load(
        self,
        net_carbs: float,
        protein: float,
        sugar: float,
    ) -> float:
        """
        Calculate estimated insulin load.

        Formula:
        (net carbs) + (protein * 0.56) + (sugar * 0.35)

        Args:
            net_carbs: Carbohydrates minus fiber
            protein: Protein content in grams
            sugar: Sugar content in grams

        Returns:
            Insulin load value (≥ 0)
        """

        insulin_load = (

            net_carbs

            +

            (protein * PROTEIN_INSULIN_FACTOR)

            +

            (sugar * SUGAR_INSULIN_FACTOR)

        )

        return max(
            0.0,
            insulin_load,
        )

    def _get_insulin_load_category(
        self,
        insulin_load: float,
    ) -> str:
        """
        Get category based on insulin load value.

        Args:
            insulin_load: Calculated insulin load

        Returns:
            Category string (LOW, MODERATE, or HIGH)
        """

        if insulin_load < INSULIN_LOAD_THRESHOLDS["LOW"]:

            return "LOW"

        if insulin_load < INSULIN_LOAD_THRESHOLDS["MODERATE"]:

            return "MODERATE"

        return "HIGH"

    def _calculate_score(
        self,
        insulin_load: float,
    ) -> float:
        """
        Calculate health score (0-100) based on insulin load.

        Args:
            insulin_load: Calculated insulin load

        Returns:
            Score between 0 and 100
        """

        raw_score = 100 - (insulin_load * 2.5)

        return max(
            0.0,
            min(
                100.0,
                raw_score,
            ),
        )

    def _calculate_pancreatic_stress(
        self,
        insulin_load: float,
    ) -> float:
        """
        Calculate pancreatic stress estimate (0-100).

        Args:
            insulin_load: Calculated insulin load

        Returns:
            Pancreatic stress score
        """

        stress = insulin_load * PANCREATIC_STRESS_MULTIPLIER

        return round(
            min(
                100.0,
                stress,
            ),
            2,
        )

    def _calculate_beta_cell_burden(
        self,
        insulin_load: float,
    ) -> float:
        """
        Calculate beta-cell burden estimate (0-100).

        Args:
            insulin_load: Calculated insulin load

        Returns:
            Beta-cell burden score
        """

        burden = insulin_load * BETA_CELL_BURDEN_MULTIPLIER

        return round(
            min(
                100.0,
                burden,
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
        Analyze insulin load for a food product.

        Args:
            nutrition: Nutrition data containing:
                - carbohydrates (g)
                - protein (g)
                - fiber (g)
                - sugar (g)
                - category (optional)

        Returns:
            Insulin load analysis with:
            - insulin_load: Estimated insulin load value
            - category: LOW / MODERATE / HIGH
            - score: Health score (0-100)
            - pancreatic_stress: Pancreatic stress estimate
            - beta_cell_burden: Beta-cell burden estimate
            - confidence: Data confidence percentage
        """

        # Extract nutrition values
        carbs = self._safe_float(
            nutrition.get(
                "carbohydrates",
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

        sugar = self._safe_float(
            nutrition.get(
                "sugar",
                0,
            )
        )

        product_category = str(

            nutrition.get(
                "category",
                "",
            )

        ).lower()

        # Handle missing carbs using category defaults
        if carbs <= 0:

            default_carbs = self._get_default_carbs_by_category(
                product_category
            )

            if default_carbs > 0:

                carbs = default_carbs

            elif sugar > 0:

                carbs = sugar * 1.5

        # Calculate net carbs
        net_carbs = max(
            0.0,
            carbs - fiber,
        )

        # Calculate insulin load
        insulin_load = self._calculate_insulin_load(
            net_carbs,
            protein,
            sugar,
        )

        # Determine category
        category = self._get_insulin_load_category(
            insulin_load,
        )

        # Calculate health score
        score = self._calculate_score(
            insulin_load,
        )

        # Calculate pancreatic stress
        pancreatic_stress = self._calculate_pancreatic_stress(
            insulin_load,
        )

        # Calculate beta-cell burden
        beta_cell_burden = self._calculate_beta_cell_burden(
            insulin_load,
        )

        # Calculate confidence
        has_carbs = (
            nutrition.get(
                "carbohydrates",
                0,
            ) > 0
            or default_carbs > 0
            or sugar > 0
        )

        confidence = self._calculate_confidence(
            has_carbs,
        )

        return {

            "insulin_load":
            round(
                insulin_load,
                2,
            ),

            "category":
            category,

            "score":
            round(
                score,
                2,
            ),

            "pancreatic_stress":
            pancreatic_stress,

            "beta_cell_burden":
            beta_cell_burden,

            "confidence":
            confidence,

        }


# ==========================================================
# SINGLETON INSTANCE
# ==========================================================


insulin_load_engine = InsulinLoadEngine()


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [

    "InsulinLoadEngine",
    "insulin_load_engine",

]


# ==========================================================
# END OF FILE – insulin_load_engine.py
# ==========================================================