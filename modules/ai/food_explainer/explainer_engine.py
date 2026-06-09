from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List


# =========================================================
# EXECUTIVE SUMMARY BUILDER
# =========================================================

class ExecutiveSummaryBuilder:

    def build(

        self,

        product_name: str,

        ingredient_intelligence: Dict[str, Any],

        metabolic_intelligence: Dict[str, Any],

        consumer_intelligence: Dict[str, Any],

        rag_result: Dict[str, Any],

    ) -> Dict[str, Any]:

        ingredient_summary = (

            ingredient_intelligence.get(
                "ingredient_summary",
                {},
            )

        )

        consumer_score = (

            consumer_intelligence
            .get(
                "consumer",
                {},
            )
            .get(
                "consumer_score",
                50,
            )

        )

        consensus = (

            rag_result.get(
                "scientific_consensus"
            )
        )

        confidence = (

            rag_result
            .get(
                "research_confidence"
            )
        )

        if isinstance(

            confidence,

            dict

        ):

            confidence_score = (

                confidence.get(
                    "score",
                    0,
                )

            )

        else:

            confidence_score = (

                getattr(
                    confidence,
                    "score",
                    0,
                )

            )

        return {

            "product":
            product_name,

            "consumer_score":
            consumer_score,

            "scientific_consensus":
            str(
                consensus
            ),

            "research_confidence":
            confidence_score,

            "ingredient_count":
            ingredient_summary.get(
                "ingredient_count",
                0,
            ),

            "summary":

            f"{product_name} contains "
            f"{ingredient_summary.get('ingredient_count',0)} "
            f"ingredients and currently has "
            f"a consumer score of "
            f"{consumer_score}.",

        }


# =========================================================
# INGREDIENT DOCTOR
# =========================================================

class IngredientDoctor:

    def analyze(

        self,

        ingredient_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        ingredient_functions = (

            ingredient_intelligence.get(

                "ingredient_functions",

                {},

            )

        )

        ingredient_risks = (

            ingredient_intelligence.get(

                "ingredient_risks",

                {},

            )

        )

        return {

            "functions":
            ingredient_functions,

            "risks":
            ingredient_risks,

        }


# =========================================================
# ADDITIVE DOCTOR
# =========================================================

class AdditiveDoctor:

    def analyze(

        self,

        ingredient_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        additives = (

            ingredient_intelligence.get(

                "additives",

                {},

            )

        )

        return {

            "total_additives":

            len(

                additives.get(

                    "detected_additives",

                    [],

                )

            ),

            "analysis":
            additives,

        }


# =========================================================
# NUTRITION DOCTOR
# =========================================================

class NutritionDoctor:

    def analyze(

        self,

        nutrition: Dict[str, Any],

    ) -> Dict[str, Any]:

        return {

            "sugar":
            nutrition.get(
                "sugar",
                0,
            ),

            "protein":
            nutrition.get(
                "protein",
                0,
            ),

            "fat":
            nutrition.get(
                "fat",
                0,
            ),

            "fiber":
            nutrition.get(
                "fiber",
                0,
            ),

            "sodium":
            nutrition.get(
                "sodium",
                0,
            ),

            "calories":
            nutrition.get(
                "calories",
                0,
            ),

        }


# =========================================================
# PROCESSING ANALYZER
# =========================================================

class ProcessingAnalyzer:

    def analyze(

        self,

        ingredient_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        return (

            ingredient_intelligence.get(

                "processing_analysis",

                {},

            )

        )


# =========================================================
# METABOLIC ANALYZER
# =========================================================

class MetabolicAnalyzer:

    def analyze(

        self,

        metabolic_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        return {

            "glycemic_load":

            metabolic_intelligence
            .get(
                "metabolic",
                {}
            )
            .get(
                "glycemic_load",
                {}
            ),

            "insulin_load":

            metabolic_intelligence
            .get(
                "metabolic",
                {}
            )
            .get(
                "insulin_load",
                {}
            ),

            "metabolic_flexibility":

            metabolic_intelligence
            .get(
                "metabolic",
                {}
            )
            .get(
                "metabolic_flexibility",
                {}
            ),

            "health_impact":

            metabolic_intelligence
            .get(
                "health_impact",
                {}
            ),

            "verdict":

            metabolic_intelligence
            .get(
                "verdict",
                {}
            ),

        }


# =========================================================
# CONSUMER ANALYZER
# =========================================================

class ConsumerAnalyzer:

    def analyze(

        self,

        consumer_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        return {

            "consumer":

            consumer_intelligence.get(
                "consumer",
                {}
            ),

            "compliance":

            consumer_intelligence.get(
                "compliance",
                {}
            ),

            "deception":

            consumer_intelligence.get(
                "deception",
                {}
            ),

            "suitability":

            consumer_intelligence.get(
                "suitability",
                {}
            ),

            "health_alerts":

            consumer_intelligence.get(
                "health_alerts",
                {}
            ),

            "verdict":

            consumer_intelligence.get(
                "verdict",
                {}
            ),

        }
    

# =========================================================
# SCIENTIFIC FINDINGS BUILDER
# =========================================================

class ScientificFindingsBuilder:

    def build(

        self,

        rag_result: Dict[str, Any],

    ) -> Dict[str, Any]:

        findings = []

        risks = []

        benefits = []

        uncertainties = []

        evidence = (

            rag_result.get(
                "evidence",
                [],
            )

        )

        for doc in evidence[:15]:

            summary = getattr(

                doc,

                "summary",

                "",

            )

            findings.append(
                summary
            )

        contradictions = (

            rag_result.get(
                "contradictions",
                [],
            )

        )

        if contradictions:

            uncertainties.extend(
                contradictions
            )

        consensus = (

            rag_result.get(
                "scientific_consensus"
            )
        )

        if str(consensus).endswith(
            "MOSTLY_NEGATIVE"
        ):

            risks.append(
                "Scientific evidence trends negative."
            )

        elif str(consensus).endswith(
            "MOSTLY_POSITIVE"
        ):

            benefits.append(
                "Scientific evidence trends positive."
            )

        return {

            "key_findings":
            findings[:10],

            "risks":
            risks,

            "benefits":
            benefits,

            "uncertainties":
            uncertainties,

        }


# =========================================================
# LONG TERM IMPACT ANALYZER
# =========================================================

class LongTermImpactAnalyzer:

    def analyze(

        self,

        metabolic_intelligence:
        Dict[str, Any],

        consumer_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        consumer_score = (

            consumer_intelligence
            .get(
                "consumer",
                {},
            )
            .get(
                "consumer_score",
                50,
            )

        )

        impact = (

            metabolic_intelligence
            .get(
                "health_impact",
                {},
            )

        )

        return {

            "30_days":

            {

                "projection":

                "Minimal measurable impact if consumed occasionally.",

                "risk_level":

                "LOW"

                if consumer_score >= 70

                else

                "MODERATE",

            },

            "90_days":

            {

                "projection":

                "Dietary patterns begin influencing metabolic outcomes.",

                "risk_level":

                "LOW"

                if consumer_score >= 70

                else

                "MODERATE",

            },

            "180_days":

            {

                "projection":

                "Repeated exposure may influence metabolic markers.",

                "risk_level":

                "MODERATE",

            },

            "365_days":

            {

                "projection":

                "Long-term dietary habits become significant determinants of health.",

                "risk_level":

                "MODERATE"

                if consumer_score >= 70

                else

                "HIGH",

            },

            "health_impact":
            impact,

        }


# =========================================================
# PREGNANCY ANALYZER
# =========================================================

class PregnancyAnalyzer:

    def analyze(

        self,

        ingredient_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        additives = (

            ingredient_intelligence
            .get(
                "additives",
                {},
            )

        )

        return {

            "status":
            "CONSULT_DOCTOR",

            "reason":

            "Pregnancy-specific dietary requirements vary by individual.",

            "additive_review":
            additives,

        }


# =========================================================
# CHILDREN ANALYZER
# =========================================================

class ChildrenAnalyzer:

    def analyze(

        self,

        ingredient_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        additive_count = (

            len(

                ingredient_intelligence
                .get(
                    "additives",
                    {},
                )
                .get(
                    "detected_additives",
                    [],
                )

            )

        )

        return {

            "suitable":

            additive_count < 5,

            "additive_count":
            additive_count,

            "recommendation":

            "Moderate consumption recommended.",

        }


# =========================================================
# DIABETIC ANALYZER
# =========================================================

class DiabeticAnalyzer:

    def analyze(

        self,

        metabolic_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        glycemic = (

            metabolic_intelligence
            .get(
                "metabolic",
                {},
            )
            .get(
                "glycemic_load",
                {},
            )

        )

        insulin = (

            metabolic_intelligence
            .get(
                "metabolic",
                {},
            )
            .get(
                "insulin_load",
                {},
            )

        )

        return {

            "glycemic_load":
            glycemic,

            "insulin_load":
            insulin,

            "recommendation":

            "Monitor portion size and blood glucose response.",

        }


# =========================================================
# HYPERTENSION ANALYZER
# =========================================================

class HypertensionAnalyzer:

    def analyze(

        self,

        nutrition: Dict[str, Any],

    ) -> Dict[str, Any]:

        sodium = (

            nutrition.get(
                "sodium",
                0,
            )

        )

        return {

            "sodium":
            sodium,

            "risk":

            "HIGH"

            if sodium >= 600

            else

            "LOW",

            "recommendation":

            "Monitor sodium intake throughout the day.",

        }


# =========================================================
# WEIGHT LOSS ANALYZER
# =========================================================

class WeightLossAnalyzer:

    def analyze(

        self,

        metabolic_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        satiety = (

            metabolic_intelligence
            .get(
                "metabolic",
                {},
            )
            .get(
                "satiety",
                {},
            )

        )

        metabolic_load = (

            metabolic_intelligence
            .get(
                "metabolic",
                {},
            )
            .get(
                "metabolic_load",
                {},
            )

        )

        return {

            "satiety":
            satiety,

            "metabolic_load":
            metabolic_load,

            "weight_loss_alignment":

            "GOOD"

            if satiety.get(
                "score",
                50,
            ) >= 70

            else

            "MODERATE",

        }
    

# =========================================================
# HEALTH HALO ANALYZER
# =========================================================

class HealthHaloAnalyzer:

    HALO_TERMS = {

        "natural",
        "healthy",
        "fitness",
        "immunity",
        "immune",
        "protein",
        "organic",
        "superfood",
        "wholesome",
        "diet",
        "lite",
        "light",

    }

    def analyze(

        self,

        claims: List[str],

        ingredient_intelligence:
        Dict[str, Any],

        consumer_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        detected_claims = []

        for claim in claims:

            claim_lower = (
                claim.lower()
            )

            for keyword in (

                self.HALO_TERMS

            ):

                if keyword in claim_lower:

                    detected_claims.append(
                        claim
                    )

                    break

        deception_score = (

            consumer_intelligence
            .get(
                "deception",
                {},
            )
            .get(
                "deception_score",
                0,
            )

        )

        return {

            "health_halo_detected":
            len(
                detected_claims
            ) > 0,

            "marketing_claims":
            detected_claims,

            "halo_risk":

            "HIGH"

            if deception_score >= 60

            else

            "LOW",

            "deception_score":
            deception_score,

        }


# =========================================================
# INGREDIENT AUTHENTICITY ANALYZER
# =========================================================

class IngredientAuthenticityAnalyzer:

    def analyze(

        self,

        claims: List[str],

        ingredients:
        List[Dict[str, Any]],

    ) -> Dict[str, Any]:

        ingredient_names = [

            item.get(
                "name",
                "",
            ).lower()

            for item

            in ingredients

        ]

        authenticity_flags = []

        for claim in claims:

            claim_lower = (
                claim.lower()
            )

            if "almond" in claim_lower:

                almond_found = any(

                    "almond" in item

                    for item in ingredient_names

                )

                if almond_found:

                    position = next(

                        (
                            i for i, item in enumerate(
                                ingredient_names
                            )
                            if "almond" in item
                        ),
                        -1

                    )

                    if position > 5:

                        authenticity_flags.append(

                            "ALMOND_CLAIM_LOW_PRESENCE"

                        )

            if "fruit" in claim_lower:

                fruit_found = any(

                    word in ingredient_names

                    for word in [

                        "apple",
                        "banana",
                        "mango",
                        "orange",
                        "grape",

                    ]

                )

                if not fruit_found:

                    authenticity_flags.append(

                        "FRUIT_CLAIM_UNSUPPORTED"

                    )

        return {

            "authenticity_flags":
            authenticity_flags,

            "authenticity_score":

            max(

                0,

                100

                -

                len(
                    authenticity_flags
                )

                * 25,

            ),

        }


# =========================================================
# ADDITIVE INTERACTION ANALYZER
# =========================================================

class AdditiveInteractionAnalyzer:

    def analyze(

        self,

        ingredient_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        additives = (

            ingredient_intelligence
            .get(
                "additives",
                {},
            )
            .get(
                "detected_additives",
                [],
            )

        )

        interactions = []

        additive_names = [

            str(a).lower()

            for a

            in additives

        ]

        if (

            "sodium benzoate"
            in additive_names

            and

            "ascorbic acid"
            in additive_names

        ):

            interactions.append(

                {

                    "type":
                    "POTENTIAL_INTERACTION",

                    "ingredients": [

                        "sodium benzoate",

                        "ascorbic acid",

                    ],

                    "note":

                    "Combination sometimes discussed in food safety literature.",

                }

            )

        return {

            "interaction_count":
            len(
                interactions
            ),

            "interactions":
            interactions,

        }


# =========================================================
# PROCESSING BURDEN ANALYZER
# =========================================================

class ProcessingBurdenAnalyzer:

    def analyze(

        self,

        ingredient_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        processing = (

            ingredient_intelligence
            .get(
                "processing_analysis",
                {},
            )

        )

        level = (

            processing.get(
                "processing_level",
                "UNKNOWN",
            )

        )

        burden_score = 30

        if level in [

            "ULTRA_PROCESSED",

            "NOVA_4",

        ]:

            burden_score = 90

        elif level in [

            "NOVA_3",

        ]:

            burden_score = 65

        elif level in [

            "NOVA_2",

        ]:

            burden_score = 35

        return {

            "processing_level":
            level,

            "processing_burden_score":
            burden_score,

            "burden_category":

            "HIGH"

            if burden_score >= 80

            else

            "MODERATE"

            if burden_score >= 50

            else

            "LOW",

        }


# =========================================================
# RISK MATRIX BUILDER
# =========================================================

class RiskMatrixBuilder:

    def build(

        self,

        ingredient_intelligence:
        Dict[str, Any],

        metabolic_intelligence:
        Dict[str, Any],

        consumer_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        ingredient_risk = (

            ingredient_intelligence
            .get(
                "ingredient_risks",
                {},
            )
            .get(
                "ingredient_health_summary",
                {},
            )
            .get(
                "average_risk_score",
                50,
            )

        )

        consumer_score = (

            consumer_intelligence
            .get(
                "consumer",
                {},
            )
            .get(
                "consumer_score",
                50,
            )

        )

        metabolic_score = (

            metabolic_intelligence
            .get(
                "metabolic",
                {},
            )
            .get(
                "metabolic_load",
                {},
            )
            .get(
                "score",
                50,
            )

        )

        overall_risk = round(

            (

                ingredient_risk

                +

                metabolic_score

                +

                (100 - consumer_score)

            )

            / 3

        )

        if overall_risk >= 80:

            category = (
                "VERY_HIGH"
            )

        elif overall_risk >= 60:

            category = (
                "HIGH"
            )

        elif overall_risk >= 40:

            category = (
                "MODERATE"
            )

        else:

            category = (
                "LOW"
            )

        return {

            "overall_risk":
            overall_risk,

            "risk_category":
            category,

            "ingredient_risk":
            ingredient_risk,

            "metabolic_risk":
            metabolic_score,

            "consumer_risk":
            100 -
            consumer_score,

        }


# =========================================================
# BENEFIT MATRIX BUILDER
# =========================================================

class BenefitMatrixBuilder:

    def build(

        self,

        nutrition: Dict[str, Any],

        metabolic_intelligence:
        Dict[str, Any],

        consumer_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        benefits = []

        protein = nutrition.get(
            "protein",
            0,
        )

        fiber = nutrition.get(
            "fiber",
            0,
        )

        consumer_score = (

            consumer_intelligence
            .get(
                "consumer",
                {},
            )
            .get(
                "consumer_score",
                50,
            )

        )

        if protein >= 10:

            benefits.append(
                "HIGH_PROTEIN"
            )

        if fiber >= 3:

            benefits.append(
                "FIBER_SOURCE"
            )

        if consumer_score >= 75:

            benefits.append(
                "GOOD_OVERALL_PROFILE"
            )

        return {

            "benefits":
            benefits,

            "benefit_score":

            min(

                100,

                len(
                    benefits
                )

                * 25,

            ),

            "benefit_count":
            len(
                benefits
            ),

        }
    

# =========================================================
# WHO SHOULD CONSUME
# =========================================================

class WhoShouldConsumeAnalyzer:

    def analyze(

        self,

        nutrition: Dict[str, Any],

        metabolic_intelligence:
        Dict[str, Any],

        consumer_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        groups = []

        protein = nutrition.get(
            "protein",
            0,
        )

        fiber = nutrition.get(
            "fiber",
            0,
        )

        consumer_score = (

            consumer_intelligence
            .get(
                "consumer",
                {},
            )
            .get(
                "consumer_score",
                50,
            )

        )

        if protein >= 10:

            groups.append(
                "ACTIVE_INDIVIDUALS"
            )

        if fiber >= 3:

            groups.append(
                "DIGESTIVE_HEALTH_FOCUSED"
            )

        if consumer_score >= 75:

            groups.append(
                "GENERAL_POPULATION"
            )

        return {

            "recommended_groups":
            groups,

            "recommendation_score":
            min(
                100,
                len(groups) * 25,
            ),

        }


# =========================================================
# WHO SHOULD AVOID
# =========================================================

class WhoShouldAvoidAnalyzer:

    def analyze(

        self,

        nutrition: Dict[str, Any],

        ingredient_intelligence:
        Dict[str, Any],

        metabolic_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        avoid_groups = []

        sugar = nutrition.get(
            "sugar",
            0,
        )

        sodium = nutrition.get(
            "sodium",
            0,
        )

        risk_summary = (

            ingredient_intelligence
            .get(
                "ingredient_risks",
                {},
            )
            .get(
                "ingredient_health_summary",
                {},
            )

        )

        if sugar >= 10:

            avoid_groups.append(
                "DIABETICS"
            )

        if sodium >= 600:

            avoid_groups.append(
                "HYPERTENSION_PATIENTS"
            )

        if (

            risk_summary.get(
                "high_risk_count",
                0,
            )

            >= 3

        ):

            avoid_groups.append(
                "HIGH_RISK_POPULATIONS"
            )

        return {

            "avoid_groups":
            avoid_groups,

            "avoidance_score":

            min(

                100,

                len(
                    avoid_groups
                )

                * 30,

            ),

        }


# =========================================================
# SUITABILITY MATRIX
# =========================================================

class SuitabilityMatrixBuilder:

    def build(

        self,

        pregnancy: Dict[str, Any],

        children: Dict[str, Any],

        diabetic: Dict[str, Any],

        hypertension: Dict[str, Any],

        weight_loss: Dict[str, Any],

    ) -> Dict[str, Any]:

        return {

            "pregnancy":
            pregnancy,

            "children":
            children,

            "diabetic":
            diabetic,

            "hypertension":
            hypertension,

            "weight_loss":
            weight_loss,

        }


# =========================================================
# FINAL VERDICT ENGINE
# =========================================================

class FinalVerdictEngine:

    def build(

        self,

        risk_matrix: Dict[str, Any],

        benefit_matrix: Dict[str, Any],

        consumer_intelligence:
        Dict[str, Any],

        rag_result: Dict[str, Any],

    ) -> Dict[str, Any]:

        risk_score = (

            risk_matrix.get(
                "overall_risk",
                50,
            )

        )

        benefit_score = (

            benefit_matrix.get(
                "benefit_score",
                50,
            )

        )

        consumer_score = (

            consumer_intelligence
            .get(
                "consumer",
                {},
            )
            .get(
                "consumer_score",
                50,
            )

        )

        confidence = (

            rag_result
            .get(
                "research_confidence"
            )
        )

        if isinstance(

            confidence,

            dict

        ):

            confidence_score = (

                confidence.get(
                    "score",
                    50,
                )

            )

        else:

            confidence_score = (

                getattr(
                    confidence,
                    "score",
                    50,
                )

            )

        final_score = round(

            (

                consumer_score
                * 0.40

            )

            +

            (

                benefit_score
                * 0.25

            )

            +

            (

                confidence_score
                * 0.20

            )

            +

            (

                (100 - risk_score)
                * 0.15

            )

        )

        if final_score >= 85:

            verdict = (
                "EXCELLENT"
            )

            recommendation = (
                "RECOMMENDED"
            )

        elif final_score >= 70:

            verdict = (
                "GOOD"
            )

            recommendation = (
                "GOOD_CHOICE"
            )

        elif final_score >= 55:

            verdict = (
                "MODERATE"
            )

            recommendation = (
                "OCCASIONAL_USE"
            )

        elif final_score >= 40:

            verdict = (
                "POOR"
            )

            recommendation = (
                "LIMIT"
            )

        else:

            verdict = (
                "AVOID"
            )

            recommendation = (
                "AVOID"
            )

        return {

            "food_score":
            final_score,

            "verdict":
            verdict,

            "recommendation":
            recommendation,

            "risk_score":
            risk_score,

            "benefit_score":
            benefit_score,

            "research_confidence":
            confidence_score,

        }


# =========================================================
# PRODUCT IDENTITY ANALYZER
# =========================================================

class ProductIdentityAnalyzer:

    def analyze(

        self,

        product: Dict[str, Any],

    ) -> Dict[str, Any]:

        return {

            "product_name":

            product.get(
                "name",
                "UNKNOWN",
            ),

            "brand":

            product.get(
                "brand",
                "UNKNOWN",
            ),

            "category":

            product.get(
                "category",
                "UNKNOWN",
            ),

            "subcategory":

            product.get(
                "subcategory",
                "UNKNOWN",
            ),

            "barcode":

            product.get(
                "barcode",
                "",
            ),

        }


# =========================================================
# CLAIMS ANALYZER
# =========================================================

class ClaimsAnalyzer:

    HEALTH_CLAIMS = {

        "healthy",
        "high protein",
        "high fibre",
        "high fiber",
        "immunity",
        "heart healthy",
        "diabetic friendly",
        "low sugar",
        "no sugar",
        "low fat",

    }

    MARKETING_TERMS = {

        "premium",
        "natural",
        "fitness",
        "superfood",
        "wholesome",
        "lite",
        "light",

    }

    def analyze(

        self,

        claims: List[str],

    ) -> Dict[str, Any]:

        health_claims = []

        marketing_claims = []

        risk_flags = []

        for claim in claims:

            claim_lower = (
                claim.lower()
            )

            for keyword in (

                self.HEALTH_CLAIMS

            ):

                if keyword in claim_lower:

                    health_claims.append(
                        claim
                    )

            for keyword in (

                self.MARKETING_TERMS

            ):

                if keyword in claim_lower:

                    marketing_claims.append(
                        claim
                    )

        if len(
            marketing_claims
        ) > 3:

            risk_flags.append(

                "HEAVY_MARKETING_LANGUAGE"

            )

        return {

            "claims":
            claims,

            "health_claims":
            sorted(
                list(
                    set(
                        health_claims
                    )
                )
            ),

            "marketing_claims":
            sorted(
                list(
                    set(
                        marketing_claims
                    )
                )
            ),

            "risk_flags":
            risk_flags,

        }


# =========================================================
# SERVING SIZE ANALYZER
# =========================================================

class ServingSizeAnalyzer:

    def analyze(

        self,

        serving_size: str,

        nutrition: Dict[str, Any],

    ) -> Dict[str, Any]:

        sugar = nutrition.get(
            "sugar",
            0,
        )

        sodium = nutrition.get(
            "sodium",
            0,
        )

        calories = nutrition.get(
            "calories",
            0,
        )

        warnings = []

        if sugar >= 15:

            warnings.append(
                "HIGH_SUGAR_PER_SERVING"
            )

        if sodium >= 600:

            warnings.append(
                "HIGH_SODIUM_PER_SERVING"
            )

        if calories >= 400:

            warnings.append(
                "HIGH_CALORIES_PER_SERVING"
            )

        return {

            "serving_size":
            serving_size,

            "nutrition_context": {

                "sugar":
                sugar,

                "sodium":
                sodium,

                "calories":
                calories,

            },

            "warnings":
            warnings,

        }


# =========================================================
# OCR CONTEXT ANALYZER
# =========================================================

class OCRContextAnalyzer:

    WARNING_TERMS = {

        "contains",

        "artificial",

        "preservative",

        "flavour",

        "flavor",

        "sweetener",

    }

    def analyze(

        self,

        ocr_text: str,

    ) -> Dict[str, Any]:

        text = str(

            ocr_text or ""

        ).lower()

        detected_terms = []

        for term in (

            self.WARNING_TERMS

        ):

            if term in text:

                detected_terms.append(
                    term
                )

        return {

            "detected_terms":
            detected_terms,

            "ocr_length":
            len(
                ocr_text or ""
            ),

            "ocr_available":

            bool(
                ocr_text
            ),

        }


# =========================================================
# BRAND TRUST ANALYZER
# =========================================================

class BrandTrustAnalyzer:

    def analyze(

        self,

        product: Dict[str, Any],

        consumer_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        trust_score = (

            consumer_intelligence
            .get(
                "consumer",
                {},
            )
            .get(
                "summary",
                {},
            )
            .get(
                "trust_score",
                50,
            )

        )

        if trust_score >= 80:

            level = (
                "HIGH"
            )

        elif trust_score >= 60:

            level = (
                "MODERATE"
            )

        else:

            level = (
                "LOW"
            )

        return {

            "brand":

            product.get(
                "brand",
                "UNKNOWN",
            ),

            "trust_score":
            trust_score,

            "trust_level":
            level,

        }


# =========================================================
# FOOD EXPLAINER ENGINE
# =========================================================

class FoodExplainerEngine:

    def __init__(self):

        self.executive_summary = (
            ExecutiveSummaryBuilder()
        )

        self.ingredient_doctor = (
            IngredientDoctor()
        )

        self.additive_doctor = (
            AdditiveDoctor()
        )

        self.nutrition_doctor = (
            NutritionDoctor()
        )

        self.processing_analyzer = (
            ProcessingAnalyzer()
        )

        self.metabolic_analyzer = (
            MetabolicAnalyzer()
        )

        self.consumer_analyzer = (
            ConsumerAnalyzer()
        )

        self.scientific_findings = (
            ScientificFindingsBuilder()
        )

        self.long_term_impact = (
            LongTermImpactAnalyzer()
        )

        self.pregnancy_analyzer = (
            PregnancyAnalyzer()
        )

        self.children_analyzer = (
            ChildrenAnalyzer()
        )

        self.diabetic_analyzer = (
            DiabeticAnalyzer()
        )

        self.hypertension_analyzer = (
            HypertensionAnalyzer()
        )

        self.weight_loss_analyzer = (
            WeightLossAnalyzer()
        )

        self.health_halo_analyzer = (
            HealthHaloAnalyzer()
        )

        self.authenticity_analyzer = (
            IngredientAuthenticityAnalyzer()
        )

        self.additive_interaction_analyzer = (
            AdditiveInteractionAnalyzer()
        )

        self.processing_burden_analyzer = (
            ProcessingBurdenAnalyzer()
        )

        self.risk_matrix_builder = (
            RiskMatrixBuilder()
        )

        self.benefit_matrix_builder = (
            BenefitMatrixBuilder()
        )

        self.consume_analyzer = (
            WhoShouldConsumeAnalyzer()
        )

        self.avoid_analyzer = (
            WhoShouldAvoidAnalyzer()
        )

        self.suitability_builder = (
            SuitabilityMatrixBuilder()
        )

        self.verdict_engine = (
            FinalVerdictEngine()
        )

        self.product_identity = (
            ProductIdentityAnalyzer()
        )

        self.claims_analyzer = (
            ClaimsAnalyzer()
        )

        self.serving_size_analyzer = (
            ServingSizeAnalyzer()
        )

        self.ocr_context_analyzer = (
            OCRContextAnalyzer()
        )

        self.brand_trust_analyzer = (
            BrandTrustAnalyzer()
        )

    def analyze(

        self,

        product: Dict[str, Any],

        nutrition: Dict[str, Any],

        claims: List[str],

        ocr_text: str,

        serving_size: str,

        ingredient_intelligence: Dict[str, Any],

        metabolic_intelligence: Dict[str, Any],

        consumer_intelligence: Dict[str, Any],

        rag_result: Dict[str, Any],

    ) -> Dict[str, Any]:

        pregnancy_analysis = (

            self.pregnancy_analyzer.analyze(

                ingredient_intelligence,

            )

        )

        children_analysis = (

            self.children_analyzer.analyze(

                ingredient_intelligence,

            )

        )

        diabetic_analysis = (

            self.diabetic_analyzer.analyze(

                metabolic_intelligence,

            )

        )

        hypertension_analysis = (

            self.hypertension_analyzer.analyze(

                nutrition,

            )

        )

        weight_loss_analysis = (

            self.weight_loss_analyzer.analyze(

                metabolic_intelligence,

            )

        )

        risk_matrix = (

            self.risk_matrix_builder.build(

                ingredient_intelligence,

                metabolic_intelligence,

                consumer_intelligence,

            )

        )

        benefit_matrix = (

            self.benefit_matrix_builder.build(

                nutrition,

                metabolic_intelligence,

                consumer_intelligence,

            )

        )

        suitability = (

            self.suitability_builder.build(

                pregnancy_analysis,

                children_analysis,

                diabetic_analysis,

                hypertension_analysis,

                weight_loss_analysis,

            )

        )

        return {

            "executive_summary":

            self.executive_summary.build(

                product.get("name", "UNKNOWN"),

                ingredient_intelligence,

                metabolic_intelligence,

                consumer_intelligence,

                rag_result,

            ),

            "product_identity":

            self.product_identity.analyze(

                product,

            ),

            "claims_analysis":

            self.claims_analyzer.analyze(

                claims,

            ),

            "serving_size_analysis":

            self.serving_size_analyzer.analyze(

                serving_size,

                nutrition,

            ),

            "ocr_context":

            self.ocr_context_analyzer.analyze(

                ocr_text,

            ),

            "brand_trust":

            self.brand_trust_analyzer.analyze(

                product,

                consumer_intelligence,

            ),

            "ingredient_analysis":

            self.ingredient_doctor.analyze(

                ingredient_intelligence,

            ),

            "additive_analysis":

            self.additive_doctor.analyze(

                ingredient_intelligence,

            ),

            "nutrition_analysis":

            self.nutrition_doctor.analyze(

                nutrition,

            ),

            "processing_analysis":

            self.processing_analyzer.analyze(

                ingredient_intelligence,

            ),

            "metabolic_analysis":

            self.metabolic_analyzer.analyze(

                metabolic_intelligence,

            ),

            "consumer_analysis":

            self.consumer_analyzer.analyze(

                consumer_intelligence,

            ),

            "scientific_findings":

            self.scientific_findings.build(

                rag_result,

            ),

            "long_term_impact":

            self.long_term_impact.analyze(

                metabolic_intelligence,

                consumer_intelligence,

            ),

            "pregnancy_analysis":
            pregnancy_analysis,

            "children_analysis":
            children_analysis,

            "diabetic_analysis":
            diabetic_analysis,

            "hypertension_analysis":
            hypertension_analysis,

            "weight_loss_analysis":
            weight_loss_analysis,

            "health_halo":

            self.health_halo_analyzer.analyze(

                claims,

                ingredient_intelligence,

                consumer_intelligence,

            ),

            "authenticity":

            self.authenticity_analyzer.analyze(

                claims,

                ingredient_intelligence.get("ingredients", []),

            ),

            "additive_interactions":

            self.additive_interaction_analyzer.analyze(

                ingredient_intelligence,

            ),

            "processing_burden":

            self.processing_burden_analyzer.analyze(

                ingredient_intelligence,

            ),

            "risk_matrix":
            risk_matrix,

            "benefit_matrix":
            benefit_matrix,

            "who_should_consume":

            self.consume_analyzer.analyze(

                nutrition,

                metabolic_intelligence,

                consumer_intelligence,

            ),

            "who_should_avoid":

            self.avoid_analyzer.analyze(

                nutrition,

                ingredient_intelligence,

                metabolic_intelligence,

            ),

            "suitability":
            suitability,

            "final_verdict":

            self.verdict_engine.build(

                risk_matrix,

                benefit_matrix,

                consumer_intelligence,

                rag_result,

            ),

        }
    

food_explainer_engine = (
    FoodExplainerEngine()
)