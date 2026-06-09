# ==========================================================
# SCANIX AI
# SYSTEM 8 – TRUST INTELLIGENCE (DECEPTION ENGINE)
# ELITE PRODUCTION GRADE – FINAL VERSION
# ==========================================================


from __future__ import annotations


from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Set


# ==========================================================
# CONSTANTS
# ==========================================================


HIDDEN_SUGARS = {

    "maltodextrin",
    "corn syrup",
    "glucose syrup",
    "fructose",
    "dextrose",
    "invert sugar",
    "liquid glucose",
    "maltose",
    "molasses",
    "sucrose",
    "hfcs",
    "jaggery",
    "honey",

}

CHILD_MARKETING_WORDS = {

    "kids",
    "children",
    "junior",
    "growing",
    "school",
    "fun",
    "magic",

}

PREMIUM_WORDS = {

    "premium",
    "gourmet",
    "gold",
    "signature",
    "artisan",
    "exclusive",
    "finest",

}

HEALTH_WORDS = {

    "healthy",
    "fitness",
    "wellness",
    "active",
    "lite",
    "light",
    "nutritious",
    "smart choice",
    "wholesome",

}

GREEN_WORDS = {

    "eco",
    "green",
    "planet",
    "earth",
    "sustainable",
    "carbon neutral",
    "environment friendly",
    "climate conscious",
    "eco-friendly",
    "net zero",

}

PROCESSING_PENALTY_MAP = {

    "MINIMALLY_PROCESSED": 0,
    "PROCESSED": 10,
    "ULTRA_PROCESSED": 25,

}

HFSS_THRESHOLDS = {

    "sugar": 22.5,
    "sodium": 400,
    "fat": 17.5,
    "saturated_fat": 5.0,

}

PROTEIN_DENSITY_THRESHOLD = 0.12
FIBER_DENSITY_THRESHOLD = 0.03

PROTEIN_PENALTY = 20
FIBER_PENALTY = 15

HEALTH_HALO_PENALTY = 20
UPF_HEALTH_HALO_PENALTY = 25
HFSS_HEALTH_HALO_PENALTY = 25

NATURALITY_FRAUD_PENALTY = 25
NO_PALM_OIL_FRAUD_PENALTY = 30
GREENWASHING_PENALTY = 15
FRONT_BACK_CONTRADICTION_PENALTY = 20
ADDITIVE_HEAVY_PENALTY = 10
HIDDEN_SUGAR_MARKETING_PENALTY = 15
INGREDIENT_SPLITTING_PENALTY = 20
CHILD_MARKETING_RISK_PENALTY = 20
PREMIUMIZATION_FRAUD_PENALTY = 15

SUGAR_FREE_FRAUD_PENALTY = 30
SWEETENER_DECEPTION_PENALTY = 25

CRITICAL_VIOLATION_PENALTY = 25
HIGH_VIOLATION_PENALTY = 15

HARM_SUGAR_THRESHOLD = 10
HARM_SODIUM_THRESHOLD = 500

HARM_PROCESSING_MULTIPLIER = 1.5

RISK_THRESHOLDS = {

    "HIGH": 70,
    "MODERATE": 35,
    "LOW": 0,

}

CONFIDENCE_BASE = 50
CONFIDENCE_INGREDIENT_BONUS = 20
CONFIDENCE_CLAIM_BONUS = 10
CONFIDENCE_NUTRITION_BONUS = 20

DECEPTION_SCORE_MAX = 100
DECEPTION_SCORE_MIN = 0

SCORE_MAX = 100
SCORE_MIN = 0

HARM_SCORE_MAX = 100

MANIPULATION_INDEX_MAX = 100

HIDDEN_SUGAR_COUNT_MULTIPLIER = 10
ADDITIVE_COUNT_MULTIPLIER = 5

INGREDIENT_SPLITTING_THRESHOLD = 3
E_NUMBERS_THRESHOLD = 4
ADDITIVE_HEAVY_THRESHOLD = 4

TRANSPARENCY_INGREDIENT_PENALTY_THRESHOLD = 15
TRANSPARENCY_INGREDIENT_PENALTY = 10

HIGH_CLAIM_DENSITY_THRESHOLD = 15
HIGH_CLAIM_DENSITY_PENALTY = 15

SUGAR_FREE_THRESHOLD = 0.5

PROCESSING_HEALTH_HALO_CHECK = "ULTRA_PROCESSED"

ALERT_TYPES = {

    "HIGH_CLAIM_DENSITY",
    "UPF_HEALTH_HALO",
    "HFSS_HEALTH_HALO",
    "HEALTH_HALO",
    "NATURALITY_FRAUD",
    "PROTEIN_INFLATION",
    "FIBER_INFLATION",
    "SUGAR_FREE_FRAUD",
    "SWEETENER_DECEPTION",
    "NO_PALM_OIL_FRAUD",
    "GREENWASHING",
    "FRONT_BACK_CONTRADICTION",
    "ADDITIVE_HEAVY_PRODUCT",
    "HIDDEN_SUGAR_MARKETING",
    "INGREDIENT_SPLITTING",
    "CHILD_MARKETING_RISK",
    "PREMIUMIZATION_FRAUD",

}


# ==========================================================
# DECEPTION ENGINE
# ==========================================================


class DeceptionEngine:
    """
    Deception Detection Engine for System 8 – Trust Intelligence.

    Detects marketing deception including:
    - Health halo effects on ultra-processed/HFSS products
    - Naturality fraud (natural claims with artificial additives)
    - Protein and fiber inflation
    - Sugar-free fraud and sweetener deception
    - Greenwashing and premiumization fraud
    - Child marketing risks
    - Ingredient splitting
    - Front-back label contradictions
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
        max_score: int = SCORE_MAX,
        min_score: int = SCORE_MIN,
    ) -> int:
        """
        Normalize score to specified range.

        Args:
            score: Raw score
            max_score: Maximum allowed value
            min_score: Minimum allowed value

        Returns:
            Normalized score
        """

        return max(
            min_score,
            min(
                max_score,
                self._safe_int(score),
            ),
        )

    def _get_risk_level(
        self,
        deception_score: int,
    ) -> str:
        """
        Get risk level based on deception score.

        Args:
            deception_score: Deception score (0-100)

        Returns:
            Risk level (HIGH, MODERATE, or LOW)
        """

        if deception_score >= RISK_THRESHOLDS["HIGH"]:
            return "HIGH"
        if deception_score >= RISK_THRESHOLDS["MODERATE"]:
            return "MODERATE"
        return "LOW"

    def _is_hfss(
        self,
        sugar: float,
        sodium: float,
        fat: float,
        saturated_fat: float,
    ) -> bool:
        """
        Check if product is HFSS (High in Fat, Sugar, or Salt).

        Args:
            sugar: Sugar content in grams
            sodium: Sodium content in mg
            fat: Fat content in grams
            saturated_fat: Saturated fat content in grams

        Returns:
            True if product meets HFSS criteria
        """

        return any([

            sugar >= HFSS_THRESHOLDS["sugar"],
            sodium >= HFSS_THRESHOLDS["sodium"],
            fat >= HFSS_THRESHOLDS["fat"],
            saturated_fat >= HFSS_THRESHOLDS["saturated_fat"],

        ])

    def _extract_ingredient_names(
        self,
        ingredients: List[Dict[str, Any]],
    ) -> List[str]:
        """
        Extract normalized ingredient names.

        Args:
            ingredients: List of ingredient dictionaries

        Returns:
            List of lowercase ingredient names
        """

        return [

            str(item.get("name", "")).lower()

            for item in ingredients

        ]

    def _count_hidden_sugars(
        self,
        ingredient_names: List[str],
    ) -> int:
        """
        Count hidden sugar occurrences in ingredients.

        Args:
            ingredient_names: List of ingredient names

        Returns:
            Count of hidden sugar matches
        """

        all_text = " ".join(
            ingredient_names
        ).lower()

        return sum(
            sugar in all_text
            for sugar in HIDDEN_SUGARS
        )

    def _get_sugar_sources(
        self,
        ingredient_names: List[str],
    ) -> List[str]:
        """
        Get ingredients that are sugar sources.

        Args:
            ingredient_names: List of ingredient names

        Returns:
            List of ingredients containing hidden sugars
        """

        return [

            ingredient

            for ingredient in ingredient_names

            if any(
                sugar in ingredient
                for sugar in HIDDEN_SUGARS
            )

        ]

    def analyze(
        self,
        claims: List[str],
        nutrition: Dict[str, Any],
        ingredient_intelligence: Dict[str, Any],
        compliance: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Master deception analysis method.

        Args:
            claims: List of marketing claims
            nutrition: Nutrition data (per 100g)
            ingredient_intelligence: Ingredient analysis from System 2
            compliance: Compliance analysis from System 4

        Returns:
            Complete deception analysis
        """

        alerts: Set[str] = set()

        evidence: List[Dict[str, Any]] = []

        deception_score = 0

        claims_lower = [

            str(c).lower()

            for c in claims

        ]

        # Extract nutrition data
        nutrition = nutrition or {}

        sugar = self._safe_float(
            nutrition.get("sugar", 0),
        )

        protein = self._safe_float(
            nutrition.get("protein", 0),
        )

        fiber = self._safe_float(
            nutrition.get("fiber", 0),
        )

        fat = self._safe_float(
            nutrition.get("fat", 0),
        )

        sodium = self._safe_float(
            nutrition.get("sodium", 0),
        )

        saturated_fat = self._safe_float(
            nutrition.get("saturated_fat", 0),
        )

        calories = self._safe_float(
            nutrition.get("calories", 0),
        )

        cal_base = calories if calories > 0 else 100

        protein_density = (protein * 4) / cal_base
        fiber_density = (fiber * 2) / cal_base

        is_hfss = self._is_hfss(
            sugar,
            sodium,
            fat,
            saturated_fat,
        )

        # Extract ingredient data
        registry = ingredient_intelligence.get(
            "registry",
            {},
        )

        e_numbers = registry.get("e_numbers", [])

        contains_palm_oil = registry.get(
            "contains_palm_oil",
            False,
        )

        sweeteners = (

            registry
            .get("artificial_sweeteners", {})
            .get("count", 0)

        )

        hyperactivity_risk = (

            registry
            .get("hyperactivity_risk", {})
            .get("risk_level", "LOW")

        )

        high_risk_additives = registry.get(
            "high_risk_additives",
            [],
        )

        ingredient_summary = ingredient_intelligence.get(
            "ingredient_summary",
            {},
        )

        artificial_count = ingredient_summary.get(
            "artificial_count",
            0,
        )

        additive_count = ingredient_summary.get(
            "additive_candidates",
            0,
        )

        total_ingredients = ingredient_summary.get(
            "ingredient_count",
            0,
        )

        processing_level = (

            ingredient_intelligence
            .get("processing_analysis", {})
            .get("processing_level", "UNKNOWN")

        )

        processing_penalty = PROCESSING_PENALTY_MAP.get(
            processing_level,
            0,
        )

        deception_score += processing_penalty

        # Extract compliance data
        critical_violations = compliance.get(
            "critical_violations",
            [],
        )

        high_violations = compliance.get(
            "high_violations",
            [],
        )

        deception_score += (
            len(critical_violations) * CRITICAL_VIOLATION_PENALTY
        )

        deception_score += (
            len(high_violations) * HIGH_VIOLATION_PENALTY
        )

        # Extract ingredients
        ingredients = ingredient_intelligence.get(
            "ingredients",
            [],
        )

        ingredient_names = self._extract_ingredient_names(
            ingredients,
        )

        hidden_sugar_count = self._count_hidden_sugars(
            ingredient_names,
        )

        # High claim density check
        claim_density = len(claims_lower)

        if claim_density >= HIGH_CLAIM_DENSITY_THRESHOLD:

            alerts.add("HIGH_CLAIM_DENSITY")

            deception_score += HIGH_CLAIM_DENSITY_PENALTY

            evidence.append({

                "type": "HIGH_CLAIM_DENSITY",
                "reason": "Excessive number of marketing claims obscures facts",

            })

        # Health halo detection
        if any(
            word in claim
            for claim in claims_lower
            for word in HEALTH_WORDS
        ):

            if processing_level == PROCESSING_HEALTH_HALO_CHECK:

                alerts.add("UPF_HEALTH_HALO")

                evidence.append({

                    "type": "UPF_HEALTH_HALO",
                    "reason": "Health claims used on ultra-processed product",

                })

                deception_score += UPF_HEALTH_HALO_PENALTY

            if is_hfss:

                alerts.add("HFSS_HEALTH_HALO")

                evidence.append({

                    "type": "HFSS_HEALTH_HALO",
                    "reason": "Health claims used on High Fat, Sugar, or Salt product",

                })

                deception_score += HFSS_HEALTH_HALO_PENALTY

            if (sugar >= 10 or sodium >= 500) and not is_hfss:

                alerts.add("HEALTH_HALO")

                evidence.append({

                    "type": "HEALTH_HALO",
                    "reason": "Healthy positioning contradicts nutrition profile",

                })

                deception_score += HEALTH_HALO_PENALTY

        # Naturality fraud detection
        if any("natural" in c for c in claims_lower):

            if artificial_count > 0 or len(high_risk_additives) > 0:

                alerts.add("NATURALITY_FRAUD")

                evidence.append({

                    "type": "NATURALITY_FRAUD",
                    "reason": "Natural claim despite artificial or high-risk additives",
                    "high_risk_additives": high_risk_additives,

                })

                deception_score += NATURALITY_FRAUD_PENALTY

        # Protein inflation detection
        if any("protein" in c for c in claims_lower):

            if protein_density < PROTEIN_DENSITY_THRESHOLD:

                alerts.add("PROTEIN_INFLATION")

                evidence.append({

                    "type": "PROTEIN_INFLATION",
                    "reason": "Protein claim unsupported by density metrics",

                })

                deception_score += PROTEIN_PENALTY

        # Fiber inflation detection
        if any("fiber" in c or "fibre" in c for c in claims_lower):

            if fiber_density < FIBER_DENSITY_THRESHOLD:

                alerts.add("FIBER_INFLATION")

                evidence.append({

                    "type": "FIBER_INFLATION",
                    "reason": "Fiber claim unsupported by density metrics",

                })

                deception_score += FIBER_PENALTY

        # Sugar-free and sweetener deception detection
        if any(
            "sugar free" in c
            or "no added sugar" in c
            or "zero sugar" in c
            for c in claims_lower
        ):

            if sugar > SUGAR_FREE_THRESHOLD:

                alerts.add("SUGAR_FREE_FRAUD")

                evidence.append({

                    "type": "SUGAR_FREE_FRAUD",
                    "reason": "Sugar detected despite sugar-free claim",

                })

                deception_score += SUGAR_FREE_FRAUD_PENALTY

            if sweeteners > 0:

                alerts.add("SWEETENER_DECEPTION")

                evidence.append({

                    "type": "SWEETENER_DECEPTION",
                    "reason": "Zero sugar claim masks artificial sweeteners",

                })

                deception_score += SWEETENER_DECEPTION_PENALTY

        # No palm oil fraud detection
        if any(
            "no palm oil" in c
            or "palm oil free" in c
            for c in claims_lower
        ):

            if contains_palm_oil:

                alerts.add("NO_PALM_OIL_FRAUD")

                evidence.append({

                    "type": "NO_PALM_OIL_FRAUD",
                    "reason": "Palm oil derivates detected",

                })

                deception_score += NO_PALM_OIL_FRAUD_PENALTY

        # Greenwashing detection
        if any(
            word in claim
            for claim in claims_lower
            for word in GREEN_WORDS
        ):

            if processing_level == PROCESSING_HEALTH_HALO_CHECK:

                alerts.add("GREENWASHING")

                evidence.append({

                    "type": "GREENWASHING",
                    "reason": "Environmental positioning on heavily processed product",

                })

                deception_score += GREENWASHING_PENALTY

        # Front-back contradiction detection
        contradictions = compliance.get(
            "claim_contradictions",
            [],
        )

        if len(contradictions) > 0:

            alerts.add("FRONT_BACK_CONTRADICTION")

            evidence.append({

                "type": "FRONT_BACK_CONTRADICTION",
                "contradictions": contradictions,

            })

            deception_score += FRONT_BACK_CONTRADICTION_PENALTY

        # Additive masking detection
        if len(e_numbers) >= ADDITIVE_HEAVY_THRESHOLD:

            alerts.add("ADDITIVE_HEAVY_PRODUCT")

            evidence.append({

                "type": "ADDITIVE_HEAVY_PRODUCT",
                "e_numbers": e_numbers,

            })

            deception_score += ADDITIVE_HEAVY_PENALTY

        # Hidden sugar marketing fraud detection
        if hidden_sugar_count > 0 and any(
            word in claim
            for claim in claims_lower
            for word in HEALTH_WORDS
        ):

            alerts.add("HIDDEN_SUGAR_MARKETING")

            evidence.append({

                "type": "HIDDEN_SUGAR_MARKETING",
                "hidden_sugars": hidden_sugar_count,

            })

            deception_score += HIDDEN_SUGAR_MARKETING_PENALTY

        # Ingredient splitting fraud detection
        sugar_sources = self._get_sugar_sources(
            ingredient_names,
        )

        if len(sugar_sources) >= INGREDIENT_SPLITTING_THRESHOLD:

            alerts.add("INGREDIENT_SPLITTING")

            evidence.append({

                "type": "INGREDIENT_SPLITTING",
                "sources": sugar_sources,

            })

            deception_score += INGREDIENT_SPLITTING_PENALTY

        # Child marketing risk detection
        if any(
            word in claim
            for claim in claims_lower
            for word in CHILD_MARKETING_WORDS
        ):

            if (
                sugar >= 10
                or sodium >= 400
                or sweeteners > 0
                or hyperactivity_risk == "HIGH"
            ):

                alerts.add("CHILD_MARKETING_RISK")

                evidence.append({

                    "type": "CHILD_MARKETING_RISK",
                    "reason": "Marketed to children despite problematic nutrition or additives",

                })

                deception_score += CHILD_MARKETING_RISK_PENALTY

        # Premiumization fraud detection
        if any(
            word in claim
            for claim in claims_lower
            for word in PREMIUM_WORDS
        ):

            if processing_level == PROCESSING_HEALTH_HALO_CHECK:

                alerts.add("PREMIUMIZATION_FRAUD")

                evidence.append({

                    "type": "PREMIUMIZATION_FRAUD",
                    "reason": "Premium claim used on ultra-processed product",

                })

                deception_score += PREMIUMIZATION_FRAUD_PENALTY

        # Cap deception score
        deception_score = self._normalize_score(
            deception_score,
            DECEPTION_SCORE_MAX,
            DECEPTION_SCORE_MIN,
        )

        # Calculate ingredient transparency score
        transparency_score = 100

        transparency_score -= (
            hidden_sugar_count * HIDDEN_SUGAR_COUNT_MULTIPLIER
        )

        transparency_score -= (
            additive_count * ADDITIVE_COUNT_MULTIPLIER
        )

        if total_ingredients > TRANSPARENCY_INGREDIENT_PENALTY_THRESHOLD:

            transparency_score -= TRANSPARENCY_INGREDIENT_PENALTY

        transparency_score = self._normalize_score(
            transparency_score,
        )

        # Calculate consumer manipulation index
        manipulation_index = 0

        if "HEALTH_HALO" in alerts:
            manipulation_index += 20
        if "UPF_HEALTH_HALO" in alerts:
            manipulation_index += 20
        if "HFSS_HEALTH_HALO" in alerts:
            manipulation_index += 20
        if "GREENWASHING" in alerts:
            manipulation_index += 20
        if "PREMIUMIZATION_FRAUD" in alerts:
            manipulation_index += 20
        if "CHILD_MARKETING_RISK" in alerts:
            manipulation_index += 20
        if "INGREDIENT_SPLITTING" in alerts:
            manipulation_index += 20

        manipulation_index = self._normalize_score(
            manipulation_index,
            MANIPULATION_INDEX_MAX,
        )

        # Calculate consumer harm score
        harm_score = 0

        if sugar >= HARM_SUGAR_THRESHOLD:
            harm_score += 15

        if sodium >= HARM_SODIUM_THRESHOLD:
            harm_score += 15

        harm_score += int(
            processing_penalty * HARM_PROCESSING_MULTIPLIER
        )

        harm_score += (
            hidden_sugar_count * HIDDEN_SUGAR_COUNT_MULTIPLIER
        )

        harm_score += sweeteners * 10

        harm_score += len(high_risk_additives) * 15

        harm_score = self._normalize_score(
            harm_score,
            HARM_SCORE_MAX,
        )

        # Calculate regulatory impact score
        regulatory_impact_score = self._normalize_score(

            len(compliance.get("violations", [])) * 20,
            SCORE_MAX,

        )

        # Calculate brand honesty and trust scores
        violations_penalty = len(critical_violations) * 10

        verification_penalty = (
            10
            if not compliance.get("verified", True)
            else 0
        )

        brand_honesty_score = self._normalize_score(

            100
            - deception_score
            - violations_penalty
            - verification_penalty,

        )

        trust_score = brand_honesty_score

        risk = self._get_risk_level(
            deception_score,
        )

        # Calculate confidence score
        confidence = CONFIDENCE_BASE

        if len(ingredient_names) >= 10:
            confidence += CONFIDENCE_INGREDIENT_BONUS

        if len(claims_lower) >= 1:
            confidence += CONFIDENCE_CLAIM_BONUS

        if nutrition:
            confidence += CONFIDENCE_NUTRITION_BONUS

        confidence = self._normalize_score(
            confidence,
        )

        # Build summary
        summary = {

            "total_alerts": len(alerts),
            "total_evidence": len(evidence),
            "has_deception": len(alerts) > 0,
            "high_risk": risk == "HIGH",

        }

        return {

            "deception_score": deception_score,
            "trust_score": trust_score,
            "brand_honesty_score": brand_honesty_score,
            "consumer_harm_score": harm_score,
            "regulatory_impact_score": regulatory_impact_score,
            "ingredient_transparency_score": transparency_score,
            "consumer_manipulation_index": manipulation_index,
            "analysis_confidence": confidence,
            "risk": risk,
            "alerts": sorted(list(alerts)),
            "evidence": evidence,
            "summary": summary,

        }


# ==========================================================
# SINGLETON INSTANCE
# ==========================================================


deception_engine = DeceptionEngine()


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [

    "DeceptionEngine",
    "deception_engine",

]


# ==========================================================
# END OF FILE – deception_engine.py
# ==========================================================