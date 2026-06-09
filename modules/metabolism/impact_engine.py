# ==========================================================
# SCANIX AI
# SYSTEM 3 – METABOLIC INTELLIGENCE (IMPACT ENGINE)
# ELITE PRODUCTION GRADE – FINAL VERSION
# ==========================================================


from __future__ import annotations


from typing import Any
from typing import Dict
from typing import List
from typing import Optional


# ==========================================================
# IMPACT ENGINE
# ==========================================================


class ImpactEngine:
    """
    Metabolic Intelligence Engine for System 3.

    Analyzes food products across multiple dimensions:
    - Satiety and hunger response
    - Energy curve and crash probability
    - Metabolic load and processing impact
    - Persona-based analysis (weight loss, diabetic, heart, etc.)
    - Longevity and metabolic flexibility
    """

    # =====================================================
    # VERIFICATION BONUS CONSTANTS
    # =====================================================

    VERIFICATION_BONUS_MAP = {

        "HIGH": 15,

        "MEDIUM": 8,

        "LOW": 0,

    }

    HIGH_QUALITY_PROTEINS = [

        "whey",
        "casein",
        "milk protein",
        "soy isolate",
        "soy protein",
        "pea protein",
        "protein isolate",

    ]

    HIGH_SUGAR_CATEGORIES = {

        "chocolate",
        "candy",
        "confectionery",
        "cookies",
        "biscuit",
        "wafer",
        "cake",
        "pastry",
        "dessert",
        "ice cream",
        "sweet snack",
        "sweetened beverage",
        "soft drink",
        "energy drink",

    }

    # =====================================================
    # SAFE HELPERS
    # =====================================================

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

    def _safe_int(
        self,
        value: Any,
        default: int = 0,
    ) -> int:
        """
        Safely convert value to int.

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

    def _verification_bonus(
        self,
        verification_level: str,
    ) -> int:
        """
        Calculate bonus based on verification level.

        Args:
            verification_level: HIGH, MEDIUM, or LOW

        Returns:
            Bonus points (15, 8, or 0)
        """

        return self.VERIFICATION_BONUS_MAP.get(
            verification_level,
            0,
        )

    def _get_protein_quality_bonus(
        self,
        ingredient_intelligence: Dict[str, Any],
    ) -> int:
        """
        Calculate bonus for high-quality protein sources.

        Args:
            ingredient_intelligence: Ingredient analysis data

        Returns:
            Bonus points (15 if high-quality protein found, else 0)
        """

        bonus = 0

        ingredients = (

            ingredient_intelligence
            .get(
                "ingredients",
                [],
            )

        )

        for item in ingredients:

            name = str(
                item.get(
                    "name",
                    "",
                )
                or
                ""
            ).lower()

            if any(
                hq in name
                for hq in self.HIGH_QUALITY_PROTEINS
            ):

                bonus += 15

                break

        return bonus

    # =====================================================
    # DATA EXTRACTION
    # =====================================================

    def extract_signals(
        self,
        nutrition: Dict[str, Any],
        ingredient_intelligence: Dict[str, Any],
        product: Dict[str, Any],
        scan_quality: Dict[str, Any],
        verification: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Extract all signals from input data for metabolic analysis.

        Args:
            nutrition: Nutrition data from System 1
            ingredient_intelligence: Ingredient analysis from System 2
            product: Product data from System 1
            scan_quality: Scan quality data from System 1
            verification: Verification data from System 1

        Returns:
            Dictionary of extracted signals
        """

        if verification is None:

            verification = {}

        registry = (

            ingredient_intelligence
            .get(
                "registry",
                {},
            )

        )

        ingredient_summary = (

            ingredient_intelligence
            .get(
                "ingredient_summary",
                {},
            )

        )

        processing = (

            ingredient_intelligence
            .get(
                "processing_analysis",
                {},
            )

        )

        additive_count = max(

            self._safe_int(

                ingredient_intelligence.get(
                    "ingredient_profile",
                    {},
                ).get(
                    "additive_count",
                    0,
                )

            ),

            len(

                ingredient_intelligence.get(
                    "additives",
                    {},
                ).get(
                    "detected_additives",
                    [],
                )

            ),

        )

        return {

            # Nutrition
            "protein":
            self._safe_float(
                nutrition.get(
                    "protein",
                    0,
                )
            ),

            "fiber":
            self._safe_float(
                nutrition.get(
                    "fiber",
                    0,
                )
            ),

            "sugar":
            self._safe_float(
                nutrition.get(
                    "sugar",
                    0,
                )
            ),

            "sodium":
            self._safe_float(
                nutrition.get(
                    "sodium",
                    0,
                )
            ),

            "carbohydrates":
            self._safe_float(
                nutrition.get(
                    "carbohydrates",
                    nutrition.get(
                        "carbs",
                        0,
                    ),
                )
            ),

            "saturated_fat":
            self._safe_float(
                nutrition.get(
                    "saturated_fat",
                    0,
                )
            ),

            "trans_fat":
            self._safe_float(
                nutrition.get(
                    "trans_fat",
                    0,
                )
            ),

            "fat":
            self._safe_float(
                nutrition.get(
                    "fat",
                    0,
                )
            ),

            "calories":
            self._safe_float(
                nutrition.get(
                    "calories",
                    0,
                )
            ),

            # System 2
            "hidden_sugars":

            self._safe_int(

                registry
                .get(
                    "hidden_sugars",
                    {},
                )
                .get(
                    "hidden_sugar_count",
                    0,
                )

            ),

            "additive_count":

            additive_count,

            "contains_palm_oil":

            bool(

                registry.get(
                    "contains_palm_oil",
                    False,
                )

            ),

            "processing_level":

            processing.get(
                "processing_level",
                "UNKNOWN",
            ),

            # System 1
            "category":

            product.get(
                "category",
                "unknown",
            ),

            "scan_quality_score":

            self._safe_int(

                scan_quality.get(
                    "scan_quality_score",
                    50,
                )

            ),

            "verification_level":

            verification.get(
                "verification_level",
                "LOW",
            ),

        }

    # =====================================================
    # SATIETY ENGINE
    # =====================================================

    def calculate_satiety(
        self,
        signals: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Calculate satiety score (0-100) and hunger return time.

        Args:
            signals: Extracted signals from extract_signals()

        Returns:
            Satiety score, verdict, hunger return time, and reasons
        """

        score = 30

        reasons: List[str] = []

        protein = signals["protein"]

        fiber = signals["fiber"]

        calories = signals["calories"]

        if protein >= 20:

            score += 30

            reasons.append(
                "High protein improves satiety"
            )

        elif protein >= 10:

            score += 15

            reasons.append(
                "Moderate protein content"
            )

        else:

            reasons.append(
                "Low protein content"
            )

        if fiber >= 8:

            score += 25

            reasons.append(
                "High fiber delays hunger"
            )

        elif fiber >= 4:

            score += 12

            reasons.append(
                "Moderate fiber support"
            )

        if (
            signals[
                "processing_level"
            ]
            ==
            "ULTRA_PROCESSED"
        ):

            score -= 20

            reasons.append(
                "Ultra processing reduces satiety"
            )

        if (
            signals[
                "hidden_sugars"
            ]
            >= 2
        ):

            score -= 10

            reasons.append(
                "Hidden sugars increase cravings"
            )

        if calories >= 400 and protein < 10 and fiber < 5:

            score -= 15

            reasons.append(
                "High calorie density without satiating macros"
            )

        score = max(
            0,
            min(
                100,
                score,
            )
        )

        if score >= 75:

            verdict = "HIGH"

            hunger_return = (
                "3-5 hours"
            )

        elif score >= 50:

            verdict = "MODERATE"

            hunger_return = (
                "2-3 hours"
            )

        else:

            verdict = "LOW"

            hunger_return = (
                "45-90 mins"
            )

        return {

            "score":
            score,

            "verdict":
            verdict,

            "hunger_return":
            hunger_return,

            "reasons":
            reasons,

        }

    # =====================================================
    # ENERGY CURVE ENGINE
    # =====================================================

    def calculate_energy_curve(
        self,
        signals: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Calculate energy curve and crash probability.

        Args:
            signals: Extracted signals from extract_signals()

        Returns:
            Curve type, crash probability, and reasons
        """

        reasons = []

        crash_probability = 20

        curve = "STABLE"

        carbs = signals["carbohydrates"]

        sugar = signals["sugar"]

        hidden_sugars = signals["hidden_sugars"]

        processing = signals[
            "processing_level"
        ]

        if sugar >= 15:

            crash_probability += 25

            reasons.append(
                "High sugar content"
            )

        if hidden_sugars >= 2:

            crash_probability += 25

            reasons.append(
                "Hidden sugars detected"
            )

        if carbs >= 40:

            crash_probability += 15

            reasons.append(
                "High carbohydrate load"
            )

        if (
            processing
            ==
            "ULTRA_PROCESSED"
        ):

            crash_probability += 20

            reasons.append(
                "Ultra processed product"
            )

        crash_probability = min(
            100,
            crash_probability,
        )

        if crash_probability >= 75:

            curve = "SPIKE_CRASH"

        elif crash_probability >= 45:

            curve = "MODERATE_SPIKE"

        return {

            "curve":
            curve,

            "crash_probability":
            crash_probability,

            "reasons":
            reasons,

        }

    # =====================================================
    # METABOLIC LOAD ENGINE
    # =====================================================

    def calculate_metabolic_load(
        self,
        signals: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Calculate metabolic load score (0-100) and risk level.

        Args:
            signals: Extracted signals from extract_signals()

        Returns:
            Metabolic load score, risk level, and reasons
        """

        score = 0

        reasons = []

        score += min(
            int(
                signals["sugar"]
            ),
            30,
        )

        sodium = signals["sodium"]

        sodium = max(
            0.0,
            sodium,
        )

        score += min(
            int(sodium / 25),
            30,
        )

        score += (

            signals[
                "additive_count"
            ]

            * 5

        )

        if (
            signals[
                "contains_palm_oil"
            ]
        ):

            score += 8

            reasons.append(
                "Contains palm oil"
            )

        if (

            signals[
                "processing_level"
            ]

            ==

            "ULTRA_PROCESSED"

        ):

            score += 25

            reasons.append(
                "Ultra processed"
            )

        if (

            signals[
                "hidden_sugars"
            ]

            >= 1

        ):

            score += 10

            reasons.append(
                "Hidden sugars detected"
            )

        score = min(
            100,
            score,
        )

        if score >= 70:

            risk = "HIGH"

        elif score >= 40:

            risk = "MODERATE"

        else:

            risk = "LOW"

        return {

            "score":
            score,

            "risk":
            risk,

            "reasons":
            reasons,

        }

    # =====================================================
    # FOOD PERSONALITY ENGINE
    # =====================================================

    def determine_food_personality(
        self,
        signals: Dict[str, Any],
        satiety: Dict[str, Any],
        energy_curve: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Determine food personality type based on signals.

        Args:
            signals: Extracted signals
            satiety: Satiety analysis results
            energy_curve: Energy curve analysis results

        Returns:
            Personality type, confidence, and reasons
        """

        personality = "STANDARD"

        confidence = 60

        reasons = []

        calories = signals.get(
            "calories",
            100,
        )

        cal_base = (
            calories
            if calories > 0
            else 100
        )

        protein_ratio = (
            (signals["protein"] * 4)
            / cal_base
        )

        if (

            signals["protein"] >= 20

            and

            signals["sugar"] <= 5

            and

            signals["processing_level"]
            != "ULTRA_PROCESSED"

            and

            protein_ratio >= 0.15

        ):

            personality = (
                "PROTEIN_FOCUSED"
            )

            confidence = 90

            reasons.append(
                "High protein profile with low sugar and adequate protein-to-calorie ratio"
            )

        elif (

            energy_curve[
                "curve"
            ]

            ==

            "SPIKE_CRASH"

        ):

            personality = (
                "SUGAR_BOMB"
            )

            confidence = 88

            reasons.append(
                "Strong spike-crash pattern"
            )

        elif (

            signals["sodium"] >= 600

        ):

            personality = (
                "HEART_UNFRIENDLY"
            )

            confidence = 85

            reasons.append(
                "High sodium burden"
            )

        elif (
            signals["hidden_sugars"] >= 2
        ):
            personality = (
                "DIABETIC_UNFRIENDLY"
            )

            confidence = 88

            reasons.append(
                "Multiple hidden sugars detected"
            )

        elif (

            signals[
                "processing_level"
            ]

            ==

            "ULTRA_PROCESSED"

        ):

            personality = (
                "CHEAT_SNACK"
            )

            confidence = 85

            reasons.append(
                "Ultra processed profile"
            )

        elif (

            satiety["score"] >= 75

            and

            signals["fiber"] >= 6

        ):

            personality = (
                "CLEAN_FUEL"
            )

            confidence = 92

            reasons.append(
                "High satiety and fiber"
            )

        return {

            "type":
            personality,

            "confidence":
            confidence,

            "reasons":
            reasons,

        }

    # =====================================================
    # BODY REACTION TIMELINE
    # =====================================================

    def build_body_reaction(
        self,
        signals: Dict[str, Any],
        energy_curve: Dict[str, Any],
        satiety: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Build timeline of body reaction after consumption.

        Args:
            signals: Extracted signals
            energy_curve: Energy curve analysis results
            satiety: Satiety analysis results

        Returns:
            Timeline of body reactions
        """

        timeline = []

        curve = energy_curve.get(
            "curve",
            "STABLE",
        )

        processing = signals.get(
            "processing_level",
            "",
        )

        if curve == "SPIKE_CRASH":

            timeline = [

                {
                    "phase":
                    "0-20 min",

                    "effect":
                    "Energy Spike",

                    "confidence":
                    85,

                    "reason":
                    "Rapid carbohydrate absorption due to high sugar or ultra-processed formulation",
                },

                {
                    "phase":
                    "20-90 min",

                    "effect":
                    "Temporary Satisfaction",

                    "confidence":
                    82,

                    "reason":
                    "Short-term reward response",
                },

                {
                    "phase":
                    "90-180 min",

                    "effect":
                    "Cravings Return",

                    "confidence":
                    80,

                    "reason":
                    "Blood sugar decline triggers hunger",
                },

            ]

        elif curve == "MODERATE_SPIKE":

            timeline = [

                {
                    "phase":
                    "0-30 min",

                    "effect":
                    "Gradual Energy Increase",

                    "confidence":
                    82,

                    "reason":
                    "Moderate glycemic load",
                },

                {
                    "phase":
                    "30-150 min",

                    "effect":
                    "Stable Satisfaction",

                    "confidence":
                    78,

                    "reason":
                    "Moderate digestion profile",
                },

            ]

        else:

            timeline = [

                {
                    "phase":
                    "0-60 min",

                    "effect":
                    "Stable Energy",

                    "confidence":
                    88,

                    "reason":
                    "Balanced metabolic response",
                },

                {
                    "phase":
                    "60-240 min",

                    "effect":
                    "Sustained Satiety",

                    "confidence":
                    85,

                    "reason":
                    "Slow digestion profile supported by complex macronutrients",
                },

            ]

        return {

            "timeline":
            timeline,

            "timeline_type":
            curve,

        }

    # =====================================================
    # WEIGHT LOSS ENGINE
    # =====================================================

    def analyze_weight_loss(
        self,
        signals: Dict[str, Any],
        satiety: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Analyze product suitability for weight loss.

        Args:
            signals: Extracted signals
            satiety: Satiety analysis results

        Returns:
            Weight loss score, verdict, and reasons
        """

        score = 100

        reasons = []

        protein = signals["protein"]

        fiber = signals["fiber"]

        sugar = signals["sugar"]

        calories = signals["calories"]

        cal_base = calories if calories > 0 else 100

        protein_density = (
            (protein * 4) / cal_base
        )

        fiber_density = (
            (fiber * 2) / cal_base
        )

        sugar_density = (
            (sugar * 4) / cal_base
        )

        processing = signals["processing_level"]

        satiety_score = satiety["score"]

        if calories > 400:

            score -= 15

            reasons.append(
                "High calorie burden per 100g/serving"
            )

        if protein_density < 0.15:

            score -= 15

            reasons.append(
                "Low protein density for calories"
            )

        if fiber_density < 0.05:

            score -= 15

            reasons.append(
                "Low fiber density for calories"
            )

        if sugar_density >= 0.20:

            score -= 20

            reasons.append(
                "High sugar burden per calorie"
            )

        if satiety_score < 50:

            score -= 20

            reasons.append(
                "Low satiety profile (will leave you hungry)"
            )

        if processing == "ULTRA_PROCESSED":

            score -= 25

            reasons.append(
                "Ultra processed food promotes overeating"
            )

        score = max(
            0,
            min(
                100,
                score,
            )
        )

        if score >= 80:

            verdict = "EXCELLENT"

        elif score >= 60:

            verdict = "GOOD"

        elif score >= 40:

            verdict = "MODERATE"

        else:

            verdict = "AVOID"

        return {

            "score":
            score,

            "verdict":
            verdict,

            "reasons":
            reasons,

        }

    # =====================================================
    # MUSCLE BUILDING ENGINE
    # =====================================================

    def analyze_muscle_building(
        self,
        signals: Dict[str, Any],
        ingredient_intelligence: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Analyze product suitability for muscle building.

        Args:
            signals: Extracted signals
            ingredient_intelligence: Ingredient analysis data

        Returns:
            Muscle building score, verdict, and reasons
        """

        score = 20

        reasons = []

        protein = signals["protein"]

        sugar = signals["sugar"]

        trans_fat = signals["trans_fat"]

        calories = signals["calories"]

        cal_base = calories if calories > 0 else 100

        protein_ratio = (
            (protein * 4) / cal_base
        )

        processing = signals["processing_level"]

        quality_bonus = (
            self._get_protein_quality_bonus(
                ingredient_intelligence
            )
        )

        score += min(
            int(
                protein * 2.5
            ),
            50,
        )

        score += quality_bonus

        if quality_bonus > 0:

            reasons.append(
                "Contains high-quality bioavailable protein"
            )

        if protein_ratio >= 0.30:

            reasons.append(
                "Excellent protein-to-calorie ratio"
            )

        elif protein_ratio >= 0.15:

            reasons.append(
                "Good protein-to-calorie ratio"
            )

        else:

            reasons.append(
                "Poor protein-to-calorie ratio"
            )

        if sugar >= 15:

            score -= 15

            reasons.append(
                "High sugar burden impairs recovery"
            )

        if trans_fat > 0:

            score -= 20

            reasons.append(
                "Trans fats increase inflammation"
            )

        if processing == "ULTRA_PROCESSED":

            score -= 15

            reasons.append(
                "Ultra processed profile limits nutrient absorption"
            )

        score = max(
            0,
            min(
                100,
                score,
            )
        )

        if score >= 80:

            verdict = "EXCELLENT"

        elif score >= 60:

            verdict = "GOOD"

        elif score >= 40:

            verdict = "AVERAGE"

        else:

            verdict = "POOR"

        return {

            "score":
            score,

            "verdict":
            verdict,

            "reasons":
            reasons,

        }

    # =====================================================
    # DIABETIC IMPACT ENGINE
    # =====================================================

    def analyze_diabetic_impact(
        self,
        signals: Dict[str, Any],
        ingredient_intelligence: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Analyze product impact on blood sugar and diabetes.

        Args:
            signals: Extracted signals
            ingredient_intelligence: Ingredient analysis data

        Returns:
            Diabetic risk, risk score, glycemic load estimate, and reasons
        """

        score = 0

        reasons = []

        carbs = signals["carbohydrates"]

        sugar = signals["sugar"]

        fiber = signals["fiber"]

        protein = signals["protein"]

        if carbs == 0 and sugar > 0:

            carbs = sugar

        hidden_sugars = signals["hidden_sugars"]

        sweeteners = (

            ingredient_intelligence
            .get(
                "registry",
                {},
            )
            .get(
                "artificial_sweeteners",
                {},
            )
            .get(
                "count",
                0,
            )

        )

        processing = signals["processing_level"]

        category = str(
            signals.get(
                "category",
                "",
            )
            or
            ""
        ).lower()

        sugar_ratio = 0

        if carbs > 0:
            sugar_ratio = sugar / carbs

        carb_impact = carbs * (
            0.8 + (0.4 * sugar_ratio)
        )

        mitigation = (
            (fiber * 0.8) + (protein * 0.3)
        )

        glycemic_load = carb_impact - mitigation

        if glycemic_load < 0:

            glycemic_load = 0

        score += min(
            int(
                glycemic_load * 3.5
            ),
            50,
        )

        score += (
            hidden_sugars * 10
        )

        if processing == "ULTRA_PROCESSED":

            score += 20

            reasons.append(
                "Ultra processed nature spikes blood sugar rapidly"
            )

        if sweeteners > 0:

            score += 10

            reasons.append(
                "Artificial sweeteners may disrupt insulin response"
            )

        if glycemic_load > 15:

            reasons.append(
                "High estimated glycemic load"
            )

        elif glycemic_load < 8 and fiber > 3:

            reasons.append(
                "Fiber blunts blood sugar impact"
            )

        if hidden_sugars >= 1:

            reasons.append(
                "Contains hidden sugars"
            )

        if (

            category in self.HIGH_SUGAR_CATEGORIES

            and

            carbs == 0

            and

            sugar == 0

        ):

            score += 40

            reasons.append(
                "Category-based diabetic risk applied due to missing nutrition data"
            )

        if (

            processing == "ULTRA_PROCESSED"

            and

            category in self.HIGH_SUGAR_CATEGORIES

        ):

            score += 15

        score = min(
            100,
            score,
        )

        if score >= 70:

            risk = "HIGH"

        elif score >= 40:

            risk = "MODERATE"

        else:

            risk = "LOW"

        return {

            "risk":
            risk,

            "risk_score":
            score,

            "blood_sugar_spike":
            score >= 60,

            "glycemic_load_estimate":
            round(glycemic_load, 1),

            "reasons":
            reasons,

        }

    # =====================================================
    # HEART IMPACT ENGINE
    # =====================================================

    def analyze_heart_impact(
        self,
        signals: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Analyze product impact on heart health.

        Args:
            signals: Extracted signals

        Returns:
            Heart risk, risk score, and reasons
        """

        score = 0

        reasons = []

        sodium = signals["sodium"]

        saturated_fat = signals["saturated_fat"]

        trans_fat = signals["trans_fat"]

        sugar = signals["sugar"]

        contains_palm_oil = signals["contains_palm_oil"]

        processing = signals["processing_level"]

        sodium = max(
            0.0,
            sodium,
        )

        if sodium >= 1200:

            score += 40

        elif sodium >= 800:

            score += 30

        elif sodium >= 600:

            score += 25

        elif sodium >= 400:

            score += 20

        elif sodium >= 200:

            score += 10

        score += min(
            int(
                saturated_fat * 8
            ),
            40,
        )

        score += min(
            int(
                sugar * 1.5
            ),
            20,
        )

        if saturated_fat >= 5.0:

            reasons.append(
                "High saturated fat burden increases cardiovascular risk"
            )

        if trans_fat > 0:

            score += 25

            reasons.append(
                "Contains trans fat (atherogenic)"
            )

        if contains_palm_oil:

            score += 15

            reasons.append(
                "Contains palm oil (high saturated fat profile)"
            )

        if processing == "ULTRA_PROCESSED":

            score += 20

            reasons.append(
                "Ultra processed foods are linked to cardiovascular risk"
            )

        if sodium >= 400:

            reasons.append(
                "High sodium burden increases blood pressure risk"
            )

        score = min(
            100,
            score,
        )

        if score >= 70:

            risk = "HIGH"

        elif score >= 40:

            risk = "MODERATE"

        else:

            risk = "LOW"

        return {

            "risk":
            risk,

            "risk_score":
            score,

            "reasons":
            reasons,

        }

    # =====================================================
    # FITNESS PERSONA ENGINES
    # =====================================================

    def analyze_keto(
        self,
        signals: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Analyze product suitability for keto diet.

        Args:
            signals: Extracted signals

        Returns:
            Keto score, verdict, net carbs, and reasons
        """

        score = 100

        reasons = []

        carbs = signals["carbohydrates"]

        sugar = signals["sugar"]

        if carbs == 0 and sugar > 0:

            carbs = sugar

        fiber = signals["fiber"]

        fat = signals["fat"]

        net_carbs = max(
            0,
            carbs - fiber,
        )

        if net_carbs > 10:

            score -= 50

            reasons.append(
                "Too high in net carbs for strict keto"
            )

        elif net_carbs > 5:

            score -= 20

            reasons.append(
                "Moderate net carbs, watch portion sizes"
            )

        if fat < 5 and net_carbs < 5:

            score -= 10

            reasons.append(
                "Low in fat, not optimal for keto macros"
            )

        if score >= 80:
            verdict = "EXCELLENT"

        elif score >= 60:
            verdict = "GOOD"

        elif score >= 40:
            verdict = "MODERATE"

        else:
            verdict = "AVOID"

        return {

            "score": score,

            "verdict": verdict,

            "net_carbs": round(
                net_carbs,
                1,
            ),

            "reasons": reasons,

        }

    def analyze_athlete(
        self,
        signals: Dict[str, Any],
        ingredient_intelligence: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Analyze product suitability for athletes.

        Args:
            signals: Extracted signals
            ingredient_intelligence: Ingredient analysis data

        Returns:
            Athlete score, verdict, and reasons
        """

        score = 50

        reasons = []

        carbs = signals["carbohydrates"]

        protein = signals["protein"]

        processing = signals["processing_level"]

        quality_bonus = (
            self._get_protein_quality_bonus(
                ingredient_intelligence
            )
        )

        score += min(
            int(carbs * 1.5),
            25,
        )

        score += min(
            int(protein * 2.0),
            25,
        )

        score += quality_bonus

        if quality_bonus > 0:

            reasons.append(
                "High quality protein supports muscle repair"
            )

        if processing == "ULTRA_PROCESSED":

            score -= 35

            reasons.append(
                "Ultra processed ingredients impede optimal recovery"
            )

        if carbs >= 20 and protein >= 5:

            reasons.append(
                "Good glycogen replenishment profile"
            )

        if score >= 80:
            verdict = "EXCELLENT"

        elif score >= 60:
            verdict = "GOOD"

        elif score >= 40:
            verdict = "MODERATE"

        else:
            verdict = "AVOID"

        return {

            "score": score,

            "verdict": verdict,

            "reasons": reasons,

        }

    def analyze_child(
        self,
        signals: Dict[str, Any],
        ingredient_intelligence: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Analyze product suitability for children.

        Args:
            signals: Extracted signals
            ingredient_intelligence: Ingredient analysis data

        Returns:
            Child safety score, verdict, and reasons
        """

        score = 100

        reasons = []

        sugar = signals["sugar"]

        sodium = signals["sodium"]

        additives_count = signals["additive_count"]

        hyperactivity_risk = (

            ingredient_intelligence
            .get(
                "registry",
                {},
            )
            .get(
                "hyperactivity_risk",
                {},
            )
            .get(
                "risk_level",
                "LOW",
            )

        )

        sweeteners = (

            ingredient_intelligence
            .get(
                "registry",
                {},
            )
            .get(
                "artificial_sweeteners",
                {},
            )
            .get(
                "count",
                0,
            )

        )

        if sugar > 40:

            score -= 50

            reasons.append(
                "Extremely high sugar content for children"
            )

        elif sugar > 20:

            score -= 35

            reasons.append(
                "Very high sugar content for children"
            )

        elif sugar > 10:

            score -= 20

            reasons.append(
                "High sugar content for children"
            )

        if sodium >= 300:

            score -= 15

        if sodium >= 600:

            score -= 15

        if additives_count >= 3:

            score -= 15

        if additives_count >= 5:

            score -= 10

        if signals["contains_palm_oil"]:

            score -= 10

            reasons.append(
                "Contains palm oil"
            )

        if signals["processing_level"] == "ULTRA_PROCESSED":

            score -= 40

            reasons.append(
                "Ultra processed food not recommended for children"
            )

        if hyperactivity_risk == "HIGH":

            score -= 30

            reasons.append(
                "Contains colors linked to hyperactivity"
            )

        if sweeteners > 0:

            score -= 20

            reasons.append(
                "Artificial sweeteners not recommended for children"
            )

        score = max(
            0,
            min(
                100,
                score,
            )
        )

        if score >= 80:
            verdict = "EXCELLENT"

        elif score >= 60:
            verdict = "GOOD"

        elif score >= 40:
            verdict = "MODERATE"

        else:
            verdict = "AVOID"

        return {

            "score": score,

            "verdict": verdict,

            "reasons": reasons,

        }

    # =====================================================
    # LONGEVITY & FLEXIBILITY ENGINES
    # =====================================================

    def analyze_longevity(
        self,
        signals: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Analyze product impact on longevity.

        Args:
            signals: Extracted signals

        Returns:
            Longevity score and reasons
        """

        score = 100

        reasons = []

        fiber = signals["fiber"]

        sugar = signals["sugar"]

        trans_fat = signals["trans_fat"]

        processing = signals["processing_level"]

        if fiber >= 5:

            reasons.append(
                "Rich in fiber, promoting microbiome health"
            )

        else:

            score -= 10

        if sugar > 10:

            score -= 15

            reasons.append(
                "High sugar promotes glycation and aging"
            )

        if trans_fat > 0:

            score -= 25

            reasons.append(
                "Trans fats strictly impair cellular longevity"
            )

        if processing == "ULTRA_PROCESSED":

            score -= 30

            reasons.append(
                "UPF correlates with reduced healthspan"
            )

        elif processing == "MINIMALLY_PROCESSED":

            reasons.append(
                "Whole foods support long-term vitality"
            )

        score = max(
            0,
            min(
                100,
                score,
            )
        )

        return {

            "score": score,

            "reasons": reasons,

        }

    def analyze_metabolic_flexibility(
        self,
        signals: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Analyze product impact on metabolic flexibility.

        Args:
            signals: Extracted signals

        Returns:
            Metabolic flexibility score and reasons
        """

        score = 50

        reasons = []

        sugar = signals["sugar"]

        fiber = signals["fiber"]

        fat = signals["fat"]

        if sugar < 5 and fiber > 3:

            score += 30

            reasons.append(
                "Low sugar and high fiber supports steady insulin"
            )

        elif sugar > 15:

            score -= 20

            reasons.append(
                "High sugar traps metabolism in glucose-burning mode"
            )

        if fat > 10 and sugar < 5:

            score += 20

            reasons.append(
                "Healthy fats encourage fat adaptation"
            )

        score = max(
            0,
            min(
                100,
                score,
            )
        )

        return {

            "score": score,

            "reasons": reasons,

        }

    # =====================================================
    # CONFIDENCE ENGINE
    # =====================================================

    def calculate_confidence(
        self,
        signals: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Calculate confidence score for the entire analysis.

        Args:
            signals: Extracted signals

        Returns:
            Engine confidence score and data quality rating
        """

        score = 50

        score += min(
            signals[
                "scan_quality_score"
            ] // 4,
            25,
        )

        score += self._verification_bonus(

            signals[
                "verification_level"
            ]

        )

        if (
            signals[
                "protein"
            ]
            > 0
        ):
            score += 5

        if (
            signals[
                "fiber"
            ]
            > 0
        ):
            score += 5

        score = max(
            0,
            min(
                100,
                score,
            )
        )

        if score >= 90:

            quality = (
                "VERY_HIGH"
            )

        elif score >= 75:

            quality = (
                "HIGH"
            )

        elif score >= 60:

            quality = (
                "MEDIUM"
            )

        else:

            quality = (
                "LOW"
            )

        return {

            "engine_confidence":
            score,

            "data_quality":
            quality,

        }

    # =====================================================
    # MASTER ANALYSIS
    # =====================================================

    def analyze(
        self,
        nutrition: Dict[str, Any],
        ingredient_intelligence: Dict[str, Any],
        product: Dict[str, Any],
        scan_quality: Dict[str, Any],
        verification: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Master analysis method for metabolic intelligence.

        Args:
            nutrition: Nutrition data from System 1
            ingredient_intelligence: Ingredient analysis from System 2
            product: Product data from System 1
            scan_quality: Scan quality data from System 1
            verification: Verification data from System 1

        Returns:
            Complete metabolic intelligence analysis
        """

        if verification is None:

            verification = {}

        signals = self.extract_signals(

            nutrition=
            nutrition,

            ingredient_intelligence=
            ingredient_intelligence,

            product=
            product,

            scan_quality=
            scan_quality,

            verification=
            verification,

        )

        satiety = (
            self.calculate_satiety(
                signals
            )
        )

        energy_curve = (
            self.calculate_energy_curve(
                signals
            )
        )

        metabolic_load = (
            self.calculate_metabolic_load(
                signals
            )
        )

        personality = (
            self.determine_food_personality(

                signals=
                signals,

                satiety=
                satiety,

                energy_curve=
                energy_curve,

            )
        )

        body_reaction = (
            self.build_body_reaction(

                signals=
                signals,

                energy_curve=
                energy_curve,

                satiety=
                satiety,

            )
        )

        weight_loss = (
            self.analyze_weight_loss(

                signals=
                signals,

                satiety=
                satiety,

            )
        )

        muscle_building = (
            self.analyze_muscle_building(

                signals=
                signals,

                ingredient_intelligence=
                ingredient_intelligence,

            )
        )

        diabetic_impact = (
            self.analyze_diabetic_impact(

                signals=
                signals,

                ingredient_intelligence=
                ingredient_intelligence,

            )
        )

        heart_impact = (
            self.analyze_heart_impact(

                signals=
                signals,

            )
        )

        keto_impact = (
            self.analyze_keto(

                signals=
                signals,

            )
        )

        athlete_impact = (
            self.analyze_athlete(

                signals=
                signals,

                ingredient_intelligence=
                ingredient_intelligence,

            )
        )

        child_impact = (
            self.analyze_child(

                signals=
                signals,

                ingredient_intelligence=
                ingredient_intelligence,

            )
        )

        longevity = (
            self.analyze_longevity(

                signals=
                signals,

            )
        )

        metabolic_flexibility = (
            self.analyze_metabolic_flexibility(

                signals=
                signals,

            )
        )

        confidence = (
            self.calculate_confidence(
                signals
            )
        )

        return {

            "impact_version":
            "2.0",

            "product_context":
            signals["category"],

            "metabolic_health": {
                "satiety": satiety,
                "energy_curve": energy_curve,
                "metabolic_load": metabolic_load,
                "food_personality": personality,
                "body_reaction": body_reaction,
            },

            "personas": {

                "weight_loss":
                weight_loss,

                "muscle_building":
                muscle_building,

                "diabetic":
                diabetic_impact,

                "heart":
                heart_impact,

                "keto":
                keto_impact,

                "athlete":
                athlete_impact,

                "child":
                child_impact,

            },

            "advanced_metrics": {

                "longevity":
                longevity,

                "metabolic_flexibility":
                metabolic_flexibility,

            },

            "confidence":
            confidence,

        }


# ==========================================================
# SINGLETON INSTANCE
# ==========================================================


impact_engine = ImpactEngine()


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [

    "ImpactEngine",
    "impact_engine",

]


# ==========================================================
# END OF FILE – impact_engine.py
# ==========================================================