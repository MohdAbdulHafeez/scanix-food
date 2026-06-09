# ==========================================================
# SCANIX AI
# SYSTEM 4 – CONSUMER INTELLIGENCE (SERVICE)
# ELITE PRODUCTION GRADE – FINAL VERSION
# ==========================================================


from __future__ import annotations


from typing import Any
from typing import Dict
from typing import List
from typing import Optional


from .consumer_engine import ConsumerEngine

from .compliance_engine import ComplianceEngine

from .deception_engine import DeceptionEngine

from .suitability_engine import SuitabilityEngine

from .consumer_verdict_engine import VerdictEngine

from .health_alert_engine import HealthAlertEngine

from .ai_reasoner import AIReasoner


# ==========================================================
# CONSTANTS
# ==========================================================


DEFAULT_SCORE = 0

DEFAULT_ALERT = "GREEN"

DEFAULT_RECOMMENDATION = "UNKNOWN"

SERVICE_VERSION = "1.0"


# ==========================================================
# CONSUMER INTELLIGENCE SERVICE
# ==========================================================


class ConsumerIntelligenceService:
    """
    Master Service for System 4 – Consumer Intelligence.

    Orchestrates all consumer intelligence engines:
    - Compliance Engine (FSSAI regulations)
    - Deception Engine (marketing deception)
    - Suitability Engine (population and lifestyle fit)
    - Consumer Engine (overall consumer score)
    - Health Alert Engine (aggregated alerts)
    - Verdict Engine (final consumer verdict)
    - AI Reasoner (AI-powered insights)
    """

    def __init__(self) -> None:
        """
        Initialize the consumer intelligence service with all engines.
        """

        self.consumer_engine = ConsumerEngine()

        self.compliance_engine = ComplianceEngine()

        self.deception_engine = DeceptionEngine()

        self.suitability_engine = SuitabilityEngine()

        self.verdict_engine = VerdictEngine()

        self.health_alert_engine = HealthAlertEngine()

        self.ai_reasoner = AIReasoner()

    def analyze(
        self,
        claims: List[str],
        nutrition: Dict[str, Any],
        ingredient_intelligence: Dict[str, Any],
        metabolic_intelligence: Dict[str, Any],
        trust: Dict[str, Any],
        ocr_text: str = "",
        product_category: str = "",
    ) -> Dict[str, Any]:
        """
        Master analysis method for consumer intelligence.

        Args:
            claims: List of marketing claims from product
            nutrition: Nutrition data from System 1 (per 100g)
            ingredient_intelligence: Ingredient analysis from System 2
            metabolic_intelligence: Metabolic analysis from System 3
            trust: Trust analysis from System 8 (unused but kept for signature)
            ocr_text: Extracted OCR text from label
            product_category: Product category string

        Returns:
            Complete consumer intelligence analysis
        """

        # ==========================================================
        # COMPLIANCE ANALYSIS
        # ==========================================================

        compliance = self.compliance_engine.analyze(

            claims=claims,
            nutrition=nutrition,
            ingredient_intelligence=ingredient_intelligence,
            ocr_text=ocr_text,
            product_category=product_category,

        )

        # ==========================================================
        # DECEPTION ANALYSIS
        # ==========================================================

        deception = self.deception_engine.analyze(

            claims=claims,
            nutrition=nutrition,
            ingredient_intelligence=ingredient_intelligence,
            compliance=compliance,

        )

        # ==========================================================
        # SUITABILITY ANALYSIS
        # ==========================================================

        suitability = self.suitability_engine.analyze(

            nutrition=nutrition,
            ingredient_intelligence=ingredient_intelligence,
            metabolic_intelligence=metabolic_intelligence,
            impact_result=metabolic_intelligence.get(
                "health_impact",
                {},
            ),
            compliance=compliance,
            deception=deception,

        )

        # ==========================================================
        # CONSUMER SCORE ANALYSIS
        # ==========================================================

        consumer = self.consumer_engine.analyze(

            ingredient_intelligence=ingredient_intelligence,
            metabolic_intelligence=metabolic_intelligence,
            compliance=compliance,
            deception=deception,
            suitability=suitability,

        )

        # ==========================================================
        # HEALTH ALERTS ANALYSIS
        # ==========================================================

        health_alerts = self.health_alert_engine.analyze(

            consumer=consumer,
            compliance=compliance,
            deception=deception,
            suitability=suitability,
            metabolic_intelligence=metabolic_intelligence,
            ingredient_intelligence=ingredient_intelligence,

        )

        # ==========================================================
        # VERDICT ANALYSIS
        # ==========================================================

        verdict = self.verdict_engine.analyze(

            consumer=consumer,
            compliance=compliance,
            deception=deception,
            suitability=suitability,
            metabolic_intelligence=metabolic_intelligence,
            health_alerts=health_alerts,
            nutrition=nutrition,

        )

        # ==========================================================
        # AI REASONING ANALYSIS
        # ==========================================================

        ai_reasoning = self.ai_reasoner.analyze(

            consumer=consumer,
            compliance=compliance,
            deception=deception,
            suitability=suitability,
            verdict=verdict,
            health_alerts=health_alerts,
            metabolic_intelligence=metabolic_intelligence,

        )

        # ==========================================================
        # FINAL RESPONSE
        # ==========================================================

        consumer_score = consumer.get(
            "consumer_score",
            DEFAULT_SCORE,
        )

        fssai_score = compliance.get(
            "fssai_score",
            DEFAULT_SCORE,
        )

        consumer_safety_index = compliance.get(
            "consumer_safety_index",
            DEFAULT_SCORE,
        )

        deception_score = deception.get(
            "deception_score",
            DEFAULT_SCORE,
        )

        overall_alert = health_alerts.get(
            "overall_alert",
            DEFAULT_ALERT,
        )

        recommendation = verdict.get(
            "recommendation_level",
            DEFAULT_RECOMMENDATION,
        )

        buy_recommendation = ai_reasoning.get(
            "buy_recommendation",
            DEFAULT_RECOMMENDATION,
        )

        ai_provider = ai_reasoning.get(
            "provider",
            "none",
        )

        ai_model = ai_reasoning.get(
            "model",
            "none",
        )

        ai_confidence = ai_reasoning.get(
            "confidence",
            DEFAULT_SCORE,
        )

        return {

            "consumer": consumer,
            "compliance": compliance,
            "deception": deception,
            "suitability": suitability,
            "health_alerts": health_alerts,
            "verdict": verdict,
            "ai_reasoning": ai_reasoning,

            "summary": {

                "consumer_score": consumer_score,
                "fssai_score": fssai_score,
                "consumer_safety_index": consumer_safety_index,
                "deception_score": deception_score,
                "overall_alert": overall_alert,
                "recommendation": recommendation,
                "buy_recommendation": buy_recommendation,
                "ai_provider": ai_provider,
                "ai_model": ai_model,
                "ai_confidence": ai_confidence,

            },

        }


# ==========================================================
# SINGLETON INSTANCE
# ==========================================================


consumer_intelligence_service = ConsumerIntelligenceService()


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [

    "ConsumerIntelligenceService",
    "consumer_intelligence_service",

]


# ==========================================================
# INITIALIZATION LOG
# ==========================================================


from core.logging import log


log.info(
    "Consumer Intelligence Service initialized",
    version=SERVICE_VERSION,
    engines_loaded=True,
)


# ==========================================================
# END OF FILE – service.py
# ==========================================================