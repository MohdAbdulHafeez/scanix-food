from typing import Dict
from typing import Any

from .body_simulation_engine import (
    body_simulation_engine
)

from .organ_impact_engine import (
    organ_impact_engine
)

from .limit_engine import (
    limit_engine
)


class DigitalTwinService:

    def analyze(
        self,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:

        try:

            body_result = (

                body_simulation_engine
                .analyze(
                    payload
                )

            )

        except Exception as e:

            body_result = {

                "error":
                str(e),

                "digital_twin_score":
                50,

            }

        try:

            organ_result = (

                organ_impact_engine
                .analyze({

                    **payload,

                    "body_simulation":
                    body_result

                })

            )

        except Exception as e:

            organ_result = {

                "error":
                str(e),

                "organ_health_score":
                50,

            }

        try:

            limit_result = (

                limit_engine
                .analyze(
                    payload
                )

            )

        except Exception as e:

            limit_result = {

                "error":
                str(e),

                "overall_limit_score":
                50,

            }

        organ_score = (
            organ_result.get(
                "organ_health_score",
                50
            )
        )

        twin_score = (
            body_result.get(
                "digital_twin_score",
                50
            )
        )

        limit_score = (
            limit_result.get(
                "overall_limit_score",
                50
            )
        )

        overall_score = round(

            (
                twin_score * 0.40
                +
                organ_score * 0.35
                +
                limit_score * 0.25
            ),

            2

        )

        return {

            "system":

            "Human Body Digital Twin",

            "version":

            "1.0.0",

            "body_simulation":

            body_result,

            "organ_impact":

            organ_result,

            "limit_analysis":

            limit_result,

            "overall_digital_twin_score":

            overall_score,

            "overall_verdict":

            self._verdict(
                overall_score
            )

        }

    def _verdict(
        self,
        score: float
    ) -> str:

        if score >= 90:
            return "EXCELLENT"

        if score >= 80:
            return "GOOD"

        if score >= 65:
            return "MODERATE"

        if score >= 50:
            return "POOR"

        return "HIGH_RISK"


digital_twin_service = (
    DigitalTwinService()
)