# ==========================================================
# SCANIX AI
# SYSTEM 1 - SCAN CONSTANTS
# ==========================================================


# ==========================================================
# UPLOAD
# ==========================================================

MAX_UPLOAD_MB = 10

MAX_SCAN_IMAGES = 4

SUPPORTED_IMAGE_TYPES = {

    "image/jpeg",

    "image/jpg",

    "image/png",

    "image/webp",

}


# ==========================================================
# OCR THRESHOLDS
# ==========================================================

MIN_OCR_CONFIDENCE = 0.40

GOOD_OCR_CONFIDENCE = 0.75

EXCELLENT_OCR_CONFIDENCE = 0.90


# ==========================================================
# SCAN QUALITY THRESHOLDS
# ==========================================================

HIGH_QUALITY_SCORE = 90

MEDIUM_QUALITY_SCORE = 70

LOW_QUALITY_SCORE = 50


# ==========================================================
# REGEX PATTERNS
# ==========================================================

E_NUMBER_PATTERN = r"(?:E|e|INS)\s*(\d{3,4}[A-Za-z]?)"


# ==========================================================
# OCR CORRECTIONS
# ==========================================================

OCR_CORRECTIONS = {

    "ingredicnts":
    "ingredients",

    "ingredents":
    "ingredients",

    "ingrdients":
    "ingredients",

    "seal":
    "shea",

    "lavourings":
    "flavourings",

    "diecolate":
    "chocolate",

}


# ==========================================================
# BRAND ALIASES
# ==========================================================

BRANDS = {

    "Lays": [

        "lays",

        "iays",

        "lays classic",

    ],

    "Doritos": [

        "doritos",

    ],

    "Pringles": [

        "pringles",

    ],

    "Cheetos": [

        "cheetos",

    ],

    "Oreo": [

        "oreo",

    ],

    "Maggi": [

        "maggi",

    ],

    "Yippee": [

        "yippee",

    ],

    "Coca Cola": [

        "coca cola",

        "coke",

    ],

    "Pepsi": [

        "pepsi",

    ],

    "Cadbury": [

        "cadbury",

        "dairy milk",

        "bournvita",

        "5 star",

    ],

    "Nestle": [

        "nestle",

        "kitkat",

        "munch",

        "milkybar",

        "cerelac",

    ],

    "Amul": [

        "amul",

        "amul dark",

        "amul milk",

    ],

    "Britannia": [

        "britannia",

        "good day",

        "bourbon",

        "nutrichoice",

        "milk bikis",

    ],

    "Parle": [

        "parle",

        "parle-g",

        "hide & seek",

        "krackjack",

        "monaco",

    ],

    "ITC": [

        "itc",

        "sunfeast",

        "bingo",

        "ashirvaad",

        "dark fantasy",

    ],

    "Red Bull": [

        "red bull",

    ],

    "Monster": [

        "monster",

        "monster energy",

    ],

    "Patanjali": [

        "patanjali",

    ],

    "Haldiram": [

        "haldiram",

        "haldirams",

        "haldiram's",

        "bhujia",

    ],

    "Kelloggs": [

        "kelloggs",

        "kellogg's",

        "corn flakes",

        "chocos",

        "muesli",

    ],

    "Hershey": [

        "hershey",

        "hershey's",

        "kisses",

        "syrup",

    ],

    "Mars": [

        "mars",

        "snickers",

        "twix",

        "bounty",

        "m&m",

    ],

    "Unilever": [

        "unilever",

        "kwality walls",

        "magnum",

        "knorr",

        "horlicks",

    ],

}


# ==========================================================
# INDIAN BRANDS (Additional)
# ==========================================================

INDIAN_BRANDS = {

    "Bingo": [

        "bingo",

        "tedhe medhe",

        "mad angles",

    ],

    "Kurkure": [

        "kurkure",

        "kurkure chilli chatka",

        "kurkure mutter",

    ],

    "Sunfeast": [

        "sunfeast",

        "dark fantasy",

        "mom's magic",

        "yipee",

    ],

    "Hide & Seek": [

        "hide & seek",

        "hide n seek",

        "hide and seek",

    ],

    "Nutrichoice": [

        "nutrichoice",

        "nutri choice",

        "nutri-choice",

    ],

    "Unibic": [

        "unibic",

        "unibic cookies",

    ],

    "McVities": [

        "mcvities",

        "mc vities",

        "digestive",

    ],

    "Paper Boat": [

        "paper boat",

        "paperboat",

        "paper boat drinks",

    ],

    "Raw Pressery": [

        "raw pressery",

        "rawpressery",

    ],

    "Tropicana": [

        "tropicana",

        "tropicana juice",

    ],

    "Real": [

        "real juice",

        "real fruit juice",

    ],

    "MuscleBlaze": [

        "muscleblaze",

        "muscle blaze",

        "mb",

    ],

    "Yogabar": [

        "yogabar",

        "yoga bar",

    ],

    "The Whole Truth": [

        "the whole truth",

        "whole truth",

        "twt",

    ],

    "Epigamia": [

        "epigamia",

        "epigamia greek yogurt",

    ],

    "Saffola": [

        "saffola",

        "saffola oats",

    ],

    "True Elements": [

        "true elements",

        "true elements muesli",

    ],

    "Bagrry's": [

        "bagrry's",

        "bagrrys",

        "bagrry",

    ],

    "Quaker": [

        "quaker",

        "quaker oats",

    ],

    "Organic India": [

        "organic india",

        "organic india muesli",

    ],

    "Fast&Up": [

        "fast&up",

        "fastandup",

        "fast and up",

    ],

    "Sting": [

        "sting",

        "sting energy",

    ],

    "Thums Up": [

        "thums up",

        "thumsup",

        "thumbs up",

    ],

    "Sprite": [

        "sprite",

        "sprite lemon",

    ],

    "Limca": [

        "limca",

        "limca lemon",

    ],

    "Fanta": [

        "fanta",

        "fanta orange",

    ],

    "Maaza": [

        "maaza",

        "maaza mango",

    ],

    "Slice": [

        "slice",

        "slice mango",

    ],

    "Frooti": [

        "frooti",

        "frooti mango drink",

    ],

    "Appy": [

        "appy",

        "appy fizz",

    ],

    "Naturals": [

        "naturals",

        "naturals ice cream",

    ],

    "Havmor": [

        "havmor",

        "havmor ice cream",

    ],

    "Kwality Walls": [

        "kwality walls",

        "kwality",

        "cornetto",

    ],

    "Baskin Robbins": [

        "baskin robbins",

        "baskin",

        "br",

    ],

    "Ching's Secret": [

        "ching's secret",

        "chings secret",

        "ching",

    ],

    "Knorr": [

        "knorr",

        "knorr soupy noodles",

    ],

    "Top Ramen": [

        "top ramen",

        "top ramen curry",

    ],

    "Wai Wai": [

        "wai wai",

        "wai wai noodles",

    ],

    "Soyakult": [

        "soyakult",

        "soya kult",

    ],

    "Mother Dairy": [

        "mother dairy",

        "mother dairy milk",

    ],

    "Nandini": [

        "nandini",

        "nandini milk",

    ],

    "Milkymist": [

        "milkymist",

        "milky mist",

    ],

    "Go Cheese": [

        "go cheese",

        "go cheese slice",

    ],

    "Dlecta": [

        "dlecta",

        "dlecta cheese",

    ],

}


# ==========================================================
# CATEGORY KEYWORDS
# ==========================================================

CATEGORY_KEYWORDS = {

    "chips": [

        "chips",

        "potato",

        "onion",

        "cream",

        "nacho",

        "crisps",

    ],

    "soft_drink": [

        "cola",

        "soda",

        "carbonated",

        "beverage",

    ],

    "noodles": [

        "noodle",

        "masala",

        "instant",

        "ramen",

    ],

    "biscuits": [

        "cookie",

        "biscuit",

        "cream biscuit",

        "cracker",

    ],

    "protein": [

        "protein",

        "whey",

        "isolate",

    ],

    "chocolate": [

        "cocoa",

        "cocoa butter",

        "cocoa mass",

        "milk chocolate",

        "dark chocolate",

        "cadbury",

        "chocolate",

    ],

    "ice_cream": [

        "ice cream",

        "frozen dessert",

        "gelato",

        "sorbet",

    ],

    "energy_drink": [

        "energy drink",

        "caffeine",

        "taurine",

    ],

    "breakfast_cereal": [

        "cereal",

        "flakes",

        "muesli",

        "granola",

        "oats",

    ],

    "protein_bar": [

        "protein bar",

        "energy bar",

        "nutrition bar",

    ],

    "cookies": [

        "cookie",

        "chocochip",

    ],

    "cakes": [

        "cake",

        "muffin",

        "brownie",

        "cupcake",

        "pastry",

    ],

    "milk_product": [

        "milk",

        "dairy",

        "paneer",

        "butter",

        "ghee",

    ],

    "yogurt": [

        "yogurt",

        "yoghurt",

        "curd",

        "dahi",

    ],

    "cheese": [

        "cheese",

        "cheddar",

        "mozzarella",

        "slice",

        "spread",

    ],

    "fruit_juice": [

        "juice",

        "nectar",

        "fruit drink",

        "100% juice",

    ],

    "sports_drink": [

        "sports drink",

        "electrolyte",

        "hydration",

    ],

    "ready_to_eat": [

        "ready to eat",

        "rte",

        "heat and eat",

        "meal",

    ],

    "baby_food": [

        "baby food",

        "infant formula",

        "cerelac",

        "farex",

    ],

    "supplements": [

        "supplement",

        "vitamin",

        "mineral",

        "capsule",

        "tablet",

    ],

}


# ==========================================================
# CATEGORY MAPPINGS (For System 2-7)
# ==========================================================

CATEGORY_MAPPINGS = {

    "chips": "CHIPS_AND_CRISPS",

    "crisps": "CHIPS_AND_CRISPS",

    "namkeen": "NAMKEEN_AND_SNACKS",

    "snacks": "NAMKEEN_AND_SNACKS",

    "biscuits": "BISCUITS_AND_COOKIES",

    "cookies": "BISCUITS_AND_COOKIES",

    "chocolate": "CHOCOLATES_AND_CANDIES",

    "candy": "CHOCOLATES_AND_CANDIES",

    "ice_cream": "ICE_CREAMS_AND_DESSERTS",

    "dessert": "ICE_CREAMS_AND_DESSERTS",

    "soft_drink": "SOFT_DRINKS_AND_BEVERAGES",

    "beverage": "SOFT_DRINKS_AND_BEVERAGES",

    "energy_drink": "ENERGY_DRINKS",

    "noodles": "NOODLES_AND_PASTA",

    "pasta": "NOODLES_AND_PASTA",

    "cereal": "BREAKFAST_CEREALS",

    "protein_bar": "PROTEIN_BARS",

    "energy_bar": "PROTEIN_BARS",

    "dairy": "DAIRY_AND_ALTERNATIVES",

    "milk_product": "DAIRY_AND_ALTERNATIVES",

    "yogurt": "DAIRY_AND_ALTERNATIVES",

    "cheese": "DAIRY_AND_ALTERNATIVES",

    "paneer": "DAIRY_AND_ALTERNATIVES",

    "bread": "BREADS_AND_BAKERY",

    "bakery": "BREADS_AND_BAKERY",

    "jam": "SPREADS_AND_JAMS",

    "spread": "SPREADS_AND_JAMS",

    "sauce": "SAUCES_AND_CHUTNEYS",

    "chutney": "SAUCES_AND_CHUTNEYS",

    "pickle": "PICKLES",

    "papad": "PAPADS",

    "sweet": "INDIAN_SWEETS",

    "mithai": "INDIAN_SWEETS",

    "health_drink": "HEALTH_DRINKS",

    "baby_food": "BABY_FOODS",

    "frozen": "FROZEN_FOODS",

    "rte": "READY_TO_EAT_MEALS",

    "ayurvedic": "AYURVEDIC_PRODUCTS",

}


# ==========================================================
# POSITIVE INGREDIENTS
# ==========================================================

POSITIVE_INGREDIENTS = {

    "protein": "Contains Protein",

    "fiber": "Contains Fiber",

    "whole grain": "Contains Whole Grain",

    "milk": "Contains Dairy",

    "oats": "Contains Oats",

    "almond": "Contains Almonds",

    "peanut": "Contains Peanuts",

    "whey": "Contains Whey",

    "soy protein": "Contains Soy Protein",

}


# ==========================================================
# NEGATIVE INGREDIENTS
# ==========================================================

NEGATIVE_INGREDIENTS = {

    "maltodextrin": "Highly Processed Additive",

    "artificial flavor": "Artificial Flavoring",

    "artificial colour": "Artificial Coloring",

    "food color": "Artificial Coloring",

    "color": "Artificial Coloring",

    "chips": "Ultra Processed Carbohydrate",

    "hydrogenated": "Processed Fat",

}


# ==========================================================
# PALM OIL INTELLIGENCE
# ==========================================================

PALM_OIL_KEYWORDS = [

    "palm",

    "palm oil",

    "palm kernel",

    "vegetable fat",

    "vegetable fats",

    "palmolein",

]


# ==========================================================
# ULTRA PROCESSED INDICATORS
# ==========================================================

ULTRA_PROCESSED_KEYWORDS = [

    "emulsifier",

    "stabilizer",

    "preservative",

    "artificial flavour",

    "artificial flavor",

    "artificial color",

    "artificial colour",

    "sweetener",

    "maltodextrin",

    "hydrogenated",

    "acidity regulator",

]


# ==========================================================
# PROCESSING LEVEL DETECTION
# ==========================================================

PROCESSING_LEVEL_KEYWORDS = {

    "RAW": [

        "raw",

        "unprocessed",

        "whole",

        "fresh",

    ],

    "MINIMALLY_PROCESSED": [

        "minimally processed",

        "lightly processed",

        "cold pressed",

        "stone ground",

        "traditionally made",

    ],

    "PROCESSED": [

        "processed",

        "cooked",

        "baked",

        "roasted",

        "pasteurized",

        "fermented",

    ],

    "HIGHLY_PROCESSED": [

        "highly processed",

        "refined",

        "hydrogenated",

    ],

    "ULTRA_PROCESSED": [

        "ultra processed",

        "ultra-processed",

        "artificial",

        "emulsifier",

        "stabilizer",

        "preservative",

        "artificial flavour",

        "artificial flavor",

        "artificial colour",

        "artificial color",

        "sweetener",

        "maltodextrin",

        "hydrogenated",

        "acidity regulator",

        "flavour enhancer",

        "flavor enhancer",

    ],

}


# ==========================================================
# NOVA GROUP KEYWORDS
# ==========================================================

NOVA_GROUP_KEYWORDS = {

    1: [

        "unprocessed",

        "minimally processed",

        "fresh",

        "raw",

        "whole",

        "natural",

    ],

    2: [

        "minimally processed",

        "lightly processed",

        "cold pressed",

        "stone ground",

    ],

    3: [

        "processed",

        "cooked",

        "baked",

        "roasted",

        "pasteurized",

    ],

    4: [

        "ultra processed",

        "ultra-processed",

        "artificial",

        "emulsifier",

        "stabilizer",

        "preservative",

        "sweetener",

    ],

}


# ==========================================================
# PRESERVATIVES
# ==========================================================

PRESERVATIVES = [

    "sodium benzoate",

    "potassium sorbate",

    "benzoate",

    "sorbate",

    "e211",

    "e202",

]


# ==========================================================
# ADDITIVES
# ==========================================================

ADDITIVES = [

    "citric acid",

    "monosodium glutamate",

    "msg",

    "stabilizer",

    "emulsifier",

    "flavour enhancer",

    "colour",

    "color",

    "preservative",

    "acidity regulator",

    "raising agent",

    "anti caking agent",

    "anti-caking agent",

    "sweetener",

    "glazing agent",

]


# ==========================================================
# HIGH RISK E-NUMBERS (India-specific)
# ==========================================================

HIGH_RISK_E_NUMBERS = {

    "E102": "Tartrazine – Banned in several countries, hyperactivity risk",

    "E104": "Quinoline Yellow – Restricted in many countries",

    "E110": "Sunset Yellow – Hyperactivity in children",

    "E120": "Cochineal – Allergen risk",

    "E122": "Carmoisine – Banned in some countries",

    "E123": "Amaranth – Banned in some countries",

    "E124": "Ponceau 4R – Banned in some countries",

    "E127": "Erythrosine – Thyroid concerns",

    "E128": "Red 2G – Banned in some countries",

    "E129": "Allura Red – Hyperactivity risk",

    "E133": "Brilliant Blue FCF – Asthma risk",

    "E142": "Green S – Banned in some countries",

    "E150d": "Caramel Colour – Contains 4-MEI (possible carcinogen)",

    "E210": "Benzoic Acid – Asthma, skin irritation",

    "E211": "Sodium Benzoate – Forms benzene (carcinogen)",

    "E220": "Sulphur Dioxide – Asthma trigger",

    "E221": "Sodium Sulphite – Allergic reactions",

    "E250": "Sodium Nitrite – Forms nitrosamines (carcinogenic)",

    "E251": "Sodium Nitrate – Forms nitrosamines",

    "E252": "Potassium Nitrate – Forms nitrosamines",

    "E284": "Boric Acid – Banned in some countries",

    "E285": "Borax – Banned",

    "E310": "Propyl Gallate – Banned in some countries",

    "E311": "Octyl Gallate – Banned in some countries",

    "E312": "Dodecyl Gallate – Banned in some countries",

    "E319": "TBHQ – Banned in some countries",

    "E320": "BHA – Endocrine disruptor, possible carcinogen",

    "E321": "BHT – Endocrine disruptor",

    "E330": "Citric Acid – Safe, but excess causes issues",

    "E338": "Phosphoric Acid – Tooth erosion, kidney issues",

    "E339": "Sodium Phosphate – Kidney risk",

    "E340": "Potassium Phosphate – Kidney risk",

    "E341": "Calcium Phosphate – Generally safe",

    "E385": "Calcium Disodium EDTA – Generally safe",

    "E407": "Carrageenan – Gut inflammation, cancer risk",

    "E412": "Guar Gum – May cause bloating",

    "E415": "Xanthan Gum – Digestive issues",

    "E420": "Sorbitol – Laxative effect",

    "E421": "Mannitol – Laxative effect",

    "E422": "Glycerol – Headaches, dizziness",

    "E431": "Polyoxyethylene Stearate – Banned in some countries",

    "E432": "Polysorbate 20 – Concerns",

    "E433": "Polysorbate 80 – Gut inflammation",

    "E434": "Polysorbate 40 – Concerns",

    "E435": "Polysorbate 60 – Concerns",

    "E436": "Polysorbate 65 – Concerns",

    "E450": "Diphosphates – Affects calcium absorption",

    "E451": "Triphosphates – Affects calcium absorption",

    "E452": "Polyphosphates – Affects calcium absorption",

    "E466": "CMC – May cause digestive issues",

    "E471": "Mono- and Diglycerides – May contain trans fats",

    "E472a": "Acetic Acid Esters – May contain trans fats",

    "E472b": "Lactic Acid Esters – May contain trans fats",

    "E472c": "Citric Acid Esters – May contain trans fats",

    "E472e": "DATEM – May contain trans fats",

    "E473": "Sucrose Esters – Generally safe",

    "E474": "Sucroglycerides – Generally safe",

    "E475": "Polyglycerol Esters – Generally safe",

    "E476": "PGPR – May contain trans fats",

    "E477": "Propylene Glycol Esters – Generally safe",

    "E500": "Sodium Carbonate – Digestive upset",

    "E503": "Ammonium Carbonate – Nausea risk",

    "E507": "Hydrochloric Acid – Tooth erosion",

    "E509": "Calcium Chloride – Digestive issues",

    "E512": "Stannous Chloride – Banned in some countries",

    "E514": "Sodium Sulphate – Laxative effect",

    "E524": "Sodium Hydroxide – Burns tissue",

    "E527": "Ammonium Hydroxide – Banned in some countries",

    "E553b": "Talc – Possible carcinogen",

    "E620": "Glutamic Acid – Concerns",

    "E621": "MSG – Headaches, nausea, weakness",

    "E622": "Monopotassium Glutamate – Similar to MSG",

    "E623": "Calcium Glutamate – Similar to MSG",

    "E624": "Monoammonium Glutamate – Similar to MSG",

    "E625": "Magnesium Glutamate – Similar to MSG",

    "E627": "Disodium Guanylate – May trigger gout",

    "E631": "Disodium Inosinate – May trigger gout",

    "E635": "Disodium Ribonucleotides – May trigger asthma",

    "E901": "Beeswax – Allergen risk",

    "E904": "Shellac – Derived from insects",

    "E905": "Microcrystalline Wax – Indigestible",

    "E950": "Acesulfame K – May affect insulin",

    "E951": "Aspartame – Headaches, neurotoxicity concerns",

    "E952": "Cyclamic Acid – Cancer concerns",

    "E953": "Isomalt – Laxative effect",

    "E954": "Saccharin – Cancer concerns (historical)",

    "E955": "Sucralose – May affect gut bacteria",

    "E956": "Alitame – Limited research",

    "E957": "Thaumatin – Generally safe",

    "E959": "Neohesperidine – Generally safe",

    "E961": "Neotame – Similar to aspartame",

    "E962": "Aspartame-Acesulfame Salt – Combined effects",

    "E963": "Tagatose – Generally safe",

    "E964": "Polyglycitol – Laxative effect",

    "E965": "Maltitol – Laxative effect",

    "E966": "Lactitol – Laxative effect",

    "E967": "Xylitol – Safe for humans, toxic to dogs",

    "E968": "Erythritol – Digestive issues",

}

# High risk E-numbers list (for quick lookup)
HIGH_RISK_E_NUMBERS_LIST = list(HIGH_RISK_E_NUMBERS.keys())


# ==========================================================
# ARTIFICIAL INGREDIENTS
# ==========================================================

ARTIFICIAL_INGREDIENTS = [

    "artificial",

    "synthetic",

    "food color",

    "artificial flavour",

    "artificial flavor",

    "nature identical",

]


# ==========================================================
# HIDDEN SUGARS
# ==========================================================

HIDDEN_SUGARS = [

    "maltose",

    "dextrose",

    "fructose",

    "glucose syrup",

    "corn syrup",

    "rice syrup",

    "invert syrup",

    "maltodextrin",

    "glucose",

    "hfcs",

    "high fructose corn syrup",

    "brown sugar",

    "invert sugar",

    "sucrose",

    "molasses",

    "treacle",

    "honey",

    "agave",

    "jaggery",

    "fruit concentrate",

    "malt extract",

    "liquid glucose",

]


# ==========================================================
# HIDDEN FATS
# ==========================================================

HIDDEN_FATS = [

    "hydrogenated oil",

    "partially hydrogenated",

    "vanaspati",

    "dalda",

    "trans fat",

    "shortening",

    "margarine",

    "palmolein",

    "palm oil",

    "coconut oil",

    "vegetable oil",

    "sunflower oil",

    "soybean oil",

    "canola oil",

    "refined oil",

]


# ==========================================================
# ALLERGENS
# ==========================================================

ALLERGENS = [

    "milk",

    "soy",

    "gluten",

    "egg",

    "nuts",

    "peanut",

    "fish",

    "shellfish",

    "sesame",

    "wheat",

    "barley",

    "rye",

    "oats",

    "cashew",

    "almond",

    "hazelnut",

    "walnut",

    "pistachio",

    "mustard",

    "sulphites",

    "lupin",

    "celery",

]


# ==========================================================
# ALLERGEN ALIASES
# ==========================================================

ALLERGEN_ALIASES = {

    "milk": [

        "milk solids",

        "skim milk",

        "whey",

        "milk powder",

        "butter",

        "cheese",

        "ghee",

        "lactose",

        "casein",

    ],

    "nuts": [

        "almond",

        "cashew",

        "hazelnut",

        "walnut",

        "pistachio",

        "macadamia",

        "pecan",

        "brazil nut",

    ],

    "wheat": [

        "wheat flour",

        "maida",

        "suji",

        "semolina",

        "whole wheat",

        "graham",

    ],

    "soy": [

        "soybean",

        "soya",

        "soy lecithin",

        "edamame",

        "tofu",

    ],

}


# ==========================================================
# RISK KEYWORDS
# ==========================================================

RISK_KEYWORDS = {

    "salt": "High Sodium",

    "sugar": "Sugar Exposure",

    "oil": "Processed Oil",

    "trans fat": "Trans Fat Risk",

    "hydrogenated": "Processed Fat Risk",

}


# ==========================================================
# MARKETING CLAIMS
# ==========================================================

MARKETING_CLAIMS = [

    "high protein",

    "protein rich",

    "sugar free",

    "no added sugar",

    "organic",

    "natural",

    "low fat",

    "high fiber",

    "gluten free",

]


# ==========================================================
# SECTION DETECTION
# ==========================================================

SECTION_KEYWORDS = {

    "nutrition_table": [

        "nutrition facts",

        "energy",

        "calories",

        "protein",

        "nutritional information",

    ],

    "ingredients": [

        "ingredients",

        "ingredients:",

        "contains",

        "ingredicnts",

        "ingredents",

        "ingrdients",

    ],

    "barcode": [

        "barcode",

    ],

    "claims": [

        "high protein",

        "sugar free",

        "organic",

    ],

}


# ==========================================================
# PRODUCT IMAGES
# ==========================================================

PRODUCT_IMAGES = {

    "Lays": (
        "https://images.openfoodfacts.org/images/products/"
        "8901491101837/front_en.5.full.jpg"
    ),

    "Doritos": (
        "https://images.openfoodfacts.org/images/products/"
        "8410199018438/front_en.5.full.jpg"
    ),

    "Pringles": (
        "https://images.openfoodfacts.org/images/products/"
        "5053990156000/front_en.3.full.jpg"
    ),

}


# ==========================================================
# NUTRISCORE RULES
# ==========================================================

NUTRISCORE_THRESHOLDS = {

    "A": 0,

    "B": 2,

    "C": 4,

    "D": 6,

    "E": 8,

}


# ==========================================================
# RECOMMENDATION RULES
# ==========================================================

RECOMMENDATION_RULES = {

    "excellent": "DAILY",

    "good": "WEEKLY",

    "average": "OCCASIONAL",

    "poor": "AVOID",

}


# ==========================================================
# HEALTH SCORE WEIGHTS (For System 3-4)
# ==========================================================

HEALTH_SCORE_WEIGHTS = {

    "sugar": 25,

    "sodium": 20,

    "saturated_fat": 15,

    "fiber": 15,

    "protein": 10,

    "processing": 15,

}

HEALTH_SCORE_THRESHOLDS = {

    "excellent": 80,

    "good": 70,

    "average": 50,

    "poor": 30,

}