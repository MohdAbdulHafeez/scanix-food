from __future__ import annotations

import logging

from typing import Any
from typing import Dict
from typing import List

from .rag_engine import (
    food_rag_engine,
)

from .explainer_engine import (
    food_explainer_engine,
)


log = logging.getLogger(__name__)


class FoodExplainerService:

    # =====================================================
    # SAFE HELPERS
    # =====================================================

    def _safe_dict(
        self,
        value: Any,
    ) -> Dict[str, Any]:

        if isinstance(
            value,
            dict,
        ):
            return value

        return {}

    def _safe_list(
        self,
        value: Any,
    ) -> List[Any]:

        if isinstance(
            value,
            list,
        ):
            return value

        return []

    def _safe_string(
        self,
        value: Any,
    ) -> str:

        if value is None:
            return ""

        return str(
            value
        )

    # =====================================================
    # MASTER ANALYSIS
    # =====================================================

    def analyze(

        self,

        product: Dict[str, Any] | None = None,

        nutrition: Dict[str, Any] | None = None,

        claims: List[str] | None = None,

        ocr_text: str = "",

        serving_size: str = "",

        ingredient_intelligence:
        Dict[str, Any] | None = None,

        metabolic_intelligence:
        Dict[str, Any] | None = None,

        consumer_intelligence:
        Dict[str, Any] | None = None,

        digital_twin:
        Dict[str, Any] | None = None,

    ) -> Dict[str, Any]:

        try:

            # =====================================
            # INPUT SANITIZATION
            # =====================================

            product = self._safe_dict(
                product
            )

            nutrition = self._safe_dict(
                nutrition
            )

            claims = self._safe_list(
                claims
            )

            ingredient_intelligence = (
                self._safe_dict(
                    ingredient_intelligence
                )
            )

            metabolic_intelligence = (
                self._safe_dict(
                    metabolic_intelligence
                )
            )

            consumer_intelligence = (
                self._safe_dict(
                    consumer_intelligence
                )
            )

            digital_twin = (
                self._safe_dict(
                    digital_twin
                )
            )

            ocr_text = self._safe_string(
                ocr_text
            )

            serving_size = (
                self._safe_string(
                    serving_size
                )
            )

            # =====================================
            # RAG ANALYSIS
            # =====================================

            rag_result = (

    food_rag_engine.analyze(

        product_name=

        product.get(

            "name",

            "Unknown Product",

        ),

        ingredient_intelligence=
        ingredient_intelligence,

        metabolic_intelligence=
        metabolic_intelligence,

        consumer_intelligence=
        consumer_intelligence,

    )

)

            # =====================================
            # FOOD EXPLAINER ANALYSIS
            # =====================================

            explainer_result = (

                food_explainer_engine.analyze(

                    product=
                    product,

                    nutrition=
                    nutrition,

                    claims=
                    claims,

                    ocr_text=
                    ocr_text,

                    serving_size=
                    serving_size,

                    ingredient_intelligence=
                    ingredient_intelligence,

                    metabolic_intelligence=
                    metabolic_intelligence,

                    consumer_intelligence=
                    consumer_intelligence,

                    rag_result=
                    rag_result,

                )

            )

            # =====================================
            # FINAL RESPONSE
            # =====================================

            return {

                "success":
                True,

                "food_explainer_version":
                "1.0",

                "rag":
                rag_result,

                "explainer":
                explainer_result,

                "summary": {

                    "research_confidence":

                    rag_result.get(
                        "research_confidence"
                    ),

                    "scientific_consensus":

                    rag_result.get(
                        "scientific_consensus"
                    ),

                    "evidence_strength":

                    rag_result.get(
                        "evidence_strength"
                    ),

                    "final_verdict":

                    explainer_result.get(
                        "final_verdict",
                        {},
                    ),

                },

            }

        except Exception as e:

            log.exception(

                f"Food Explainer failed: {e}"

            )

            return {

                "success":
                False,

                "food_explainer_version":
                "1.0",

                "rag": {},

                "explainer": {},

                "summary": {},

                "error":
                str(e),

            }


food_explainer_service = (
    FoodExplainerService()
)