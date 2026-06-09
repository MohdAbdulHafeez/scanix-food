# ==========================================================
# SCANIX AI
# SYSTEM 4 – CONSUMER INTELLIGENCE (VERDICT ENGINE)
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
DEFAULT_TRUST_SCORE = 100
DEFAULT_DECEPTION_SCORE = 0
DEFAULT_BUY_DECISION = "UNKNOWN"
DEFAULT_FREQUENCY = "UNKNOWN"

NUTRITION_CONFIDENCE_LOW_THRESHOLD = 25

WEIGHT_SUITABILITY = 0.30
WEIGHT_METABOLIC = 0.20
WEIGHT_COMPLIANCE = 0.15
WEIGHT_TRUST = 0.10
WEIGHT_SAFETY_INDEX = 0.25

ULTRA_PROCESSED_PENALTY = 10
PALM_OIL_PENALTY = 5
RED_ALERTS_PENALTY_THRESHOLD = 3
RED_ALERTS_PENALTY = 10

DECEPTION_PENALTY_FACTOR = 0.15

STAR_RATING_DIVISOR = 20

CONFIDENCE_AVERAGE_DIVISOR = 2

GRADE_THRESHOLDS = {

    "A+": 90,
    "A": 80,
    "B": 70,
    "C": 55,
    "D": 40,
    "F": 0,

}

BADGE_MAP = {

    "EXCELLENT": "SCANIX_APPROVED",
    "HIGH": "HEALTHY_CHOICE",
    "MODERATE": "MODERATE",
    "LOW": "USE_CAUTION",

}

RECOMMENDATION_MAP = {

    "EXCELLENT": "STRONGLY_RECOMMENDED",
    "HIGH": "RECOMMENDED",
    "MODERATE": "LIMITED_CONSUMPTION",
    "LOW": "NOT_RECOMMENDED",

}

CHILD_SAFETY_THRESHOLDS = {

    "UNSAFE": 40,
    "CAUTION": 70,
    "SAFE": 100,

}

DIABETIC_RISK_HIGH = ["HIGH", "VERY_HIGH"]
DIABETIC_RISK_MODERATE = ["MODERATE"]

HEART_RISK_HIGH = ["HIGH", "VERY_HIGH"]
HEART_RISK_MODERATE = ["MODERATE"]

CONSUMER_SCORE_CATEGORIES = {

    "EXCELLENT": 90,
    "HIGH": 80,
    "MODERATE": 60,
    "LOW": 0,

}

STRENGTHS_COMPLIANCE_THRESHOLD = 85
STRENGTHS_TRUST_THRESHOLD = 80
STRENGTHS_SUITABILITY_THRESHOLD = 80
STRENGTHS_METABOLIC_THRESHOLD = 80

CONCERNS_DECEPTION_THRESHOLD = 50
CONCERNS_COMPLIANCE_THRESHOLD = 70
CONCERNS_SUITABILITY_THRESHOLD = 60
CONCERNS_METABOLIC_THRESHOLD = 60

EXECUTIVE_VERDICT_THRESHOLDS = {

    "EXCELLENT": 85,
    "HIGH": 70,
    "MODERATE": 60,
    "LOW": 40,
    "VERY_LOW": 0,

}

RISK_LEVEL_SCORES = {

    "LOW": 80,
    "MODERATE": 60,
    "HIGH": 0,

}

HEALTH_IMPACT_METABOLIC_KEY = "metabolic_health"
HEALTH_IMPACT_PERSONAS_KEY = "personas"

ALERT_CATEGORY_CHILDREN = "CHILDREN"
ALERT_CATEGORY_PREGNANCY = "PREGNANCY"
ALERT_CATEGORY_DIABETIC = "DIABETIC"
ALERT_CATEGORY_HEART = "HEART"


# ==========================================================
# VERDICT ENGINE
# ==========================================================


class VerdictEngine:
    """
    Verdict Engine for System 4 – Consumer Intelligence.

    Synthesizes all analyses into final consumer verdict:
    - Consumer score and grade (A+ to F)
    - Star rating (1-5)
    - Badge and recommendation level
    - Population-specific safety assessments
    - Top strengths and concerns
    - Executive verdict summary
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
                self._safe_int(score),
            ),
        )

    def _get_consumer_grade(
        self,
        consumer_score: int,
    ) -> str:
        """
        Get letter grade based on consumer score.

        Args:
            consumer_score: Consumer score (0-100)

        Returns:
            Letter grade (A+, A, B, C, D, or F)
        """

        if consumer_score >= GRADE_THRESHOLDS["A+"]:
            return "A+"
        if consumer_score >= GRADE_THRESHOLDS["A"]:
            return "A"
        if consumer_score >= GRADE_THRESHOLDS["B"]:
            return "B"
        if consumer_score >= GRADE_THRESHOLDS["C"]:
            return "C"
        if consumer_score >= GRADE_THRESHOLDS["D"]:
            return "D"
        return "F"

    def _get_badge(
        self,
        consumer_score: int,
    ) -> str:
        """
        Get badge based on consumer score.

        Args:
            consumer_score: Consumer score (0-100)

        Returns:
            Badge string
        """

        if consumer_score >= GRADE_THRESHOLDS["A+"]:
            return BADGE_MAP["EXCELLENT"]
        if consumer_score >= GRADE_THRESHOLDS["A"]:
            return BADGE_MAP["HIGH"]
        if consumer_score >= CONSUMER_SCORE_CATEGORIES["MODERATE"]:
            return BADGE_MAP["MODERATE"]
        return BADGE_MAP["LOW"]

    def _get_recommendation_level(
        self,
        consumer_score: int,
    ) -> str:
        """
        Get recommendation level based on consumer score.

        Args:
            consumer_score: Consumer score (0-100)

        Returns:
            Recommendation level string
        """

        if consumer_score >= GRADE_THRESHOLDS["A+"]:
            return RECOMMENDATION_MAP["EXCELLENT"]
        if consumer_score >= GRADE_THRESHOLDS["A"]:
            return RECOMMENDATION_MAP["HIGH"]
        if consumer_score >= CONSUMER_SCORE_CATEGORIES["MODERATE"]:
            return RECOMMENDATION_MAP["MODERATE"]
        return RECOMMENDATION_MAP["LOW"]

    def _get_star_rating(
        self,
        consumer_score: int,
    ) -> int:
        """
        Get star rating (1-5) based on consumer score.

        Args:
            consumer_score: Consumer score (0-100)

        Returns:
            Star rating between 1 and 5
        """

        return max(
            1,
            min(
                5,
                round(
                    consumer_score / STAR_RATING_DIVISOR
                ),
            ),
        )

    def _get_risk_level(
        self,
        consumer_score: int,
    ) -> str:
        """
        Get risk level based on consumer score.

        Args:
            consumer_score: Consumer score (0-100)

        Returns:
            Risk level (LOW, MODERATE, or HIGH)
        """

        if consumer_score >= RISK_LEVEL_SCORES["LOW"]:
            return "LOW"
        if consumer_score >= RISK_LEVEL_SCORES["MODERATE"]:
            return "MODERATE"
        return "HIGH"

    def _get_child_safety(
        self,
        child_score: int,
    ) -> str:
        """
        Get child safety assessment.

        Args:
            child_score: Child persona score (0-100)

        Returns:
            Safety string (UNSAFE, CAUTION, or SAFE)
        """

        if child_score < CHILD_SAFETY_THRESHOLDS["UNSAFE"]:
            return "UNSAFE"
        if child_score < CHILD_SAFETY_THRESHOLDS["CAUTION"]:
            return "CAUTION"
        return "SAFE"

    def _get_pregnancy_safety(
        self,
        pregnancy_safety_flag: bool,
        red_alerts: int,
    ) -> str:
        """
        Get pregnancy safety assessment.

        Args:
            pregnancy_safety_flag: Whether pregnancy alert exists
            red_alerts: Number of red alerts

        Returns:
            Safety string (UNSAFE, CAUTION, or SAFE)
        """

        if pregnancy_safety_flag:
            return "UNSAFE"
        if red_alerts >= RED_ALERTS_PENALTY_THRESHOLD:
            return "CAUTION"
        return "SAFE"

    def _get_diabetic_safety(
        self,
        diabetic_risk: str,
    ) -> str:
        """
        Get diabetic safety assessment.

        Args:
            diabetic_risk: Risk level (HIGH, MODERATE, LOW)

        Returns:
            Safety string (UNSAFE, CAUTION, or SAFE)
        """

        if diabetic_risk in DIABETIC_RISK_HIGH:
            return "UNSAFE"
        if diabetic_risk in DIABETIC_RISK_MODERATE:
            return "CAUTION"
        return "SAFE"

    def _get_heart_health_safety(
        self,
        heart_risk: str,
    ) -> str:
        """
        Get heart health safety assessment.

        Args:
            heart_risk: Risk level (HIGH, MODERATE, LOW)

        Returns:
            Safety string (UNSAFE, CAUTION, or SAFE)
        """

        if heart_risk in HEART_RISK_HIGH:
            return "UNSAFE"
        if heart_risk in HEART_RISK_MODERATE:
            return "CAUTION"
        return "SAFE"

    def _get_executive_verdict(
        self,
        consumer_score: int,
    ) -> str:
        """
        Get executive verdict summary.

        Args:
            consumer_score: Consumer score (0-100)

        Returns:
            Executive verdict string
        """

        if consumer_score >= EXECUTIVE_VERDICT_THRESHOLDS["EXCELLENT"]:
            return (
                "Highly recommended product suitable for regular consumption."
            )
        if consumer_score >= EXECUTIVE_VERDICT_THRESHOLDS["HIGH"]:
            return (
                "Generally recommended with minor considerations."
            )
        if consumer_score >= EXECUTIVE_VERDICT_THRESHOLDS["MODERATE"]:
            return (
                "Acceptable for occasional consumption."
            )
        if consumer_score >= EXECUTIVE_VERDICT_THRESHOLDS["LOW"]:
            return (
                "Consume cautiously and infrequently."
            )
        return (
            "Avoid where healthier alternatives exist."
        )

    def analyze(
        self,
        consumer: Dict[str, Any],
        compliance: Dict[str, Any],
        deception: Dict[str, Any],
        suitability: Dict[str, Any],
        metabolic_intelligence: Dict[str, Any],
        health_alerts: Dict[str, Any] = None,
        nutrition: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Master analysis method for consumer verdict.

        Args:
            consumer: Consumer intelligence data
            compliance: Compliance analysis data
            deception: Deception analysis data
            suitability: Suitability analysis data
            metabolic_intelligence: Metabolic analysis data
            health_alerts: Health alerts from compliance engine
            nutrition: Nutrition data for confidence check

        Returns:
            Complete verdict analysis
        """

        if health_alerts is None:
            health_alerts = {}

        if nutrition is None:
            nutrition = {}

        nutrition_confidence = nutrition.get(
            "nutrition_confidence",
            0,
        )

        # Early return for insufficient data
        if (
            nutrition_confidence < NUTRITION_CONFIDENCE_LOW_THRESHOLD
            and not nutrition.get(
                "nutrition_detected",
                False,
            )
        ):

            return self._get_insufficient_data_response()

        # Extract scores
        compliance_score = self._safe_float(
            compliance.get(
                "fssai_score",
                DEFAULT_SCORE,
            )
        )

        deception_score = self._safe_float(
            deception.get(
                "deception_score",
                DEFAULT_DECEPTION_SCORE,
            )
        )

        trust_score = self._safe_float(
            deception.get(
                "trust_score",
                DEFAULT_TRUST_SCORE,
            )
        )

        suitability_score = self._safe_float(
            suitability.get(
                "overall_score",
                DEFAULT_SCORE,
            )
        )

        health_impact = metabolic_intelligence.get(
            "health_impact",
            {},
        )

        metabolic_health = health_impact.get(
            HEALTH_IMPACT_METABOLIC_KEY,
            {},
        )

        metabolic_load_score = self._safe_float(
            metabolic_health
            .get(
                "metabolic_load",
                {},
            )
            .get(
                "score",
                DEFAULT_SCORE,
            )
        )

        satiety_score = self._safe_float(
            metabolic_health
            .get(
                "satiety",
                {},
            )
            .get(
                "score",
                DEFAULT_SCORE,
            )
        )

        metabolic_score = (
            satiety_score
            +
            (
                DEFAULT_SCORE
                -
                metabolic_load_score
            )
        ) // 2

        consumer_safety_index = self._safe_float(
            compliance.get(
                "consumer_safety_index",
                DEFAULT_SCORE,
            )
        )

        # Extract alerts
        all_alerts = health_alerts.get(
            "all_alerts",
            health_alerts.get(
                "alerts",
                [],
            ),
        )

        traffic_lights = compliance.get(
            "traffic_lights",
            {},
        )

        red_alerts = 0
        yellow_alerts = 0

        child_safety_flag = False
        pregnancy_safety_flag = False
        diabetic_safety_flag = False
        heart_health_safety_flag = False

        for alert in all_alerts:

            alert_type = alert.get(
                "severity",
                alert.get(
                    "type",
                    "",
                ),
            )

            if alert_type == "RED":
                red_alerts += 1
            elif alert_type == "YELLOW":
                yellow_alerts += 1

            cat = alert.get(
                "category",
                "",
            ).upper()

            if ALERT_CATEGORY_CHILDREN in cat:
                child_safety_flag = True
            if ALERT_CATEGORY_PREGNANCY in cat:
                pregnancy_safety_flag = True
            if ALERT_CATEGORY_DIABETIC in cat:
                diabetic_safety_flag = True
            if ALERT_CATEGORY_HEART in cat:
                heart_health_safety_flag = True

        # Calculate consumer score
        consumer_score = round(

            suitability_score * WEIGHT_SUITABILITY
            + metabolic_score * WEIGHT_METABOLIC
            + compliance_score * WEIGHT_COMPLIANCE
            + trust_score * WEIGHT_TRUST
            + consumer_safety_index * WEIGHT_SAFETY_INDEX

        )

        # Apply penalties
        ingredient_profile = consumer.get(
            "ingredient_profile",
            {},
        )

        if ingredient_profile.get(
            "processing_level"
        ) == "ULTRA_PROCESSED":
            consumer_score -= ULTRA_PROCESSED_PENALTY

        if ingredient_profile.get(
            "contains_palm_oil",
            False,
        ):
            consumer_score -= PALM_OIL_PENALTY

        if red_alerts >= RED_ALERTS_PENALTY_THRESHOLD:
            consumer_score -= RED_ALERTS_PENALTY

        consumer_score -= int(
            deception_score * DECEPTION_PENALTY_FACTOR
        )

        consumer_score = self._normalize_score(
            consumer_score,
        )

        # Calculate derived metrics
        star_rating = self._get_star_rating(
            consumer_score,
        )

        confidence = round(

            (
                compliance.get(
                    "regulatory_confidence",
                    DEFAULT_SCORE,
                )
                + trust_score
            ) / CONFIDENCE_AVERAGE_DIVISOR

        )

        consumer_grade = self._get_consumer_grade(
            consumer_score,
        )

        badge = self._get_badge(
            consumer_score,
        )

        recommendation_level = self._get_recommendation_level(
            consumer_score,
        )

        risk_level = self._get_risk_level(
            consumer_score,
        )

        # Population safety assessments
        personas = health_impact.get(
            HEALTH_IMPACT_PERSONAS_KEY,
            {},
        )

        child_score = self._safe_float(
            personas.get(
                "child",
                {},
            ).get(
                "score",
                DEFAULT_SCORE,
            )
        )

        diabetic_risk = personas.get(
            "diabetic",
            {},
        ).get(
            "risk",
            "UNKNOWN",
        )

        heart_risk = personas.get(
            "heart",
            {},
        ).get(
            "risk",
            "UNKNOWN",
        )

        child_safety = self._get_child_safety(
            child_score,
        )

        pregnancy_safety = self._get_pregnancy_safety(
            pregnancy_safety_flag,
            red_alerts,
        )

        diabetic_safety = self._get_diabetic_safety(
            diabetic_risk,
        )

        heart_health_safety = self._get_heart_health_safety(
            heart_risk,
        )

        population_verdicts = {

            "children": child_safety,
            "pregnancy": pregnancy_safety,
            "diabetic": diabetic_safety,
            "heart": heart_health_safety,

        }

        # Build top strengths
        strengths = []

        if compliance_score >= STRENGTHS_COMPLIANCE_THRESHOLD:
            strengths.append(
                "Strong regulatory compliance"
            )

        if trust_score >= STRENGTHS_TRUST_THRESHOLD:
            strengths.append(
                "Trustworthy product positioning"
            )

        if suitability_score >= STRENGTHS_SUITABILITY_THRESHOLD:
            strengths.append(
                "High consumer suitability"
            )

        if metabolic_score >= STRENGTHS_METABOLIC_THRESHOLD:
            strengths.append(
                "Strong metabolic profile"
            )

        # Build top concerns
        concerns = []

        if deception_score >= CONCERNS_DECEPTION_THRESHOLD:
            concerns.append(
                "Marketing deception indicators detected"
            )

        if compliance_score < CONCERNS_COMPLIANCE_THRESHOLD:
            concerns.append(
                "Compliance concerns present"
            )

        if suitability_score < CONCERNS_SUITABILITY_THRESHOLD:
            concerns.append(
                "Limited suitability across populations"
            )

        if metabolic_score < CONCERNS_METABOLIC_THRESHOLD:
            concerns.append(
                "Suboptimal metabolic profile"
            )

        # Executive verdict
        executive_verdict = self._get_executive_verdict(
            consumer_score,
        )

        # Traffic light verdict
        traffic_light_verdict = {

            "overall": traffic_lights.get(
                "overall",
                "UNKNOWN",
            ),
            "sugar": traffic_lights.get(
                "sugar",
                "UNKNOWN",
            ),
            "sodium": traffic_lights.get(
                "sodium",
                "UNKNOWN",
            ),
            "fat": traffic_lights.get(
                "fat",
                "UNKNOWN",
            ),

        }

        # Build summary
        summary = {

            "consumer_score": consumer_score,
            "consumer_grade": consumer_grade,
            "risk_level": risk_level,
            "buy_decision": suitability.get(
                "buy_decision",
                DEFAULT_BUY_DECISION,
            ),
            "frequency": suitability.get(
                "consumption_frequency",
                DEFAULT_FREQUENCY,
            ),
            "red_alerts_count": red_alerts,
            "yellow_alerts_count": yellow_alerts,

        }

        return {

            "consumer_score": consumer_score,
            "consumer_grade": consumer_grade,
            "star_rating": star_rating,
            "badge": badge,
            "recommendation_level": recommendation_level,
            "confidence": confidence,
            "child_safety": child_safety,
            "pregnancy_safety": pregnancy_safety,
            "diabetic_safety": diabetic_safety,
            "heart_health_safety": heart_health_safety,
            "traffic_light_verdict": traffic_light_verdict,
            "population_verdicts": population_verdicts,
            "top_strengths": strengths,
            "top_concerns": concerns,
            "executive_verdict": executive_verdict,
            "summary": summary,

        }

    def _get_insufficient_data_response(self) -> Dict[str, Any]:
        """
        Get response for insufficient data scenario.

        Returns:
            Standardized insufficient data response
        """

        return {

            "consumer_score": 50,
            "consumer_grade": "F",
            "star_rating": 1,
            "badge": "INSUFFICIENT_DATA",
            "recommendation_level": "NOT_RECOMMENDED",
            "confidence": "LOW",
            "child_safety": "UNKNOWN",
            "pregnancy_safety": "UNKNOWN",
            "diabetic_safety": "UNKNOWN",
            "heart_health_safety": "UNKNOWN",
            "traffic_light_verdict": {
                "overall": "UNKNOWN",
                "sugar": "UNKNOWN",
                "sodium": "UNKNOWN",
                "fat": "UNKNOWN",
            },
            "population_verdicts": {
                "children": "Unable to assess — scan quality too low",
                "pregnancy": "Unable to assess — scan quality too low",
                "diabetic": "Unable to assess — scan quality too low",
                "heart": "Unable to assess — scan quality too low",
            },
            "top_strengths": [],
            "top_concerns": [
                "Insufficient nutrition confidence — OCR may have failed or label was unreadable",
            ],
            "executive_verdict": (
                "Scan quality was too low to provide a reliable recommendation. "
                "Please try scanning again with better lighting and focus."
            ),
            "summary": {
                "consumer_score": 50,
                "consumer_grade": "F",
                "risk_level": "HIGH",
                "buy_decision": DEFAULT_BUY_DECISION,
                "frequency": DEFAULT_FREQUENCY,
                "red_alerts_count": 0,
                "yellow_alerts_count": 0,
            },

        }


# ==========================================================
# SINGLETON INSTANCE
# ==========================================================


verdict_engine = VerdictEngine()


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [

    "VerdictEngine",
    "verdict_engine",

]


# ==========================================================
# END OF FILE – verdict_engine.py
# ==========================================================