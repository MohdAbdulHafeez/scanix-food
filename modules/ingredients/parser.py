# ==========================================================
# SCANIX AI
# SYSTEM 2 – INGREDIENT PARSER
# ELITE PRODUCTION GRADE – FINAL VERSION
# ==========================================================


from __future__ import annotations


import logging
import re

from dataclasses import dataclass
from dataclasses import asdict
from collections import Counter
from typing import Any
from typing import Dict
from typing import List
from typing import Set
from typing import Tuple


from rapidfuzz import fuzz


log = logging.getLogger(__name__)


# ==========================================================
# SECTION BOUNDARIES
# ==========================================================


SECTION_BOUNDARIES = [

    "allergen advice",

    "nutritional information",

    "nutrition facts",

    "nutrition information",

    "nutrition",

    "serving size",

    "barcode",

    "fssai",

    "manufactured by",

    "marketed by",

    "customer care",

    "storage instruction",

    "storage instructions",

    "best before",

    "net weight",

    "license no",

    "lic no",

    "contains permitted",

    "contains nature identical",

    "nature identical",

    "flavouring substances",

    "flavoring substances",

    "allergy advice",

]


# ==========================================================
# HIDDEN SUGARS
# ==========================================================


HIDDEN_SUGARS = {

    "corn syrup",

    "glucose syrup",

    "fructose",

    "dextrose",

    "maltose",

    "maltodextrin",

    "invert sugar",

    "cane syrup",

    "rice syrup",

    "molasses",

    "sucrose",

    "glucose",

    "hfcs",

    "jaggery",

    "honey",

    "brown sugar",

    "palm sugar",

    "coconut sugar",

    "date syrup",

    "agave nectar",

    "maple syrup",

    "barley malt",

    "rice malt",

    "corn sweetener",

    "fruit juice concentrate",

    "evaporated cane juice",

}


# ==========================================================
# HIDDEN FATS
# ==========================================================


HIDDEN_FATS = {

    "palm oil",

    "palmolein",

    "hydrogenated oil",

    "vegetable shortening",

    "partially hydrogenated oil",

    "vegetable fat",

    "vegetable fats",

    "palm kernel",

    "shea",

    "coconut oil",

    "margarine",

    "dalda",

    "vanaspati",

    "trans fat",

    "interesterified fat",

}


# ==========================================================
# PALM KEYWORDS
# ==========================================================


PALM_KEYWORDS = {

    "palm",

    "palmolein",

    "shea",

    "vegetable fat",

    "vegetable fats",

    "palm kernel",

    "palm oil",

}


# ==========================================================
# ALLERGEN KEYWORDS
# ==========================================================


ALLERGEN_KEYWORDS = {

    "milk",

    "milk solids",

    "whey",

    "casein",

    "soy",

    "gluten",

    "wheat",

    "nuts",

    "almond",

    "cashew",

    "peanut",

    "hazelnut",

    "walnut",

    "pistachio",

    "barley",

    "rye",

    "oats",

    "sesame",

    "mustard",

    "egg",

    "fish",

    "shellfish",

    "sulphites",

    "lupin",

    "celery",

}


# ==========================================================
# NATURAL KEYWORDS (Includes Indian Ingredients)
# ==========================================================


NATURAL_KEYWORDS = {

    "potato",

    "tomato",

    "onion",

    "garlic",

    "milk",

    "wheat",

    "corn",

    "rice",

    "salt",

    "water",

    "cocoa",

    "coconut",

    "almond",

    "peanut",

    "oats",

    "soy",

    "soybean",

    "fruit",

    "vegetable",

    # Indian natural ingredients
    "besan",

    "gram flour",

    "chickpea flour",

    "atta",

    "whole wheat flour",

    "maida",

    "suji",

    "semolina",

    "rava",

    "paneer",

    "ghee",

    "curd",

    "dahi",

    "yogurt",

    "buttermilk",

    "chaas",

    "lassi",

    "hing",

    "asafoetida",

    "ajwain",

    "carom seeds",

    "jeera",

    "cumin",

    "dhania",

    "coriander",

    "haldi",

    "turmeric",

    "mirch",

    "chilli",

    "elaichi",

    "cardamom",

    "dalchini",

    "cinnamon",

    "laung",

    "clove",

    "kali mirch",

    "black pepper",

    "saunf",

    "fennel",

    "methi",

    "fenugreek",

    "kasturi methi",

    "amchur",

    "dry mango powder",

    "tamarind",

    "imli",

    "coconut milk",

    "nariyal",

    "kaju",

    "cashew",

    "badam",

    "almond",

    "pista",

    "pistachio",

    "kishmish",

    "raisins",

    "chana",

    "chickpea",

    "masoor",

    "lentil",

    "moong",

    "mung bean",

    "urad",

    "black gram",

    "toor",

    "pigeon pea",

    "rajma",

    "kidney bean",

    "soya",

    "soybean",

    "palm jaggery",

    "nolen gur",

}


# ==========================================================
# PROCESSED KEYWORDS
# ==========================================================


PROCESSED_KEYWORDS = {

    "starch",

    "modified starch",

    "flour",

    "protein isolate",

    "maltodextrin",

    "vegetable oil",

    "refined oil",

    "glucose syrup",

    "corn syrup",

}


# ==========================================================
# ARTIFICIAL KEYWORDS
# ==========================================================


ARTIFICIAL_KEYWORDS = {

    "artificial flavour",

    "artificial flavor",

    "artificial colour",

    "artificial color",

    "synthetic",

    "flavour enhancer",

    "flavor enhancer",

    "msg",

    "monosodium glutamate",

}


# ==========================================================
# HIGH RISK ADDITIVES
# ==========================================================


HIGH_RISK_ADDITIVES = {

    "e102",

    "e110",

    "e129",

    "e133",

    "e211",

    "e220",

    "e250",

    "e621",

    "e951",

    "e955",

    "e124",

    "e127",

    "e150d",

    "e210",

    "e221",

    "e251",

    "e252",

    "e284",

    "e285",

    "e319",

    "e320",

    "e321",

    "e407",

    "e433",

    "e434",

    "e435",

    "e436",

    "e450",

    "e451",

    "e452",

    "e466",

    "e471",

    "e472a",

    "e472b",

    "e472c",

    "e472e",

    "e476",

    "e500",

    "e503",

    "e507",

    "e509",

    "e514",

    "e524",

    "e527",

    "e553b",

    "e620",

    "e622",

    "e623",

    "e624",

    "e625",

    "e627",

    "e631",

    "e635",

    "e901",

    "e904",

    "e905",

    "e950",

    "e952",

    "e953",

    "e954",

    "e955",

    "e956",

    "e961",

    "e962",

    "e964",

    "e965",

    "e966",

    "e967",

    "e968",

}


# ==========================================================
# INGREDIENT FUNCTIONS (Stabilizers, Emulsifiers, Preservatives)
# ==========================================================


FUNCTION_KEYWORDS = {

    "stabilizer": [

        "xanthan gum",

        "guar gum",

        "carrageenan",

        "agar agar",

        "pectin",

        "gellan gum",

        "locust bean gum",

        "cellulose gum",

        "carboxymethyl cellulose",

        "cmc",

        "methyl cellulose",

        "hydroxypropyl methylcellulose",

        "hpmc",

        "sodium alginate",

        "potassium alginate",

        "propylene glycol alginate",

    ],

    "emulsifier": [

        "lecithin",

        "soy lecithin",

        "sunflower lecithin",

        "monoglycerides",

        "diglycerides",

        "mono-diglycerides",

        "datem",

        "polyglycerol esters",

        "pgpr",

        "polysorbate 60",

        "polysorbate 65",

        "polysorbate 80",

        "sorbitan monostearate",

        "sucrose esters",

        "sodium stearoyl lactylate",

        "ssl",

        "calcium stearoyl lactylate",

        "csl",

    ],

    "preservative": [

        "sodium benzoate",

        "potassium sorbate",

        "calcium propionate",

        "sodium propionate",

        "sorbic acid",

        "benzoic acid",

        "nitrite",

        "sodium nitrite",

        "potassium nitrate",

        "sodium nitrate",

        "sulphur dioxide",

        "sulfite",

        "sodium metabisulfite",

        "potassium metabisulfite",

        "natamycin",

        "nisin",

        "ethylenediaminetetraacetic acid",

        "edta",

        "butylated hydroxyanisole",

        "bha",

        "butylated hydroxytoluene",

        "bht",

        "tert-butylhydroquinone",

        "tbhq",

    ],

    "thickener": [

        "corn starch",

        "maize starch",

        "potato starch",

        "tapioca starch",

        "modified starch",

        "modified corn starch",

        "wheat starch",

        "rice starch",

        "arrowroot",

        "gelatin",

    ],

    "acidity_regulator": [

        "citric acid",

        "lactic acid",

        "malic acid",

        "tartaric acid",

        "acetic acid",

        "phosphoric acid",

        "sodium citrate",

        "potassium citrate",

        "calcium citrate",

        "sodium acetate",

        "potassium acetate",

        "sodium carbonate",

        "potassium carbonate",

        "sodium bicarbonate",

        "baking soda",

    ],

    "anti_caking": [

        "silicon dioxide",

        "calcium silicate",

        "sodium aluminosilicate",

        "magnesium stearate",

        "calcium stearate",

        "talc",

        "tricalcium phosphate",

    ],

    "flavor_enhancer": [

        "monosodium glutamate",

        "msg",

        "disodium guanylate",

        "disodium inosinate",

        "disodium ribonucleotides",

        "yeast extract",

        "hydrolyzed vegetable protein",

        "hvp",

        "hydrolysed vegetable protein",

    ],

    "sweetener": [

        "aspartame",

        "sucralose",

        "saccharin",

        "acesulfame k",

        "acesulfame potassium",

        "stevia",

        "steviol glycosides",

        "neotame",

        "advantame",

        "cyclamate",

        "sodium cyclamate",

        "maltitol",

        "sorbitol",

        "xylitol",

        "erythritol",

        "isomalt",

        "lactitol",

    ],

    "color": [

        "tartrazine",

        "sunset yellow",

        "allura red",

        "brilliant blue",

        "indigo carmine",

        "erythrosine",

        "ponceau 4r",

        "carmoisine",

        "amaranth",

        "quinoline yellow",

        "caramel color",

        "caramel colour",

        "annatto",

        "curcumin",

        "titanium dioxide",

        "paprika extract",

        "beetroot red",

        "chlorophyll",

    ],

}


# ==========================================================
# JUNK PATTERNS
# ==========================================================


JUNK_PATTERNS = {

    "every bite",

    "bursting with flavour",

    "bursting with flavor",

    "carefully selected",

    "quality potatoes",

    "experts for",

    "to perfection",

    "deliciously seasoned",

    "great snack",

    "american style",

    "cream onion flavour",

}


# ==========================================================
# DATACLASSES
# ==========================================================


@dataclass
class IngredientRecord:

    name: str

    normalized_name: str

    category: str

    is_hidden_sugar: bool

    is_hidden_fat: bool

    is_additive_candidate: bool

    is_allergen: bool

    confidence: int

    weight: float

    functions: Dict[str, Any] = None


@dataclass
class IngredientProfile:

    ingredient_count: int

    natural_count: int

    processed_count: int

    artificial_count: int

    hidden_sugar_count: int

    hidden_fat_count: int

    additive_candidate_count: int

    contains_palm_oil: bool

    # New fields
    stabilizer_count: int = 0

    emulsifier_count: int = 0

    preservative_count: int = 0

    thickener_count: int = 0

    acidity_regulator_count: int = 0

    anti_caking_count: int = 0

    flavor_enhancer_count: int = 0

    artificial_sweetener_count: int = 0

    artificial_color_count: int = 0


# ==========================================================
# INGREDIENT PARSER
# ==========================================================


class IngredientParser:

    def __init__(self) -> None:

        self.known_ingredients: List[str] = list(
            NATURAL_KEYWORDS
            | PROCESSED_KEYWORDS
            | ARTIFICIAL_KEYWORDS
            | PALM_KEYWORDS
            | ALLERGEN_KEYWORDS
            | HIDDEN_SUGARS
            | HIDDEN_FATS
        )


    # ==========================================================
    # TEXT NORMALIZATION
    # ==========================================================

    @staticmethod
    def normalize_text(
        text: str,
    ) -> str:

        if not text:

            return ""

        text = text.replace(
            "\n",
            " ",
        )

        text = text.replace(
            "\r",
            " ",
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()


    @staticmethod
    def clean_ingredient_name(
        ingredient: str,
    ) -> str:

        if not ingredient:

            return ""

        ingredient = str(ingredient).lower()

        # ==========================================
        # REMOVE COMMON LABEL NOISE
        # ==========================================

        REMOVE_PATTERNS = [

            r"\ballergen advice\b.*",
            r"\bas favouring agent\b.*",
            r"\bas flavoring agent\b.*",
            r"\bas flavouring agent\b.*",

        ]

        for pattern in REMOVE_PATTERNS:

            ingredient = re.sub(
                pattern,
                "",
                ingredient,
                flags=re.IGNORECASE,
            )

        # ==========================================
        # REMOVE PERCENTAGES
        # ==========================================

        ingredient = re.sub(
            r"\d+(?:\.\d+)?%",
            "",
            ingredient,
        )

        # ==========================================
        # REMOVE STANDALONE NUMBERS
        # ==========================================

        ingredient = re.sub(
            r"\b(?!(e\d{3,4}|ins\d{3,4}|330|412|451|500|501|508|551|621|627|631|635)\b)\d+\b",
            "",
            ingredient,
            flags=re.IGNORECASE,
        )

        # ==========================================
        # OCR CORRECTIONS
        # ==========================================

        OCR_CORRECTIONS = {

            "sunilower":
            "sunflower",

            "vegetablk":
            "vegetable",

            "ediblk":
            "edible",

            "o1":
            "oil",

            "ol":
            "oil",

            "sal":
            "salt",

            "toial":
            "total",

            "soonm":
            "sodium",

            "soilids":
            "solids",

            "hydroilysed":
            "hydrolysed",

            "palmoilein":
            "palmolein",

            "milk to perfection solids":
            "milk solids",

            "paim oil":
            "palm oil",

            "ralm oil":
            "palm oil",

            "palm oi":
            "palm oil",

            "palm ol":
            "palm oil",

            "ralm cl":
            "palm oil",

            "palm cl":
            "palm oil",

            "palmoii":
            "palm oil",

            "paimolein":
            "palmolein",

            "mallodextrin":
            "maltodextrin",

            "hycrolysed":
            "hydrolysed",

            "edble":
            "edible",

            "poxder":
            "powder",

            "aavour":
            "flavour",

            "mkk solids":
            "milk solids",

            "mkk scids":
            "milk solids",

            "vegetable deliciously seasoned palmolein":
            "palmolein oil",

            "xanthum":
            "xanthan",

            "xanthun":
            "xanthan",

            "xanthen":
            "xanthan",

            "carboxymethylcellulose":
            "carboxymethyl cellulose",

            "sodiumbenzoate":
            "sodium benzoate",

            "potassiumsorbate":
            "potassium sorbate",

            "monosodiumglutamate":
            "monosodium glutamate",

        }

        for wrong, correct in (
            OCR_CORRECTIONS.items()
        ):

            ingredient = re.sub(

                rf"\b{re.escape(wrong)}\b",
                correct,
                ingredient,
                flags=re.IGNORECASE,

            )

        # ==========================================
        # SPECIAL NORMALIZATIONS
        # ==========================================

        ingredient = ingredient.replace(

            "anticaking agent 551",
            "anticaking agent e551",

        )

        ingredient = ingredient.replace(

            "anticaking agent",
            "anticaking agent",

        )

        ingredient = re.sub(
            r"\b627\b",
            "e627",
            ingredient,
        )

        ingredient = re.sub(
            r"\b631\b",
            "e631",
            ingredient,
        )

        ingredient = re.sub(
            r"\b551\b",
            "e551",
            ingredient,
        )

        # ==========================================
        # FORMAT E-NUMBERS
        # ==========================================

        ingredient = re.sub(
            r"\b(?:e|ins)[-\s]?(\d{3,4}[a-z]?)\b",
            r"e\1",
            ingredient,
            flags=re.IGNORECASE,
        )

        # ==========================================
        # REMOVE OCR SYMBOL GARBAGE
        # ==========================================

        ingredient = re.sub(
            r"[~\"'{}<>]",
            "",
            ingredient,
        )

        ingredient = re.sub(
            r"[|]",
            " ",
            ingredient,
        )

        ingredient = re.sub(
            r"\s+",
            " ",
            ingredient,
        )

        return ingredient.strip()


    def fuzzy_match_ingredient(
        self,
        ingredient: str,
        threshold: int = 85,
    ) -> Tuple[str, int]:

        """
        Fuzzy match ingredient against known ingredient database.

        Args:
            ingredient: OCR-extracted ingredient string
            threshold: Minimum similarity score (0-100)

        Returns:
            Tuple of (matched_name, confidence_score)
        """

        best_match = ingredient
        best_score = 100

        for known in self.known_ingredients:

            score = fuzz.ratio(
                ingredient.lower(),
                known.lower(),
            )

            if score > best_score:

                best_score = score
                best_match = known

        if best_score >= threshold:

            return best_match, best_score

        return ingredient, best_score


    # ==========================================================
    # SECTION EXTRACTION
    # ==========================================================

    def extract_ingredients_section(
        self,
        text: str,
    ) -> str:

        normalized = self.normalize_text(
            text,
        )

        pattern = re.compile(

            r"(?i)\b(?:ingredients?|ingredicnts|ingredents|ingrdients|seasoning\s*mix|seasoning|tastemaker|noodles|masala)\b[\s:;-]*"

        )

        match = pattern.search(
            normalized
        )

        start_index = -1

        if match:

            start_index = match.start()

        else:

            INGREDIENT_MARKERS = [

                "ingredients",

                "ingredient",

                "seasoning",

                "seasoning mix",

                "tastemaker",

                "noodles",

                "masala",

            ]

            words = normalized.split()

            for idx, word in enumerate(words):

                clean_word = re.sub(
                    r"[^a-zA-Z]",
                    "",
                    word.lower(),
                )

                for marker in INGREDIENT_MARKERS:

                    if fuzz.ratio(clean_word, marker) > 85:

                        start_index = normalized.find(
                            word,
                        )

                        break

                if start_index != -1:

                    break

        if start_index == -1:

            return ""

        section = normalized[
            start_index:
        ]

        lower_section = section.lower()

        cutoff = len(
            section,
        )

        for boundary in SECTION_BOUNDARIES:

            index = lower_section.find(
                boundary,
            )

            if index > 25:

                cutoff = min(
                    cutoff,
                    index,
                )

        return section[
            :cutoff
        ].strip()


    # ==========================================================
    # INGREDIENT SPLITTING
    # ==========================================================

    def split_ingredients(
        self,
        ingredients_text: str,
    ) -> List[str]:

        if not ingredients_text:

            return []

        # ==========================================
        # BRACKET EXPANSION (NO REMOVAL)
        # ==========================================

        ingredients_text = re.sub(
            r"[()\[\]]",
            ",",
            ingredients_text,
        )

        ingredients_text = ingredients_text.replace(
            ";",
            ",",
        )

        ingredients_text = ingredients_text.replace(
            "|",
            ",",
        )

        raw_items = re.split(

            r"[,•\n]+",

            ingredients_text,

        )

        cleaned = []

        for item in raw_items:

            item = self.clean_ingredient_name(
                item,
            )

            # Fuzzy match against known ingredients
            matched_item, match_confidence = self.fuzzy_match_ingredient(
                item,
                threshold=85,
            )

            if match_confidence >= 85:

                item = matched_item

            item = re.sub(
                r"^(ingredients?|ingredient)\s*:\s*",
                "",
                item,
                flags=re.IGNORECASE,
            )

            item = item.strip(" :,.-")

            if not item:

                continue

            if any(
                junk in item.lower()
                for junk in JUNK_PATTERNS
            ):
                continue

            if len(item) < 2 and not re.match(r"^e\d+$", item):

                continue

            if item in {

                "ingredients",
                "ingredient",
                "seasoning",
                "nutrition",
                "nutritional information",
                "allergen advice",

            }:

                continue

            cleaned.append(
                item,
            )

        return cleaned


    def deduplicate_ingredients(
        self,
        ingredients: List[str],
    ) -> List[str]:

        seen: Set[str] = set()

        unique = []

        for ingredient in ingredients:

            normalized = str(ingredient or "").lower()

            if normalized in seen:

                continue

            seen.add(
                normalized,
            )

            unique.append(
                ingredient,
            )

        return unique


    # ==========================================================
    # INGREDIENT CLASSIFICATION
    # ==========================================================

    def classify_ingredient(
        self,
        ingredient: str,
    ) -> str:

        ingredient = str(ingredient or "").lower()

        for keyword in ARTIFICIAL_KEYWORDS:

            if keyword in ingredient:

                return "artificial"

        for keyword in PROCESSED_KEYWORDS:

            if keyword in ingredient:

                return "processed"

        for keyword in NATURAL_KEYWORDS:

            if keyword in ingredient:

                return "natural"

        if re.search(

            r"\be\d{3,4}[a-z]?\b",

            ingredient,

            re.IGNORECASE,

        ):

            return "artificial"

        return "processed"


    def is_hidden_sugar(
        self,
        ingredient: str,
    ) -> bool:

        ingredient = str(ingredient or "").lower()

        return any(

            sugar in ingredient

            for sugar in HIDDEN_SUGARS

        )


    def is_hidden_fat(
        self,
        ingredient: str,
    ) -> bool:

        ingredient = str(ingredient or "").lower()

        return any(

            fat in ingredient

            for fat in HIDDEN_FATS

        )


    def is_palm_oil(
        self,
        ingredient: str,
    ) -> bool:

        ingredient = str(ingredient or "").lower()

        return any(

            palm in ingredient

            for palm in PALM_KEYWORDS

        )


    def is_allergen(
        self,
        ingredient: str,
    ) -> bool:

        ingredient = str(ingredient or "").lower()

        return any(

            allergen in ingredient

            for allergen in ALLERGEN_KEYWORDS

        )


    def is_additive_candidate(
        self,
        ingredient: str,
    ) -> bool:

        ingredient = str(ingredient or "").lower()

        if re.search(

            r"\be\d{3,4}[a-z]?\b",

            ingredient,

            re.IGNORECASE,

        ):

            return True

        additive_keywords = [

            "stabilizer",

            "emulsifier",

            "preservative",

            "colour",

            "color",

            "flavour",

            "flavor",

            "enhancer",

            "sweetener",

            "acidity regulator",

            "raising agent",

            "anti caking",

        ]

        return any(

            keyword in ingredient

            for keyword in additive_keywords

        )


    def detect_ingredient_function(
        self,
        ingredient: str,
    ) -> Dict[str, Any]:

        """
        Detect the functional role of an ingredient.

        Args:
            ingredient: Ingredient name

        Returns:
            Dictionary with functions, confidence, and risk level
        """

        ingredient_lower = ingredient.lower()

        detected_functions = []

        for function, keywords in FUNCTION_KEYWORDS.items():

            for keyword in keywords:

                if keyword in ingredient_lower:

                    detected_functions.append(function)

                    break

        return {

            "functions": list(set(detected_functions)),

            "has_stabilizer": "stabilizer" in detected_functions,

            "has_emulsifier": "emulsifier" in detected_functions,

            "has_preservative": "preservative" in detected_functions,

            "has_thickener": "thickener" in detected_functions,

            "has_acidity_regulator": "acidity_regulator" in detected_functions,

            "has_anti_caking": "anti_caking" in detected_functions,

            "has_flavor_enhancer": "flavor_enhancer" in detected_functions,

            "has_artificial_sweetener": (
                "sweetener" in detected_functions
                and ingredient_lower not in ["stevia", "steviol glycosides"]
            ),

            "has_artificial_color": (
                "color" in detected_functions
                and ingredient_lower not in ["annatto", "curcumin", "paprika extract", "beetroot red", "chlorophyll"]
            ),

            "confidence": 85 if detected_functions else 0,
        }


    # ==========================================================
    # INGREDIENT RECORD BUILDING
    # ==========================================================

    def calculate_ingredient_confidence(
        self,
        ingredient: str,
    ) -> int:

        if re.search(r"\be\d{3,4}[a-z]?\b", ingredient, re.IGNORECASE):

            return 95

        if len(ingredient) > 3 and ingredient.isalpha():

            return 90

        return 75


    def build_records(
        self,
        ingredients: List[str],
        min_confidence: int = 50,
    ) -> List[IngredientRecord]:

        records = []

        total_ingredients = len(ingredients)

        for index, ingredient in enumerate(ingredients):

            confidence = self.calculate_ingredient_confidence(
                ingredient,
            )

            # Skip low confidence ingredients
            if confidence < min_confidence:

                log.debug(
                    f"Skipping low confidence ingredient: {ingredient} (confidence={confidence})"
                )

                continue

            category = self.classify_ingredient(
                ingredient,
            )

            # Improved weight calculation based on position
            if total_ingredients <= 5:

                weight = 1.0

            elif index < 3:

                weight = 1.0

            elif index < 8:

                weight = 0.8

            elif index < 15:

                weight = 0.6

            else:

                weight = 0.4

            # Detect ingredient functions
            functions = self.detect_ingredient_function(
                ingredient,
            )

            record = IngredientRecord(

                name=ingredient,

                normalized_name=ingredient.lower(),

                category=category,

                is_hidden_sugar=self.is_hidden_sugar(
                    ingredient,
                ),

                is_hidden_fat=self.is_hidden_fat(
                    ingredient,
                ),

                is_additive_candidate=self.is_additive_candidate(
                    ingredient,
                ),

                is_allergen=self.is_allergen(
                    ingredient,
                ),

                confidence=confidence,

                weight=weight,

                functions=functions,

            )

            records.append(
                record,
            )

        return records


    # ==========================================================
    # PROFILE BUILDING
    # ==========================================================

    def build_profile(
        self,
        records: List[IngredientRecord],
    ) -> IngredientProfile:

        natural_count = 0

        processed_count = 0

        artificial_count = 0

        hidden_sugar_count = 0

        hidden_fat_count = 0

        additive_candidate_count = 0

        contains_palm_oil = False

        # New counters
        stabilizer_count = 0

        emulsifier_count = 0

        preservative_count = 0

        thickener_count = 0

        acidity_regulator_count = 0

        anti_caking_count = 0

        flavor_enhancer_count = 0

        artificial_sweetener_count = 0

        artificial_color_count = 0

        for record in records:

            if record.category == "natural":

                natural_count += 1

            elif record.category == "processed":

                processed_count += 1

            elif record.category == "artificial":

                artificial_count += 1

            if record.is_hidden_sugar:

                hidden_sugar_count += 1

            if record.is_hidden_fat:

                hidden_fat_count += 1

            if record.is_additive_candidate:

                additive_candidate_count += 1

            if self.is_palm_oil(record.normalized_name):

                contains_palm_oil = True

            # Count functions
            if record.functions:

                if record.functions.get("has_stabilizer"):

                    stabilizer_count += 1

                if record.functions.get("has_emulsifier"):

                    emulsifier_count += 1

                if record.functions.get("has_preservative"):

                    preservative_count += 1

                if record.functions.get("has_thickener"):

                    thickener_count += 1

                if record.functions.get("has_acidity_regulator"):

                    acidity_regulator_count += 1

                if record.functions.get("has_anti_caking"):

                    anti_caking_count += 1

                if record.functions.get("has_flavor_enhancer"):

                    flavor_enhancer_count += 1

                if record.functions.get("has_artificial_sweetener"):

                    artificial_sweetener_count += 1

                if record.functions.get("has_artificial_color"):

                    artificial_color_count += 1

        return IngredientProfile(

            ingredient_count=len(
                records,
            ),

            natural_count=natural_count,

            processed_count=processed_count,

            artificial_count=artificial_count,

            hidden_sugar_count=hidden_sugar_count,

            hidden_fat_count=hidden_fat_count,

            additive_candidate_count=additive_candidate_count,

            contains_palm_oil=contains_palm_oil,

            stabilizer_count=stabilizer_count,

            emulsifier_count=emulsifier_count,

            preservative_count=preservative_count,

            thickener_count=thickener_count,

            acidity_regulator_count=acidity_regulator_count,

            anti_caking_count=anti_caking_count,

            flavor_enhancer_count=flavor_enhancer_count,

            artificial_sweetener_count=artificial_sweetener_count,

            artificial_color_count=artificial_color_count,

        )


    # ==========================================================
    # E-NUMBER EXTRACTION
    # ==========================================================

    def extract_e_numbers(
        self,
        records: List[IngredientRecord],
    ) -> List[str]:

        e_numbers = []

        for record in records:

            matches = re.findall(

                r"\be(\d{3,4}[a-z]?)\b",

                record.normalized_name,

                re.IGNORECASE,

            )

            for match in matches:

                e_numbers.append(

                    f"E{match.upper()}"

                )

        return list(set(e_numbers))


    def extract_allergens(
        self,
        records: List[IngredientRecord],
    ) -> List[str]:

        allergens = []

        for record in records:

            for keyword in ALLERGEN_KEYWORDS:

                if keyword in record.normalized_name:

                    allergens.append(

                        keyword.upper()

                    )

        return list(set(allergens))


    def extract_high_risk_additives(
        self,
        e_numbers: List[str],
    ) -> List[str]:

        high_risk = []

        for e_num in e_numbers:

            if e_num.lower() in HIGH_RISK_ADDITIVES:

                high_risk.append(

                    e_num

                )

        return high_risk


    # ==========================================================
    # SCORE CALCULATIONS
    # ==========================================================

    def calculate_complexity_score(
        self,
        records: List[IngredientRecord],
    ) -> int:

        if not records:

            return 0

        score = 100

        score -= (
            len(records) * 2
        )

        chemical_names = 0

        for record in records:

            if len(
                record.name
            ) > 15:

                chemical_names += 1

        score -= (
            chemical_names * 3
        )

        score -= (

            sum(
                1
                for record in records
                if record.is_additive_candidate
            ) * 4

        )

        return max(
            min(score, 100),
            0,
        )


    def calculate_clean_label_score(
        self,
        profile: IngredientProfile,
    ) -> int:

        score = 100

        score -= (

            profile.artificial_count
            * 8

        )

        score -= (

            profile.additive_candidate_count
            * 5

        )

        score -= (

            profile.hidden_sugar_count
            * 6

        )

        score -= (

            profile.hidden_fat_count
            * 6

        )

        return max(
            min(score, 100),
            0,
        )


    def calculate_quality_score(
        self,
        profile: IngredientProfile,
        records: List[IngredientRecord],
    ) -> int:

        if not records:

            return 0

        total_weight = sum(
            record.weight
            for record
            in records
        )

        if total_weight == 0:

            return 0

        natural_weighted = sum(
            record.weight
            for record
            in records
            if record.category == "natural"
        )

        processed_weighted = sum(
            record.weight
            for record
            in records
            if record.category == "processed"
        )

        artificial_weighted = sum(
            record.weight
            for record
            in records
            if record.category == "artificial"
        )

        natural_ratio = (

            natural_weighted
            / total_weight

        )

        processed_ratio = (

            processed_weighted
            / total_weight

        )

        artificial_ratio = (

            artificial_weighted
            / total_weight

        )

        score = 50

        score += int(
            natural_ratio * 50
        )

        score -= int(
            processed_ratio * 15
        )

        score -= int(
            artificial_ratio * 35
        )

        score -= (

            profile.hidden_sugar_count
            * 5

        )

        score -= (

            profile.hidden_fat_count
            * 5

        )

        return max(
            min(score, 100),
            0,
        )


    def calculate_quality_grade(
        self,
        score: int,
    ) -> str:

        if score >= 95:

            return "A+"

        if score >= 90:

            return "A"

        if score >= 80:

            return "B"

        if score >= 70:

            return "C"

        if score >= 60:

            return "D"

        return "F"


    # ==========================================================
    # PROCESSING DETECTION
    # ==========================================================

    def detect_ultra_processed(
        self,
        profile: IngredientProfile,
        records: List[IngredientRecord],
    ) -> Dict[str, Any]:

        confidence = 0

        if profile.ingredient_count >= 12:

            confidence += 20

        if profile.additive_candidate_count >= 3:

            confidence += 30

        if profile.artificial_count >= 2:

            confidence += 20

        if profile.hidden_sugar_count >= 1:

            confidence += 10

        if profile.hidden_fat_count >= 1:

            confidence += 15

        if profile.ingredient_count >= 10:

            confidence += 15

        if profile.artificial_count >= 1 and profile.additive_candidate_count >= 2:

            confidence += 40

        # New: Check for stabilizers, emulsifiers, preservatives
        if profile.stabilizer_count >= 1:

            confidence += 10

        if profile.emulsifier_count >= 1:

            confidence += 10

        if profile.preservative_count >= 1:

            confidence += 15

        if profile.artificial_sweetener_count >= 1:

            confidence += 15

        if profile.artificial_color_count >= 1:

            confidence += 10

        trigger_keywords = {

            "maltodextrin",

            "flavour enhancer",

            "flavor enhancer",

            "hydrolysed",

            "hydrolyzed",

            "tastemaker",

            "seasoning",

            "instant noodle",

            "masala",

            "stabilizer",

            "emulsifier",

            "colour",

            "color",

            "preservative",

            "sweetener",

        }

        for record in records:

            text = record.normalized_name

            if any(

                keyword in text

                for keyword

                in trigger_keywords

            ):

                confidence += 5

            if re.search(r"\be\d{3,4}[a-z]?\b", text):

                confidence += 5

        confidence = min(
            confidence,
            100,
        )

        if confidence >= 60:

            level = "ULTRA_PROCESSED"

        elif confidence >= 35:

            level = "PROCESSED"

        else:

            level = "MINIMALLY_PROCESSED"

        return {

            "processing_level":
            level,

            "confidence":
            confidence,

        }


    # ==========================================================
    # MAIN ANALYZE METHOD
    # ==========================================================

    def analyze(
        self,
        text: str,
    ) -> Dict[str, Any]:

        try:

            section = (

                self.extract_ingredients_section(
                    text,
                )

            )

            ingredients = (

                self.split_ingredients(
                    section,
                )

            )

            ingredients = (

                self.deduplicate_ingredients(
                    ingredients,
                )

            )

            records = (

                self.build_records(
                    ingredients,
                )

            )

            profile = (

                self.build_profile(
                    records,
                )

            )

            complexity_score = (

                self.calculate_complexity_score(
                    records,
                )

            )

            clean_label_score = (

                self.calculate_clean_label_score(
                    profile,
                )

            )

            quality_score = (

                self.calculate_quality_score(
                    profile,
                    records,
                )

            )

            quality_grade = (

                self.calculate_quality_grade(
                    quality_score,
                )

            )

            processing = (

                self.detect_ultra_processed(
                    profile,
                    records,
                )

            )

            e_numbers = (

                self.extract_e_numbers(
                    records,
                )

            )

            allergens = (

                self.extract_allergens(
                    records,
                )

            )

            high_risk = (

                self.extract_high_risk_additives(
                    e_numbers,
                )

            )

            # Build ingredients list with functions
            ingredients_with_functions = []

            for record in records:

                ingredient_dict = asdict(
                    record,
                )

                # Ensure functions is included
                if "functions" not in ingredient_dict:

                    ingredient_dict["functions"] = {}

                ingredients_with_functions.append(
                    ingredient_dict,
                )

            return {

                "ingredient_profile":

                asdict(
                    profile,
                ),

                "ingredients":

                ingredients_with_functions,

                "registry": {

                    "e_numbers":
                    e_numbers,

                    "high_risk_additives":
                    high_risk,

                    "allergens":
                    allergens,

                    "contains_palm_oil":
                    profile.contains_palm_oil,

                },

                "scores": {

                    "quality_score":
                    quality_score,

                    "quality_grade":
                    quality_grade,

                    "clean_label_score":
                    clean_label_score,

                    "complexity_score":
                    complexity_score,

                },

                "processing_analysis":
                processing,

                "ingredient_summary": {

                    "ingredient_count":

                    profile.ingredient_count,

                    "natural_count":

                    profile.natural_count,

                    "processed_count":

                    profile.processed_count,

                    "artificial_count":

                    profile.artificial_count,

                    "hidden_sugars":

                    profile.hidden_sugar_count,

                    "hidden_fats":

                    profile.hidden_fat_count,

                    "additive_candidates":

                    profile.additive_candidate_count,

                    # New summary fields
                    "stabilizers":
                    profile.stabilizer_count,

                    "emulsifiers":
                    profile.emulsifier_count,

                    "preservatives":
                    profile.preservative_count,

                    "thickeners":
                    profile.thickener_count,

                    "acidity_regulators":
                    profile.acidity_regulator_count,

                    "anti_caking_agents":
                    profile.anti_caking_count,

                    "flavor_enhancers":
                    profile.flavor_enhancer_count,

                    "artificial_sweeteners":
                    profile.artificial_sweetener_count,

                    "artificial_colors":
                    profile.artificial_color_count,

                },

            }

        except Exception as e:

            log.exception(

                f"Ingredient parsing failed: {e}"

            )

            return {

                "ingredient_profile":
                {},

                "ingredients":
                [],

                "registry":
                {},

                "scores":
                {},

                "processing_analysis":
                {},

                "ingredient_summary":
                {},

                "error":

                str(e),

            }


# ==========================================================
# END OF FILE – parser.py
# ==========================================================