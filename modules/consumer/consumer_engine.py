# ==========================================================
# SCANIX AI
# SYSTEM 4 – CONSUMER INTELLIGENCE (CONSUMER ENGINE)
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


DEFAULT_SCORE = 50

DEFAULT_PERCENTAGE = 50

DEFAULT_PENALTY = 50

DEFAULT_TRUST_SCORE = 50

DEFAULT_BRAND_HONESTY = 50

DEFAULT_HARM_SCORE = 0

DEFAULT_BUY_DECISION = "UNKNOWN"

DEFAULT_OVERALL_GRADE = "UNKNOWN"

DEFAULT_SCORE_BREAKDOWN = {

    "suitability": DEFAULT_SCORE,
    "metabolic": DEFAULT_SCORE,
    "compliance": DEFAULT_SCORE,
    "trust": DEFAULT_TRUST_SCORE,
    "deception_penalty": DEFAULT_PENALTY,

}


WEIGHT_SUITABILITY = 0.35
WEIGHT_METABOLIC = 0.25
WEIGHT_COMPLIANCE = 0.20
WEIGHT_TRUST = 0.20

DECEPTION_PENALTY_FACTOR = 0.15

CONFIDENCE_AVERAGE_DIVISOR = 3

ADDITIVE_COUNT_HIGH_THRESHOLD = 5
INGREDIENT_COUNT_HIGH_THRESHOLD = 20

PROCESSING_LEVEL_HIGH_RISK = ["ULTRA_PROCESSED", "NOVA_4"]

METABOLIC_FLEXIBILITY_EXCELLENT_THRESHOLD = 80

TRUST_EXCELLENT_THRESHOLD = 80
COMPLIANCE_EXCELLENT_THRESHOLD = 85

DECEPTION_HIGH_THRESHOLD = 50
CONSUMER_HARM_HIGH_THRESHOLD = 60
ADDITIVE_HIGH_THRESHOLD = 5

CONSUMER_SCORE_CATEGORIES = {

    "EXCELLENT": 85,
    "GOOD": 70,
    "MODERATE": 55,
    "POOR": 40,
    "AVOID": 0,

}

EXECUTIVE_STATUS_MAP = {

    "EXCELLENT": "RECOMMENDED",
    "GOOD": "GOOD_CHOICE",
    "MODERATE": "OCCASIONAL_USE",
    "POOR": "AVOID",
    "AVOID": "AVOID",

}

GLYCEMIC_LOAD_LOW = "LOW"
INSULIN_LOAD_HIGH = "HIGH"


# ==========================================================
# CONSUMER ENGINE
# ==========================================================


class ConsumerEngine:
    """
    Consumer Intelligence Engine for System 4.

    Synthesizes all analyses into consumer-friendly insights:
    - Overall consumer score (0-100)
    - Consumer category (EXCELLENT, GOOD, MODERATE, POOR, AVOID)
    - Executive status (RECOMMENDED, GOOD_CHOICE, OCCASIONAL_USE, AVOID)
    - Positive signals, concerns, and risk flags
    - Population fit and risk recommendations
    - Score breakdown and executive summary
    """

    def _safe_int(
        self,
        value: Any,
        default: int = 0,
    ) -> int:
        """
        Safely convert value to integer.

        Args:
            value: Value to convert
            default: Default value if conversion fails

        Returns:
            Integer value or default
        """

        try:

            if value is None:

                return default

            return int(value)

        except Exception:

            return default

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

    def _normalize_score(
        self,
        score: float,
    ) -> int:
        """
        Normalize score to 0-100 range.

        Args:
            score: Raw score

        Returns:
            Normalized score between 0 and 100
        """

        return max(
            0,
            min(
                100,
                int(score),
            ),
        )

    def _calculate_metabolic_score(
        self,
        satiety_score: float,
        metabolic_load_score: float,
    ) -> int:
        """
        Calculate combined metabolic score.

        Formula:
        (satiety_score + (100 - metabolic_load_score)) / 2

        Args:
            satiety_score: Satiety score (0-100)
            metabolic_load_score: Metabolic load score (0-100)

        Returns:
            Metabolic score between 0 and 100
        """

        raw_score = (

            satiety_score

            +

            (
                DEFAULT_SCORE - metabolic_load_score
            )

        ) // 2

        return self._normalize_score(
            raw_score,
        )

    def _calculate_consumer_score(
        self,
        suitability_score: float,
        metabolic_score: float,
        compliance_score: float,
        trust_score: float,
        deception_score: float,
    ) -> int:
        """
        Calculate overall consumer score.

        Args:
            suitability_score: Suitability score (0-100)
            metabolic_score: Metabolic score (0-100)
            compliance_score: Compliance score (0-100)
            trust_score: Trust score (0-100)
            deception_score: Deception penalty (0-100)

        Returns:
            Consumer score between 0 and 100
        """

        raw_score = (

            suitability_score * WEIGHT_SUITABILITY

            +

            metabolic_score * WEIGHT_METABOLIC

            +

            compliance_score * WEIGHT_COMPLIANCE

            +

            trust_score * WEIGHT_TRUST

        )

        # Apply deception penalty
        raw_score -= deception_score * DECEPTION_PENALTY_FACTOR

        return self._normalize_score(
            raw_score,
        )

    def _calculate_confidence(
        self,
        compliance_score: float,
        trust_score: float,
        suitability_score: float,
    ) -> int:
        """
        Calculate confidence score for the analysis.

        Args:
            compliance_score: Compliance score (0-100)
            trust_score: Trust score (0-100)
            suitability_score: Suitability score (0-100)

        Returns:
            Confidence score between 0 and 100
        """

        raw_confidence = (

            compliance_score

            +

            trust_score

            +

            suitability_score

        ) // CONFIDENCE_AVERAGE_DIVISOR

        return self._normalize_score(
            raw_confidence,
        )

    def _get_consumer_category(
        self,
        consumer_score: int,
    ) -> str:
        """
        Get consumer category based on score.

        Args:
            consumer_score: Consumer score (0-100)

        Returns:
            Category string (EXCELLENT, GOOD, MODERATE, POOR, AVOID)
        """

        if consumer_score >= CONSUMER_SCORE_CATEGORIES["EXCELLENT"]:

            return "EXCELLENT"

        if consumer_score >= CONSUMER_SCORE_CATEGORIES["GOOD"]:

            return "GOOD"

        if consumer_score >= CONSUMER_SCORE_CATEGORIES["MODERATE"]:

            return "MODERATE"

        if consumer_score >= CONSUMER_SCORE_CATEGORIES["POOR"]:

            return "POOR"

        return "AVOID"

    def _get_executive_status(
        self,
        category: str,
    ) -> str:
        """
        Get executive status based on category.

        Args:
            category: Consumer category

        Returns:
            Executive status string
        """

        return EXECUTIVE_STATUS_MAP.get(
            category,
            "AVOID",
        )

    def _build_risk_flags(
        self,
        additive_count: int,
        ingredient_count: int,
        processing_level: str,
    ) -> List[str]:
        """
        Build risk flags based on product characteristics.

        Args:
            additive_count: Number of additives
            ingredient_count: Number of ingredients
            processing_level: Processing level

        Returns:
            List of risk flags
        """

        risk_flags = []

        if additive_count >= ADDITIVE_COUNT_HIGH_THRESHOLD:

            risk_flags.append(
                "HIGH_ADDITIVE_LOAD"
            )

        if ingredient_count >= INGREDIENT_COUNT_HIGH_THRESHOLD:

            risk_flags.append(
                "LONG_INGREDIENT_LIST"
            )

        if processing_level in PROCESSING_LEVEL_HIGH_RISK:

            risk_flags.append(
                "ULTRA_PROCESSED"
            )

        return sorted(
            list(
                set(
                    risk_flags
                )
            )
        )

    def _build_population_fit(
        self,
        glycemic_load_category: str,
        metabolic_flexibility_score: float,
    ) -> List[str]:
        """
        Build population fit recommendations.

        Args:
            glycemic_load_category: LOW, MODERATE, or HIGH
            metabolic_flexibility_score: Score (0-100)

        Returns:
            List of populations that fit this product
        """

        population_fit = []

        if glycemic_load_category == GLYCEMIC_LOAD_LOW:

            population_fit.append(
                "DIABETICS"
            )

        if metabolic_flexibility_score >= METABOLIC_FLEXIBILITY_EXCELLENT_THRESHOLD:

            population_fit.append(
                "ACTIVE_ADULTS"
            )

        return sorted(
            list(
                set(
                    population_fit
                )
            )
        )

    def _build_population_risk(
        self,
        insulin_load_category: str,
    ) -> List[str]:
        """
        Build population risk warnings.

        Args:
            insulin_load_category: LOW, MODERATE, or HIGH

        Returns:
            List of populations at risk from this product
        """

        population_risk = []

        if insulin_load_category == INSULIN_LOAD_HIGH:

            population_risk.append(
                "INSULIN_RESISTANT_USERS"
            )

        return sorted(
            list(
                set(
                    population_risk
                )
            )
        )

    def _build_positive_signals(
        self,
        metabolic_score: int,
        trust_score: int,
        compliance_score: int,
    ) -> List[str]:
        """
        Build positive signals based on scores.

        Args:
            metabolic_score: Metabolic score (0-100)
            trust_score: Trust score (0-100)
            compliance_score: Compliance score (0-100)

        Returns:
            List of positive signals
        """

        positive_signals = []

        if metabolic_score >= CONSUMER_SCORE_CATEGORIES["GOOD"]:

            positive_signals.append(
                "METABOLICALLY_FRIENDLY"
            )

        if trust_score >= TRUST_EXCELLENT_THRESHOLD:

            positive_signals.append(
                "TRUSTWORTHY"
            )

        if compliance_score >= COMPLIANCE_EXCELLENT_THRESHOLD:

            positive_signals.append(
                "HIGH_COMPLIANCE"
            )

        return sorted(
            list(
                set(
                    positive_signals
                )
            )
        )

    def _build_concerns(
        self,
        deception_score: float,
        consumer_harm_score: float,
        additive_count: int,
    ) -> List[str]:
        """
        Build concerns based on product characteristics.

        Args:
            deception_score: Deception score (0-100)
            consumer_harm_score: Consumer harm score (0-100)
            additive_count: Number of additives

        Returns:
            List of concerns
        """

        concerns = []

        if deception_score >= DECEPTION_HIGH_THRESHOLD:

            concerns.append(
                "HIGH_DECEPTION"
            )

        if consumer_harm_score >= CONSUMER_HARM_HIGH_THRESHOLD:

            concerns.append(
                "HIGH_CONSUMER_HARM"
            )

        if additive_count >= ADDITIVE_HIGH_THRESHOLD:

            concerns.append(
                "HIGH_ADDITIVES"
            )

        return sorted(
            list(
                set(
                    concerns
                )
            )
        )

    def _build_executive_summary(
        self,
        glycemic_load_category: str,
        additive_count: int,
        trust_score: float,
    ) -> List[str]:
        """
        Build executive summary flags.

        Args:
            glycemic_load_category: LOW, MODERATE, or HIGH
            additive_count: Number of additives
            trust_score: Trust score (0-100)

        Returns:
            List of executive summary flags
        """

        summary = []

        if glycemic_load_category == INSULIN_LOAD_HIGH:

            summary.append(
                "HIGH_GLYCEMIC_LOAD"
            )

        if additive_count >= ADDITIVE_HIGH_THRESHOLD:

            summary.append(
                "HIGH_ADDITIVE_LOAD"
            )

        if trust_score >= TRUST_EXCELLENT_THRESHOLD:

            summary.append(
                "TRUSTWORTHY_BRAND"
            )

        return sorted(
            list(
                set(
                    summary
                )
            )
        )

    def analyze(
        self,
        ingredient_intelligence: Dict[str, Any],
        metabolic_intelligence: Dict[str, Any],
        compliance: Dict[str, Any],
        deception: Dict[str, Any],
        suitability: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Master consumer intelligence analysis.

        Args:
            ingredient_intelligence: Ingredient analysis from System 2
            metabolic_intelligence: Metabolic analysis from System 3
            compliance: Compliance analysis from System 4
            deception: Deception analysis from System 8
            suitability: Suitability analysis from System 4

        Returns:
            Complete consumer intelligence analysis
        """

        # Extract ingredient data
        ingredient_profile = ingredient_intelligence.get(
            "ingredient_profile",
            {},
        )

        ingredient_summary = ingredient_intelligence.get(
            "ingredient_summary",
            {},
        )

        ingredient_count = self._safe_int(
            ingredient_profile.get(
                "ingredient_count",
                0,
            )
        )

        additive_count = self._safe_int(

            ingredient_summary.get(
                "additive_candidates",
                ingredient_intelligence.get(
                    "additive_count",
                    0,
                ),
            )

        )

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

        # Extract metabolic data
        metabolic_load = metabolic_intelligence.get(
            "metabolic_load",
            {},
        )

        satiety = metabolic_intelligence.get(
            "satiety",
            {},
        )

        metabolic_load_score = self._safe_float(
            metabolic_load.get(
                "score",
                DEFAULT_SCORE,
            )
        )

        satiety_score = self._safe_float(
            satiety.get(
                "score",
                DEFAULT_SCORE,
            )
        )

        metabolic_score = self._calculate_metabolic_score(
            satiety_score,
            metabolic_load_score,
        )

        # Extract compliance data
        compliance_score = self._safe_float(
            compliance.get(
                "fssai_score",
                DEFAULT_SCORE,
            )
        )

        # Extract deception data
        deception_score = self._safe_float(
            deception.get(
                "deception_score",
                DEFAULT_PENALTY,
            )
        )

        trust_score = self._safe_float(
            deception.get(
                "trust_score",
                DEFAULT_TRUST_SCORE,
            )
        )

        brand_honesty_score = self._safe_float(
            deception.get(
                "brand_honesty_score",
                DEFAULT_BRAND_HONESTY,
            )
        )

        consumer_harm_score = self._safe_float(
            deception.get(
                "consumer_harm_score",
                DEFAULT_HARM_SCORE,
            )
        )

        # Extract suitability data
        suitability_score = self._safe_float(
            suitability.get(
                "overall_score",
                DEFAULT_SCORE,
            )
        )

        overall_grade = suitability.get(
            "overall_grade",
            DEFAULT_OVERALL_GRADE,
        )

        buy_decision = suitability.get(
            "buy_decision",
            DEFAULT_BUY_DECISION,
        )

        # Extract metabolic metrics
        metabolic = metabolic_intelligence.get(
            "metabolic",
            {},
        )

        glycemic_load = metabolic.get(
            "glycemic_load",
            {},
        )

        insulin_load = metabolic.get(
            "insulin_load",
            {},
        )

        metabolic_flexibility = metabolic.get(
            "metabolic_flexibility",
            {},
        )

        glycemic_load_category = glycemic_load.get(
            "category",
            "UNKNOWN",
        )

        insulin_load_category = insulin_load.get(
            "category",
            "UNKNOWN",
        )

        metabolic_flexibility_score = self._safe_float(
            metabolic_flexibility.get(
                "score",
                DEFAULT_SCORE,
            )
        )

        # Calculate consumer score
        consumer_score = self._calculate_consumer_score(
            suitability_score,
            float(metabolic_score),
            compliance_score,
            trust_score,
            deception_score,
        )

        # Calculate confidence
        confidence = self._calculate_confidence(
            compliance_score,
            trust_score,
            suitability_score,
        )

        # Get consumer category and executive status
        consumer_category = self._get_consumer_category(
            consumer_score,
        )

        executive_status = self._get_executive_status(
            consumer_category,
        )

        # Build all derived lists
        risk_flags = self._build_risk_flags(
            additive_count,
            ingredient_count,
            processing_level,
        )

        population_fit = self._build_population_fit(
            glycemic_load_category,
            metabolic_flexibility_score,
        )

        population_risk = self._build_population_risk(
            insulin_load_category,
        )

        positive_signals = self._build_positive_signals(
            metabolic_score,
            int(trust_score),
            int(compliance_score),
        )

        concerns = self._build_concerns(
            deception_score,
            consumer_harm_score,
            additive_count,
        )

        executive_summary = self._build_executive_summary(
            glycemic_load_category,
            additive_count,
            trust_score,
        )

        # Build score breakdown
        score_breakdown = {

            "suitability":
            self._safe_int(
                suitability_score,
            ),

            "metabolic":
            metabolic_score,

            "compliance":
            self._safe_int(
                compliance_score,
            ),

            "trust":
            self._safe_int(
                trust_score,
            ),

            "deception_penalty":
            self._safe_int(
                deception_score,
            ),

        }

        return {

            "consumer_score":
            consumer_score,

            "consumer_category":
            consumer_category,

            "executive_status":
            executive_status,

            "confidence":
            confidence,

            "positive_signals":
            positive_signals,

            "concerns":
            concerns,

            "risk_flags":
            risk_flags,

            "population_fit":
            population_fit,

            "population_risk":
            population_risk,

            "executive_summary":
            executive_summary,

            "score_breakdown":
            score_breakdown,

            "summary": {

                "trust_score":
                self._safe_int(
                    trust_score,
                ),

                "brand_honesty":
                self._safe_int(
                    brand_honesty_score,
                ),

                "harm_score":
                self._safe_int(
                    consumer_harm_score,
                ),

                "buy_decision":
                buy_decision,

            },

            "signals": {

                "ingredient_count":
                ingredient_count,

                "additive_count":
                additive_count,

                "processing_level":
                processing_level,

                "metabolic_score":
                metabolic_score,

                "compliance_score":
                self._safe_int(
                    compliance_score,
                ),

                "suitability_score":
                self._safe_int(
                    suitability_score,
                ),

                "deception_score":
                self._safe_int(
                    deception_score,
                ),

                "glycemic_load_score":
                self._safe_int(
                    glycemic_load.get(
                        "score",
                        DEFAULT_SCORE,
                    ),
                ),

                "insulin_load_score":
                self._safe_int(
                    insulin_load.get(
                        "score",
                        DEFAULT_SCORE,
                    ),
                ),

                "metabolic_flexibility_score":
                self._safe_int(
                    metabolic_flexibility_score,
                ),

                "overall_grade":
                overall_grade,

            },

        }


# ==========================================================
# SINGLETON INSTANCE
# ==========================================================


consumer_engine = ConsumerEngine()


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [

    "ConsumerEngine",
    "consumer_engine",

]


# ==========================================================
# END OF FILE – consumer_engine.py
# ==========================================================