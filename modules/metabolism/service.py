# ==========================================================
# SCANIX AI
# SYSTEM 3 – METABOLIC INTELLIGENCE (SERVICE)
# ELITE PRODUCTION GRADE – FINAL VERSION
# ==========================================================


from __future__ import annotations


from typing import Any
from typing import Dict
from typing import Optional
from typing import Union


from modules.metabolism.metabolic_engine import (
    metabolic_engine,
)

from modules.metabolism.impact_engine import (
    impact_engine,
)

from modules.metabolism.verdict_engine import (
    verdict_engine,
)


# ==========================================================
# CONSTANTS
# ==========================================================


SERVICE_VERSION = "1.0"

DEFAULT_EMPTY_DICT: Dict[str, Any] = {}


# ==========================================================
# METABOLISM SERVICE
# ==========================================================


class MetabolismService:
    """
    Master Metabolism Service for System 3.

    Orchestrates all metabolic engines:
    - Metabolic Engine (satiety, energy curve, metabolic load)
    - Impact Engine (persona-based analysis)
    - Verdict Engine (final consumer verdict)

    Integrates data from:
    - System 1: Nutrition, Product, Scan Quality
    - System 2: Ingredient Intelligence
    """

    # =====================================================
    # SAFE HELPERS
    # =====================================================

    def _safe_dict(
        self,
        value: Any,
    ) -> Dict[str, Any]:
        """
        Safely convert value to dictionary.

        Args:
            value: Value to convert

        Returns:
            Dictionary if value is dict, otherwise empty dict
        """

        if isinstance(
            value,
            dict,
        ):

            return value

        return DEFAULT_EMPTY_DICT

    # =====================================================
    # MASTER ANALYSIS
    # =====================================================

    def analyze(
        self,
        nutrition: Optional[Dict[str, Any]] = None,
        ingredient_intelligence: Optional[Dict[str, Any]] = None,
        product: Optional[Dict[str, Any]] = None,
        scan_quality: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Master analysis method for metabolic intelligence.

        Args:
            nutrition: Nutrition data from System 1 (per 100g)
            ingredient_intelligence: Ingredient analysis from System 2
            product: Product data from System 1
            scan_quality: Scan quality data from System 1

        Returns:
            Complete metabolic analysis including:
            - metabolic: Metabolic engine results
            - health_impact: Impact engine results (personas)
            - verdict: Final consumer verdict
        """

        # Safely convert all inputs to dictionaries
        nutrition = self._safe_dict(
            nutrition
        )

        ingredient_intelligence = self._safe_dict(
            ingredient_intelligence
        )

        product = self._safe_dict(
            product
        )

        scan_quality = self._safe_dict(
            scan_quality
        )

        # ==========================================
        # METABOLIC ENGINE
        # ==========================================

        metabolic_result = metabolic_engine.analyze(

            nutrition=nutrition,

            ingredient_intelligence=ingredient_intelligence,

            product=product,

            scan_quality=scan_quality,

        )

        # ==========================================
        # IMPACT ENGINE
        # ==========================================

        impact_result = impact_engine.analyze(

            nutrition=nutrition,

            ingredient_intelligence=ingredient_intelligence,

            scan_quality=scan_quality,

            product=product,

        )

        # ==========================================
        # VERDICT ENGINE
        # ==========================================

        # Extract confidence from metabolic result
        confidence = metabolic_result.get(
            "confidence",
            {},
        )

        verdict_result = verdict_engine.analyze(

            product=product,

            ingredient_intelligence=ingredient_intelligence,

            metabolic_result=metabolic_result,

            impact_result=impact_result,

            confidence=confidence,

        )

        # ==========================================
        # FINAL RESPONSE
        # ==========================================

        return {

            "metabolism_version":
            SERVICE_VERSION,

            "metabolic":
            metabolic_result,

            "health_impact":
            impact_result,

            "verdict":
            verdict_result,

        }


# ==========================================================
# SINGLETON INSTANCE
# ==========================================================


metabolism_service = MetabolismService()


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [

    "MetabolismService",
    "metabolism_service",

]


# ==========================================================
# END OF FILE – service.py
# ==========================================================