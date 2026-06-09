# ==========================================================
# SCANIX AI
# SYSTEM 2 – INGREDIENT FUNCTION ENGINE
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
from collections import Counter


from core.logging import log


# ==========================================================
# CONSTANTS
# ==========================================================


FUZZY_MATCH_CUTOFF: float = 0.85

UNKNOWN_VALUE: str = "UNKNOWN"


# ==========================================================
# INGREDIENT FUNCTION ENGINE
# ==========================================================


class IngredientFunctionEngine:
    """
    Comprehensive ingredient function detection engine.

    Features:
    - Detects function, category, and subcategory of ingredients
    - Fuzzy matching for OCR errors
    - Caching for performance
    - Batch analysis support
    - Usage category filtering
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize the ingredient function engine.

        Loads function database from JSON and builds alias maps for lookups.
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
        Load ingredient function profiles from JSON file.

        Returns:
            Dictionary of ingredient function profiles
        """

        db_path = (

            Path(__file__)
            .parent
            /
            "ingredient_functions.json"

        )

        if not db_path.exists():

            log.warning(
                f"Function database not found at {db_path}"
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
                    f"Loaded {len(data)} ingredient function profiles"
                )

                return data

        except json.JSONDecodeError as e:

            log.error(
                f"Invalid JSON in function database: {e}"
            )

            return {}

        except Exception as e:

            log.exception(
                f"Failed to load function database: {e}"
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
        - Alias mappings from database
        - OCR correction mappings

        Returns:
            Dictionary mapping normalized names to canonical ingredient names
        """

        alias_map: Dict[str, str] = {}

        # Add all ingredients from database with their aliases
        for ingredient, profile in self.database.items():

            alias_map[
                ingredient.lower()
            ] = ingredient

            aliases = profile.get(
                "aliases",
                [],
            )

            for alias in aliases:

                alias_map[
                    alias.lower()
                ] = ingredient

        # OCR corrections for common misreads
        ocr_corrections = {

            # Maltodextrin variations
            "mallodextrin": "maltodextrin",
            "maltodextin": "maltodextrin",
            "maltodextrn": "maltodextrin",

            # Hydrolysed protein variations
            "hycrolysed": "hydrolysed",
            "hycrolyzed": "hydrolyzed",

            # E-number to ingredient mapping
            "e102": "tartrazine",
            "e110": "sunset yellow",
            "e129": "allura red",
            "e133": "brilliant blue",
            "e202": "potassium sorbate",
            "e211": "sodium benzoate",
            "e220": "sulphur dioxide",
            "e250": "sodium nitrite",
            "e270": "lactic acid",
            "e282": "calcium propionate",
            "e320": "bha",
            "e321": "bht",
            "e322": "soy lecithin",
            "e330": "citric acid",
            "e338": "phosphoric acid",
            "e406": "agar agar",
            "e407": "carrageenan",
            "e433": "polysorbate 80",
            "e440": "pectin",
            "e441": "gelatin",
            "e476": "pgpr",
            "e500": "sodium bicarbonate",
            "e551": "silicon dioxide",
            "e572": "magnesium stearate",
            "e621": "msg",
            "e627": "disodium guanylate",
            "e631": "disodium inosinate",
            "e950": "acesulfame potassium",
            "e951": "aspartame",
            "e955": "sucralose",

            # Common misreads
            "hycrolysed vegetable protein": "hydrolysed vegetable protein",
            "soya lecithin": "soy lecithin",
            "soya protein": "soy protein",
            "whey protein": "whey",
            "methyl cellulose": "methylcellulose",
            "carboxy methyl cellulose": "carboxymethyl cellulose",
            "sodium benzoate": "sodium benzoate",
            "potassium sorbate": "potassium sorbate",

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
            "Ingredient function engine cache cleared"
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
        Look up function profile for a single ingredient.

        Features:
        - Exact match first
        - Fuzzy match fallback (85% similarity)
        - Caching for repeated lookups

        Args:
            ingredient: Ingredient name

        Returns:
            Function profile dictionary with fields:
            - name: Original ingredient name
            - matched_alias: Canonical ingredient name matched
            - function: Function of ingredient (SWEETENER, PRESERVATIVE, etc.)
            - category: Category (CARBOHYDRATE, FOOD_ADDITIVE, etc.)
            - subcategory: Detailed subcategory
            - description: Human-readable description
            - used_in: List of product categories where used
            - known: Whether ingredient is in database
        """

        normalized = self._normalize(
            ingredient
        )

        # Check cache first
        if normalized in self._lookup_cache:

            return self._lookup_cache[normalized]

        # Try exact match from alias map
        matched_key = self.alias_map.get(
            normalized
        )

        # Try fuzzy match if exact match fails
        if not matched_key:

            close = get_close_matches(

                normalized,

                self.alias_map.keys(),

                n=1,

                cutoff=FUZZY_MATCH_CUTOFF,

            )

            if close:

                matched_key = self.alias_map.get(
                    close[0]
                )

        # Return unknown result if no match found
        if not matched_key:

            result = {

                "name": ingredient,

                "matched_alias": None,

                "function": UNKNOWN_VALUE,

                "category": UNKNOWN_VALUE,

                "subcategory": UNKNOWN_VALUE,

                "description": "",

                "used_in": [],

                "known": False,

            }

            self._lookup_cache[normalized] = result

            return result

        # Get profile from database
        profile = self.database.get(
            matched_key,
            {},
        )

        result = {

            "name": ingredient,

            "matched_alias": matched_key,

            "function": profile.get(
                "function",
                UNKNOWN_VALUE,
            ),

            "category": profile.get(
                "category",
                UNKNOWN_VALUE,
            ),

            "subcategory": profile.get(
                "subcategory",
                UNKNOWN_VALUE,
            ),

            "description": profile.get(
                "description",
                "",
            ),

            "used_in": profile.get(
                "used_in",
                [],
            ),

            "known": True,

        }

        # Store in cache
        self._lookup_cache[normalized] = result

        return result


    # ==========================================================
    # HELPER METHODS
    # ==========================================================

    def get_function(
        self,
        ingredient: str,
    ) -> str:
        """
        Get just the function of an ingredient.

        Args:
            ingredient: Ingredient name

        Returns:
            Function string (SWEETENER, PRESERVATIVE, etc.)
        """

        return self.lookup(ingredient).get(
            "function",
            UNKNOWN_VALUE,
        )


    def get_category(
        self,
        ingredient: str,
    ) -> str:
        """
        Get just the category of an ingredient.

        Args:
            ingredient: Ingredient name

        Returns:
            Category string (CARBOHYDRATE, FOOD_ADDITIVE, etc.)
        """

        return self.lookup(ingredient).get(
            "category",
            UNKNOWN_VALUE,
        )


    def is_known(
        self,
        ingredient: str,
    ) -> bool:
        """
        Check if an ingredient is in the function database.

        Args:
            ingredient: Ingredient name

        Returns:
            True if ingredient is known
        """

        return self.lookup(ingredient).get(
            "known",
            False,
        )


    def is_function(
        self,
        ingredient: str,
        target_function: str,
    ) -> bool:
        """
        Check if ingredient has a specific function.

        Args:
            ingredient: Ingredient name
            target_function: Function to check (e.g., "PRESERVATIVE")

        Returns:
            True if ingredient matches the target function
        """

        return self.get_function(ingredient) == target_function


    def filter_by_used_in(
        self,
        ingredients: List[str],
        category: str,
    ) -> List[str]:
        """
        Filter ingredients by where they are commonly used.

        Args:
            ingredients: List of ingredient names
            category: Usage category (e.g., "BAKERY", "BEVERAGES")

        Returns:
            Filtered list of ingredients used in the specified category
        """

        filtered = []

        for ingredient in ingredients:

            analysis = self.lookup(ingredient)

            used_in = analysis.get("used_in", [])

            if category in used_in:

                filtered.append(ingredient)

        return filtered


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
        Analyze a list of ingredients for functional classification.

        Calculates:
        - Individual function profiles for each ingredient
        - Function and category distributions
        - Known vs unknown ingredient counts

        Args:
            ingredients: List of ingredient names

        Returns:
            Comprehensive function analysis dictionary
        """

        results = []

        known_count = 0

        unknown_count = 0

        function_counts: Dict[str, int] = {}

        category_counts: Dict[str, int] = {}

        subcategory_counts: Dict[str, int] = {}

        for ingredient in ingredients:

            analysis = self.lookup(
                ingredient
            )

            results.append(
                analysis
            )

            if analysis.get("known"):

                known_count += 1

            else:

                unknown_count += 1

            function_name = analysis.get(
                "function",
                UNKNOWN_VALUE,
            )

            category_name = analysis.get(
                "category",
                UNKNOWN_VALUE,
            )

            subcategory_name = analysis.get(
                "subcategory",
                UNKNOWN_VALUE,
            )

            function_counts[
                function_name
            ] = function_counts.get(
                function_name,
                0,
            ) + 1

            category_counts[
                category_name
            ] = category_counts.get(
                category_name,
                0,
            ) + 1

            subcategory_counts[
                subcategory_name
            ] = subcategory_counts.get(
                subcategory_name,
                0,
            ) + 1

        # Get top functions
        top_functions = sorted(
            function_counts.items(),
            key=lambda x: x[1],
            reverse=True,
        )[:5]

        # Get top categories
        top_categories = sorted(
            category_counts.items(),
            key=lambda x: x[1],
            reverse=True,
        )[:5]

        return {

            "total_ingredients": len(ingredients),

            "known_count": known_count,

            "unknown_count": unknown_count,

            "known_percentage": round(
                (known_count / len(ingredients)) * 100 if ingredients else 0,
                1,
            ),

            "function_distribution": function_counts,

            "category_distribution": category_counts,

            "subcategory_distribution": subcategory_counts,

            "top_functions": [
                {"function": func, "count": count}
                for func, count in top_functions
            ],

            "top_categories": [
                {"category": cat, "count": count}
                for cat, count in top_categories
            ],

            "ingredients": results,

        }


    # ==========================================================
    # STATISTICS
    # ==========================================================

    def get_database_stats(
        self,
    ) -> Dict[str, Any]:
        """
        Get statistics about the function database.

        Returns:
            Dictionary with database statistics
        """

        function_counts: Counter = Counter()

        category_counts: Counter = Counter()

        for profile in self.database.values():

            function = profile.get("function", UNKNOWN_VALUE)

            category = profile.get("category", UNKNOWN_VALUE)

            function_counts[function] += 1

            category_counts[category] += 1

        return {

            "total_ingredients": len(self.database),

            "function_distribution": dict(function_counts),

            "category_distribution": dict(category_counts),

            "cache_size": self.get_cache_size(),

        }


# ==========================================================
# SINGLETON INSTANCE
# ==========================================================


ingredient_function_engine = IngredientFunctionEngine()


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [

    "IngredientFunctionEngine",

    "ingredient_function_engine",

]


# ==========================================================
# INITIALIZATION LOG
# ==========================================================


log.info(
    "Ingredient Function Engine initialized",
    total_ingredients=len(ingredient_function_engine.database),
    fuzzy_match_cutoff=FUZZY_MATCH_CUTOFF,
    cache_enabled=True,
)


# ==========================================================
# END OF FILE – ingredient_function_engine.py
# ==========================================================