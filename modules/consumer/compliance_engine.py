# ==========================================================
# SCANIX AI
# SYSTEM 4 – CONSUMER INTELLIGENCE (COMPLIANCE ENGINE)
# ELITE PRODUCTION GRADE – FINAL VERSION
# ==========================================================


from __future__ import annotations


import json
import re
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple


# ==========================================================
# CONSTANTS
# ==========================================================


DEFAULT_SCORE = 100

PENALTY_CRITICAL = 25
PENALTY_HIGH = 15
PENALTY_MEDIUM = 10
PENALTY_LOW = 5

LABEL_SCORE_GOOD_THRESHOLD = 80
LABEL_SCORE_POOR_THRESHOLD = 60
LABEL_PENALTY_POOR = 15
LABEL_PENALTY_MODERATE = 5

REGULATORY_CONFIDENCE_BASE = 100
REGULATORY_CONFIDENCE_NO_CLAIMS = 10
REGULATORY_CONFIDENCE_NO_NUTRITION = 30
REGULATORY_CONFIDENCE_NO_INGREDIENTS = 20
REGULATORY_CONFIDENCE_NO_OCR = 15

HFSS_OVERALL_RED = "RED"
HFSS_YELLOW_COUNT_THRESHOLD = 2
HFSS_SCORE_PENALTY = 10

NOVA_4_PENALTY = 10

ALLERGEN_PENALTY = 10

HFSS_HEALTH_ALERT_SCORE_RED = 25
HFSS_HEALTH_ALERT_SCORE_YELLOW = 10

LABEL_FIELD_PENALTIES = {

    "fssai_license_number": 15,
    "ingredients_list": 15,
    "nutrition_information": 15,

}

DEFAULT_LABEL_PENALTY = 5


# ==========================================================
# COMPLIANCE ENGINE
# ==========================================================


class ComplianceEngine:
    """
    FSSAI Compliance Engine for System 4 – Consumer Intelligence.

    Validates:
    - Nutrient content claims (high protein, low sugar, etc.)
    - Health claims (prohibited/conditional)
    - Ingredient quality claims (natural, whole grain)
    - Additive regulations (colors, sweeteners, preservatives)
    - Allergen declarations
    - Label compliance (mandatory fields)
    - Special population warnings (children, diabetic, heart, pregnancy)
    - HFSS classification
    - NOVA classification
    """

    def __init__(self) -> None:
        """
        Initialize compliance engine with FSSAI knowledge base.
        """

        kb_path = (

            Path(__file__)
            .parent
            / "fssai_knowledge_base.json"

        )

        with open(

            kb_path,
            "r",
            encoding="utf-8",

        ) as f:

            self.kb = json.load(f)

    # =====================================================
    # NUTRIENT CONTENT CLAIMS VALIDATION
    # =====================================================

    def validate_nutrient_content_claims(
        self,
        claims: List[str],
        nutrition: Dict[str, Any],
        ingredients: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Validate nutrient content claims against actual nutrition data.

        Args:
            claims: List of marketing claims from product
            nutrition: Nutrition data (per 100g)
            ingredients: List of ingredient dictionaries

        Returns:
            List of violations with claim, severity, reason, and type
        """

        violations = []

        kb_ncc = self.kb.get(
            "nutrient_content_claims",
            {},
        )

        claims_lower = [
            c.lower()
            for c in claims
        ]

        ingredient_names = [

            str(item.get("name", "")).lower()

            for item in ingredients

        ]

        for nutrient_key, nutrient_data in kb_ncc.items():

            if not isinstance(nutrient_data, dict):

                continue

            for claim_key, claim_rules in nutrient_data.items():

                if not isinstance(claim_rules, dict):

                    continue

                if "aliases" not in claim_rules:

                    continue

                aliases = claim_rules.get("aliases", [])

                matched = False

                for alias in aliases:

                    if any(alias in c for c in claims_lower):

                        matched = True

                        break

                if not matched:

                    continue

                condition = claim_rules.get("condition", "")

                if condition == "per_100g":

                    target = claim_rules.get("nutrient", nutrient_key)

                    threshold = claim_rules.get("threshold", 0)

                    operator = claim_rules.get("operator", "<=")

                    actual = nutrition.get(target, 0)

                    is_violation = False

                    if operator == "<=" and actual > threshold:

                        is_violation = True

                    elif operator == ">=" and actual < threshold:

                        is_violation = True

                    if is_violation:

                        violations.append({

                            "claim": claim_rules.get("claim_name", ""),

                            "severity": claim_rules.get("severity", "HIGH"),

                            "reason": f"Actual {target} ({actual}) violates {operator} {threshold}",

                            "type": claim_rules.get("violation_class", "LABEL_DECEPTION"),

                        })

                elif condition == "ingredient_based":

                    if "sugar" in claim_key.lower():

                        sugar_aliases = claim_rules.get("sugar_aliases", [])

                        for item in ingredient_names:

                            if any(sa in item for sa in sugar_aliases):

                                violations.append({

                                    "claim": claim_rules.get("claim_name", ""),

                                    "severity": claim_rules.get("severity", "CRITICAL"),

                                    "reason": f"Found prohibited sugar alias: {item}",

                                    "type": claim_rules.get("violation_class", "LABEL_DECEPTION"),

                                })

        return violations

    # =====================================================
    # HEALTH CLAIMS VALIDATION
    # =====================================================

    def validate_health_claims(
        self,
        claims: List[str],
        nutrition: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Validate health claims against FSSAI regulations.

        Args:
            claims: List of marketing claims
            nutrition: Nutrition data (per 100g)

        Returns:
            List of violations
        """

        violations = []

        kb_health = self.kb.get(
            "health_claims",
            {},
        )

        claims_lower = [
            c.lower()
            for c in claims
        ]

        for h_claim, rules in kb_health.items():

            if not isinstance(rules, dict):

                continue

            if "aliases" not in rules:

                continue

            aliases = rules.get("aliases", [])

            matched = False

            for alias in aliases:

                if any(alias in c for c in claims_lower):

                    matched = True

                    break

            if not matched:

                continue

            condition = rules.get("condition", "")

            if condition == "PROHIBITED_CLAIM":

                violations.append({

                    "claim": rules.get("claim_name", ""),

                    "severity": rules.get("severity", "CRITICAL"),

                    "reason": rules.get("note", "Prohibited health claim"),

                    "type": rules.get("violation_class", "PROHIBITED_CLAIM_VIOLATION"),

                })

            elif "conditions" in rules:

                for cond in rules.get("conditions", []):

                    if "calcium" in cond.lower() and nutrition.get("calcium", 0) < 240:

                        violations.append({

                            "claim": rules.get("claim_name", ""),

                            "severity": rules.get("severity", "MEDIUM"),

                            "reason": "Insufficient calcium for claim",

                        })

        return violations

    # =====================================================
    # PROHIBITED CLAIMS DETECTION
    # =====================================================

    def detect_prohibited_claims(
        self,
        claims: List[str],
    ) -> List[Dict[str, Any]]:
        """
        Detect absolutely prohibited claims.

        Args:
            claims: List of marketing claims

        Returns:
            List of prohibited claim violations
        """

        violations = []

        kb_prohibited = (

            self.kb
            .get("prohibited_claims", {})
            .get("absolutely_prohibited", [])

        )

        claims_lower = [
            c.lower()
            for c in claims
        ]

        for p_claim in kb_prohibited:

            pattern = p_claim.get("claim_pattern", "")

            patterns = pattern.split("|")

            for pat in patterns:

                if any(pat in c for c in claims_lower):

                    violations.append({

                        "claim": pat,

                        "severity": p_claim.get("severity", "CRITICAL"),

                        "reason": "Prohibited medical or absolute claim",

                        "type": p_claim.get("violation_class", "PROHIBITED_CLAIM"),

                    })

        return violations

    # =====================================================
    # QUALITY CLAIMS VALIDATION
    # =====================================================

    def validate_quality_claims(
        self,
        claims: List[str],
        ingredients: List[Dict[str, Any]],
        additives: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Validate quality claims like natural, whole grain.

        Args:
            claims: List of marketing claims
            ingredients: List of ingredient dictionaries
            additives: Additive analysis data

        Returns:
            List of violations
        """

        violations = []

        kb_quality = self.kb.get(
            "ingredient_quality_claims",
            {},
        )

        claims_lower = [
            c.lower()
            for c in claims
        ]

        detected_e_numbers = additives.get(
            "e_numbers",
            [],
        )

        ingredient_names = [

            str(item.get("name", "")).lower()

            for item in ingredients

        ]

        # Natural claim validation
        natural_aliases = kb_quality.get("natural", {}).get("aliases", [])

        if any(a in c for c in claims_lower for a in natural_aliases):

            prohibited = kb_quality.get("natural", {}).get("prohibited_additive_codes", [])

            for e_num in detected_e_numbers:

                if e_num in prohibited:

                    violations.append({

                        "claim": "Natural",

                        "severity": kb_quality.get("natural", {}).get("severity", "HIGH"),

                        "reason": f"Contradicted by {e_num}",

                    })

        # Whole grain claim validation
        whole_grain_aliases = kb_quality.get("whole_grain", {}).get("aliases", [])

        if any(a in c for c in claims_lower for a in whole_grain_aliases):

            disqualifying = kb_quality.get("whole_grain", {}).get("disqualifying_primary_ingredient", [])

            if len(ingredient_names) > 0:

                primary = ingredient_names[0]

                if any(dq in primary for dq in disqualifying):

                    violations.append({

                        "claim": "Whole Grain",

                        "severity": kb_quality.get("whole_grain", {}).get("severity", "HIGH"),

                        "reason": f"Primary ingredient is refined: {primary}",

                    })

        return violations

    # =====================================================
    # ADDITIVE REGULATIONS ANALYSIS
    # =====================================================

    def analyze_additive_regulations(
        self,
        additives: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Analyze additives against FSSAI regulations.

        Args:
            additives: Additive analysis data (e_numbers, etc.)

        Returns:
            Additive regulation analysis with risk score, warnings, alerts
        """

        detected_e_numbers = additives.get(
            "e_numbers",
            [],
        )

        kb_additives = self.kb.get(
            "additive_regulations",
            {},
        )

        restricted = []

        child_risk = []

        pregnancy_risk = []

        warnings = []

        alerts = []

        risk_score = 0

        # Check artificial colours
        colors = kb_additives.get("artificial_colours", {}).get("prohibited_colours", [])

        for col in colors:

            ins_code = col.get("ins_code", "")

            if ins_code in detected_e_numbers:

                restricted.append(ins_code)

                child_risk.append(ins_code)

                warnings.append(col.get("eu_mandatory_warning", "Colour risk"))

                risk_score += 25

                alerts.append({

                    "type": "RED",

                    "title": "Artificial Colour Risk",

                    "message": f"Contains {col.get('name')} ({ins_code}), which {col.get('risk', 'poses health risk')}",

                })

        # Check sweeteners
        sweeteners = kb_additives.get("sweeteners", {}).get("artificial_sweeteners", [])

        for sw in sweeteners:

            ins_code = sw.get("ins_code", "")

            if ins_code in detected_e_numbers:

                severity = sw.get("severity", "LOW")

                if severity == "MODERATE":

                    pregnancy_risk.append(ins_code)

                    risk_score += 15

                if sw.get("mandatory_warning"):

                    warnings.append(sw.get("mandatory_warning"))

                alert_type = "YELLOW" if severity == "LOW" else "RED"

                alerts.append({

                    "type": alert_type,

                    "title": "Artificial Sweetener",

                    "message": f"Contains {sw.get('name')}. {sw.get('risk', '')}",

                })

        # Check preservatives
        preservatives = kb_additives.get("preservatives", {}).get("regulated_preservatives", [])

        for pr in preservatives:

            ins_code = pr.get("ins_code", "")

            if ins_code in detected_e_numbers:

                risk_score += 10

                alerts.append({

                    "type": "YELLOW",

                    "title": "Regulated Preservative",

                    "message": f"Contains {pr.get('name')}. {pr.get('risk', 'Within limits')}",

                })

        return {

            "risk_score": risk_score,

            "restricted": restricted,

            "child_risk": child_risk,

            "pregnancy_risk": pregnancy_risk,

            "warnings": warnings,

            "alerts": alerts,

        }

    # =====================================================
    # ALLERGEN ANALYSIS
    # =====================================================

    def analyze_allergens(
        self,
        ingredients: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Analyze allergens in ingredients.

        Args:
            ingredients: List of ingredient dictionaries

        Returns:
            Allergen analysis with detected allergens, high risk, alerts
        """

        detected = []

        high_risk = []

        alerts = []

        kb_allergens = (

            self.kb
            .get("allergen_declarations", {})
            .get("mandatory_allergens", {})
            .get("allergens", [])

        )

        ingredient_names = [

            str(item.get("name", "")).lower()

            for item in ingredients

        ]

        for item in ingredient_names:

            for allergen in kb_allergens:

                name = allergen.get("name", "")

                sources = allergen.get("sources", [])

                if any(s.lower() in item for s in sources):

                    if name not in detected:

                        detected.append(name)

                        high_risk.append(name)

                        alerts.append({

                            "type": "RED",

                            "title": f"Allergen: {name}",

                            "message": allergen.get("declaration", f"Contains {name}"),

                        })

        return {

            "detected": detected,

            "high_risk": high_risk,

            "alerts": alerts,

        }

    # =====================================================
    # LABEL COMPLIANCE ANALYSIS
    # =====================================================

    def analyze_label_compliance(
        self,
        ocr_text: str,
    ) -> Dict[str, Any]:
        """
        Analyze label for mandatory declarations.

        Args:
            ocr_text: Extracted OCR text from label

        Returns:
            Label compliance analysis with score and missing fields
        """

        missing = []

        label_score = DEFAULT_SCORE

        kb_mandatory = (

            self.kb
            .get("mandatory_label_declarations", {})
            .get("required_on_all_labels", [])

        )

        text_lower = ocr_text.lower()

        for req in kb_mandatory:

            field = req.get("field", "")

            aliases = req.get("aliases", [])

            if not aliases:

                if field == "fssai_license_number":
                    aliases = ["fssai", "lic", "license"]
                elif field == "net_quantity":
                    aliases = ["net quantity", "net weight", "net volume", "net wt", "net vol"]
                elif field == "date_marking":
                    aliases = ["best before", "expiry", "use by", "mfg", "pkd"]
                else:
                    aliases = [field.replace("_", " ")]

            found = False

            for alias in aliases:

                if alias in text_lower:

                    found = True

                    break

            if not found:

                missing.append(field)

                penalty = LABEL_FIELD_PENALTIES.get(field, DEFAULT_LABEL_PENALTY)

                label_score -= penalty

        label_score = max(
            0,
            label_score,
        )

        return {

            "label_score": label_score,

            "missing": missing,

        }

    # =====================================================
    # SPECIAL POPULATIONS ANALYSIS
    # =====================================================

    def analyze_special_populations(
        self,
        nutrition: Dict[str, Any],
        ingredients: List[Dict[str, Any]],
        additive_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Analyze product suitability for special populations.

        Args:
            nutrition: Nutrition data (per 100g)
            ingredients: List of ingredient dictionaries
            additive_analysis: Additive regulation analysis

        Returns:
            Alerts for children, diabetic, heart patients, pregnancy
        """

        kb_special = self.kb.get(
            "special_dietary_populations",
            {},
        )

        sugar = nutrition.get("sugar", 0)

        sodium = nutrition.get("sodium", 0)

        fat = nutrition.get("fat", 0)

        sat_fat = nutrition.get("saturated_fat", 0)

        trans_fat = nutrition.get("trans_fat", 0)

        caffeine = nutrition.get("caffeine", 0)

        ingredient_names = [

            str(item.get("name", "")).lower()

            for item in ingredients

        ]

        alerts_children = []
        alerts_diabetic = []
        alerts_heart = []
        alerts_pregnancy = []

        # Children analysis
        child_rules = kb_special.get("children_under_12", {})

        if sugar > child_rules.get("max_sugar_g_per100g", 10):

            alerts_children.append({

                "type": "RED",
                "title": "High Sugar",
                "message": "Exceeds recommended sugar threshold for children.",

            })

        if sodium > child_rules.get("max_sodium_mg_per100g", 600):

            alerts_children.append({

                "type": "RED",
                "title": "High Sodium",
                "message": "Exceeds recommended sodium threshold for children.",

            })

        for cr in additive_analysis.get("child_risk", []):

            alerts_children.append({

                "type": "RED",
                "title": "Restricted Additive",
                "message": f"Contains {cr}, restricted for children.",

            })

        # Diabetic analysis
        diabetic_rules = kb_special.get("diabetics", {})

        if sugar > diabetic_rules.get("safe_sugar_threshold_g_per100g", 5):

            alerts_diabetic.append({

                "type": "RED",
                "title": "High Sugar",
                "message": "Not recommended for diabetic profiles.",

            })

        # Heart patients analysis
        heart_rules = kb_special.get("heart_patients", {})

        if sodium > heart_rules.get("max_sodium_mg_per100g", 200):

            alerts_heart.append({

                "type": "RED",
                "title": "High Sodium",
                "message": "Exceeds cardiac sodium thresholds.",

            })

        if sat_fat > heart_rules.get("max_saturated_fat_g_per100g", 1.5):

            alerts_heart.append({

                "type": "RED",
                "title": "High Saturated Fat",
                "message": "Exceeds cardiac saturated fat thresholds.",

            })

        if trans_fat > 0:

            alerts_heart.append({

                "type": "RED",
                "title": "Trans Fat Detected",
                "message": "Contains trans fat which increases cardiovascular risk.",

            })

        # Pregnancy analysis
        preg_rules = kb_special.get("pregnant_women", {})

        caffeine_limit = preg_rules.get("caffeine_max_mg_per_day", 200)

        if caffeine > caffeine_limit:

            alerts_pregnancy.append({

                "type": "RED",
                "title": "High Caffeine",
                "message": f"Contains {caffeine}mg caffeine. High levels are restricted during pregnancy.",

            })

        avoid_list = preg_rules.get("avoid", [])

        for item in ingredient_names:

            for avoid_ing in avoid_list:

                if avoid_ing.lower() in item:

                    alerts_pregnancy.append({

                        "type": "RED",
                        "title": "Restricted Ingredient",
                        "message": f"Contains {avoid_ing}, which is not recommended during pregnancy.",

                    })

        for pr in additive_analysis.get("pregnancy_risk", []):

            alerts_pregnancy.append({

                "type": "RED",
                "title": "Additives to Avoid",
                "message": f"Contains {pr}, not recommended during pregnancy.",

            })

        return {

            "children": alerts_children,

            "pregnancy": alerts_pregnancy,

            "diabetic": alerts_diabetic,

            "heart_patient": alerts_heart,

        }

    # =====================================================
    # MARKETING PRACTICES ANALYSIS
    # =====================================================

    def analyze_marketing_practices(
        self,
        claims: List[str],
        ingredients: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Detect misleading marketing practices.

        Args:
            claims: List of marketing claims
            ingredients: List of ingredient dictionaries

        Returns:
            List of marketing practice violations
        """

        kb_marketing = (

            self.kb
            .get("prohibited_claims", {})
            .get("misleading_marketing_practices", [])

        )

        violations = []

        claims_lower = [
            c.lower()
            for c in claims
        ]

        ingredient_names = [

            str(item.get("name", "")).lower()

            for item in ingredients

        ]

        # Count sugar ingredients
        sugar_count = 0

        for ing in ingredient_names:

            if any(s in ing for s in ["sugar", "syrup", "dextrose", "fructose"]):

                sugar_count += 1

        # Detect greenwashing
        green_patterns = [

            r"\beco\b",
            r"\bgreen\b",
            r"\bearth\b",
            r"\bplanet\b",
            r"\bsustainable\b",
            r"carbon neutral",
            r"net zero",

        ]

        is_greenwashing = False

        for c in claims_lower:

            if any(re.search(pat, c) for pat in green_patterns):

                is_greenwashing = True

                break

        for rule in kb_marketing:

            practice = rule.get("practice", "")

            if practice == "ingredient_order_manipulation":

                if sugar_count >= 3:

                    violations.append({

                        "claim": "Multiple Sugars",

                        "severity": rule.get("severity", "HIGH"),

                        "reason": rule.get("description", "Ingredient splitting"),

                        "type": rule.get("violation_class", "DECEPTIVE_PRACTICE"),

                    })

            elif practice == "green_washing":

                if is_greenwashing:

                    violations.append({

                        "claim": "Eco/Sustainable",

                        "severity": rule.get("severity", "MEDIUM"),

                        "reason": rule.get("description", "Potential greenwashing"),

                        "type": rule.get("violation_class", "MISLEADING_CLAIM"),

                    })

        return violations

    # =====================================================
    # FOOD CATEGORY ANALYSIS
    # =====================================================

    def analyze_food_categories(
        self,
        product_category: str,
        claims: List[str],
        nutrition: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Analyze product against category-specific rules.

        Args:
            product_category: Product category string
            claims: List of marketing claims
            nutrition: Nutrition data (per 100g)

        Returns:
            List of category-specific violations
        """

        violations = []

        if not product_category:

            return violations

        kb_cats = self.kb.get(
            "food_category_specific_rules",
            {},
        )

        cat_key = product_category.lower().replace(" ", "_")

        cat_rules = kb_cats.get(cat_key, {})

        if not cat_rules:

            return violations

        claims_lower = [
            c.lower()
            for c in claims
        ]

        prohibited = cat_rules.get("prohibited_claims", [])

        for pc in prohibited:

            if any(pc.lower() in c for c in claims_lower):

                violations.append({

                    "claim": pc,
                    "severity": "CRITICAL",
                    "reason": f"Prohibited claim for category {product_category}",
                    "type": "PROHIBITED_CLAIM_VIOLATION",

                })

        return violations

    # =====================================================
    # TRAFFIC LIGHTS CALCULATION
    # =====================================================

    def calculate_traffic_lights(
        self,
        nutrition: Dict[str, Any],
    ) -> Dict[str, str]:
        """
        Calculate front-of-pack traffic light labels.

        Args:
            nutrition: Nutrition data (per 100g)

        Returns:
            Traffic light colors for sugar, sodium, fat, overall
        """

        kb_hfss = (

            self.kb
            .get("front_of_pack_labelling", {})
            .get("high_fat_salt_sugar", {})

        )

        sugar_limit = kb_hfss.get("high_sugar_threshold_per100g", 10)

        sodium_limit = kb_hfss.get("high_salt_threshold_per100g_sodium_mg", 600)

        fat_limit = kb_hfss.get("high_fat_threshold_per100g", 20)

        sugar = nutrition.get("sugar", 0)

        sodium = nutrition.get("sodium", 0)

        fat = nutrition.get("fat", 0)

        def get_light(value: float, limit: float) -> str:
            if value >= limit:
                return "RED"
            if value >= (limit / 2):
                return "YELLOW"
            return "GREEN"

        sugar_light = get_light(sugar, sugar_limit)
        sodium_light = get_light(sodium, sodium_limit)
        fat_light = get_light(fat, fat_limit)

        overall = "GREEN"

        if sugar_light == "RED" or sodium_light == "RED" or fat_light == "RED":
            overall = "RED"
        elif sugar_light == "YELLOW" or sodium_light == "YELLOW" or fat_light == "YELLOW":
            overall = "YELLOW"

        return {

            "sugar": sugar_light,
            "sodium": sodium_light,
            "fat": fat_light,
            "overall": overall,

        }

    # =====================================================
    # MASTER ANALYSIS
    # =====================================================

    def analyze(
        self,
        claims: List[str],
        nutrition: Dict[str, Any],
        ingredient_intelligence: Dict[str, Any],
        ocr_text: str = "",
        product_category: str = "",
    ) -> Dict[str, Any]:
        """
        Master compliance analysis method.

        Args:
            claims: List of marketing claims
            nutrition: Nutrition data (per 100g)
            ingredient_intelligence: Ingredient analysis from System 2
            ocr_text: Extracted OCR text from label
            product_category: Product category string

        Returns:
            Complete compliance analysis
        """

        violations = []
        warnings = []
        regulatory_insights = []

        score = DEFAULT_SCORE
        violation_score = 0
        health_alert_score = 0

        ingredients = ingredient_intelligence.get(
            "ingredients",
            [],
        )

        additives = ingredient_intelligence.get(
            "additives",
            {},
        )

        nutrition = nutrition or {}

        # Run all validations
        nutrient_claim_violations = self.validate_nutrient_content_claims(
            claims,
            nutrition,
            ingredients,
        )

        health_claim_violations = self.validate_health_claims(
            claims,
            nutrition,
        )

        prohibited_claim_violations = self.detect_prohibited_claims(
            claims,
        )

        quality_claim_violations = self.validate_quality_claims(
            claims,
            ingredients,
            additives,
        )

        marketing_practice_violations = self.analyze_marketing_practices(
            claims,
            ingredients,
        )

        category_violations = self.analyze_food_categories(
            product_category,
            claims,
            nutrition,
        )

        additive_analysis = self.analyze_additive_regulations(
            additives,
        )

        allergen_analysis = self.analyze_allergens(
            ingredients,
        )

        label_compliance = self.analyze_label_compliance(
            ocr_text,
        )

        population_alerts = self.analyze_special_populations(
            nutrition,
            ingredients,
            additive_analysis,
        )

        traffic_lights = self.calculate_traffic_lights(
            nutrition,
        )

        # Aggregate all violations
        all_violation_lists = [
            nutrient_claim_violations,
            health_claim_violations,
            prohibited_claim_violations,
            quality_claim_violations,
            marketing_practice_violations,
            category_violations,
        ]

        for v_list in all_violation_lists:

            for v in v_list:

                violations.append(v)

                sev = v.get("severity", "LOW")

                if sev == "CRITICAL":
                    penalty = PENALTY_CRITICAL
                elif sev == "HIGH":
                    penalty = PENALTY_HIGH
                elif sev == "MEDIUM":
                    penalty = PENALTY_MEDIUM
                else:
                    penalty = PENALTY_LOW

                violation_score += penalty

                score -= penalty

        # Label compliance impact
        label_score = label_compliance.get("label_score", DEFAULT_SCORE)

        if label_score < LABEL_SCORE_POOR_THRESHOLD:

            score -= LABEL_PENALTY_POOR

        elif label_score < LABEL_SCORE_GOOD_THRESHOLD:

            score -= LABEL_PENALTY_MODERATE

        # Additive and allergen impact
        score -= additive_analysis.get("risk_score", 0)

        violation_score += additive_analysis.get("risk_score", 0)

        for w in additive_analysis.get("warnings", []):

            warnings.append(w)

        if len(allergen_analysis.get("detected", [])) > 0:

            warnings.append("CONTAINS_ALLERGENS")

            score -= ALLERGEN_PENALTY

        # HFSS classification
        processing_level = (

            ingredient_intelligence
            .get("processing_analysis", {})
            .get("processing_level", "")

        )

        yellow_count = list(traffic_lights.values()).count("YELLOW")

        hfss_classified = (
            traffic_lights.get("overall") == HFSS_OVERALL_RED
            or (yellow_count >= HFSS_YELLOW_COUNT_THRESHOLD and processing_level in ["ULTRA_PROCESSED", "NOVA_4"])
        )

        hfss = {

            "classified": hfss_classified,
            "reasons": [k for k, v in traffic_lights.items() if v == "RED" and k != "overall"],

        }

        if hfss_classified:

            warnings.append("HFSS_PRODUCT")

            score -= HFSS_SCORE_PENALTY

        # NOVA classification
        nova_classification = processing_level

        if processing_level == "ULTRA_PROCESSED" or processing_level == "NOVA_4":

            nova_classification = "NOVA_4"

            warnings.append("ULTRA_PROCESSED")

            score -= NOVA_4_PENALTY

        # Build health alerts
        health_alerts = {

            "children": population_alerts.get("children", []),

            "pregnancy": population_alerts.get("pregnancy", []),

            "diabetic": population_alerts.get("diabetic", []),

            "heart_patient": population_alerts.get("heart_patient", []),

            "allergen_alerts": allergen_analysis.get("alerts", []),

            "additive_alerts": additive_analysis.get("alerts", []),

        }

        for category, alerts in health_alerts.items():

            for alert in alerts:

                a_type = alert.get("type", "")

                if a_type == "RED":

                    health_alert_score += HFSS_HEALTH_ALERT_SCORE_RED

                elif a_type == "YELLOW":

                    health_alert_score += HFSS_HEALTH_ALERT_SCORE_YELLOW

        # Generate regulatory insights
        if hfss_classified:

            regulatory_insights.append(
                "Product qualifies as HFSS. A FOPL warning label may be required under draft regulations."
            )

        if len(allergen_analysis.get("detected", [])) > 0:

            regulatory_insights.append(
                f"Ensure allergens are declared in bold. Detected: {', '.join(allergen_analysis.get('detected'))}."
            )

        if additive_analysis.get("risk_score", 0) > 0:

            regulatory_insights.append(
                "Contains restricted or high-risk additives. Verify usage levels strictly against Schedule I."
            )

        # Calculate regulatory confidence
        regulatory_confidence = REGULATORY_CONFIDENCE_BASE

        if not claims:
            regulatory_confidence -= REGULATORY_CONFIDENCE_NO_CLAIMS

        if not nutrition:
            regulatory_confidence -= REGULATORY_CONFIDENCE_NO_NUTRITION

        if not ingredients:
            regulatory_confidence -= REGULATORY_CONFIDENCE_NO_INGREDIENTS

        if not ocr_text:
            regulatory_confidence -= REGULATORY_CONFIDENCE_NO_OCR

        regulatory_confidence = max(0, regulatory_confidence)

        # Normalize score
        score = max(0, min(DEFAULT_SCORE, score))

        # Count critical violations
        critical_count = len([v for v in violations if v.get("severity") == "CRITICAL"])

        compliant = critical_count == 0 and score >= 70

        consumer_safety_index = round((score + regulatory_confidence) / 2)

        # Deduplicate warnings and insights
        warnings = sorted(list(set(warnings)))

        regulatory_insights = sorted(list(set(regulatory_insights)))

        # Build summary
        summary = {

            "compliant": compliant,
            "fssai_score": score,
            "consumer_safety_index": consumer_safety_index,
            "violation_score": violation_score,
            "health_alert_score": health_alert_score,
            "critical_violations": critical_count,
            "warning_count": len(warnings),
            "hfss": hfss_classified,
            "nova": nova_classification,

        }

        return {

            "fssai_score": score,

            "compliance_score": score,

            "compliant": compliant,

            "consumer_safety_index": consumer_safety_index,

            "violation_score": violation_score,

            "regulatory_confidence": regulatory_confidence,

            "violations": violations,

            "warnings": warnings,

            "health_claim_violations": health_claim_violations,

            "prohibited_claim_violations": prohibited_claim_violations,

            "quality_claim_violations": quality_claim_violations,

            "marketing_practice_violations": marketing_practice_violations,

            "allergen_analysis": allergen_analysis,

            "additive_analysis": additive_analysis,

            "label_compliance": label_compliance,

            "health_alerts": health_alerts,

            "traffic_lights": traffic_lights,

            "hfss": hfss,

            "nova_classification": nova_classification,

            "regulatory_insights": regulatory_insights,

            "summary": summary,

        }


# ==========================================================
# SINGLETON INSTANCE
# ==========================================================


compliance_engine = ComplianceEngine()


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [

    "ComplianceEngine",
    "compliance_engine",

]


# ==========================================================
# END OF FILE – compliance_engine.py
# ==========================================================