# ==========================================================
# SCANIX AI
# SYSTEM 8 – TRUST INTELLIGENCE (HEALTH ALERT ENGINE)
# ELITE PRODUCTION GRADE – FINAL VERSION
# ==========================================================


from __future__ import annotations


from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple


# ==========================================================
# CONSTANTS
# ==========================================================


SEVERITY_SCORE_MAP = {

    "GREEN": 0,
    "YELLOW": 10,
    "RED": 25,

}

POPULATION_CATEGORY_MAP = {

    "children": "CHILDREN",
    "pregnancy": "PREGNANCY",
    "diabetic": "DIABETIC",
    "heart_patient": "HEART_HEALTH",

}

DECEPTION_HIGH_THRESHOLD = 70
DECEPTION_MODERATE_THRESHOLD = 40

METABOLIC_POOR_THRESHOLD = 40
METABOLIC_AVERAGE_THRESHOLD = 60

SUITABILITY_POOR_THRESHOLD = 50

CONSUMER_POOR_THRESHOLD = 40
CONSUMER_AVERAGE_THRESHOLD = 60

RED_ALERT_HIGH_COUNT_THRESHOLD = 3
RED_ALERT_MODERATE_COUNT_THRESHOLD = 1
YELLOW_ALERT_HIGH_COUNT_THRESHOLD = 3

SOUND_CRITICAL = "critical_alert"
SOUND_WARNING = "warning_alert"
SOUND_CAUTION = "caution_alert"

VOLUME_CRITICAL = 1.0
VOLUME_WARNING = 0.8
VOLUME_CAUTION = 0.6

PRIORITY_HIGH = "HIGH"
PRIORITY_MEDIUM = "MEDIUM"
PRIORITY_LOW = "LOW"
PRIORITY_NONE = "NONE"

ALERT_TYPE_RED = "RED"
ALERT_TYPE_YELLOW = "YELLOW"
ALERT_TYPE_GREEN = "GREEN"

TRAFFIC_LIGHT_NUTRIENTS = ["sugar", "sodium", "fat"]


# ==========================================================
# HEALTH ALERT ENGINE
# ==========================================================


class HealthAlertEngine:
    """
    Health Alert Engine for System 8 – Trust Intelligence.

    Aggregates alerts from:
    - Compliance engine (health alerts, traffic lights)
    - Deception engine
    - Population-specific alerts (children, pregnancy, diabetic, heart)
    - Metabolic intelligence
    - Suitability engine
    - Consumer intelligence

    Provides:
    - Overall alert level (RED, YELLOW, GREEN)
    - Frontend-ready cards
    - Sound trigger configuration
    - Alert statistics and summary
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

    def build_alert(
        self,
        severity: str,
        title: str,
        message: str,
        category: str,
    ) -> Dict[str, Any]:
        """
        Build a standardized alert object.

        Args:
            severity: RED, YELLOW, or GREEN
            title: Alert title
            message: Alert message
            category: Alert category (e.g., TRAFFIC_LIGHT, DECEPTION)

        Returns:
            Standardized alert dictionary
        """

        return {

            "severity": severity,
            "title": title,
            "message": message,
            "category": category,
            "score": SEVERITY_SCORE_MAP.get(
                severity,
                0,
            ),

        }

    def merge_alerts(
        self,
        *alert_lists: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Merge multiple alert lists, removing duplicates.

        Args:
            *alert_lists: Variable number of alert lists

        Returns:
            Merged deduplicated alert list
        """

        merged: List[Dict[str, Any]] = []

        seen: Set[Tuple[str, str]] = set()

        for alert_list in alert_lists:

            for alert in alert_list:

                key = (

                    alert.get("title", ""),
                    alert.get("message", ""),

                )

                if key not in seen:

                    seen.add(key)

                    merged.append(alert)

        return merged

    def extract_compliance_alerts(
        self,
        compliance: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Extract alerts from compliance engine.

        Args:
            compliance: Compliance analysis data

        Returns:
            List of compliance alerts
        """

        alerts = []

        health_alerts = compliance.get(
            "health_alerts",
            {},
        )

        categories = [

            "children",
            "pregnancy",
            "diabetic",
            "heart_patient",
            "allergen_alerts",
            "additive_alerts",

        ]

        for category in categories:

            alerts.extend(
                health_alerts.get(
                    category,
                    [],
                )
            )

        return alerts

    def extract_traffic_light_alerts(
        self,
        compliance: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Extract traffic light alerts from compliance engine.

        Args:
            compliance: Compliance analysis data

        Returns:
            List of traffic light alerts
        """

        alerts = []

        lights = compliance.get(
            "traffic_lights",
            {},
        )

        for nutrient in TRAFFIC_LIGHT_NUTRIENTS:

            status = lights.get(
                nutrient,
                ALERT_TYPE_GREEN,
            )

            if status == ALERT_TYPE_RED:

                alerts.append(
                    self.build_alert(
                        ALERT_TYPE_RED,
                        f"High {nutrient.title()}",
                        f"{nutrient.title()} exceeds recommended thresholds.",
                        "TRAFFIC_LIGHT",
                    )
                )

            elif status == ALERT_TYPE_YELLOW:

                alerts.append(
                    self.build_alert(
                        ALERT_TYPE_YELLOW,
                        f"Moderate {nutrient.title()}",
                        f"{nutrient.title()} should be consumed carefully.",
                        "TRAFFIC_LIGHT",
                    )
                )

        return alerts

    def extract_deception_alerts(
        self,
        deception: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Extract alerts from deception engine.

        Args:
            deception: Deception analysis data

        Returns:
            List of deception alerts
        """

        alerts = []

        score = self._safe_float(
            deception.get(
                "deception_score",
                0,
            )
        )

        if score >= DECEPTION_HIGH_THRESHOLD:

            alerts.append(
                self.build_alert(
                    ALERT_TYPE_RED,
                    "High Marketing Deception",
                    "Claims may significantly misrepresent the product.",
                    "DECEPTION",
                )
            )

        elif score >= DECEPTION_MODERATE_THRESHOLD:

            alerts.append(
                self.build_alert(
                    ALERT_TYPE_YELLOW,
                    "Moderate Marketing Deception",
                    "Some claims may require verification.",
                    "DECEPTION",
                )
            )

        return alerts

    def extract_population_alerts(
        self,
        compliance: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Extract population-specific alerts from compliance engine.

        Args:
            compliance: Compliance analysis data

        Returns:
            List of population alerts
        """

        alerts = []

        health_alerts = compliance.get(
            "health_alerts",
            {},
        )

        for key, category in POPULATION_CATEGORY_MAP.items():

            for alert in health_alerts.get(
                key,
                [],
            ):

                alerts.append(
                    self.build_alert(
                        alert.get(
                            "type",
                            ALERT_TYPE_YELLOW,
                        ),
                        alert.get(
                            "title",
                            "Health Alert",
                        ),
                        alert.get(
                            "message",
                            "",
                        ),
                        category,
                    )
                )

        return alerts

    def extract_metabolic_alerts(
        self,
        metabolic_intelligence: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Extract alerts from metabolic intelligence.

        Args:
            metabolic_intelligence: Metabolic analysis data

        Returns:
            List of metabolic alerts
        """

        alerts = []

        overall = metabolic_intelligence.get(
            "overall",
            {},
        )

        score = self._safe_float(
            overall.get(
                "score",
                50,
            )
        )

        if score < METABOLIC_POOR_THRESHOLD:

            alerts.append(
                self.build_alert(
                    ALERT_TYPE_RED,
                    "Poor Metabolic Profile",
                    "Product may negatively impact metabolic health.",
                    "METABOLIC",
                )
            )

        elif score < METABOLIC_AVERAGE_THRESHOLD:

            alerts.append(
                self.build_alert(
                    ALERT_TYPE_YELLOW,
                    "Average Metabolic Profile",
                    "Consume in moderation for metabolic wellness.",
                    "METABOLIC",
                )
            )

        return alerts

    def extract_suitability_alerts(
        self,
        suitability: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Extract alerts from suitability engine.

        Args:
            suitability: Suitability analysis data

        Returns:
            List of suitability alerts
        """

        alerts = []

        score = self._safe_float(
            suitability.get(
                "overall_score",
                50,
            )
        )

        buy_decision = suitability.get(
            "buy_decision",
            "",
        )

        if score < SUITABILITY_POOR_THRESHOLD:

            alerts.append(
                self.build_alert(
                    ALERT_TYPE_RED,
                    "Low Suitability",
                    "Product has poor suitability across multiple populations.",
                    "SUITABILITY",
                )
            )

        if buy_decision == "AVOID":

            alerts.append(
                self.build_alert(
                    ALERT_TYPE_RED,
                    "Avoid Product",
                    "Suitability engine recommends avoiding this product.",
                    "SUITABILITY",
                )
            )

        return alerts

    def extract_consumer_alerts(
        self,
        consumer: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Extract alerts from consumer intelligence.

        Args:
            consumer: Consumer analysis data

        Returns:
            List of consumer alerts
        """

        alerts = []

        score = self._safe_int(
            consumer.get(
                "consumer_score",
                50,
            )
        )

        if score < CONSUMER_POOR_THRESHOLD:

            alerts.append(
                self.build_alert(
                    ALERT_TYPE_RED,
                    "Poor Consumer Score",
                    "Overall consumer intelligence score is very low.",
                    "CONSUMER",
                )
            )

        elif score < CONSUMER_AVERAGE_THRESHOLD:

            alerts.append(
                self.build_alert(
                    ALERT_TYPE_YELLOW,
                    "Moderate Consumer Score",
                    "Product should be consumed cautiously.",
                    "CONSUMER",
                )
            )

        return alerts

    def calculate_overall_alert(
        self,
        alerts: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Calculate overall alert level and metrics.

        Args:
            alerts: List of all alerts

        Returns:
            Overall alert metrics
        """

        red_count = 0
        yellow_count = 0
        score = 0

        for alert in alerts:

            severity = alert.get(
                "severity",
                ALERT_TYPE_GREEN,
            )

            score += alert.get(
                "score",
                0,
            )

            if severity == ALERT_TYPE_RED:

                red_count += 1

            elif severity == ALERT_TYPE_YELLOW:

                yellow_count += 1

        if red_count >= RED_ALERT_HIGH_COUNT_THRESHOLD:

            overall = ALERT_TYPE_RED

        elif red_count >= RED_ALERT_MODERATE_COUNT_THRESHOLD:

            overall = ALERT_TYPE_YELLOW

        elif yellow_count >= YELLOW_ALERT_HIGH_COUNT_THRESHOLD:

            overall = ALERT_TYPE_YELLOW

        else:

            overall = ALERT_TYPE_GREEN

        return {

            "overall_alert": overall,
            "health_alert_score": score,
            "red_alerts": red_count,
            "yellow_alerts": yellow_count,

        }

    def build_frontend_cards(
        self,
        alerts: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Build frontend-ready alert cards.

        Args:
            alerts: List of alerts

        Returns:
            List of frontend card objects
        """

        cards = []

        for alert in alerts:

            severity = alert.get(
                "severity",
                alert.get(
                    "type",
                    ALERT_TYPE_GREEN,
                ),
            )

            cards.append({

                "severity": severity,
                "title": alert.get("title", ""),
                "message": alert.get("message", ""),
                "category": alert.get("category", ""),
                "show_blinking": severity == ALERT_TYPE_RED,

            })

        return cards

    def build_sound_triggers(
        self,
        red_count: int,
        yellow_count: int,
    ) -> Dict[str, Any]:
        """
        Build sound trigger configuration based on alert counts.

        Args:
            red_count: Number of red alerts
            yellow_count: Number of yellow alerts

        Returns:
            Sound trigger configuration
        """

        if red_count >= RED_ALERT_HIGH_COUNT_THRESHOLD:

            return {

                "play_sound": True,
                "sound": SOUND_CRITICAL,
                "volume": VOLUME_CRITICAL,
                "priority": PRIORITY_HIGH,

            }

        if red_count >= RED_ALERT_MODERATE_COUNT_THRESHOLD:

            return {

                "play_sound": True,
                "sound": SOUND_WARNING,
                "volume": VOLUME_WARNING,
                "priority": PRIORITY_MEDIUM,

            }

        if yellow_count >= YELLOW_ALERT_HIGH_COUNT_THRESHOLD:

            return {

                "play_sound": True,
                "sound": SOUND_CAUTION,
                "volume": VOLUME_CAUTION,
                "priority": PRIORITY_LOW,

            }

        return {

            "play_sound": False,
            "sound": None,
            "volume": 0,
            "priority": PRIORITY_NONE,

        }

    def analyze(
        self,
        consumer: Dict[str, Any],
        compliance: Dict[str, Any],
        deception: Dict[str, Any],
        suitability: Dict[str, Any],
        metabolic_intelligence: Dict[str, Any],
        ingredient_intelligence: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Master analysis method for health alerts.

        Args:
            consumer: Consumer analysis data
            compliance: Compliance analysis data
            deception: Deception analysis data
            suitability: Suitability analysis data
            metabolic_intelligence: Metabolic analysis data
            ingredient_intelligence: Ingredient analysis data (reserved)

        Returns:
            Complete health alert analysis
        """

        # Extract alerts from all sources
        compliance_alerts = self.extract_compliance_alerts(
            compliance
        )

        traffic_alerts = self.extract_traffic_light_alerts(
            compliance
        )

        deception_alerts = self.extract_deception_alerts(
            deception
        )

        population_alerts = self.extract_population_alerts(
            compliance
        )

        metabolic_alerts = self.extract_metabolic_alerts(
            metabolic_intelligence
        )

        suitability_alerts = self.extract_suitability_alerts(
            suitability
        )

        consumer_alerts = self.extract_consumer_alerts(
            consumer
        )

        # Merge all alerts
        all_alerts = self.merge_alerts(

            compliance_alerts,
            traffic_alerts,
            deception_alerts,
            population_alerts,
            metabolic_alerts,
            suitability_alerts,
            consumer_alerts,

        )

        # Calculate overall alert metrics
        alert_metrics = self.calculate_overall_alert(
            all_alerts
        )

        # Build frontend cards
        frontend_cards = self.build_frontend_cards(
            all_alerts
        )

        # Build sound triggers
        sound_trigger = self.build_sound_triggers(

            alert_metrics["red_alerts"],
            alert_metrics["yellow_alerts"],

        )

        # Categorize alerts by severity
        critical_alerts = [

            a for a in all_alerts
            if a.get("severity") == ALERT_TYPE_RED

        ]

        warning_alerts = [

            a for a in all_alerts
            if a.get("severity") == ALERT_TYPE_YELLOW

        ]

        info_alerts = [

            a for a in all_alerts
            if a.get("severity") == ALERT_TYPE_GREEN

        ]

        # Build alert statistics
        alert_statistics = {

            "total_alerts": len(all_alerts),
            "critical_alerts": len(critical_alerts),
            "warning_alerts": len(warning_alerts),
            "info_alerts": len(info_alerts),

        }

        # Build alert summary
        overall_alert = alert_metrics["overall_alert"]

        if overall_alert == ALERT_TYPE_RED:

            recommendation = "Immediate Attention Required"

        elif overall_alert == ALERT_TYPE_YELLOW:

            recommendation = "Consume With Caution"

        else:

            recommendation = "Generally Safe"

        alert_summary = {

            "overall_alert": overall_alert,
            "health_alert_score": alert_metrics["health_alert_score"],
            "recommendation": recommendation,

        }

        return {

            "overall_alert": alert_metrics["overall_alert"],
            "health_alert_score": alert_metrics["health_alert_score"],
            "critical_alerts": critical_alerts,
            "warning_alerts": warning_alerts,
            "info_alerts": info_alerts,
            "frontend_cards": frontend_cards,
            "sound_trigger": sound_trigger,
            "alert_statistics": alert_statistics,
            "alert_summary": alert_summary,
            "all_alerts": all_alerts,

        }


# ==========================================================
# SINGLETON INSTANCE
# ==========================================================


health_alert_engine = HealthAlertEngine()


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [

    "HealthAlertEngine",
    "health_alert_engine",

]


# ==========================================================
# END OF FILE – health_alert_engine.py
# ==========================================================