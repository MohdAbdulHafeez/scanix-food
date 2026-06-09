# ==========================================================
# SCANIX AI
# SYSTEM 2 – ADDITIVE ENGINE
# ELITE PRODUCTION GRADE – FINAL VERSION
# ==========================================================


from __future__ import annotations


import json
import logging
import re
import asyncio
import hashlib
import time
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from datetime import datetime
from datetime import timedelta
from collections import OrderedDict


from core.config import get_settings
from core.logging import log


log = logging.getLogger(__name__)


settings = get_settings()


# ==========================================================
# ATTEMPT TO LOAD ADDITIVES REGISTRY
# ==========================================================

try:
    from .additives_registry import ADDITIVES
except ImportError:
    log.warning("additives_registry.py not found, using empty registry")
    ADDITIVES = []


# ==========================================================
# AI CLIENT FOR ADDITIVE EXPLANATIONS
# ==========================================================


class AdditiveAIClient:
    """
    AI client for generating additive explanations.
    Uses OpenRouter with fallback to Gemini/Groq.
    """

    def __init__(self) -> None:
        self._cache: Dict[str, str] = {}
        self._last_request_time: float = 0
        self._request_count: int = 0

    async def _rate_limit(self) -> None:
        """Rate limit to 30 requests per minute."""
        now = time.time()
        if now - self._last_request_time < 2.0:
            await asyncio.sleep(2.0 - (now - self._last_request_time))
        self._last_request_time = time.time()
        self._request_count += 1

    def _get_cache_key(self, additive_name: str, e_number: str) -> str:
        """Generate cache key for additive explanation."""
        return hashlib.md5(f"{additive_name}:{e_number}".encode()).hexdigest()

    async def get_explanation(
        self,
        additive_name: str,
        e_number: str,
        risk_level: str,
        function: str,
    ) -> str:
        """
        Get AI-generated explanation for an additive.

        Args:
            additive_name: Name of the additive
            e_number: E-number of the additive
            risk_level: Risk level (HIGH/MODERATE/LOW)
            function: Function of additive

        Returns:
            Human-readable explanation
        """

        # Check cache
        cache_key = self._get_cache_key(additive_name, e_number)

        if cache_key in self._cache:

            return self._cache[cache_key]

        # Check if AI is configured
        if not settings.OPENROUTER_API_KEY and not settings.GEMINI_API_KEY:

            return self._get_template_explanation(
                additive_name,
                e_number,
                risk_level,
                function,
            )

        await self._rate_limit()

        prompt = f"""
You are a food safety expert. Explain what "{additive_name}" ({e_number}) is in ONE short sentence for an Indian consumer.

Facts:
- Function: {function}
- Risk level: {risk_level}

Keep it simple, factual, and under 80 words. Focus on health impact.
"""

        try:

            from modules.smart_food.swap_providers import ai_client

            response, provider = await ai_client.generate(
                prompt,
                max_tokens=150,
                temperature=0.3,
            )

            explanation = response.strip()

            if len(explanation) > 200:

                explanation = explanation[:197] + "..."

            # Cache the response
            self._cache[cache_key] = explanation

            # Limit cache size
            if len(self._cache) > 1000:

                # Remove oldest 200 entries
                items = list(self._cache.items())

                self._cache = dict(items[-800:])

            return explanation

        except Exception as e:

            log.warning(f"AI explanation failed: {e}")

            return self._get_template_explanation(
                additive_name,
                e_number,
                risk_level,
                function,
            )

    def _get_template_explanation(
        self,
        additive_name: str,
        e_number: str,
        risk_level: str,
        function: str,
    ) -> str:
        """Fallback template explanation when AI is unavailable."""

        templates = {

            "HIGH": f"⚠️ {additive_name} ({e_number}) is a {function} with potential health concerns. Limit consumption.",

            "MODERATE": f"📊 {additive_name} ({e_number}) is a {function}. Moderate consumption is acceptable.",

            "LOW": f"✅ {additive_name} ({e_number}) is a {function} with low health risk. Generally recognized as safe.",

        }

        return templates.get(
            risk_level,
            f"ℹ️ {additive_name} ({e_number}) is a {function} used in food processing.",
        )


# ==========================================================
# CONSTANTS
# ==========================================================


MSG_ALIASES = {

    "msg",
    "monosodium glutamate",
    "e621",
    "621",
    "msg.",
    "mono sodium glutamate",
    "flavour enhancer 621",
    "flavor enhancer 621",
    "e635",
    "635",
    "disodium 5-ribonucleotides",
    "ribonucleotides",

}


PALM_OIL_ALIASES = {

    "palm oil",
    "palmolein",
    "palm kernel oil",
    "hydrogenated palm oil",
    "palm",
    "palm fat",
    "palmoilein",
    "paim oil",
    "palm oi",
    "palm ol",
    "ralm oil",
    "ralm cl",
    "palm cl",
    "paimolein",
    "refined palmolein oil",
    "vegetable oil (palm)",
    "vegetable oil palm",
    "edible vegetable oil palmolein",
    "palmolein oil",

}


ARTIFICIAL_SWEETENERS = {

    "aspartame",
    "sucralose",
    "acesulfame k",
    "saccharin",
    "neotame",
    "acesulfame potassium",
    "steviol glycosides",
    "stevia",
    "advantame",
    "cyclamate",

}


HYPERACTIVITY_COLORS = {

    "e102",
    "e104",
    "e110",
    "e122",
    "e124",
    "e129",

}


EXPANDED_CATEGORY_KEYWORDS = {

    "preservative": [
        "preservative",
        "preservatives",
        "antimicrobial",
        "mold inhibitor",
        "yeast inhibitor",
    ],

    "color": [
        "colour",
        "color",
        "colouring",
        "coloring",
        "dye",
        "pigment",
        "food color",
        "food colour",
    ],

    "sweetener": [
        "sweetener",
        "artificial sweetener",
        "high intensity sweetener",
        "non-nutritive sweetener",
        "sugar substitute",
    ],

    "emulsifier": [
        "emulsifier",
        "emulsifying agent",
        "emulcifier",
        "emulsifiers",
    ],

    "stabilizer": [
        "stabilizer",
        "stabilising agent",
        "stabilising agent",
        "stabilisers",
        "stabilizers",
    ],

    "flavor_enhancer": [
        "flavour enhancer",
        "flavor enhancer",
        "flavour enhancers",
        "flavor enhancers",
        "umami enhancer",
    ],

    "thickener": [
        "thickener",
        "thickening agent",
        "thickeners",
        "viscosity agent",
    ],

    "acidity_regulator": [
        "acidity regulator",
        "ph regulator",
        "acidulant",
        "buffering agent",
    ],

    "anti_caking": [
        "anti caking",
        "anti-caking",
        "anticaking",
        "flow agent",
        "free flow agent",
    ],

}


PRESERVATIVE_E_NUMBERS = {

    "e200",
    "e202",
    "e203",
    "e210",
    "e211",
    "e212",
    "e213",
    "e214",
    "e215",
    "e216",
    "e217",
    "e218",
    "e219",
    "e220",
    "e221",
    "e222",
    "e223",
    "e224",
    "e225",
    "e226",
    "e227",
    "e228",
    "e234",
    "e235",
    "e239",
    "e242",
    "e249",
    "e250",
    "e251",
    "e252",
    "e260",
    "e261",
    "e262",
    "e263",
    "e270",
    "e280",
    "e281",
    "e282",
    "e283",
    "e284",
    "e285",
    "e290",
    "e296",
    "e297",

}


EMULSIFIER_E_NUMBERS = {

    "e322",
    "e471",
    "e472a",
    "e472b",
    "e472c",
    "e472d",
    "e472e",
    "e472f",
    "e473",
    "e474",
    "e475",
    "e476",
    "e477",
    "e478",
    "e479",
    "e481",
    "e482",
    "e483",
    "e484",
    "e491",
    "e492",
    "e493",
    "e494",
    "e495",

}


STABILIZER_E_NUMBERS = {

    "e400",
    "e401",
    "e402",
    "e403",
    "e404",
    "e405",
    "e406",
    "e407",
    "e407a",
    "e410",
    "e412",
    "e413",
    "e414",
    "e415",
    "e416",
    "e417",
    "e418",
    "e419",
    "e420",
    "e421",
    "e422",
    "e425",
    "e426",
    "e427",
    "e428",
    "e429",
    "e430",
    "e431",
    "e432",
    "e433",
    "e434",
    "e435",
    "e436",
    "e440",
    "e441",
    "e442",
    "e443",
    "e444",
    "e445",
    "e446",
    "e450",
    "e451",
    "e452",
    "e453",
    "e454",
    "e455",
    "e456",
    "e457",
    "e458",
    "e459",
    "e460",
    "e461",
    "e462",
    "e463",
    "e464",
    "e465",
    "e466",
    "e467",
    "e468",
    "e469",
    "e470",
    "e470a",
    "e470b",
    "e471",
    "e472",
    "e473",
    "e474",
    "e475",
    "e476",
    "e477",
    "e478",
    "e479",
    "e480",
    "e481",
    "e482",
    "e483",
    "e484",
    "e485",
    "e486",
    "e487",
    "e488",
    "e489",
    "e490",

}


FSSAI_WARNINGS = {

    "e951": {
        "alert": "Contains Aspartame. Not recommended for phenylketonurics.",
        "restricted_for_children": True,
        "restricted_for_pregnancy": False,
        "mandatory_warning_required": True,
    },

    "e955": {
        "alert": "Contains Sucralose. Not recommended for children.",
        "restricted_for_children": True,
        "restricted_for_pregnancy": False,
        "mandatory_warning_required": True,
    },

    "e621": {
        "alert": "Contains MSG. Not recommended for infants below 12 months.",
        "restricted_for_children": True,
        "restricted_for_pregnancy": False,
        "mandatory_warning_required": True,
    },

    "e102": {
        "alert": "May have an adverse effect on activity and attention in children.",
        "restricted_for_children": True,
        "restricted_for_pregnancy": False,
        "mandatory_warning_required": True,
    },

    "e110": {
        "alert": "May have an adverse effect on activity and attention in children.",
        "restricted_for_children": True,
        "restricted_for_pregnancy": False,
        "mandatory_warning_required": True,
    },

    "e124": {
        "alert": "May have an adverse effect on activity and attention in children.",
        "restricted_for_children": True,
        "restricted_for_pregnancy": False,
        "mandatory_warning_required": True,
    },

    "e129": {
        "alert": "May have an adverse effect on activity and attention in children.",
        "restricted_for_children": True,
        "restricted_for_pregnancy": False,
        "mandatory_warning_required": True,
    },

    "e211": {
        "alert": "May cause reactions in aspirin-sensitive individuals.",
        "restricted_for_children": False,
        "restricted_for_pregnancy": False,
        "mandatory_warning_required": False,
    },

}


# ==========================================================
# CACHE MANAGER
# ==========================================================


class AdditiveAnalysisCache:
    """
    Cache for additive analysis results with TTL.
    """

    def __init__(self, max_size: int = 500, ttl_seconds: int = 3600) -> None:

        self._cache: OrderedDict[str, tuple[Any, float]] = OrderedDict()
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds

    def _get_cache_key(self, ingredients: List[str]) -> str:
        """Generate cache key from ingredient list."""
        sorted_ingredients = sorted(set(ingredients))
        return hashlib.md5(
            "||".join(sorted_ingredients).encode()
        ).hexdigest()

    def get(self, ingredients: List[str]) -> Optional[Dict[str, Any]]:
        """Get cached analysis result if valid."""
        key = self._get_cache_key(ingredients)

        if key in self._cache:

            result, timestamp = self._cache[key]

            if time.time() - timestamp < self.ttl_seconds:

                return result

            else:

                del self._cache[key]

        return None

    def set(self, ingredients: List[str], result: Dict[str, Any]) -> None:
        """Cache analysis result."""
        key = self._get_cache_key(ingredients)

        self._cache[key] = (result, time.time())

        # Maintain max size
        while len(self._cache) > self.max_size:

            self._cache.popitem(last=False)

    def clear(self) -> None:
        """Clear all cache entries."""
        self._cache.clear()
        log.debug("Additive analysis cache cleared")

    def get_size(self) -> int:
        """Get current cache size."""
        return len(self._cache)


# ==========================================================
# ADDITIVE ENGINE
# ==========================================================


class AdditiveEngine:

    def __init__(self) -> None:
        """
        Initialize the additive engine.
        """

        self.registry = self._build_registry()

        self.sugar_aliases = self._load_sugar_aliases()

        self.ai_client = AdditiveAIClient()

        self.cache = AdditiveAnalysisCache()


    # ==========================================================
    # INITIALIZATION HELPERS
    # ==========================================================

    def _build_registry(
        self,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Build registry of additives by E-number.

        Returns:
            Dictionary mapping E-numbers to additive profiles
        """

        registry = {}

        for additive in ADDITIVES:

            number = additive.get("number", "").lower().strip()

            if not number:

                continue

            registry[number] = additive

        log.debug(f"Built additive registry with {len(registry)} entries")

        return registry


    def _load_sugar_aliases(
        self,
    ) -> Set[str]:
        """
        Load sugar aliases from JSON file.

        Returns:
            Set of sugar alias strings
        """

        try:

            file_path = Path(__file__).parent / "sugar_aliases.json"

            if not file_path.exists():

                log.warning(f"Sugar aliases file not found at {file_path}")

                return set()

            with open(file_path, "r", encoding="utf-8") as file:

                aliases = json.load(file)

            return {alias.lower() for alias in aliases}

        except Exception as e:

            log.exception(f"Failed loading sugar aliases: {e}")

            return set()


    # ==========================================================
    # UTILITY METHODS
    # ==========================================================

    @staticmethod
    def normalize(text: str) -> str:
        """
        Normalize text for consistent matching.

        Args:
            text: Input text

        Returns:
            Normalized text
        """

        text = text.lower()

        text = re.sub(r"\s+", " ", text)

        return text.strip()


    def clear_cache(self) -> None:
        """Clear all cached analysis results."""
        self.cache.clear()
        self.ai_client._cache.clear()
        log.info("Additive engine cache cleared")


    # ==========================================================
    # E-NUMBER EXTRACTION
    # ==========================================================

    def extract_e_numbers(
        self,
        ingredients: List[str],
    ) -> List[str]:
        """
        Extract E-numbers from ingredient list.

        Args:
            ingredients: List of ingredient names

        Returns:
            Sorted list of unique E-numbers
        """

        found = set()

        for ingredient in ingredients:

            normalized = self.normalize(ingredient)

            # Extract explicit E-number patterns
            explicit = re.findall(
                r"\b(?:e|ins)[-\s]?(\d{3,4}[a-z]?)\b",
                normalized,
                re.IGNORECASE,
            )

            for match in explicit:

                found.add(f"e{match.lower()}")

            # Extract numeric patterns
            numeric = re.findall(r"\b\d{3,4}\b", normalized)

            for number in numeric:

                key = f"e{number}"

                if key in self.registry:

                    found.add(key)

            # Check registry for keyword matches
            for additive in self.registry.values():

                number = additive.get("number", "")

                if not number:

                    continue

                raw_number = number.lower().replace("e", "")

                if re.search(rf"\b{raw_number}\b", normalized):

                    found.add(number.lower())

        # OCR corrections for common misreads
        ocr_e_number_map = {
            "63s": "635",
            "g35": "635",
            "33o": "330",
            "45i": "451",
            "5o8": "508",
            "s51": "551",
        }

        for ingredient in ingredients:

            normalized = self.normalize(ingredient)

            for broken, actual in ocr_e_number_map.items():

                if broken in normalized:

                    found.add(f"e{actual}")

        return sorted(found)


    # ==========================================================
    # ADDITIVE DETECTION
    # ==========================================================

    def match_registry_additives(
        self,
        e_numbers: List[str],
    ) -> List[Dict[str, Any]]:
        """
        Match E-numbers against additive registry.

        Args:
            e_numbers: List of E-numbers

        Returns:
            List of additive profiles
        """

        matches = []

        for e_number in e_numbers:

            additive = self.registry.get(e_number)

            if additive:

                matches.append(additive)

        return matches


    # ==========================================================
    # HIDDEN SUGARS
    # ==========================================================

    def detect_hidden_sugars(
        self,
        ingredients: List[str],
    ) -> Dict[str, Any]:
        """
        Detect hidden sugars in ingredient list.

        Args:
            ingredients: List of ingredient names

        Returns:
            Hidden sugar detection results
        """

        found = set()

        for ingredient in ingredients:

            ingredient = self.normalize(ingredient)

            for alias in self.sugar_aliases:

                if re.search(rf"\b{re.escape(alias)}\b", ingredient):

                    found.add(alias)

        count = len(found)

        score = min(count * 12, 100)

        if count >= 6:

            severity = "HIGH"

        elif count >= 3:

            severity = "MODERATE"

        else:

            severity = "LOW"

        return {

            "hidden_sugars": sorted(found),

            "hidden_sugar_count": count,

            "hidden_sugar_score": score,

            "severity": severity,

        }


    # ==========================================================
    # PALM OIL
    # ==========================================================

    def detect_palm_oil(
        self,
        ingredients: List[str],
    ) -> Dict[str, Any]:
        """
        Detect palm oil in ingredient list.

        Args:
            ingredients: List of ingredient names

        Returns:
            Palm oil detection results
        """

        found = []

        for ingredient in ingredients:

            normalized = self.normalize(ingredient)

            for alias in PALM_OIL_ALIASES:

                if alias in normalized:

                    found.append(alias)

        found = sorted(set(found))

        return {

            "contains_palm_oil": bool(found),

            "matches": found,

            "severity": "MODERATE" if found else "NONE",

        }


    # ==========================================================
    # MSG DETECTION
    # ==========================================================

    def detect_msg(
        self,
        ingredients: List[str],
    ) -> Dict[str, Any]:
        """
        Detect MSG in ingredient list.

        Args:
            ingredients: List of ingredient names

        Returns:
            MSG detection results
        """

        found = []

        for ingredient in ingredients:

            normalized = self.normalize(ingredient)

            for alias in MSG_ALIASES:

                if alias in normalized:

                    found.append(alias)

        found = sorted(set(found))

        return {

            "contains_msg": bool(found),

            "matches": found,

            "severity": "MODERATE" if found else "NONE",

        }


    # ==========================================================
    # ARTIFICIAL SWEETENERS
    # ==========================================================

    def detect_artificial_sweeteners(
        self,
        ingredients: List[str],
    ) -> Dict[str, Any]:
        """
        Detect artificial sweeteners in ingredient list.

        Args:
            ingredients: List of ingredient names

        Returns:
            Artificial sweetener detection results
        """

        found = []

        for ingredient in ingredients:

            normalized = self.normalize(ingredient)

            for sweetener in ARTIFICIAL_SWEETENERS:

                if sweetener in normalized:

                    found.append(sweetener)

        found = sorted(set(found))

        count = len(found)

        return {

            "sweeteners": found,

            "count": count,

            "severity": "HIGH" if count >= 2 else "MODERATE" if count == 1 else "NONE",

        }


    # ==========================================================
    # ADDITIVE CLASSIFICATION
    # ==========================================================

    def classify_additives(
        self,
        ingredients: List[str],
    ) -> Dict[str, List[str]]:
        """
        Classify additives by their function.

        Args:
            ingredients: List of ingredient names

        Returns:
            Dictionary of classified additives by function
        """

        result = {

            "preservatives": [],
            "colors": [],
            "sweeteners": [],
            "emulsifiers": [],
            "stabilizers": [],
            "flavor_enhancers": [],
            "thickeners": [],
            "acidity_regulators": [],
            "anti_caking": [],

        }

        for ingredient in ingredients:

            normalized = self.normalize(ingredient)

            # Check each function category
            for func_key, keywords in EXPANDED_CATEGORY_KEYWORDS.items():

                for keyword in keywords:

                    if keyword in normalized:

                        result[func_key].append(ingredient)

                        break

            # Check preservative E-numbers
            for e_num in PRESERVATIVE_E_NUMBERS:

                if e_num in normalized:

                    result["preservatives"].append(ingredient)

                    break

            # Check emulsifier E-numbers
            for e_num in EMULSIFIER_E_NUMBERS:

                if e_num in normalized:

                    result["emulsifiers"].append(ingredient)

                    break

            # Check stabilizer E-numbers
            for e_num in STABILIZER_E_NUMBERS:

                if e_num in normalized:

                    result["stabilizers"].append(ingredient)

                    break

        # Deduplicate
        for key in result:

            result[key] = sorted(set(result[key]))

        return result


    # ==========================================================
    # HYPERACTIVITY RISK
    # ==========================================================

    def detect_hyperactivity_risk(
        self,
        additives: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Detect hyperactivity risk from additives.

        Args:
            additives: List of additive profiles

        Returns:
            Hyperactivity risk assessment
        """

        risky = []

        for additive in additives:

            number = additive.get("number", "").lower()

            if number in HYPERACTIVITY_COLORS:

                risky.append(number)

        count = len(risky)

        if count >= 3:

            level = "HIGH"

        elif count >= 1:

            level = "MODERATE"

        else:

            level = "LOW"

        return {

            "risk_level": level,

            "trigger_additives": sorted(risky),

            "count": count,

        }


    # ==========================================================
    # SYNERGY DETECTION
    # ==========================================================

    def detect_synergies(
        self,
        e_numbers: List[str],
    ) -> List[Dict[str, Any]]:
        """
        Detect harmful additive synergies.

        Args:
            e_numbers: List of E-numbers

        Returns:
            List of detected synergies
        """

        synergies = []

        e_set = set(e_numbers)

        flavor_enhancers = {"e621", "e627", "e631"}

        sweeteners = {"e950", "e951", "e955", "e954"}

        if len(flavor_enhancers.intersection(e_set)) >= 2:

            synergies.append({

                "name": "Flavor Enhancer Synergy",

                "risk_boost": 15,

                "description": "Multiple flavor enhancers combine to create hyper-palatability.",

            })

        if len(sweeteners.intersection(e_set)) >= 2:

            synergies.append({

                "name": "Artificial Sweetener Synergy",

                "risk_boost": 20,

                "description": "Multiple sweeteners used together to mask bitter aftertastes.",

            })

        if "e211" in e_set and {"e300", "e301"}.intersection(e_set):

            synergies.append({

                "name": "Preservative-Vitamin C Synergy",

                "risk_boost": 30,

                "description": "Sodium benzoate and Vitamin C can react to form benzene.",

            })

        return synergies


    # ==========================================================
    # REGULATORY ALERTS
    # ==========================================================

    def detect_regulatory_alerts(
        self,
        e_numbers: List[str],
    ) -> List[Dict[str, Any]]:
        """
        Detect regulatory alerts for additives.

        Args:
            e_numbers: List of E-numbers

        Returns:
            List of regulatory alerts
        """

        alerts = []

        for e_num in e_numbers:

            if e_num in FSSAI_WARNINGS:

                alert_data = dict(FSSAI_WARNINGS[e_num])

                alert_data["e_number"] = e_num

                alerts.append(alert_data)

        return alerts


    # ==========================================================
    # RISK SCORING
    # ==========================================================

    def calculate_additive_load_score(
        self,
        additives: List[Dict[str, Any]],
    ) -> int:
        """
        Calculate additive load score (0-100).

        Args:
            additives: List of additive profiles

        Returns:
            Additive load score
        """

        if not additives:

            return 0

        score = 0

        for additive in additives:

            risk = additive.get("risk", 0)

            score += int(risk) * 15

        return min(score, 100)


    def calculate_child_safety_score(
        self,
        additives: List[Dict[str, Any]],
        hyperactivity_risk: Dict[str, Any],
    ) -> int:
        """
        Calculate child safety score (0-100).

        Args:
            additives: List of additive profiles
            hyperactivity_risk: Hyperactivity risk assessment

        Returns:
            Child safety score
        """

        score = 100

        for additive in additives:

            risk = additive.get("risk", 0)

            score -= int(risk) * 5

        if hyperactivity_risk["risk_level"] == "HIGH":

            score -= 25

        elif hyperactivity_risk["risk_level"] == "MODERATE":

            score -= 10

        return max(score, 0)


    def calculate_processing_contribution(
        self,
        additive_count: int,
        ingredient_count: int,
        e_numbers: List[str],
    ) -> int:
        """
        Calculate processing contribution score (0-100).

        Args:
            additive_count: Number of additives
            ingredient_count: Number of total ingredients
            e_numbers: List of E-numbers

        Returns:
            Processing contribution score
        """

        if ingredient_count == 0:

            return 0

        ratio = additive_count / ingredient_count

        score = int(ratio * 100)

        upf_signals = {"e950", "e951", "e955", "e621", "e211", "e102", "e110", "e129"}

        upf_matches = upf_signals.intersection(set(e_numbers))

        upf_count = len(upf_matches)

        if upf_count >= 2:

            score += 30

        elif upf_count == 1:

            score += 15

        return min(score, 100)


    def calculate_risk_distribution(
        self,
        additives: List[Dict[str, Any]],
    ) -> Dict[str, int]:
        """
        Calculate risk distribution across additives.

        Args:
            additives: List of additive profiles

        Returns:
            Risk distribution counts
        """

        high = 0
        moderate = 0
        low = 0

        for additive in additives:

            risk = int(additive.get("risk", 0))

            if risk >= 3:

                high += 1

            elif risk >= 2:

                moderate += 1

            else:

                low += 1

        return {

            "high_risk": high,
            "moderate_risk": moderate,
            "low_risk": low,

        }


    def get_top_risky_additives(
        self,
        additives: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Get top 5 riskiest additives.

        Args:
            additives: List of additive profiles

        Returns:
            Top 5 riskiest additives
        """

        sorted_additives = sorted(
            additives,
            key=lambda x: x.get("risk", 0),
            reverse=True,
        )

        return sorted_additives[:5]


    # ==========================================================
    # AI EXPLANATIONS
    # ==========================================================

    async def build_ai_explanations(
        self,
        additives: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Build AI-generated explanations for additives.

        Args:
            additives: List of additive profiles

        Returns:
            Additives with AI explanations
        """

        if not additives:

            return []

        # Create tasks for each additive
        tasks = []

        for additive in additives:

            name = additive.get("name", "Unknown")

            number = additive.get("number", "")

            risk = additive.get("risk", 0)

            function = additive.get("function", "food additive")

            risk_level = "HIGH" if risk >= 3 else "MODERATE" if risk >= 2 else "LOW"

            tasks.append(
                self.ai_client.get_explanation(
                    name,
                    number,
                    risk_level,
                    function,
                )
            )

        # Run all tasks concurrently
        explanations = await asyncio.gather(*tasks, return_exceptions=True)

        # Build result list
        results = []

        for i, additive in enumerate(additives):

            explanation = explanations[i]

            if isinstance(explanation, Exception):

                explanation = str(explanation)

            results.append({

                "number": additive.get("number"),

                "name": additive.get("name"),

                "risk": additive.get("risk"),

                "function": additive.get("function", "food additive"),

                "description": additive.get("description", ""),

                "usage": additive.get("use", ""),

                "ai_explanation": explanation,

            })

        return results


    # ==========================================================
    # MAIN ANALYSIS METHOD
    # ==========================================================

    async def analyze(
        self,
        ingredients: List[str],
        use_ai: bool = True,
    ) -> Dict[str, Any]:
        """
        Analyze ingredients for additives and risks.

        Args:
            ingredients: List of ingredient names
            use_ai: Whether to use AI for explanations

        Returns:
            Comprehensive additive analysis
        """

        try:

            # Check cache
            cached_result = self.cache.get(ingredients)

            if cached_result:

                return cached_result

            e_numbers = self.extract_e_numbers(ingredients)

            additives = self.match_registry_additives(e_numbers)

            hidden_sugars = self.detect_hidden_sugars(ingredients)

            palm_oil = self.detect_palm_oil(ingredients)

            msg = self.detect_msg(ingredients)

            sweeteners = self.detect_artificial_sweeteners(ingredients)

            categories = self.classify_additives(ingredients)

            hyperactivity = self.detect_hyperactivity_risk(additives)

            synergies = self.detect_synergies(e_numbers)

            regulatory_alerts = self.detect_regulatory_alerts(e_numbers)

            additive_load_score = self.calculate_additive_load_score(additives)

            child_safety_score = self.calculate_child_safety_score(additives, hyperactivity)

            processing_score = self.calculate_processing_contribution(
                additive_count=len(additives),
                ingredient_count=len(ingredients),
                e_numbers=e_numbers,
            )

            risk_distribution = self.calculate_risk_distribution(additives)

            top_risky = self.get_top_risky_additives(additives)

            # Build AI explanations if requested
            explanations = []

            if use_ai:

                explanations = await self.build_ai_explanations(additives)

            synergy_boost = sum(s.get("risk_boost", 0) for s in synergies)

            overall_risk_score = round(
                additive_load_score * 0.4 +
                (100 - child_safety_score) * 0.4 +
                processing_score * 0.2 +
                synergy_boost
            )

            if overall_risk_score >= 75:

                risk_level = "HIGH"

            elif overall_risk_score >= 40:

                risk_level = "MODERATE"

            else:

                risk_level = "LOW"

            top_concerns = []

            if palm_oil.get("contains_palm_oil"):

                top_concerns.append("Palm Oil")

            if hidden_sugars.get("hidden_sugar_count", 0) > 0:

                top_concerns.append("Hidden Sugars")

            if sweeteners.get("count", 0) > 0:

                top_concerns.append("Artificial Sweeteners")

            if len(top_concerns) < 3 and msg.get("contains_msg"):

                top_concerns.append("MSG")

            confidence = 40

            confidence += len(e_numbers) * 8

            confidence += len(additives) * 6

            confidence += min(len(ingredients), 10)

            confidence = min(confidence, 100)

            result = {

                "detected_additives": additives,

                "additive_count": len(additives),

                "e_numbers": e_numbers,

                "hidden_sugars": hidden_sugars,

                "palm_oil": palm_oil,

                "msg": msg,

                "artificial_sweeteners": sweeteners,

                "categories": categories,

                "hyperactivity_risk": hyperactivity,

                "synergies": synergies,

                "regulatory_alerts": regulatory_alerts,

                "scores": {

                    "additive_load_score": additive_load_score,

                    "child_safety_score": child_safety_score,

                    "processing_contribution": processing_score,

                },

                "overall_risk_score": overall_risk_score,

                "overall_risk_level": risk_level,

                "traffic_light": {

                    "green": risk_distribution.get("low_risk", 0),

                    "yellow": risk_distribution.get("moderate_risk", 0),

                    "red": risk_distribution.get("high_risk", 0),

                },

                "top_concerns": top_concerns,

                "analysis_confidence": confidence,

                "risk_distribution": risk_distribution,

                "top_risky_additives": top_risky,

                "explanations": explanations,

            }

            # Cache the result
            self.cache.set(ingredients, result)

            return result

        except Exception as e:

            log.exception(f"Additive analysis failed: {e}")

            return {

                "detected_additives": [],
                "additive_count": 0,
                "regulatory_alerts": [],
                "error": str(e),

            }


# ==========================================================
# SINGLETON INSTANCE
# ==========================================================


additive_engine = AdditiveEngine()


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [

    "AdditiveEngine",
    "additive_engine",
    "AdditiveAIClient",
    "AdditiveAnalysisCache",

]


# ==========================================================
# INITIALIZATION LOG
# ==========================================================


log.info(
    "Additive Engine initialized",
    registry_size=len(additive_engine.registry),
    sugar_aliases_count=len(additive_engine.sugar_aliases),
    ai_enabled=bool(settings.OPENROUTER_API_KEY or settings.GEMINI_API_KEY),
)


# ==========================================================
# END OF FILE – additive_engine.py
# ==========================================================