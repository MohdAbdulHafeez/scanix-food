# ==========================================================
# SCANIX AI
# SYSTEM 2 – INGREDIENT RISK ENGINE
# ELITE PRODUCTION GRADE – FINAL VERSION
# ==========================================================


from __future__ import annotations


import json
from pathlib import Path
from difflib import get_close_matches
from typing import Any
from typing import Dict
from typing import List
from typing import Optional


from core.logging import log


# ==========================================================
# CONSTANTS
# ==========================================================


DEFAULT_RISK_THRESHOLDS = {

    "high_risk_ingredient_count": 3,

    "average_risk_score_threshold": 50,

    "fuzzy_match_cutoff": 0.85,

}


# ==========================================================
# INGREDIENT RISK ENGINE
# ==========================================================


class IngredientRiskEngine:
    """
    Comprehensive risk assessment engine for food ingredients.

    Features:
    - Risk scoring (0-100) for each ingredient
    - Domain-specific risk tracking (CARDIOVASCULAR, OBESITY, etc.)
    - Population-specific risk flags (DIABETICS, HEART_PATIENTS, etc.)
    - Fuzzy matching for OCR errors
    - Caching for performance
    - Batch analysis support
    - High-risk product detection
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize the ingredient risk engine.

        Loads risk profiles from JSON and builds alias maps for lookups.
        """

        self.database = self._load_database()

        self.alias_map = self._build_alias_map()

        self._lookup_cache: Dict[str, Dict[str, Any]] = {}


    # ==========================================================
    # DATABASE LOADING
    # ==========================================================

    def _load_database(
        self,
    ) -> Dict[str, Any]:
        """
        Load ingredient risk profiles from JSON file.

        Returns:
            Dictionary of ingredient risk profiles
        """

        db_path = (

            Path(__file__)
            .parent
            /
            "ingredient_risk_profiles.json"

        )

        if not db_path.exists():

            log.warning(
                f"Risk profile database not found at {db_path}"
            )

            return {}

        try:

            with open(

                db_path,

                "r",

                encoding="utf-8",

            ) as f:

                data = json.load(f)

                log.info(
                    f"Loaded {len(data)} ingredient risk profiles"
                )

                return data

        except json.JSONDecodeError as e:

            log.error(
                f"Invalid JSON in risk profile database: {e}"
            )

            return {}

        except Exception as e:

            log.exception(
                f"Failed to load risk profile database: {e}"
            )

            return {}


    # ==========================================================
    # ALIAS MAP BUILDING
    # ==========================================================

    def _build_alias_map(
        self,
    ) -> Dict[str, str]:
        """
        Build alias map for ingredient lookups.

        Includes:
        - Direct ingredient name mapping
        - OCR correction mappings
        - E-number to ingredient name mapping

        Returns:
            Dictionary mapping normalized names to canonical ingredient names
        """

        alias_map: Dict[str, str] = {}

        # Add all ingredients from database
        for ingredient in self.database:

            alias_map[
                ingredient.lower()
            ] = ingredient

        # OCR corrections for common misreads
        ocr_corrections = {

            # Maltodextrin variations
            "mallodextrin": "maltodextrin",
            "maltodextin": "maltodextrin",
            "maltodextrn": "maltodextrin",
            "maltodex": "maltodextrin",

            # Hydrolysed protein variations
            "hycrolysed": "hydrolysed",
            "hycrolyzed": "hydrolyzed",
            "hydrolised": "hydrolysed",

            # E-number to ingredient mapping
            "e102": "tartrazine",
            "e110": "sunset yellow",
            "e129": "allura red",
            "e133": "brilliant blue",
            "e211": "sodium benzoate",
            "e220": "sulphur dioxide",
            "e250": "sodium nitrite",
            "e621": "msg",
            "e627": "disodium guanylate",
            "e631": "disodium inosinate",
            "e635": "disodium ribonucleotides",
            "e951": "aspartame",
            "e955": "sucralose",

            # Common brand/product names
            "dalda": "vanaspati",
            "dalda vanaspati": "vanaspati",

            # Ingredient name corrections
            "methyl cellulose": "methylcellulose",
            "carboxy methyl cellulose": "carboxymethyl cellulose",
            "soya lecithin": "soy lecithin",
            "soya protein": "soy protein",
            "whey protein": "whey",

        }

        for wrong, correct in ocr_corrections.items():

            alias_map[wrong] = correct

        return alias_map


    # ==========================================================
    # NORMALIZATION
    # ==========================================================

    def _normalize(
        self,
        ingredient: str,
    ) -> str:
        """
        Normalize ingredient name for consistent lookup.

        Steps:
        - Lowercase
        - Remove extra spaces
        - Replace underscores and hyphens with spaces
        - Remove commas

        Args:
            ingredient: Raw ingredient name

        Returns:
            Normalized ingredient name
        """

        ingredient = (

            ingredient
            .strip()
            .lower()

        )

        ingredient = ingredient.replace(
            "_",
            " ",
        )

        ingredient = ingredient.replace(
            "-",
            " ",
        )

        ingredient = ingredient.replace(
            ",",
            "",
        )

        ingredient = ingredient.replace(
            "  ",
            " ",
        )

        return ingredient


    # ==========================================================
    # CACHE MANAGEMENT
    # ==========================================================

    def clear_cache(
        self,
    ) -> None:
        """
        Clear the lookup cache.

        Useful for testing and when database updates are loaded.
        """

        self._lookup_cache.clear()

        log.debug(
            "Ingredient risk engine cache cleared"
        )


    def get_cache_size(
        self,
    ) -> int:
        """
        Get the current size of the lookup cache.

        Returns:
            Number of cached lookups
        """

        return len(self._lookup_cache)


    # ==========================================================
    # SINGLE INGREDIENT LOOKUP
    # ==========================================================

    def lookup(
        self,
        ingredient: str,
    ) -> Dict[str, Any]:
        """
        Look up risk profile for a single ingredient.

        Features:
        - Exact match first
        - Fuzzy match fallback (85% similarity)
        - Caching for repeated lookups

        Args:
            ingredient: Ingredient name

        Returns:
            Risk profile dictionary with fields:
            - name: Original ingredient name
            - known: Whether ingredient is in database
            - risk_level: HIGH/MODERATE/LOW/UNKNOWN
            - risk_score: 0-100 integer
            - risk_domains: List of affected health domains
            - population_risk: List of at-risk populations
            - evidence_level: HIGH/MODERATE/LOW/UNKNOWN
            - safe_frequency: AVOID/LIMIT/MODERATE/SAFE/UNKNOWN
            - digital_twin_weight: 0.0-1.0 weight for System 5
            - explanation: Human-readable explanation
        """

        normalized = self._normalize(
            ingredient
        )

        # Check cache first
        if normalized in self._lookup_cache:

            return self._lookup_cache[normalized]

        # Try exact match from alias map
        matched = self.alias_map.get(
            normalized
        )

        # Try fuzzy match if exact match fails
        if not matched:

            close = get_close_matches(

                normalized,

                self.alias_map.keys(),

                n=1,

                cutoff=DEFAULT_RISK_THRESHOLDS[
                    "fuzzy_match_cutoff"
                ],

            )

            if close:

                matched = self.alias_map.get(
                    close[0]
                )

            if not matched:

                result = {

                    "name": ingredient,

                    "known": False,

                    "risk_level": "UNKNOWN",

                    "risk_score": 0,

                    "risk_domains": [],

                    "population_risk": [],

                    "evidence_level": "UNKNOWN",

                    "safe_frequency": "UNKNOWN",

                    "digital_twin_weight": 0.0,

                    "explanation": "Ingredient not found in risk database.",

                }

                self._lookup_cache[normalized] = result

                return result

        # Get profile from database
        profile = self.database.get(
            matched,
            {},
        )

        result = {

            "name": ingredient,

            "known": True,

            "risk_level": profile.get(
                "risk_level",
                "UNKNOWN",
            ),

            "risk_score": profile.get(
                "risk_score",
                0,
            ),

            "risk_domains": profile.get(
                "risk_domains",
                [],
            ),

            "population_risk": profile.get(
                "population_risk",
                [],
            ),

            "evidence_level": profile.get(
                "evidence_level",
                "UNKNOWN",
            ),

            "safe_frequency": profile.get(
                "safe_frequency",
                "UNKNOWN",
            ),

            "digital_twin_weight": profile.get(
                "digital_twin_weight",
                0.0,
            ),

            "explanation": profile.get(
                "explanation",
                "",
            ),

        }

        # Store in cache
        self._lookup_cache[normalized] = result

        return result


    # ==========================================================
    # HELPER METHODS
    # ==========================================================

    def get_risk_level(
        self,
        ingredient: str,
    ) -> str:
        """
        Get just the risk level of an ingredient.

        Args:
            ingredient: Ingredient name

        Returns:
            Risk level string (HIGH/MODERATE/LOW/UNKNOWN)
        """

        return self.lookup(ingredient).get(
            "risk_level",
            "UNKNOWN",
        )


    def get_risk_score(
        self,
        ingredient: str,
    ) -> int:
        """
        Get just the risk score of an ingredient.

        Args:
            ingredient: Ingredient name

        Returns:
            Risk score integer (0-100)
        """

        return self.lookup(ingredient).get(
            "risk_score",
            0,
        )


    def is_high_risk_ingredient(
        self,
        ingredient: str,
    ) -> bool:
        """
        Check if an ingredient is high risk.

        Args:
            ingredient: Ingredient name

        Returns:
            True if risk level is HIGH
        """

        return self.get_risk_level(ingredient) == "HIGH"


    def is_known_ingredient(
        self,
        ingredient: str,
    ) -> bool:
        """
        Check if an ingredient is in the risk database.

        Args:
            ingredient: Ingredient name

        Returns:
            True if ingredient is known
        """

        return self.lookup(ingredient).get(
            "known",
            False,
        )


    # ==========================================================
    # BATCH ANALYSIS
    # ==========================================================

    def analyze_batch(
        self,
        ingredient_lists: List[List[str]],
    ) -> List[Dict[str, Any]]:
        """
        Analyze multiple ingredient lists in batch.

        Args:
            ingredient_lists: List of ingredient lists

        Returns:
            List of analysis results for each ingredient list
        """

        results = []

        for ingredients in ingredient_lists:

            results.append(
                self.analyze(ingredients)
            )

        log.debug(
            f"Batch analysis completed for {len(ingredient_lists)} products"
        )

        return results


    # ==========================================================
    # MAIN ANALYSIS METHOD
    # ==========================================================

    def analyze(
        self,
        ingredients: List[str],
    ) -> Dict[str, Any]:
        """
        Analyze a list of ingredients for health risks.

        Calculates:
        - Individual risk profiles for each ingredient
        - Aggregated risk statistics
        - Dominant risk domains
        - Population-specific risks

        Args:
            ingredients: List of ingredient names

        Returns:
            Comprehensive risk analysis dictionary
        """

        ingredient_results = []

        high_risk_count = 0

        moderate_risk_count = 0

        low_risk_count = 0

        unknown_risk_count = 0

        risk_domains: Dict[str, int] = {}

        population_risks: Dict[str, int] = {}

        top_risk_ingredients = []

        highest_score = -1

        highest_risk_ingredient = None

        cumulative_risk_score = 0

        cumulative_digital_twin_weight = 0.0

        for ingredient in ingredients:

            result = self.lookup(
                ingredient
            )

            ingredient_results.append(
                result
            )

            score = result.get(
                "risk_score",
                0,
            )

            cumulative_risk_score += score

            cumulative_digital_twin_weight += (

                result.get(
                    "digital_twin_weight",
                    0.0,
                )

            )

            if score > highest_score:

                highest_score = score

                highest_risk_ingredient = ingredient

            level = result.get(
                "risk_level",
                "",
            )

            if level == "HIGH":

                high_risk_count += 1

                top_risk_ingredients.append(
                    ingredient
                )

            elif level == "MODERATE":

                moderate_risk_count += 1

            elif level == "LOW":

                low_risk_count += 1

            elif level == "UNKNOWN":

                unknown_risk_count += 1

            for domain in result.get(
                "risk_domains",
                [],
            ):

                risk_domains[
                    domain
                ] = (

                    risk_domains.get(
                        domain,
                        0,
                    )

                    + 1

                )

            for population in result.get(
                "population_risk",
                [],
            ):

                population_risks[
                    population
                ] = (

                    population_risks.get(
                        population,
                        0,
                    )

                    + 1

                )

        total_ingredients = len(
            ingredients
        )

        avg_risk_score = 0

        if total_ingredients > 0:

            avg_risk_score = round(

                cumulative_risk_score

                /

                total_ingredients,

                2,
            )

        avg_digital_twin_weight = 0.0

        if total_ingredients > 0:

            avg_digital_twin_weight = round(

                cumulative_digital_twin_weight

                /

                total_ingredients,

                3,
            )

        dominant_domain = None

        if risk_domains:

            dominant_domain = max(
                risk_domains,
                key=risk_domains.get,
            )

        dominant_population_risk = None

        if population_risks:

            dominant_population_risk = max(

                population_risks,

                key=population_risks.get,

            )

        ingredient_health_summary = {

            "total_ingredients": total_ingredients,

            "high_risk_count": high_risk_count,

            "moderate_risk_count": moderate_risk_count,

            "low_risk_count": low_risk_count,

            "unknown_risk_count": unknown_risk_count,

            "top_risk_ingredients": sorted(
                list(
                    set(
                        top_risk_ingredients
                    )
                )
            )[:10],

            "highest_risk_ingredient": highest_risk_ingredient,

            "highest_risk_score": highest_score,

            "average_risk_score": avg_risk_score,

            "dominant_risk_domain": dominant_domain,

            "dominant_population_risk": dominant_population_risk,

            "digital_twin_weight": avg_digital_twin_weight,

        }

        return {

            "ingredient_risks": ingredient_results,

            "ingredient_health_summary": ingredient_health_summary,

            "risk_domain_distribution": risk_domains,

            "population_risk_distribution": population_risks,

        }


    # ==========================================================
    # HIGH RISK PRODUCT DETECTION
    # ==========================================================

    def is_high_risk_product(
        self,
        analysis: Dict[str, Any],
        high_risk_threshold: Optional[int] = None,
        avg_risk_threshold: Optional[float] = None,
    ) -> bool:
        """
        Determine if a product is high risk based on analysis.

        Args:
            analysis: Result from analyze() method
            high_risk_threshold: Number of high-risk ingredients to flag
            avg_risk_threshold: Average risk score threshold

        Returns:
            True if product is high risk
        """

        if high_risk_threshold is None:

            high_risk_threshold = DEFAULT_RISK_THRESHOLDS[
                "high_risk_ingredient_count"
            ]

        if avg_risk_threshold is None:

            avg_risk_threshold = DEFAULT_RISK_THRESHOLDS[
                "average_risk_score_threshold"
            ]

        summary = analysis.get(
            "ingredient_health_summary",
            {},
        )

        high_risk_count = summary.get(
            "high_risk_count",
            0,
        )

        avg_risk_score = summary.get(
            "average_risk_score",
            0,
        )

        return (
            high_risk_count >= high_risk_threshold
            or avg_risk_score >= avg_risk_threshold
        )


    # ==========================================================
    # STATISTICS
    # ==========================================================

    def get_database_stats(
        self,
    ) -> Dict[str, Any]:
        """
        Get statistics about the risk database.

        Returns:
            Dictionary with database statistics
        """

        risk_level_counts = {

            "HIGH": 0,

            "MODERATE": 0,

            "LOW": 0,

        }

        for profile in self.database.values():

            level = profile.get(
                "risk_level",
                "UNKNOWN",
            )

            if level in risk_level_counts:

                risk_level_counts[level] += 1

        return {

            "total_ingredients": len(self.database),

            "high_risk_count": risk_level_counts["HIGH"],

            "moderate_risk_count": risk_level_counts["MODERATE"],

            "low_risk_count": risk_level_counts["LOW"],

            "cache_size": self.get_cache_size(),

        }


# ==========================================================
# SINGLETON INSTANCE
# ==========================================================


ingredient_risk_engine = IngredientRiskEngine()


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [

    "IngredientRiskEngine",

    "ingredient_risk_engine",

]


# ==========================================================
# INITIALIZATION LOG
# ==========================================================


log.info(
    "Ingredient Risk Engine initialized",
    total_ingredients=len(ingredient_risk_engine.database),
    cache_enabled=True,
    fuzzy_match_cutoff=DEFAULT_RISK_THRESHOLDS["fuzzy_match_cutoff"],
)


# ==========================================================
# END OF FILE – ingredient_risk_engine.py
# ==========================================================