# ==========================================================
# SCANIX AI
# SYSTEM 2 – INGREDIENT VERIFIER
# ELITE PRODUCTION GRADE – FINAL VERSION
# ==========================================================


from __future__ import annotations


import logging
from typing import Any
from typing import Dict
from typing import List
from typing import Set
from typing import Tuple


log = logging.getLogger(__name__)


# ==========================================================
# CLAIMS REGISTRY
# ==========================================================


CLAIMS_REGISTRY = {

    "vegan": {
        "title": "Vegan",
        "icon": "🌱",
    },

    "vegetarian": {
        "title": "Vegetarian",
        "icon": "🥗",
    },

    "dairy_free": {
        "title": "Dairy Free",
        "icon": "🥛",
    },

    "gluten_free": {
        "title": "Gluten Free",
        "icon": "🌾",
    },

    "no_added_sugar": {
        "title": "No Added Sugar",
        "icon": "🍬",
    },

    "no_palm_oil": {
        "title": "No Palm Oil",
        "icon": "🌴",
    },

    "no_msg": {
        "title": "No MSG",
        "icon": "🧂",
    },

    "no_artificial_additives": {
        "title": "No Artificial Additives",
        "icon": "🧪",
    },

    "no_preservatives": {
        "title": "No Preservatives",
        "icon": "🛡️",
    },

    "no_artificial_colors": {
        "title": "No Artificial Colors",
        "icon": "🎨",
    },

    "no_soy": {
        "title": "No Soy",
        "icon": "🫘",
    },

    "no_nuts": {
        "title": "No Nuts",
        "icon": "🥜",
    },

}


# ==========================================================
# DAIRY KEYWORDS
# ==========================================================


DAIRY_KEYWORDS = {

    "milk",
    "whey",
    "butter",
    "cheese",
    "casein",
    "lactose",
    "cream",
    "ghee",
    "paneer",
    "curd",
    "yogurt",
    "buttermilk",
    "milk solids",
    "skim milk",
    "whole milk",

}


# ==========================================================
# GLUTEN KEYWORDS
# ==========================================================


GLUTEN_KEYWORDS = {

    "wheat",
    "barley",
    "rye",
    "gluten",
    "spelt",
    "semolina",
    "durum",
    "farina",
    "farro",
    "graham",
    "kamut",
    "triticale",
    "malt",
    "brewers yeast",

}


# ==========================================================
# SOY KEYWORDS
# ==========================================================


SOY_KEYWORDS = {

    "soy",
    "soya",
    "soybean",
    "soy protein",
    "soy lecithin",
    "soya lecithin",
    "tofu",
    "edamame",
    "tempeh",
    "miso",
    "natto",
    "soy flour",

}


# ==========================================================
# NUT KEYWORDS
# ==========================================================


NUT_KEYWORDS = {

    "almond",
    "cashew",
    "walnut",
    "hazelnut",
    "pistachio",
    "pecan",
    "peanut",
    "macadamia",
    "brazil nut",
    "chestnut",
    "pine nut",
    "beechnut",
    "ginkgo nut",

}


# ==========================================================
# NON-VEGAN KEYWORDS
# ==========================================================


NON_VEGAN_KEYWORDS = {

    "gelatin",
    "honey",
    "collagen",
    "fish oil",
    "egg",
    "egg white",
    "egg yolk",
    "egg powder",
    "albumin",
    "milk",
    "milk solids",
    "cheese",
    "cheese powder",
    "whey",
    "casein",
    "lactose",
    "butter",
    "cream",
    "ghee",
    "paneer",
    "curd",
    "yogurt",

}


# ==========================================================
# MSG KEYWORDS
# ==========================================================


MSG_KEYWORDS = {

    "msg",
    "monosodium glutamate",
    "e621",
    "monosodium l-glutamate",
    "sodium glutamate",

}


# ==========================================================
# MARKETING CLAIMS
# ==========================================================


MARKETING_CLAIMS = {

    "natural",
    "healthy",
    "clean",
    "pure",
    "organic",
    "wholesome",
    "real",
    "authentic",
    "traditional",
    "homemade",

}


# ==========================================================
# MEAT KEYWORDS (For Vegetarian Check)
# ==========================================================


MEAT_KEYWORDS = {

    "chicken",
    "fish",
    "beef",
    "mutton",
    "pork",
    "seafood",
    "lamb",
    "turkey",
    "duck",
    "goat",
    "veal",
    "bacon",
    "ham",
    "sausage",
    "meat",
    "broth",
    "stock",

}


# ==========================================================
# INGREDIENT VERIFIER
# ==========================================================


class IngredientVerifier:

    """
    Comprehensive ingredient verifier for food products.

    Verifies claims like:
    - Vegan, Vegetarian
    - Dairy Free, Gluten Free
    - No Added Sugar, No MSG, No Palm Oil
    - No Artificial Additives, No Preservatives, No Artificial Colors
    - No Soy, No Nuts
    """

    # Class-level OCR corrections for common misreads
    OCR_FOOD_CORRECTIONS = {

        "weeat": "wheat",
        "wteat": "wheat",
        "wte": "wheat",
        "gtejen": "gluten",
        "gtjen": "gluten",
        "glutem": "gluten",
        "gluteen": "gluten",
        "wheal": "wheat",
        "sooy": "soy",
        "soyaa": "soya",
        "soyabean": "soybean",
        "soyabena": "soybean",
        "soyabeen": "soybean",
        "casein": "casein",
        "lactos": "lactose",
        "lactse": "lactose",
        "monosodiurn": "monosodium",
        "monosodlum": "monosodium",
        "glutamat": "glutamate",
        "glutamte": "glutamate",

    }


    def __init__(
        self,
    ) -> None:

        pass


    @staticmethod
    def normalize(
        text: str,
    ) -> str:
        """
        Normalize text by lowercasing and stripping whitespace.

        Args:
            text: Input text to normalize

        Returns:
            Normalized text string
        """

        return (
            text
            .lower()
            .strip()
        )


    @staticmethod
    def contains_keyword(
        ingredients: List[str],
        keywords: Set[str],
    ) -> List[str]:
        """
        Check which keywords are present in the ingredient list.

        Args:
            ingredients: List of ingredient names
            keywords: Set of keywords to search for

        Returns:
            List of found keywords (unique, sorted)
        """

        found = []

        for ingredient in ingredients:

            normalized = ingredient.lower()

            # Apply OCR corrections
            for wrong, correct in IngredientVerifier.OCR_FOOD_CORRECTIONS.items():

                normalized = normalized.replace(
                    wrong,
                    correct,
                )

            for keyword in keywords:

                if keyword in normalized:

                    found.append(keyword)

        return sorted(
            list(
                set(found)
            )
        )


    def build_result(
        self,
        claim: str,
        passed: bool,
        found: List[str],
        reason: str,
    ) -> Dict[str, Any]:
        """
        Build a standardized verification result.

        Args:
            claim: Name of the claim being verified
            passed: Whether the verification passed
            found: List of conflicting ingredients found
            reason: Human-readable reason

        Returns:
            Standardized verification result dictionary
        """

        confidence = (
            90
            if passed
            else min(
                60 + (len(found) * 10),
                99,
            )
        )

        return {

            "claim": claim,

            "verdict": "PASS" if passed else "FAIL",

            "confidence": confidence,

            "found": found,

            "reason": reason,

        }


    def insufficient_data_result(
        self,
        claim: str,
    ) -> Dict[str, Any]:
        """
        Return result when there is insufficient ingredient data.

        Args:
            claim: Name of the claim being verified

        Returns:
            Result indicating insufficient data
        """

        return {

            "claim": claim,

            "verdict": "UNKNOWN",

            "confidence": 0,

            "found": [],

            "reason": "Insufficient ingredient data to verify claim.",

        }


    # ==========================================================
    # VERIFICATION METHODS
    # ==========================================================

    def verify_vegan(
        self,
        ingredients: List[str],
    ) -> Dict[str, Any]:
        """
        Verify if product is vegan (no animal-derived ingredients).

        Checks for:
        - Gelatin, honey, collagen, fish oil, eggs, dairy

        Args:
            ingredients: List of ingredient names

        Returns:
            Verification result dictionary
        """

        found = self.contains_keyword(
            ingredients,
            NON_VEGAN_KEYWORDS,
        )

        return self.build_result(
            claim=CLAIMS_REGISTRY["vegan"]["title"],
            passed=len(found) == 0,
            found=found,
            reason=(
                "No non-vegan ingredients detected."
                if not found
                else "Animal-derived ingredients detected."
            ),
        )


    def verify_vegetarian(
        self,
        ingredients: List[str],
    ) -> Dict[str, Any]:
        """
        Verify if product is vegetarian (no meat/fish).

        Checks for:
        - Chicken, fish, beef, mutton, pork, seafood

        Args:
            ingredients: List of ingredient names

        Returns:
            Verification result dictionary
        """

        found = self.contains_keyword(
            ingredients,
            MEAT_KEYWORDS,
        )

        return self.build_result(
            claim=CLAIMS_REGISTRY["vegetarian"]["title"],
            passed=len(found) == 0,
            found=found,
            reason=(
                "No meat ingredients detected."
                if not found
                else "Non-vegetarian ingredients detected."
            ),
        )


    def verify_dairy_free(
        self,
        ingredients: List[str],
    ) -> Dict[str, Any]:
        """
        Verify if product is dairy free.

        Checks for:
        - Milk, whey, butter, cheese, casein, lactose, cream, ghee, paneer, curd

        Args:
            ingredients: List of ingredient names

        Returns:
            Verification result dictionary
        """

        found = self.contains_keyword(
            ingredients,
            DAIRY_KEYWORDS,
        )

        return self.build_result(
            claim=CLAIMS_REGISTRY["dairy_free"]["title"],
            passed=len(found) == 0,
            found=found,
            reason=(
                "No dairy ingredients found."
                if not found
                else "Dairy ingredients detected."
            ),
        )


    def verify_gluten_free(
        self,
        ingredients: List[str],
    ) -> Dict[str, Any]:
        """
        Verify if product is gluten free.

        Checks for:
        - Wheat, barley, rye, gluten, spelt, semolina

        Args:
            ingredients: List of ingredient names

        Returns:
            Verification result dictionary
        """

        found = self.contains_keyword(
            ingredients,
            GLUTEN_KEYWORDS,
        )

        return self.build_result(
            claim=CLAIMS_REGISTRY["gluten_free"]["title"],
            passed=len(found) == 0,
            found=found,
            reason=(
                "No gluten ingredients found."
                if not found
                else "Gluten-containing ingredients detected."
            ),
        )


    def verify_no_soy(
        self,
        ingredients: List[str],
    ) -> Dict[str, Any]:
        """
        Verify if product contains no soy.

        Checks for:
        - Soy, soya, soybean, soy protein, soy lecithin

        Args:
            ingredients: List of ingredient names

        Returns:
            Verification result dictionary
        """

        found = self.contains_keyword(
            ingredients,
            SOY_KEYWORDS,
        )

        return self.build_result(
            claim=CLAIMS_REGISTRY["no_soy"]["title"],
            passed=len(found) == 0,
            found=found,
            reason=(
                "No soy ingredients found."
                if not found
                else "Soy ingredients detected."
            ),
        )


    def verify_no_nuts(
        self,
        ingredients: List[str],
    ) -> Dict[str, Any]:
        """
        Verify if product contains no nuts.

        Checks for:
        - Almond, cashew, walnut, hazelnut, pistachio, pecan, peanut, macadamia

        Args:
            ingredients: List of ingredient names

        Returns:
            Verification result dictionary
        """

        found = self.contains_keyword(
            ingredients,
            NUT_KEYWORDS,
        )

        return self.build_result(
            claim=CLAIMS_REGISTRY["no_nuts"]["title"],
            passed=len(found) == 0,
            found=found,
            reason=(
                "No nut ingredients found."
                if not found
                else "Nut ingredients detected."
            ),
        )


    def verify_no_msg(
        self,
        ingredients: List[str],
    ) -> Dict[str, Any]:
        """
        Verify if product contains no MSG.

        Checks for:
        - MSG, monosodium glutamate, E621

        Args:
            ingredients: List of ingredient names

        Returns:
            Verification result dictionary
        """

        found = self.contains_keyword(
            ingredients,
            MSG_KEYWORDS,
        )

        return self.build_result(
            claim=CLAIMS_REGISTRY["no_msg"]["title"],
            passed=len(found) == 0,
            found=found,
            reason=(
                "No MSG detected."
                if not found
                else "MSG detected."
            ),
        )


    def verify_no_palm_oil(
        self,
        additive_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Verify if product contains no palm oil.

        Args:
            additive_analysis: Analysis results from additive engine

        Returns:
            Verification result dictionary
        """

        palm_data = additive_analysis.get(
            "palm_oil",
            {},
        )

        found = palm_data.get(
            "matches",
            [],
        )

        return self.build_result(
            claim=CLAIMS_REGISTRY["no_palm_oil"]["title"],
            passed=not palm_data.get(
                "contains_palm_oil",
                False,
            ),
            found=found,
            reason=(
                "No palm oil detected."
                if not found
                else "Palm oil detected."
            ),
        )


    def verify_no_added_sugar(
        self,
        additive_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Verify if product contains no added sugar.

        Args:
            additive_analysis: Analysis results from additive engine

        Returns:
            Verification result dictionary
        """

        sugar_data = additive_analysis.get(
            "hidden_sugars",
            {},
        )

        found = sugar_data.get(
            "hidden_sugars",
            [],
        )

        return self.build_result(
            claim=CLAIMS_REGISTRY["no_added_sugar"]["title"],
            passed=len(found) == 0,
            found=found,
            reason=(
                "No added sugars detected."
                if not found
                else "Added sugar ingredients detected."
            ),
        )


    def verify_no_artificial_additives(
        self,
        additive_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Verify if product contains no risky artificial additives.

        Args:
            additive_analysis: Analysis results from additive engine

        Returns:
            Verification result dictionary
        """

        additives = additive_analysis.get(
            "detected_additives",
            [],
        )

        risky_additives = []

        for additive in additives:

            if isinstance(additive, dict):

                # Check risk level if available
                risk = additive.get("risk", 0)

                if isinstance(risk, str):

                    try:

                        risk = int(risk)

                    except ValueError:

                        risk = 0

                if int(risk) >= 2:

                    risky_additives.append(additive)

            elif isinstance(additive, str):

                # Assume string additives have moderate risk
                risky_additives.append({"name": additive})

        found = []

        for a in risky_additives:

            if isinstance(a, dict):

                found.append(a.get("name", "unknown"))

            else:

                found.append(a)

        return self.build_result(
            claim=CLAIMS_REGISTRY["no_artificial_additives"]["title"],
            passed=len(risky_additives) == 0,
            found=found,
            reason=(
                "No risky artificial additives detected."
                if not risky_additives
                else "Risky artificial additives detected."
            ),
        )


    def verify_no_preservatives(
        self,
        additive_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Verify if product contains no preservatives.

        Args:
            additive_analysis: Analysis results from additive engine

        Returns:
            Verification result dictionary
        """

        categories = additive_analysis.get(
            "categories",
            {},
        )

        found = categories.get(
            "preservatives",
            [],
        )

        return self.build_result(
            claim=CLAIMS_REGISTRY["no_preservatives"]["title"],
            passed=len(found) == 0,
            found=found,
            reason=(
                "No preservatives detected."
                if not found
                else "Preservatives detected."
            ),
        )


    def verify_no_artificial_colors(
        self,
        additive_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Verify if product contains no artificial colors.

        Args:
            additive_analysis: Analysis results from additive engine

        Returns:
            Verification result dictionary
        """

        categories = additive_analysis.get(
            "categories",
            {},
        )

        found = categories.get(
            "colors",
            [],
        )

        return self.build_result(
            claim=CLAIMS_REGISTRY["no_artificial_colors"]["title"],
            passed=len(found) == 0,
            found=found,
            reason=(
                "No artificial colors detected."
                if not found
                else "Artificial colors detected."
            ),
        )


    # ==========================================================
    # COMPOSITE VERIFICATIONS
    # ==========================================================

    def verify_clean_label(
        self,
        parser_analysis: Dict[str, Any],
        additive_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Verify if product meets clean label standards.

        Args:
            parser_analysis: Analysis results from ingredient parser
            additive_analysis: Analysis results from additive engine

        Returns:
            Clean label verification result
        """

        quality_score = (
            parser_analysis.get(
                "scores",
                {},
            ).get(
                "quality_score",
                0,
            )
        )

        clean_label_score = (
            parser_analysis.get(
                "scores",
                {},
            ).get(
                "clean_label_score",
                0,
            )
        )

        additive_load = (
            additive_analysis.get(
                "scores",
                {},
            ).get(
                "additive_load_score",
                0,
            )
        )

        passed = (
            quality_score >= 75
            and clean_label_score >= 70
            and additive_load <= 40
        )

        return {

            "status": "PASS" if passed else "FAIL",

            "quality_score": quality_score,

            "clean_label_score": clean_label_score,

            "additive_load": additive_load,

        }


    def verify_child_safety(
        self,
        additive_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Verify if product is safe for children.

        Args:
            additive_analysis: Analysis results from additive engine

        Returns:
            Child safety verification result
        """

        score = (
            additive_analysis.get(
                "scores",
                {},
            ).get(
                "child_safety_score",
                0,
            )
        )

        hyperactivity = (
            additive_analysis.get(
                "hyperactivity_risk",
                {},
            )
        )

        return {

            "status": "PASS" if score >= 70 else "FAIL",

            "score": score,

            "hyperactivity_risk": hyperactivity.get(
                "risk_level",
                "LOW",
            ),

        }


    def verify_diabetic_friendly(
        self,
        additive_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Verify if product is diabetic friendly.

        Args:
            additive_analysis: Analysis results from additive engine

        Returns:
            Diabetic friendly verification result
        """

        sugar_data = additive_analysis.get(
            "hidden_sugars",
            {},
        )

        sweetener_data = additive_analysis.get(
            "artificial_sweeteners",
            {},
        )

        sugar_count = sugar_data.get(
            "hidden_sugar_count",
            0,
        )

        sweetener_count = sweetener_data.get(
            "count",
            0,
        )

        passed = (
            sugar_count == 0
            and sweetener_count <= 1
        )

        return {

            "status": "PASS" if passed else "FAIL",

            "hidden_sugar_count": sugar_count,

            "artificial_sweetener_count": sweetener_count,

        }


    def verify_ultra_processed(
        self,
        parser_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Verify if product is ultra processed.

        Args:
            parser_analysis: Analysis results from ingredient parser

        Returns:
            Ultra processed verification result
        """

        processing = (
            parser_analysis.get(
                "processing_analysis",
                {},
            )
        )

        level = processing.get(
            "processing_level",
            "UNKNOWN",
        )

        return {

            "status": "FAIL" if level == "ULTRA_PROCESSED" else "PASS",

            "processing_level": level,

            "confidence": processing.get(
                "confidence",
                0,
            ),

        }


    # ==========================================================
    # SCORE CALCULATIONS
    # ==========================================================

    def calculate_authenticity_score(
        self,
        parser_analysis: Dict[str, Any],
        additive_analysis: Dict[str, Any],
    ) -> int:
        """
        Calculate product authenticity score (0-100).

        Args:
            parser_analysis: Analysis results from ingredient parser
            additive_analysis: Analysis results from additive engine

        Returns:
            Authenticity score (higher = more authentic)
        """

        score = 100

        additive_load = (
            additive_analysis.get(
                "scores",
                {},
            ).get(
                "additive_load_score",
                0,
            )
        )

        hidden_sugars = (
            additive_analysis.get(
                "hidden_sugars",
                {},
            ).get(
                "hidden_sugar_count",
                0,
            )
        )

        processing_confidence = (
            parser_analysis.get(
                "processing_analysis",
                {},
            ).get(
                "confidence",
                0,
            )
        )

        score -= int(
            additive_load * 0.5
        )

        score -= (
            hidden_sugars * 5
        )

        score -= int(
            processing_confidence * 0.2
        )

        return max(
            min(score, 100),
            0,
        )


    def calculate_health_score(
        self,
        claim_results: List[Dict[str, Any]],
    ) -> int:
        """
        Calculate overall health score based on claim results.

        Args:
            claim_results: List of claim verification results

        Returns:
            Health score (0-100)
        """

        score = 100

        major_claims = {

            "No Artificial Additives",
            "No Added Sugar",
            "No Preservatives",
            "No MSG",

        }

        for result in claim_results:

            if result.get("verdict") != "FAIL":

                continue

            if result.get("claim") in major_claims:

                score -= 12

            else:

                score -= 5

        return max(
            score,
            0,
        )


    # ==========================================================
    # MAIN VERIFY METHOD
    # ==========================================================

    def verify(
        self,
        ingredients: List[str],
        parser_analysis: Dict[str, Any],
        additive_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Run all verifications on a product.

        Args:
            ingredients: List of ingredient names
            parser_analysis: Analysis results from ingredient parser
            additive_analysis: Analysis results from additive engine

        Returns:
            Complete verification results
        """

        try:

            ingredient_count = len(
                ingredients
            )

            if ingredient_count == 0:

                return {

                    "health_score": 0,

                    "claim_results": [],

                    "verification_summary": {
                        "passed": 0,
                        "failed": 0,
                        "total": 0,
                    },

                    "data_quality": "INSUFFICIENT_INGREDIENT_DATA",

                }

            results = [

                self.verify_vegan(
                    ingredients,
                ),

                self.verify_vegetarian(
                    ingredients,
                ),

                self.verify_dairy_free(
                    ingredients,
                ),

                self.verify_gluten_free(
                    ingredients,
                ),

                self.verify_no_soy(
                    ingredients,
                ),

                self.verify_no_nuts(
                    ingredients,
                ),

                self.verify_no_msg(
                    ingredients,
                ),

                self.verify_no_palm_oil(
                    additive_analysis,
                ),

                self.verify_no_added_sugar(
                    additive_analysis,
                ),

                self.verify_no_artificial_additives(
                    additive_analysis,
                ),

                self.verify_no_preservatives(
                    additive_analysis,
                ),

                self.verify_no_artificial_colors(
                    additive_analysis,
                ),

            ]

            health_score = self.calculate_health_score(
                results,
            )

            passed_count = len([
                result
                for result in results
                if result.get("verdict") == "PASS"
            ])

            failed_count = len([
                result
                for result in results
                if result.get("verdict") == "FAIL"
            ])

            return {

                "health_score": health_score,

                "claim_results": results,

                "verification_summary": {

                    "passed": passed_count,

                    "failed": failed_count,

                    "total": len(results),

                },

                "clean_label": self.verify_clean_label(
                    parser_analysis,
                    additive_analysis,
                ),

                "child_safety": self.verify_child_safety(
                    additive_analysis,
                ),

                "diabetic_friendly": self.verify_diabetic_friendly(
                    additive_analysis,
                ),

                "ultra_processed": self.verify_ultra_processed(
                    parser_analysis,
                ),

                "authenticity_score": self.calculate_authenticity_score(
                    parser_analysis,
                    additive_analysis,
                ),

            }

        except Exception as e:

            log.exception(
                f"Verification failed: {e}"
            )

            return {

                "health_score": 0,

                "claim_results": [],

                "verification_summary": {

                    "passed": 0,

                    "failed": 0,

                    "total": 0,

                },

                "error": str(e),

            }


# ==========================================================
# END OF FILE – ingredient_verifier.py
# ==========================================================