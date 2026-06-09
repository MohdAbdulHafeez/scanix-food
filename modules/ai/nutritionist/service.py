from __future__ import annotations

import logging

from typing import Any
from typing import Dict
from typing import List

from .nutritionist_engine import (
    ai_nutritionist_engine,
)

from .meal_planner_engine import (
    meal_planner_engine,
)

from ..food_explainer.service import (
    food_explainer_service,
)


log = logging.getLogger(__name__)


class NutritionistService:

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

        return str(value)

    # =====================================================
    # MASTER ANALYSIS
    # =====================================================

    def analyze(

        self,

        profile: Dict[str, Any] | None = None,

        product: Dict[str, Any] | None = None,

        nutrition: Dict[str, Any] | None = None,

        claims: List[str] | None = None,

        ocr_text: str = "",

        serving_size: str = "",

        scan_quality: Dict[str, Any] | None = None,

        ingredient_intelligence:
        Dict[str, Any] | None = None,

        metabolic_intelligence:
        Dict[str, Any] | None = None,

        consumer_intelligence:
        Dict[str, Any] | None = None,

        body_intelligence:
        Dict[str, Any] | None = None,

        scan_history:
        List[Dict[str, Any]] | None = None,

        conversation_history:
        List[Dict[str, Any]] | None = None,

        user_query: str = "",


    ) -> Dict[str, Any]:

        try:

            # =====================================
            # SANITIZATION
            # =====================================

            profile = self._safe_dict(
                profile
            )

            product = self._safe_dict(
                product
            )

            nutrition = self._safe_dict(
                nutrition
            )

            claims = self._safe_list(
                claims
            )

            scan_quality = (
                self._safe_dict(
                    scan_quality
                )
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

            body_intelligence = (
                self._safe_dict(
                    body_intelligence
                )
            )

            scan_history = (
                self._safe_list(
                    scan_history
                )
            )

            conversation_history = (
                self._safe_list(
                    conversation_history
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
            # FOOD EXPLAINER
            # =====================================

            food_explainer = (

                food_explainer_service
                .analyze(

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

                )

            )

            # =====================================
            # AI NUTRITIONIST
            # =====================================

            nutritionist = (

                ai_nutritionist_engine
                .analyze(

                    profile=
                    profile,

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

                    scan_quality=
                    scan_quality,

                    ingredient_intelligence=
                    ingredient_intelligence,

                    metabolic_intelligence=
                    metabolic_intelligence,

                    consumer_intelligence=
                    consumer_intelligence,

                    food_explainer=
                    food_explainer,

                    body_intelligence=
                    body_intelligence,

                    scan_history=
                    scan_history,

                    conversation_history=
                    conversation_history,

                    user_query=
                    user_query,

                )

            )

            # =====================================
            # MEAL PLANNER
            # =====================================

            meal_plan = (

                meal_planner_engine
                .analyze(

                    profile=
                    profile,

                    metabolic_intelligence=
                    metabolic_intelligence,

                )

            )

            # =====================================
            # EXTRACTS
            # =====================================

            voice_response = (

                nutritionist.get(

                    "voice_response",

                    {},

                )

            )

            nutrition_targets = (

                nutritionist.get(

                    "nutrition_targets",

                    {},

                )

            )

            recommendations = (

                voice_response.get(

                    "recommendations",

                    [],

                )

            )

            warnings = (

                voice_response.get(

                    "warnings",

                    [],

                )

            )

            confidence = (

                nutritionist.get(

                    "confidence",

                    0,

                )

            )

            # =====================================
            # FINAL RESPONSE
            # =====================================

            return {

                "success":
                True,

                "nutritionist_version":
                "1.0",

                "nutritionist":
                nutritionist,

                "meal_plan":
                meal_plan,

                "food_guidance":

                food_explainer.get(

                    "explainer",

                    {},

                ),

                "voice_response":
                voice_response,

                "nutrition_targets":
                nutrition_targets,

                "recommendations":
                recommendations,

                "warnings":
                warnings,

                "confidence":
                confidence,

                "summary": {

                    "goal":

                    nutritionist
                    .get(
                        "goals",
                        {},
                    )
                    .get(
                        "primary_goal",
                        "GENERAL_HEALTH",
                    ),

                    "consumer_score":

                    consumer_intelligence
                    .get(
                        "consumer",
                        {},
                    )
                    .get(
                        "consumer_score",
                        0,
                    ),

                    "meal_plan_ready":
                    True,

                    "voice_ready":
                    True,

                    "food_explainer_ready":
                    True,

                },

            }

        except Exception as e:

            log.exception(

                f"Nutritionist Service Failed: {e}"

            )

            return {

                "success":
                False,

                "nutritionist_version":
                "1.0",

                "nutritionist": {},

                "meal_plan": {},

                "food_guidance": {},

                "voice_response": {},

                "nutrition_targets": {},

                "recommendations": [],

                "warnings": [],

                "confidence": 0,

                "error":
                str(e),

            }


nutritionist_service = (
    NutritionistService()
)