# ==========================================================
# SCANIX AI
# SYSTEM 4 – CONSUMER INTELLIGENCE (AI REASONER)
# ELITE PRODUCTION GRADE – FINAL VERSION
# ==========================================================


from __future__ import annotations


import json
import os
import hashlib
import time
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple


import requests
from cachetools import TTLCache


# ==========================================================
# CONSTANTS
# ==========================================================


DEFAULT_TIMEOUT_SECONDS = 45
DEFAULT_MAX_RETRIES = 3
CACHE_MAX_SIZE = 2000
CACHE_TTL_SECONDS = 86400
DEFAULT_TEMPERATURE = 0.2
DEFAULT_MAX_TOKENS = 1200

CONFIDENCE_BASE = 50
CONFIDENCE_BOOST_CONSUMER = 5
CONFIDENCE_BOOST_COMPLIANCE = 5
CONFIDENCE_BOOST_METABOLIC = 5
CONFIDENCE_MIN = 0
CONFIDENCE_MAX = 100

SCORE_EXCELLENT_THRESHOLD = 80
SCORE_GOOD_THRESHOLD = 75
SCORE_LOW_THRESHOLD = 50
DECEPTION_LOW_THRESHOLD = 20
DECEPTION_HIGH_THRESHOLD = 50

CONSUMER_SCORE_HIGH_THRESHOLD = 80
COMPLIANCE_SCORE_HIGH_THRESHOLD = 80
SAFETY_INDEX_HIGH_THRESHOLD = 80
METABOLIC_SCORE_HIGH_THRESHOLD = 75

CONSUMER_SCORE_LOW_THRESHOLD = 50
METABOLIC_SCORE_LOW_THRESHOLD = 50

HEALTH_ALERT_RED = "RED"

BUY_RECOMMENDATION_STRONGLY_RECOMMENDED = "STRONGLY_RECOMMENDED"
BUY_RECOMMENDATION_RECOMMENDED = "RECOMMENDED"
BUY_RECOMMENDATION_LIMITED_CONSUMPTION = "LIMITED_CONSUMPTION"
BUY_RECOMMENDATION_NOT_RECOMMENDED = "NOT_RECOMMENDED"
BUY_RECOMMENDATION_UNKNOWN = "UNKNOWN"

PROVIDER_OPENROUTER = "openrouter"
PROVIDER_GROQ = "groq"
PROVIDER_LOCAL_FALLBACK = "local_fallback"
PROVIDER_NONE = "none"

MODEL_RULES_ENGINE = "rules_engine"


# ==========================================================
# AI REASONER
# ==========================================================


class AIReasoner:
    """
    AI Reasoner for System 4 – Consumer Intelligence.

    Provides AI-powered reasoning using:
    - OpenRouter as primary (GPT-5-mini, Claude Sonnet, Gemini 2.5 Pro)
    - Groq as fallback (Llama 3.3 70B, DeepSeek R1)
    - Local rules engine as final fallback

    Features:
    - Caching for repeated analyses
    - Health tracking for model performance
    - Timeout and retry mechanisms
    - JSON response validation
    """

    def __init__(self) -> None:
        """
        Initialize the AI Reasoner with API keys and configuration.
        """

        # API Keys
        self.openrouter_api_key = os.getenv(
            "OPENROUTER_API_KEY",
            "",
        )

        self.groq_api_key = os.getenv(
            "GROQ_API_KEY",
            "",
        )

        # Endpoints
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"

        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"

        # Primary models (OpenRouter)
        self.openrouter_models = [

            "openai/gpt-5-mini",
            "anthropic/claude-sonnet-4",
            "google/gemini-2.5-pro",

        ]

        # Fallback models (Groq)
        self.groq_models = [

            "llama-3.3-70b-versatile",
            "deepseek-r1-distill-llama-70b",

        ]

        # Configuration
        self.timeout = int(
            os.getenv(
                "AI_TIMEOUT_SECONDS",
                str(DEFAULT_TIMEOUT_SECONDS),
            )
        )

        self.max_retries = int(
            os.getenv(
                "AI_MAX_RETRIES",
                str(DEFAULT_MAX_RETRIES),
            )
        )

        # Session and cache
        self.session = requests.Session()

        self._cache = TTLCache(
            maxsize=CACHE_MAX_SIZE,
            ttl=CACHE_TTL_SECONDS,
        )

        # Health tracking for models
        self.model_health: Dict[str, Dict[str, Any]] = {}

        for model in self.openrouter_models + self.groq_models:

            self.model_health[model] = {

                "successes": 0,
                "failures": 0,
                "latency_ms": [],

            }

    # ==========================================================
    # MODEL ACCESSORS
    # ==========================================================

    def get_openrouter_models(self) -> List[str]:
        """
        Get list of OpenRouter models.

        Returns:
            List of OpenRouter model names
        """

        return self.openrouter_models

    def get_groq_models(self) -> List[str]:
        """
        Get list of Groq models.

        Returns:
            List of Groq model names
        """

        return self.groq_models

    def get_all_models(self) -> List[str]:
        """
        Get list of all available models.

        Returns:
            List of all model names
        """

        return self.openrouter_models + self.groq_models

    # ==========================================================
    # CACHING & HEALTH TRACKING
    # ==========================================================

    def _generate_cache_key(
        self,
        payload: Dict[str, Any],
    ) -> str:
        """
        Generate cache key from payload.

        Args:
            payload: Dictionary to hash

        Returns:
            SHA256 hash string
        """

        payload_str = json.dumps(
            payload,
            sort_keys=True,
        )

        return hashlib.sha256(
            payload_str.encode()
        ).hexdigest()

    def _record_health(
        self,
        model: str,
        success: bool,
        latency: float,
    ) -> None:
        """
        Record health metrics for a model.

        Args:
            model: Model name
            success: Whether call succeeded
            latency: Response latency in milliseconds
        """

        if model not in self.model_health:

            return

        if success:

            self.model_health[model]["successes"] += 1

            self.model_health[model]["latency_ms"].append(latency)

            # Keep only last 100 latency values
            self.model_health[model]["latency_ms"] = (
                self.model_health[model]["latency_ms"][-100:]
            )

        else:

            self.model_health[model]["failures"] += 1

    # ==========================================================
    # PROMPT & RESPONSE HELPERS
    # ==========================================================

    def clean_json_response(
        self,
        text: str,
    ) -> Dict[str, Any]:
        """
        Clean and parse JSON response from AI.

        Args:
            text: Raw response text

        Returns:
            Parsed JSON dictionary
        """

        if not text:

            return {}

        text = text.strip()

        # Remove markdown code blocks
        if text.startswith("```json"):

            text = text.replace("```json", "", 1)

        if text.startswith("```"):

            text = text.replace("```", "", 1)

        if text.endswith("```"):

            text = text[:-3]

        text = text.strip()

        try:

            return json.loads(text)

        except Exception:

            return {

                "executive_summary": text,
                "consumer_advice": "Could not parse AI advice structurally.",
                "health_summary": "Parse error in AI response.",
                "strengths": [],
                "concerns": [],
                "buy_recommendation": BUY_RECOMMENDATION_UNKNOWN,
                "confidence": CONFIDENCE_BASE,

            }

    def build_system_prompt(self) -> str:
        """
        Build system prompt for AI.

        Returns:
            System prompt string
        """

        return """
You are Scanix Consumer Intelligence AI, an expert clinical and regulatory analyst.

CRITICAL INSTRUCTIONS:
1. Explain WHY using ONLY the supplied evidence.
2. Do NOT invent facts, numbers, or ingredients.
3. The 'buy_recommendation' must reflect the raw data; do not invent a recommendation.
4. Return ONLY valid JSON matching the exact schema below. Do not include markdown code blocks or conversational text.

SCHEMA:
{
  "executive_summary": "High-level summary of the product's safety and quality.",
  "consumer_advice": "Actionable advice for the consumer.",
  "health_summary": "Detailed breakdown of metabolic, heart, and diabetic impact.",
  "strengths": ["List of exact strengths based on evidence"],
  "concerns": ["List of exact concerns based on evidence"],
  "buy_recommendation": "STRONGLY_RECOMMENDED|RECOMMENDED|LIMITED_CONSUMPTION|NOT_RECOMMENDED|UNKNOWN",
  "confidence": 0-100
}
"""

    def build_user_prompt(
        self,
        signal_summary: Dict[str, Any],
    ) -> str:
        """
        Build user prompt from signal summary.

        Args:
            signal_summary: Dictionary of signals

        Returns:
            JSON string for user prompt
        """

        return json.dumps(
            signal_summary,
            indent=2,
        )

    def build_signal_summary(
        self,
        consumer: Dict[str, Any],
        compliance: Dict[str, Any],
        deception: Dict[str, Any],
        suitability: Dict[str, Any],
        verdict: Dict[str, Any],
        health_alerts: Dict[str, Any],
        metabolic_intelligence: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Build signal summary for AI analysis.

        Args:
            consumer: Consumer analysis data
            compliance: Compliance analysis data
            deception: Deception analysis data
            suitability: Suitability analysis data (unused but kept for signature)
            verdict: Verdict analysis data
            health_alerts: Health alerts data
            metabolic_intelligence: Metabolic intelligence data

        Returns:
            Signal summary dictionary
        """

        metabolic_load = (

            metabolic_intelligence
            .get(
                "metabolic_load",
                {},
            )
            .get(
                "score",
                CONFIDENCE_BASE,
            )

        )

        satiety_score = (

            metabolic_intelligence
            .get(
                "satiety",
                {},
            )
            .get(
                "score",
                CONFIDENCE_BASE,
            )

        )

        metabolic_score = max(
            0,
            min(
                100,
                (satiety_score + (100 - metabolic_load)) // 2,
            ),
        )

        flat_metrics = {

            "consumer_score":

            consumer.get(
                "consumer_score",
                CONFIDENCE_BASE,
            ),

            "consumer_safety_index":

            health_alerts.get(
                "consumer_safety_index",
                consumer.get(
                    "consumer_safety_index",
                    CONFIDENCE_BASE,
                ),
            ),

            "compliance_score":

            compliance.get(
                "fssai_score",
                compliance.get(
                    "overall_compliance_score",
                    CONFIDENCE_BASE,
                ),
            ),

            "deception_score":

            deception.get(
                "deception_score",
                0,
            ),

            "trust_score":

            deception.get(
                "trust_score",
                CONFIDENCE_BASE,
            ),

            "brand_honesty_score":

            deception.get(
                "brand_honesty_score",
                CONFIDENCE_BASE,
            ),

            "consumer_harm_score":

            deception.get(
                "consumer_harm_score",
                0,
            ),

            "metabolic_score":

            metabolic_score,

            "overall_alert":

            health_alerts.get(
                "overall_alert",
                "GREEN",
            ),

        }

        structured_evidence = {

            "health_and_metabolic": {

                "hfss":
                health_alerts.get("hfss", False),

                "nova_processing_level":
                compliance.get("nova_classification", "UNKNOWN"),

                "health_alerts":
                health_alerts.get("alerts", []),

                "metabolic_concerns":
                metabolic_intelligence.get("concerns", []),

            },

            "compliance_and_deception": {

                "critical_violations":
                compliance.get("critical_violations", []),

                "deception_alerts":
                deception.get("alerts", []),

                "deception_evidence":
                deception.get("evidence", []),

            },

            "consumer_and_suitability": {

                "consumer_category":
                consumer.get("consumer_category", "UNKNOWN"),

                "positive_signals":
                consumer.get("positive_signals", []),

                "risk_flags":
                consumer.get("risk_flags", []),

            },

            "verdict_context": {

                "buy_decision":
                verdict.get("summary", {}).get("buy_decision", BUY_RECOMMENDATION_UNKNOWN),

                "overall_grade":
                verdict.get("summary", {}).get("grade", "C"),

            },

        }

        clinical_context = {

            "HFSS": (
                "High Fat, Sugar, Salt products are linked to obesity and metabolic diseases."
            ),

            "NOVA_4": (
                "Ultra-processed foods contain industrial formulations, "
                "promoting overconsumption and cardiovascular risks."
            ),

            "ADDITIVE_RISK": (
                "High additive loads can disrupt gut microbiome and metabolic signaling."
            ),

        }

        return {

            "metrics": flat_metrics,
            "evidence": structured_evidence,
            "clinical_context": clinical_context,

        }

    def _generate_local_fallback(
        self,
        signal_summary: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate local fallback reasoning when AI is unavailable.

        Args:
            signal_summary: Signal summary dictionary

        Returns:
            Fallback reasoning dictionary
        """

        metrics = signal_summary.get("metrics", {})

        evidence = signal_summary.get("evidence", {})

        deception_score = metrics.get("deception_score", 0)

        metabolic_score = metrics.get("metabolic_score", CONFIDENCE_BASE)

        overall_alert = metrics.get("overall_alert", "GREEN")

        verdict_data = evidence.get("verdict_context", {})

        health_data = evidence.get("health_and_metabolic", {})

        if overall_alert == HEALTH_ALERT_RED or deception_score >= DECEPTION_HIGH_THRESHOLD:

            exec_summary = (
                "High risk profile detected. Significant concerns regarding "
                "formulation or marketing."
            )

            advice = (
                "Avoid regular consumption. Seek whole-food alternatives."
            )

        elif overall_alert == "YELLOW" or deception_score >= DECEPTION_LOW_THRESHOLD:

            exec_summary = (
                "Moderate risk profile. Some formulation or marketing concerns exist."
            )

            advice = (
                "Consume in moderation. Be mindful of portion sizes."
            )

        else:

            exec_summary = (
                "Generally acceptable profile with low immediate health or deception risks."
            )

            advice = (
                "Safe for regular consumption as part of a balanced diet."
            )

        health_summary = (
            f"Metabolic Score is {metabolic_score}/100. "
            f"Processing Level: {health_data.get('nova_processing_level', 'UNKNOWN')}."
        )

        return {

            "executive_summary": exec_summary,
            "consumer_advice": advice,
            "health_summary": health_summary,
            "strengths": self.extract_strengths(metrics),
            "concerns": self.extract_concerns(metrics),
            "buy_recommendation": verdict_data.get("buy_decision", BUY_RECOMMENDATION_UNKNOWN),
            "confidence": 30,
            "provider": PROVIDER_LOCAL_FALLBACK,
            "model": MODEL_RULES_ENGINE,

        }

    # ==========================================================
    # API CALLS
    # ==========================================================

    def _call_openrouter(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Call OpenRouter API.

        Args:
            model: Model name
            system_prompt: System prompt
            user_prompt: User prompt

        Returns:
            Parsed response or None
        """

        if not self.openrouter_api_key:

            return None

        headers = {

            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json",

        }

        payload = {

            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": DEFAULT_TEMPERATURE,
            "max_tokens": DEFAULT_MAX_TOKENS,

        }

        start_time = time.time()

        try:

            response = self.session.post(

                self.openrouter_url,
                headers=headers,
                json=payload,
                timeout=self.timeout,

            )

            latency = int((time.time() - start_time) * 1000)

            if response.status_code != 200:

                self._record_health(model, False, latency)

                return None

            data = response.json()

            content = data["choices"][0]["message"]["content"]

            self._record_health(model, True, latency)

            return self.clean_json_response(content)

        except Exception:

            latency = int((time.time() - start_time) * 1000)

            self._record_health(model, False, latency)

            return None

    def _call_groq(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Call Groq API.

        Args:
            model: Model name
            system_prompt: System prompt
            user_prompt: User prompt

        Returns:
            Parsed response or None
        """

        if not self.groq_api_key:

            return None

        headers = {

            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json",

        }

        payload = {

            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": DEFAULT_TEMPERATURE,
            "max_tokens": DEFAULT_MAX_TOKENS,

        }

        start_time = time.time()

        try:

            response = self.session.post(

                self.groq_url,
                headers=headers,
                json=payload,
                timeout=self.timeout,

            )

            latency = int((time.time() - start_time) * 1000)

            if response.status_code != 200:

                self._record_health(model, False, latency)

                return None

            data = response.json()

            content = data["choices"][0]["message"]["content"]

            self._record_health(model, True, latency)

            return self.clean_json_response(content)

        except Exception:

            latency = int((time.time() - start_time) * 1000)

            self._record_health(model, False, latency)

            return None

    # ==========================================================
    # RESPONSE VALIDATION
    # ==========================================================

    def validate_response(
        self,
        result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Validate and normalize AI response.

        Args:
            result: Raw AI response

        Returns:
            Validated response dictionary
        """

        if not isinstance(result, dict):

            result = {}

        result.setdefault("executive_summary", "")
        result.setdefault("consumer_advice", "")
        result.setdefault("health_summary", "")
        result.setdefault("strengths", [])
        result.setdefault("concerns", [])
        result.setdefault("buy_recommendation", BUY_RECOMMENDATION_UNKNOWN)
        result.setdefault("confidence", CONFIDENCE_BASE)

        result["confidence"] = max(
            CONFIDENCE_MIN,
            min(
                CONFIDENCE_MAX,
                int(result.get("confidence", CONFIDENCE_BASE)),
            ),
        )

        return result

    # ==========================================================
    # REASONING GENERATION
    # ==========================================================

    def generate_reasoning(
        self,
        signal_summary: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate AI reasoning with fallback chain.

        Args:
            signal_summary: Signal summary dictionary

        Returns:
            Reasoning result dictionary
        """

        cache_key = self._generate_cache_key(signal_summary)

        if cache_key in self._cache:

            return self._cache[cache_key]

        system_prompt = self.build_system_prompt()

        user_prompt = self.build_user_prompt(signal_summary)

        # Try OpenRouter models
        for model in self.openrouter_models:

            for _ in range(self.max_retries):

                result = self._call_openrouter(
                    model,
                    system_prompt,
                    user_prompt,
                )

                if result:

                    result = self.validate_response(result)

                    result["provider"] = PROVIDER_OPENROUTER
                    result["model"] = model

                    self._cache[cache_key] = result

                    return result

        # Try Groq models as fallback
        for model in self.groq_models:

            for _ in range(self.max_retries):

                result = self._call_groq(
                    model,
                    system_prompt,
                    user_prompt,
                )

                if result:

                    result = self.validate_response(result)

                    result["provider"] = PROVIDER_GROQ
                    result["model"] = model

                    self._cache[cache_key] = result

                    return result

        # Final local fallback
        local_result = self._generate_local_fallback(signal_summary)

        self._cache[cache_key] = local_result

        return local_result

    # ==========================================================
    # LOCAL STRENGTH EXTRACTION
    # ==========================================================

    def extract_strengths(
        self,
        metrics: Dict[str, Any],
    ) -> List[str]:
        """
        Extract strengths from metrics.

        Args:
            metrics: Metrics dictionary

        Returns:
            List of strength strings
        """

        strengths = []

        if metrics.get("consumer_score", 0) >= CONSUMER_SCORE_HIGH_THRESHOLD:

            strengths.append("High consumer intelligence score")

        if metrics.get("compliance_score", 0) >= COMPLIANCE_SCORE_HIGH_THRESHOLD:

            strengths.append("Strong regulatory compliance")

        if metrics.get("consumer_safety_index", 0) >= SAFETY_INDEX_HIGH_THRESHOLD:

            strengths.append("Good overall safety profile")

        if metrics.get("deception_score", 100) <= DECEPTION_LOW_THRESHOLD:

            strengths.append("Low marketing deception risk")

        if metrics.get("metabolic_score", 0) >= METABOLIC_SCORE_HIGH_THRESHOLD:

            strengths.append("Favorable metabolic profile")

        return list(set(strengths))

    # ==========================================================
    # LOCAL CONCERN EXTRACTION
    # ==========================================================

    def extract_concerns(
        self,
        metrics: Dict[str, Any],
    ) -> List[str]:
        """
        Extract concerns from metrics.

        Args:
            metrics: Metrics dictionary

        Returns:
            List of concern strings
        """

        concerns = []

        if metrics.get("consumer_score", 100) < CONSUMER_SCORE_LOW_THRESHOLD:

            concerns.append("Low consumer score")

        if metrics.get("deception_score", 0) >= DECEPTION_HIGH_THRESHOLD:

            concerns.append("Potential marketing deception")

        if metrics.get("overall_alert", "GREEN") == HEALTH_ALERT_RED:

            concerns.append("Critical health alerts detected")

        if metrics.get("metabolic_score", 100) < METABOLIC_SCORE_LOW_THRESHOLD:

            concerns.append("Weak metabolic profile")

        return list(set(concerns))

    # ==========================================================
    # CONFIDENCE CALIBRATION
    # ==========================================================

    def calibrate_confidence(
        self,
        ai_result: Dict[str, Any],
        metrics: Dict[str, Any],
    ) -> int:
        """
        Calibrate confidence score.

        Args:
            ai_result: AI result dictionary
            metrics: Metrics dictionary

        Returns:
            Calibrated confidence score
        """

        confidence = int(
            ai_result.get(
                "confidence",
                CONFIDENCE_BASE,
            )
        )

        if metrics.get("consumer_score", 0) >= CONFIDENCE_BASE:

            confidence += CONFIDENCE_BOOST_CONSUMER

        if metrics.get("compliance_score", 0) >= CONFIDENCE_BASE:

            confidence += CONFIDENCE_BOOST_COMPLIANCE

        if metrics.get("metabolic_score", 0) >= CONFIDENCE_BASE:

            confidence += CONFIDENCE_BOOST_METABOLIC

        return max(
            CONFIDENCE_MIN,
            min(
                CONFIDENCE_MAX,
                confidence,
            ),
        )

    # ==========================================================
    # MAIN ENTRYPOINT
    # ==========================================================

    def analyze(
        self,
        consumer: Dict[str, Any],
        compliance: Dict[str, Any],
        deception: Dict[str, Any],
        suitability: Dict[str, Any],
        verdict: Dict[str, Any],
        health_alerts: Dict[str, Any],
        metabolic_intelligence: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Master analysis method for AI reasoning.

        Args:
            consumer: Consumer analysis data
            compliance: Compliance analysis data
            deception: Deception analysis data
            suitability: Suitability analysis data
            verdict: Verdict analysis data
            health_alerts: Health alerts data
            metabolic_intelligence: Metabolic intelligence data

        Returns:
            Complete AI reasoning analysis
        """

        signal_summary = self.build_signal_summary(

            consumer,
            compliance,
            deception,
            suitability,
            verdict,
            health_alerts,
            metabolic_intelligence,

        )

        ai_result = self.generate_reasoning(signal_summary)

        metrics = signal_summary.get("metrics", {})

        strengths = self.extract_strengths(metrics)

        concerns = self.extract_concerns(metrics)

        confidence = self.calibrate_confidence(ai_result, metrics)

        # Merge AI strengths with rule-based strengths
        merged_strengths = list(
            set(
                ai_result.get("strengths", []) + strengths
            )
        )

        merged_concerns = list(
            set(
                ai_result.get("concerns", []) + concerns
            )
        )

        return {

            "executive_summary": ai_result.get(
                "executive_summary",
                "",
            ),

            "consumer_advice": ai_result.get(
                "consumer_advice",
                "",
            ),

            "health_summary": ai_result.get(
                "health_summary",
                "",
            ),

            "strengths": merged_strengths,
            "concerns": merged_concerns,
            "buy_recommendation": ai_result.get(
                "buy_recommendation",
                BUY_RECOMMENDATION_UNKNOWN,
            ),
            "confidence": confidence,
            "provider": ai_result.get("provider", PROVIDER_NONE),
            "model": ai_result.get("model", MODEL_RULES_ENGINE),
            "signal_summary": signal_summary,

        }


# ==========================================================
# SINGLETON INSTANCE
# ==========================================================


ai_reasoner = AIReasoner()


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [

    "AIReasoner",
    "ai_reasoner",

]


# ==========================================================
# INITIALIZATION LOG
# ==========================================================


from core.logging import log


log.info(
    "AI Reasoner initialized",
    openrouter_enabled=bool(ai_reasoner.openrouter_api_key),
    groq_enabled=bool(ai_reasoner.groq_api_key),
    openrouter_models=ai_reasoner.openrouter_models,
    groq_models=ai_reasoner.groq_models,
    cache_size=CACHE_MAX_SIZE,
    cache_ttl=CACHE_TTL_SECONDS,
)


# ==========================================================
# END OF FILE – ai_reasoner.py
# ==========================================================