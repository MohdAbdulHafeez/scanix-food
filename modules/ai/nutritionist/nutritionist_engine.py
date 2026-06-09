from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List


# =========================================================
# USER PROFILE ANALYZER
# =========================================================

class UserProfileAnalyzer:

    def analyze(

        self,

        profile: Dict[str, Any],

    ) -> Dict[str, Any]:

        return {

            "age":
            profile.get(
                "age"
            ),

            "gender":
            profile.get(
                "gender"
            ),

            "height":
            profile.get(
                "height"
            ),

            "weight":
            profile.get(
                "weight"
            ),

            "bmi":
            profile.get(
                "bmi"
            ),

            "activity_level":
            profile.get(
                "activity_level"
            ),

            "goals":
            profile.get(
                "goals",
                [],
            ),

            "diet_preference":
            profile.get(
                "diet_preference"
            ),

        }


# =========================================================
# HEALTH CONDITION ANALYZER
# =========================================================

class HealthConditionAnalyzer:

    CONDITIONS = [

        "diabetes",
        "prediabetes",
        "hypertension",
        "obesity",
        "pcos",
        "thyroid",
        "fatty_liver",
        "kidney_disease",
        "heart_disease",

    ]

    def analyze(

        self,

        profile: Dict[str, Any],

    ) -> Dict[str, Any]:

        active_conditions = []

        for condition in self.CONDITIONS:

            if profile.get(
                condition,
                False,
            ):

                active_conditions.append(
                    condition.upper()
                )

        return {

            "conditions":
            active_conditions,

            "condition_count":
            len(
                active_conditions
            ),

        }


# =========================================================
# ALLERGY ANALYZER
# =========================================================

class AllergyAnalyzer:

    def analyze(

        self,

        profile: Dict[str, Any],

    ) -> Dict[str, Any]:

        allergies = (

            profile.get(
                "allergies",
                [],
            )

        )

        return {

            "allergies":
            allergies,

            "count":
            len(
                allergies
            ),

        }


# =========================================================
# GOAL ANALYZER
# =========================================================

class GoalAnalyzer:

    def analyze(

        self,

        profile: Dict[str, Any],

    ) -> Dict[str, Any]:

        goals = (

            profile.get(
                "goals",
                [],
            )

        )

        primary_goal = (

            goals[0]

            if goals

            else

            "GENERAL_HEALTH"

        )

        return {

            "goals":
            goals,

            "primary_goal":
            primary_goal,

        }


# =========================================================
# SCAN HISTORY ANALYZER
# =========================================================

class ScanHistoryAnalyzer:

    def analyze(

        self,

        scan_history:
        List[Dict[str, Any]],

    ) -> Dict[str, Any]:

        if not scan_history:

            return {

                "total_scans": 0,

                "favorite_categories": [],

                "high_risk_products": [],

            }

        return {

            "total_scans":
            len(
                scan_history
            ),

            "favorite_categories":
            [],

            "high_risk_products":
            [],

        }


# =========================================================
# PERSONAL HEALTH MEMORY
# =========================================================

class PersonalHealthMemory:

    def analyze(

        self,

        profile: Dict[str, Any],

        scan_history:
        List[Dict[str, Any]],

    ) -> Dict[str, Any]:

        return {

            "known_allergies":

            profile.get(
                "allergies",
                [],
            ),

            "known_conditions":

            [

                key

                for key, value

                in profile.items()

                if value is True

            ],

            "scan_count":

            len(
                scan_history
            ),

        }
    

# =========================================================
# PRODUCT GUIDANCE ENGINE
# =========================================================

class ProductGuidanceEngine:

    def analyze(

        self,

        food_explainer: Dict[str, Any],

        ingredient_intelligence:
        Dict[str, Any],

        metabolic_intelligence:
        Dict[str, Any],

        consumer_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        final_verdict = (

            food_explainer
            .get(
                "explainer",
                {},
            )
            .get(
                "final_verdict",
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

        recommendation = (

            final_verdict.get(
                "recommendation",
                "UNKNOWN",
            )

        )

        if consumer_score >= 85:

            frequency = (
                "REGULAR"
            )

        elif consumer_score >= 70:

            frequency = (
                "MODERATE"
            )

        elif consumer_score >= 55:

            frequency = (
                "LIMITED"
            )

        else:

            frequency = (
                "RARE"
            )

        return {

            "should_eat":

            recommendation

            not in [

                "AVOID",

                "LIMIT",

            ],

            "frequency":
            frequency,

            "recommendation":
            recommendation,

            "consumer_score":
            consumer_score,

        }


# =========================================================
# FOOD RESTRICTION ENGINE
# =========================================================

class FoodRestrictionEngine:

    def analyze(

        self,

        profile: Dict[str, Any],

        nutrition: Dict[str, Any],

        ingredient_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        restrictions = []

        sugar = nutrition.get(
            "sugar",
            0,
        )

        sodium = nutrition.get(
            "sodium",
            0,
        )

        allergies = (

            profile.get(
                "allergies",
                [],
            )

        )

        ingredients = [

            item.get(
                "name",
                "",
            ).lower()

            for item

            in

            ingredient_intelligence.get(
                "ingredients",
                [],
            )

        ]

        if (

            profile.get(
                "diabetes",
                False,
            )

            and

            sugar >= 10

        ):

            restrictions.append(

                "HIGH_SUGAR"

            )

        if (

            profile.get(
                "hypertension",
                False,
            )

            and

            sodium >= 600

        ):

            restrictions.append(

                "HIGH_SODIUM"

            )

        for allergy in allergies:

            allergy_lower = (
                allergy.lower()
            )

            if any(

                allergy_lower

                in ingredient

                for ingredient

                in ingredients

            ):

                restrictions.append(

                    f"ALLERGY_{allergy.upper()}"

                )

        return {

            "restrictions":

            sorted(

                list(
                    set(
                        restrictions
                    )
                )

            ),

            "safe":

            len(
                restrictions
            ) == 0,

        }


# =========================================================
# SUPPLEMENT ENGINE
# =========================================================

class SupplementEngine:

    def analyze(

        self,

        profile: Dict[str, Any],

    ) -> Dict[str, Any]:

        goals = (

            profile.get(
                "goals",
                [],
            )

        )

        recommendations = []

        if (

            "MUSCLE_GAIN"

            in goals

        ):

            recommendations.extend(

                [

                    "WHEY_PROTEIN",

                    "CREATINE",

                ]

            )

        if (

            "WEIGHT_LOSS"

            in goals

        ):

            recommendations.append(

                "PROTEIN_INTAKE_FOCUS"

            )

        recommendations.extend(

            [

                "OMEGA_3",

                "VITAMIN_D",

            ]

        )

        return {

            "supplements":

            sorted(

                list(
                    set(
                        recommendations
                    )
                )

            ),

            "evidence_based":
            True,

        }


# =========================================================
# NUTRITION TARGET ENGINE
# =========================================================

class NutritionTargetEngine:

    def analyze(

        self,

        profile: Dict[str, Any],

    ) -> Dict[str, Any]:

        weight = (

            profile.get(
                "weight",
                70,
            )

        )

        goals = (

            profile.get(
                "goals",
                [],
            )

        )

        calories = 2200

        if (

            "WEIGHT_LOSS"

            in goals

        ):

            calories = 1800

        elif (

            "MUSCLE_GAIN"

            in goals

        ):

            calories = 2800

        protein = round(
            weight * 1.8,
            1,
        )

        water = round(
            weight * 0.035,
            1,
        )

        return {

            "calories":
            calories,

            "protein":
            protein,

            "carbs":

            round(

                calories
                * 0.45
                / 4,

                1,

            ),

            "fat":

            round(

                calories
                * 0.25
                / 9,

                1,

            ),

            "fiber":
            30,

            "water_liters":
            water,

        }


# =========================================================
# VOICE RESPONSE BUILDER
# =========================================================

class VoiceResponseBuilder:

    def build(

        self,

        response_text: str,

        confidence: int,

        recommendations:
        List[str],

        warnings:
        List[str],

    ) -> Dict[str, Any]:

        follow_ups = []

        if warnings:

            follow_ups.append(

                "Would you like a safer alternative?"

            )

        else:

            follow_ups.append(

                "Would you like a meal plan?"

            )

        return {

            "response_text":
            response_text,

            "voice_text":
            response_text,

            "confidence":
            confidence,

            "recommendations":
            recommendations,

            "warnings":
            warnings,

            "follow_up_questions":
            follow_ups,

        }
    

    # =========================================================
# CONVERSATION MEMORY ENGINE
# =========================================================

class ConversationMemoryEngine:

    def analyze(

        self,

        conversation_history:
        List[Dict[str, Any]],

    ) -> Dict[str, Any]:

        if not conversation_history:

            return {

                "conversation_count": 0,

                "topics": [],

                "last_question": None,

            }

        topics = []

        for item in conversation_history:

            topic = item.get(
                "topic"
            )

            if topic:

                topics.append(
                    topic
                )

        return {

            "conversation_count":

            len(
                conversation_history
            ),

            "topics":

            sorted(

                list(
                    set(
                        topics
                    )
                )

            ),

            "last_question":

            conversation_history[-1].get(
                "question"
            ),

        }


# =========================================================
# MEDICATION INTERACTION ENGINE
# =========================================================

class MedicationInteractionEngine:

    HIGH_RISK = {

        "warfarin": [

            "vitamin k",

            "spinach",

            "kale",

        ],

        "metformin": [

            "alcohol",

        ],

        "statins": [

            "grapefruit",

        ],

    }

    def analyze(

        self,

        profile: Dict[str, Any],

        ingredient_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        medications = (

            profile.get(
                "medications",
                [],
            )

        )

        ingredients = [

            item.get(
                "name",
                "",
            ).lower()

            for item

            in

            ingredient_intelligence.get(
                "ingredients",
                [],
            )

        ]

        warnings = []

        for medication in medications:

            medication_lower = (
                medication.lower()
            )

            risky_foods = (

                self.HIGH_RISK.get(
                    medication_lower,
                    [],
                )

            )

            for risky_food in risky_foods:

                if any(

                    risky_food
                    in ingredient

                    for ingredient

                    in ingredients

                ):

                    warnings.append(

                        {

                            "medication":
                            medication,

                            "food":
                            risky_food,

                            "severity":
                            "HIGH",

                        }

                    )

        return {

            "interaction_count":

            len(
                warnings
            ),

            "interactions":
            warnings,

        }


# =========================================================
# HABIT IMPROVEMENT ENGINE
# =========================================================

class HabitImprovementEngine:

    def analyze(

        self,

        profile: Dict[str, Any],

        scan_history:
        List[Dict[str, Any]],

    ) -> Dict[str, Any]:

        habits = []

        goals = (

            profile.get(
                "goals",
                [],
            )

        )

        if (

            "WEIGHT_LOSS"

            in goals

        ):

            habits.extend(

                [

                    "INCREASE_PROTEIN",

                    "WALK_AFTER_MEALS",

                    "TRACK_CALORIES",

                ]

            )

        if (

            "MUSCLE_GAIN"

            in goals

        ):

            habits.extend(

                [

                    "HIT_PROTEIN_TARGET",

                    "POST_WORKOUT_MEAL",

                    "PROGRESSIVE_OVERLOAD",

                ]

            )

        return {

            "recommended_habits":

            sorted(

                list(
                    set(
                        habits
                    )
                )

            )

        }


# =========================================================
# HEALTHY SWAP ENGINE
# =========================================================

class HealthySwapEngine:

    def analyze(

        self,

        nutrition: Dict[str, Any],

        product: Dict[str, Any],

    ) -> Dict[str, Any]:

        swaps = []

        sugar = nutrition.get(
            "sugar",
            0,
        )

        sodium = nutrition.get(
            "sodium",
            0,
        )

        if sugar >= 10:

            swaps.append(

                "LOW_SUGAR_ALTERNATIVE"

            )

        if sodium >= 600:

            swaps.append(

                "LOW_SODIUM_ALTERNATIVE"

            )

        return {

            "product":

            product.get(
                "name",
                "UNKNOWN",
            ),

            "recommended_swaps":
            swaps,

        }


# =========================================================
# NUTRITION REASONING ENGINE
# =========================================================

class NutritionReasoningEngine:

    def analyze(

        self,

        profile: Dict[str, Any],

        product_guidance:
        Dict[str, Any],

        restriction_analysis:
        Dict[str, Any],

        nutrition_targets:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        reasoning = []

        goals = (

            profile.get(
                "goals",
                [],
            )

        )

        if goals:

            reasoning.append(

                f"Recommendations aligned with goal: {goals[0]}"

            )

        if not restriction_analysis.get(
            "safe",
            True,
        ):

            reasoning.append(

                "Restrictions detected based on health profile."

            )

        if product_guidance.get(
            "should_eat",
            False,
        ):

            reasoning.append(

                "Product considered acceptable based on current profile."

            )

        reasoning.append(

            "Nutrition targets personalized using body weight and goals."

        )

        return {

            "reasoning":
            reasoning

        }


# =========================================================
# CONFIDENCE ENGINE
# =========================================================

class ConfidenceEngine:

    def analyze(

        self,

        profile: Dict[str, Any],

        nutrition_targets:
        Dict[str, Any],

        product_guidance:
        Dict[str, Any],

    ) -> int:

        confidence = 50

        if profile.get(
            "weight"
        ):

            confidence += 10

        if profile.get(
            "height"
        ):

            confidence += 10

        if profile.get(
            "goals"
        ):

            confidence += 10

        if nutrition_targets:

            confidence += 10

        if product_guidance:

            confidence += 10

        return max(
            0,
            min(
                100,
                confidence,
            )
        )
    

    # =========================================================
# SCAN INTELLIGENCE ANALYZER
# =========================================================

class ScanIntelligenceAnalyzer:

    def analyze(

        self,

        product: Dict[str, Any],

        nutrition: Dict[str, Any],

        claims: List[str],

        ocr_text: str,

        serving_size: str,

        scan_quality: Dict[str, Any],

    ) -> Dict[str, Any]:

        category = (

            product.get(
                "category",
                "UNKNOWN",
            )

        )

        brand = (

            product.get(
                "brand",
                "UNKNOWN",
            )

        )

        quality_score = (

            scan_quality.get(
                "confidence",
                0,
            )

        )

        health_claims = []

        for claim in claims:

            claim_lower = (
                claim.lower()
            )

            if any(

                keyword in claim_lower

                for keyword in [

                    "healthy",
                    "protein",
                    "immunity",
                    "natural",
                    "fitness",
                    "low sugar",
                    "high fiber",

                ]

            ):

                health_claims.append(
                    claim
                )

        return {

            "brand":
            brand,

            "category":
            category,

            "serving_size":
            serving_size,

            "health_claims":
            health_claims,

            "ocr_available":

            bool(
                ocr_text
            ),

            "scan_quality":
            quality_score,

        }


# =========================================================
# METABOLIC NUTRITION ANALYZER
# =========================================================

class MetabolicNutritionAnalyzer:

    def analyze(

        self,

        metabolic_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        metabolic = (

            metabolic_intelligence.get(
                "metabolic",
                {},
            )

        )

        glycemic_load = (

            metabolic.get(
                "glycemic_load",
                {},
            )

        )

        insulin_load = (

            metabolic.get(
                "insulin_load",
                {},
            )

        )

        flexibility = (

            metabolic.get(
                "metabolic_flexibility",
                {},
            )

        )

        impact = (

            metabolic_intelligence.get(
                "health_impact",
                {},
            )

        )

        recommendations = []

        gl_score = (

            glycemic_load.get(
                "score",
                0,
            )

        )

        insulin_score = (

            insulin_load.get(
                "score",
                0,
            )

        )

        if gl_score >= 70:

            recommendations.append(

                "REDUCE_HIGH_GLYCEMIC_FOODS"

            )

        if insulin_score >= 70:

            recommendations.append(

                "PAIR_CARBS_WITH_PROTEIN"

            )

        flexibility_score = (

            flexibility.get(
                "score",
                50,
            )

        )

        return {

            "glycemic_load":
            glycemic_load,

            "insulin_load":
            insulin_load,

            "metabolic_flexibility":
            flexibility,

            "health_impact":
            impact,

            "recommendations":
            recommendations,

            "metabolic_flexibility_score":
            flexibility_score,

        }
    

    # =========================================================
# NUTRITIONIST RESPONSE ENGINE
# =========================================================

class NutritionistResponseEngine:

    def build(

        self,

        profile_analysis: Dict[str, Any],

        condition_analysis: Dict[str, Any],

        goal_analysis: Dict[str, Any],

        product_guidance: Dict[str, Any],

        restriction_analysis: Dict[str, Any],

        supplement_analysis: Dict[str, Any],

        nutrition_targets: Dict[str, Any],

        swap_analysis: Dict[str, Any],

        habit_analysis: Dict[str, Any],

        reasoning_analysis: Dict[str, Any],

        confidence: int,

    ) -> Dict[str, Any]:

        recommendations = []

        warnings = []

        recommendations.extend(

            habit_analysis.get(
                "recommended_habits",
                [],
            )

        )

        recommendations.extend(

            supplement_analysis.get(
                "supplements",
                [],
            )

        )

        recommendations.extend(

            swap_analysis.get(
                "recommended_swaps",
                [],
            )

        )

        restrictions = (

            restriction_analysis.get(
                "restrictions",
                [],
            )

        )

        warnings.extend(
            restrictions
        )

        if restrictions:

            response_text = (

                "Based on your profile, "
                "this product should be consumed carefully."

            )

        elif product_guidance.get(
            "should_eat",
            False,
        ):

            response_text = (

                "This product can fit into your nutrition plan."

            )

        else:

            response_text = (

                "This product is not an ideal choice for your goals."

            )

        return {

            "response_text":
            response_text,

            "voice_text":
            response_text,

            "confidence":
            confidence,

            "recommendations":

            sorted(

                list(
                    set(
                        recommendations
                    )
                )

            ),

            "warnings":

            sorted(

                list(
                    set(
                        warnings
                    )
                )

            ),

            "follow_up_questions": [

                "Would you like a personalized meal plan?",

                "Would you like healthier alternatives?",

            ],

            "reasoning":

            reasoning_analysis.get(
                "reasoning",
                [],
            ),

        }


# =========================================================
# AI NUTRITIONIST ENGINE
# =========================================================

class AINutritionistEngine:

    def __init__(self):

        self.profile_analyzer = (
            UserProfileAnalyzer()
        )

        self.condition_analyzer = (
            HealthConditionAnalyzer()
        )

        self.allergy_analyzer = (
            AllergyAnalyzer()
        )

        self.goal_analyzer = (
            GoalAnalyzer()
        )

        self.scan_history_analyzer = (
            ScanHistoryAnalyzer()
        )

        self.memory_analyzer = (
            PersonalHealthMemory()
        )

        self.product_guidance_engine = (
            ProductGuidanceEngine()
        )

        self.restriction_engine = (
            FoodRestrictionEngine()
        )

        self.supplement_engine = (
            SupplementEngine()
        )

        self.target_engine = (
            NutritionTargetEngine()
        )

        self.voice_builder = (
            VoiceResponseBuilder()
        )

        self.conversation_memory_engine = (
            ConversationMemoryEngine()
        )

        self.medication_engine = (
            MedicationInteractionEngine()
        )

        self.habit_engine = (
            HabitImprovementEngine()
        )

        self.swap_engine = (
            HealthySwapEngine()
        )

        self.reasoning_engine = (
            NutritionReasoningEngine()
        )

        self.confidence_engine = (
            ConfidenceEngine()
        )

        self.response_engine = (
            NutritionistResponseEngine()
        )

        self.scan_intelligence_analyzer = (
            ScanIntelligenceAnalyzer()
        )

        self.metabolic_nutrition_analyzer = (
            MetabolicNutritionAnalyzer()
        )

    # =====================================================
    # MASTER ANALYSIS
    # =====================================================
    def analyze(

    self,

    profile: Dict[str, Any],

    product: Dict[str, Any],

    nutrition: Dict[str, Any],

    claims: List[str],

    ocr_text: str,

    serving_size: str,

    scan_quality: Dict[str, Any],

    ingredient_intelligence: Dict[str, Any],

    metabolic_intelligence: Dict[str, Any],

    consumer_intelligence: Dict[str, Any],

    food_explainer: Dict[str, Any],

    body_intelligence: Dict[str, Any],

    scan_history: List[Dict[str, Any]],

    conversation_history: List[Dict[str, Any]],

    user_query: str = "",

) -> Dict[str, Any]:

        profile_analysis = (

            self.profile_analyzer
            .analyze(
                profile
            )

        )

        condition_analysis = (

            self.condition_analyzer
            .analyze(
                profile
            )

        )

        allergy_analysis = (

            self.allergy_analyzer
            .analyze(
                profile
            )

        )

        goal_analysis = (

            self.goal_analyzer
            .analyze(
                profile
            )

        )

        scan_analysis = (

            self.scan_history_analyzer
            .analyze(
                scan_history
            )

        )

        memory_analysis = (

            self.memory_analyzer
            .analyze(

                profile,

                scan_history,

            )

        )

        conversation_analysis = (

            self.conversation_memory_engine
            .analyze(
                conversation_history
            )

        )

        scan_intelligence = (

    self.scan_intelligence_analyzer
    .analyze(

        product,

        nutrition,

        claims,

        ocr_text,

        serving_size,

        scan_quality,

    )

)

        metabolic_nutrition = (

            self.metabolic_nutrition_analyzer
            .analyze(

                metabolic_intelligence

            )

        )

        product_guidance = (

            self.product_guidance_engine
            .analyze(

                food_explainer,

                ingredient_intelligence,

                metabolic_intelligence,

                consumer_intelligence,

            )

        )

        restriction_analysis = (

            self.restriction_engine
            .analyze(

                profile,

                nutrition,

                ingredient_intelligence,

            )

        )

        supplement_analysis = (

            self.supplement_engine
            .analyze(
                profile
            )

        )

        nutrition_targets = (

            self.target_engine
            .analyze(
                profile
            )

        )

        medication_analysis = (

            self.medication_engine
            .analyze(

                profile,

                ingredient_intelligence,

            )

        )

        habit_analysis = (

            self.habit_engine
            .analyze(

                profile,

                scan_history,

            )

        )

        swap_analysis = (

            self.swap_engine
            .analyze(

                nutrition,

                product,

            )

        )

        reasoning_analysis = (

            self.reasoning_engine
            .analyze(

                profile,

                product_guidance,

                restriction_analysis,

                nutrition_targets,

            )

        )

        confidence = (

            self.confidence_engine
            .analyze(

                profile,

                nutrition_targets,

                product_guidance,

            )

        )

        voice_response = (

            self.response_engine
            .build(

                profile_analysis,

                condition_analysis,

                goal_analysis,

                product_guidance,

                restriction_analysis,

                supplement_analysis,

                nutrition_targets,

                swap_analysis,

                habit_analysis,

                reasoning_analysis,

                confidence,

            )

        )

        return {

            "nutritionist_version":
            "1.0",

            "user_query":
            user_query,

            "profile":
            profile_analysis,

            "conditions":
            condition_analysis,

            "allergies":
            allergy_analysis,

            "goals":
            goal_analysis,

            "scan_history":
            scan_analysis,

            "personal_memory":
            memory_analysis,

            "conversation_memory":
            conversation_analysis,

            "product_guidance":
            product_guidance,

            "food_restrictions":
            restriction_analysis,

            "supplements":
            supplement_analysis,

            "nutrition_targets":
            nutrition_targets,

            "medication_interactions":
            medication_analysis,

            "habit_improvements":
            habit_analysis,

            "healthy_swaps":
            swap_analysis,

            "reasoning":
            reasoning_analysis,

            "voice_response":
            voice_response,

            "confidence":
            confidence,

            "scan_intelligence":
            scan_intelligence,

            "metabolic_nutrition":
            metabolic_nutrition,

        }


ai_nutritionist_engine = (
    AINutritionistEngine()
)