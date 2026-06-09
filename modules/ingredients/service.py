# ==========================================================
# SCANIX AI
# SYSTEM 2 – INGREDIENT INTELLIGENCE SERVICE
# ELITE PRODUCTION GRADE – FINAL VERSION
# ==========================================================


from __future__ import annotations


import logging
from typing import Any
from typing import Dict
from typing import List
from typing import Optional


from .parser import IngredientParser

from .additive_engine import AdditiveEngine

from .verifier import IngredientVerifier

from .ingredient_function_engine import (
    ingredient_function_engine,
)

from .ingredient_risk_engine import (
    ingredient_risk_engine,
)


log = logging.getLogger(__name__)


# ==========================================================
# INGREDIENT INTELLIGENCE SERVICE
# ==========================================================


class IngredientIntelligenceService:
    """
    Master orchestrator for System 2 – Ingredient Intelligence.

    Integrates:
    - Ingredient parsing and classification
    - Additive detection and risk scoring
    - Ingredient function detection
    - Ingredient risk profiling
    - Claim verification
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize the ingredient intelligence service with all engines.
        """

        self.parser = IngredientParser()

        self.additive_engine = AdditiveEngine()

        self.verifier = IngredientVerifier()

        self.function_engine = ingredient_function_engine

        self.risk_engine = ingredient_risk_engine


    def analyze(
        self,
        ingredients_text: str,
    ) -> Dict[str, Any]:
        """
        Analyze ingredients text and return comprehensive intelligence.

        Args:
            ingredients_text: Raw OCR text containing ingredients

        Returns:
            Complete ingredient analysis including:
            - Ingredient profile and classification
            - Additive detection and risk scores
            - Ingredient functions
            - Ingredient risk profiling
            - Claim verification
        """

        try:

            # Step 1: Parse ingredients
            parser_analysis = self.parser.analyze(
                ingredients_text
            )

            # Step 2: Extract ingredient names
            ingredient_records = parser_analysis.get(
                "ingredients",
                [],
            )

            ingredients = [

                ingredient.get("name", "")

                for ingredient in ingredient_records

                if ingredient.get("name")

            ]

            # Step 3: Analyze additives
            additive_analysis = self.additive_engine.analyze(
                ingredients
            )

            # Step 4: Analyze ingredient functions
            function_analysis = self.function_engine.analyze(
                ingredients
            )

            # Step 5: Analyze ingredient risks
            risk_analysis = self.risk_engine.analyze(
                ingredients
            )

            # Step 6: Verify claims
            verification_analysis = self.verifier.verify(
                ingredients,
                parser_analysis,
                additive_analysis,
            )

            # Step 7: Build registry info from parser
            registry = parser_analysis.get(
                "registry",
                {},
            )

            # Step 8: Build summary with all fields
            ingredient_summary = parser_analysis.get(
                "ingredient_summary",
                {},
            )

            scores = parser_analysis.get(
                "scores",
                {},
            )

            processing_analysis = parser_analysis.get(
                "processing_analysis",
                {},
            )

            ingredient_profile = parser_analysis.get(
                "ingredient_profile",
                {},
            )

            return {

                "success": True,

                "ingredient_intelligence_version": "2.2",

                # Parser outputs
                "ingredient_profile": ingredient_profile,

                "ingredients": ingredient_records,

                "scores": scores,

                "processing_analysis": processing_analysis,

                "ingredient_summary": ingredient_summary,

                # Registry outputs (from parser)
                "registry": {

                    "e_numbers": registry.get(
                        "e_numbers",
                        [],
                    ),

                    "high_risk_additives": registry.get(
                        "high_risk_additives",
                        [],
                    ),

                    "allergens": registry.get(
                        "allergens",
                        [],
                    ),

                    "contains_palm_oil": registry.get(
                        "contains_palm_oil",
                        False,
                    ),

                },

                # Additive engine outputs
                "additives": additive_analysis,

                # Function engine outputs
                "ingredient_functions": function_analysis,

                # Risk engine outputs
                "ingredient_risks": risk_analysis,

                # Verifier outputs
                "verification": verification_analysis,

            }

        except Exception as e:

            log.exception(
                f"Ingredient Intelligence failed: {e}"
            )

            return {

                "success": False,

                "ingredient_intelligence_version": "2.2",

                "ingredient_profile": {},

                "ingredients": [],

                "scores": {},

                "processing_analysis": {},

                "ingredient_summary": {},

                "registry": {

                    "e_numbers": [],

                    "high_risk_additives": [],

                    "allergens": [],

                    "contains_palm_oil": False,

                },

                "additives": {},

                "ingredient_functions": {},

                "ingredient_risks": {},

                "verification": {},

                "error": str(e),

            }


# ==========================================================
# SINGLETON INSTANCE
# ==========================================================


ingredient_intelligence_service = IngredientIntelligenceService()


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [
    "IngredientIntelligenceService",
    "ingredient_intelligence_service",
]


# ==========================================================
# INITIALIZATION LOG
# ==========================================================


log.info(
    "Ingredient Intelligence Service initialized",
    version="2.2",
)


# ==========================================================
# END OF FILE – service.py
# ==========================================================

# modules/ingredients/service.py

from . import ingredient_intelligence_service
__all__ = ["ingredient_intelligence_service"]