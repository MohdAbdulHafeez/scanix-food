from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List


# =========================================================
# CALORIE ENGINE
# =========================================================

class CalorieTargetEngine:

    def calculate(

        self,

        profile: Dict[str, Any],

    ) -> Dict[str, Any]:

        weight = profile.get(
            "weight",
            70,
        )

        height = profile.get(
            "height",
            170,
        )

        age = profile.get(
            "age",
            25,
        )

        gender = str(
            profile.get(
                "gender",
                "male",
            )
        ).lower()

        activity = str(
            profile.get(
                "activity_level",
                "moderate",
            )
        ).lower()

        goals = profile.get(
            "goals",
            [],
        )

        if gender == "female":

            bmr = (

                10 * weight

                +

                6.25 * height

                -

                5 * age

                -

                161

            )

        else:

            bmr = (

                10 * weight

                +

                6.25 * height

                -

                5 * age

                +

                5

            )

        activity_multiplier = {

            "sedentary": 1.2,

            "light": 1.375,

            "moderate": 1.55,

            "active": 1.725,

            "athlete": 1.9,

        }

        tdee = (

            bmr

            *

            activity_multiplier.get(
                activity,
                1.55,
            )

        )

        target = tdee

        if "WEIGHT_LOSS" in goals:

            target -= 500

        elif "MUSCLE_GAIN" in goals:

            target += 300

        return {

            "bmr":
            round(bmr),

            "tdee":
            round(tdee),

            "target_calories":
            round(target),

        }


# =========================================================
# MACRO ENGINE
# =========================================================

class MacroTargetEngine:

    def calculate(

        self,

        profile: Dict[str, Any],

        calories: int,

    ) -> Dict[str, Any]:

        weight = profile.get(
            "weight",
            70,
        )

        goals = profile.get(
            "goals",
            [],
        )

        protein_multiplier = 1.6

        if "MUSCLE_GAIN" in goals:

            protein_multiplier = 2.2

        elif "WEIGHT_LOSS" in goals:

            protein_multiplier = 2.0

        protein = round(
            weight
            *
            protein_multiplier,
            1,
        )

        fat = round(

            (
                calories
                * 0.25
            )

            / 9,

            1,

        )

        carbs = round(

            (
                calories

                -

                protein * 4

                -

                fat * 9

            )

            / 4,

            1,

        )

        return {

            "protein":
            protein,

            "carbs":
            carbs,

            "fat":
            fat,

            "fiber":
            30,

        }


# =========================================================
# CONDITION ANALYZER
# =========================================================

class MedicalConditionAnalyzer:

    def analyze(

        self,

        profile: Dict[str, Any],

    ) -> Dict[str, Any]:

        conditions = []

        checks = [

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

        for condition in checks:

            if profile.get(
                condition,
                False,
            ):

                conditions.append(
                    condition.upper()
                )

        return {

            "conditions":
            conditions,

            "count":
            len(
                conditions
            ),

        }


# =========================================================
# DIET PREFERENCE ANALYZER
# =========================================================

class DietPreferenceAnalyzer:

    def analyze(

        self,

        profile: Dict[str, Any],

    ) -> Dict[str, Any]:

        return {

            "diet_preference":

            profile.get(
                "diet_preference",
                "mixed",
            ),

            "budget":

            profile.get(
                "budget",
                "medium",
            ),

        }


# =========================================================
# NUTRITION TARGET BUILDER
# =========================================================

class NutritionTargetBuilder:

    def build(

        self,

        calorie_targets:
        Dict[str, Any],

        macro_targets:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        return {

            "calories":

            calorie_targets.get(
                "target_calories",
                0,
            ),

            "protein":

            macro_targets.get(
                "protein",
                0,
            ),

            "carbs":

            macro_targets.get(
                "carbs",
                0,
            ),

            "fat":

            macro_targets.get(
                "fat",
                0,
            ),

            "fiber":

            macro_targets.get(
                "fiber",
                0,
            ),

        }
    

    # =========================================================
# BREAKFAST ENGINE
# =========================================================

class BreakfastEngine:

    def generate(

        self,

        profile: Dict[str, Any],

    ) -> List[Dict[str, Any]]:

        preference = str(

            profile.get(
                "diet_preference",
                "mixed",
            )

        ).lower()

        if preference == "vegan":

            return [

                {
                    "meal":
                    "Oats With Chia Seeds",

                    "protein":
                    15,
                },

                {
                    "meal":
                    "Peanut Butter Toast",

                    "protein":
                    12,
                },

            ]

        if preference == "vegetarian":

            return [

                {
                    "meal":
                    "Paneer Sandwich",

                    "protein":
                    22,
                },

                {
                    "meal":
                    "Greek Yogurt",

                    "protein":
                    12,
                },

            ]

        return [

            {
                "meal":
                "Egg Omelette",

                "protein":
                24,
            },

            {
                "meal":
                "Whole Wheat Toast",

                "protein":
                8,
            },

        ]


# =========================================================
# LUNCH ENGINE
# =========================================================

class LunchEngine:

    def generate(

        self,

        profile: Dict[str, Any],

    ) -> List[Dict[str, Any]]:

        preference = str(

            profile.get(
                "diet_preference",
                "mixed",
            )

        ).lower()

        if preference == "vegan":

            return [

                {
                    "meal":
                    "Brown Rice",

                    "protein":
                    8,
                },

                {
                    "meal":
                    "Mixed Dal",

                    "protein":
                    18,
                },

            ]

        if preference == "vegetarian":

            return [

                {
                    "meal":
                    "Paneer Curry",

                    "protein":
                    30,
                },

                {
                    "meal":
                    "Roti",

                    "protein":
                    8,
                },

            ]

        return [

            {
                "meal":
                "Chicken Breast",

                "protein":
                45,
            },

            {
                "meal":
                "Rice",

                "protein":
                5,
            },

        ]


# =========================================================
# DINNER ENGINE
# =========================================================

class DinnerEngine:

    def generate(

        self,

        profile: Dict[str, Any],

    ) -> List[Dict[str, Any]]:

        preference = str(

            profile.get(
                "diet_preference",
                "mixed",
            )

        ).lower()

        if preference == "vegan":

            return [

                {
                    "meal":
                    "Tofu Stir Fry",

                    "protein":
                    22,
                },

                {
                    "meal":
                    "Vegetable Soup",

                    "protein":
                    5,
                },

            ]

        if preference == "vegetarian":

            return [

                {
                    "meal":
                    "Paneer Salad",

                    "protein":
                    28,
                },

                {
                    "meal":
                    "Vegetable Soup",

                    "protein":
                    5,
                },

            ]

        return [

            {
                "meal":
                "Fish Curry",

                "protein":
                35,
            },

            {
                "meal":
                "Vegetables",

                "protein":
                5,
            },

        ]


# =========================================================
# SNACK ENGINE
# =========================================================

class SnackEngine:

    def generate(

        self,

        profile: Dict[str, Any],

    ) -> List[Dict[str, Any]]:

        return [

            {
                "meal":
                "Mixed Nuts",

                "protein":
                8,
            },

            {
                "meal":
                "Fruit",

                "protein":
                2,
            },

        ]


# =========================================================
# INDIAN MEAL ENGINE
# =========================================================

class IndianMealEngine:

    def generate(

        self,

        profile: Dict[str, Any],

    ) -> Dict[str, Any]:

        return {

            "breakfast":

            [

                "Poha",

                "Upma",

                "Idli",

                "Dosa",

            ],

            "lunch":

            [

                "Dal",

                "Rice",

                "Roti",

                "Sabzi",

            ],

            "dinner":

            [

                "Paneer",

                "Chicken",

                "Vegetables",

            ],

        }


# =========================================================
# VEGETARIAN ENGINE
# =========================================================

class VegetarianMealEngine:

    def generate(

        self,

    ) -> Dict[str, Any]:

        return {

            "protein_sources":

            [

                "Paneer",

                "Tofu",

                "Greek Yogurt",

                "Lentils",

                "Beans",

            ]

        }


# =========================================================
# NON VEG ENGINE
# =========================================================

class NonVegMealEngine:

    def generate(

        self,

    ) -> Dict[str, Any]:

        return {

            "protein_sources":

            [

                "Chicken",

                "Eggs",

                "Fish",

                "Turkey",

            ]

        }


# =========================================================
# VEGAN ENGINE
# =========================================================

class VeganMealEngine:

    def generate(

        self,

    ) -> Dict[str, Any]:

        return {

            "protein_sources":

            [

                "Tofu",

                "Tempeh",

                "Soy",

                "Lentils",

                "Beans",

            ]

        }
    


    # =========================================================
# WEIGHT LOSS PLANNER
# =========================================================

class WeightLossPlanner:

    def generate(

        self,

        nutrition_targets:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        return {

            "focus": [

                "HIGH_PROTEIN",

                "HIGH_FIBER",

                "CALORIE_DEFICIT",

                "SATIETY_FOCUSED",

            ],

            "meal_rules": [

                "PROTEIN_EVERY_MEAL",

                "LIMIT_ULTRA_PROCESSED",

                "INCREASE_VEGETABLES",

            ],

        }


# =========================================================
# MUSCLE GAIN PLANNER
# =========================================================

class MuscleGainPlanner:

    def generate(

        self,

        nutrition_targets:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        return {

            "focus": [

                "HIGH_PROTEIN",

                "SURPLUS_CALORIES",

                "POST_WORKOUT_NUTRITION",

            ],

            "meal_rules": [

                "PROTEIN_EVERY_MEAL",

                "PRE_WORKOUT_CARBS",

                "POST_WORKOUT_PROTEIN",

            ],

        }


# =========================================================
# DIABETES PLANNER
# =========================================================

class DiabetesPlanner:

    def generate(

        self,

        metabolic_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        return {

            "focus": [

                "LOW_GLYCEMIC_LOAD",

                "BLOOD_SUGAR_STABILITY",

            ],

            "meal_rules": [

                "PAIR_CARBS_WITH_PROTEIN",

                "AVOID_SUGAR_SPIKES",

                "HIGH_FIBER_CARBS",

            ],

        }


# =========================================================
# PCOS PLANNER
# =========================================================

class PCOSPlanner:

    def generate(

        self,

    ) -> Dict[str, Any]:

        return {

            "focus": [

                "INSULIN_SENSITIVITY",

                "ANTI_INFLAMMATORY",

            ],

            "meal_rules": [

                "HIGH_PROTEIN",

                "HIGH_FIBER",

                "LIMIT_REFINED_CARBS",

            ],

        }


# =========================================================
# HEART HEALTH PLANNER
# =========================================================

class HeartHealthPlanner:

    def generate(

        self,

    ) -> Dict[str, Any]:

        return {

            "focus": [

                "LOW_SODIUM",

                "HEART_HEALTHY_FATS",

            ],

            "meal_rules": [

                "LIMIT_TRANS_FATS",

                "INCREASE_OMEGA_3",

                "INCREASE_VEGETABLES",

            ],

        }


# =========================================================
# KIDNEY HEALTH PLANNER
# =========================================================

class KidneyPlanner:

    def generate(

        self,

    ) -> Dict[str, Any]:

        return {

            "focus": [

                "CONTROLLED_SODIUM",

                "RENAL_FRIENDLY",

            ],

            "meal_rules": [

                "LIMIT_EXCESS_SODIUM",

                "MONITOR_PROTEIN",

            ],

        }


# =========================================================
# PREGNANCY PLANNER
# =========================================================

class PregnancyPlanner:

    def generate(

        self,

    ) -> Dict[str, Any]:

        return {

            "focus": [

                "FOLATE",

                "IRON",

                "PROTEIN",

            ],

            "meal_rules": [

                "BALANCED_MEALS",

                "MICRONUTRIENT_DENSE",

            ],

        }


# =========================================================
# BUDGET PLANNER
# =========================================================

class BudgetPlanner:

    def generate(

        self,

        profile: Dict[str, Any],

    ) -> Dict[str, Any]:

        budget = str(

            profile.get(
                "budget",
                "medium",
            )

        ).lower()

        if budget == "low":

            foods = [

                "EGGS",

                "DAL",

                "RICE",

                "OATS",

                "PEANUTS",

            ]

        elif budget == "high":

            foods = [

                "SALMON",

                "GREEK_YOGURT",

                "LEAN_MEAT",

                "AVOCADO",

            ]

        else:

            foods = [

                "EGGS",

                "CHICKEN",

                "DAL",

                "FRUITS",

            ]

        return {

            "budget_level":
            budget,

            "recommended_foods":
            foods,

        }


# =========================================================
# CONDITION PLAN ENGINE
# =========================================================

class ConditionPlanEngine:

    def __init__(self):

        self.weight_loss = (
            WeightLossPlanner()
        )

        self.muscle_gain = (
            MuscleGainPlanner()
        )

        self.diabetes = (
            DiabetesPlanner()
        )

        self.pcos = (
            PCOSPlanner()
        )

        self.heart = (
            HeartHealthPlanner()
        )

        self.kidney = (
            KidneyPlanner()
        )

        self.pregnancy = (
            PregnancyPlanner()
        )

    def generate(

        self,

        profile: Dict[str, Any],

        nutrition_targets:
        Dict[str, Any],

        metabolic_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        plans = {}

        goals = profile.get(
            "goals",
            [],
        )

        if "WEIGHT_LOSS" in goals:

            plans["weight_loss"] = (

                self.weight_loss.generate(

                    nutrition_targets

                )

            )

        if "MUSCLE_GAIN" in goals:

            plans["muscle_gain"] = (

                self.muscle_gain.generate(

                    nutrition_targets

                )

            )

        if profile.get(
            "diabetes",
            False,
        ):

            plans["diabetes"] = (

                self.diabetes.generate(

                    metabolic_intelligence

                )

            )

        if profile.get(
            "pcos",
            False,
        ):

            plans["pcos"] = (

                self.pcos.generate()

            )

        if profile.get(
            "heart_disease",
            False,
        ):

            plans["heart"] = (

                self.heart.generate()

            )

        if profile.get(
            "kidney_disease",
            False,
        ):

            plans["kidney"] = (

                self.kidney.generate()

            )

        if profile.get(
            "pregnant",
            False,
        ):

            plans["pregnancy"] = (

                self.pregnancy.generate()

            )

        return plans
    

    # =========================================================
# GROCERY LIST ENGINE
# =========================================================

class GroceryListEngine:

    def generate(

        self,

        breakfast: List[Dict[str, Any]],

        lunch: List[Dict[str, Any]],

        dinner: List[Dict[str, Any]],

        snacks: List[Dict[str, Any]],

    ) -> List[str]:

        groceries = set()

        for meal_group in [

            breakfast,

            lunch,

            dinner,

            snacks,

        ]:

            for item in meal_group:

                meal_name = str(

                    item.get(
                        "meal",
                        "",
                    )

                )

                if meal_name:

                    groceries.add(
                        meal_name
                    )

        return sorted(
            list(
                groceries
            )
        )


# =========================================================
# DAILY MEAL PLAN BUILDER
# =========================================================

class DailyMealPlanBuilder:

    def build(

        self,

        breakfast: List[Dict[str, Any]],

        lunch: List[Dict[str, Any]],

        dinner: List[Dict[str, Any]],

        snacks: List[Dict[str, Any]],

        nutrition_targets:
        Dict[str, Any],

        grocery_list:
        List[str],

    ) -> Dict[str, Any]:

        return {

            "breakfast":
            breakfast,

            "lunch":
            lunch,

            "dinner":
            dinner,

            "snacks":
            snacks,

            "calories":

            nutrition_targets.get(
                "calories",
                0,
            ),

            "protein":

            nutrition_targets.get(
                "protein",
                0,
            ),

            "carbs":

            nutrition_targets.get(
                "carbs",
                0,
            ),

            "fat":

            nutrition_targets.get(
                "fat",
                0,
            ),

            "fiber":

            nutrition_targets.get(
                "fiber",
                0,
            ),

            "grocery_list":
            grocery_list,

        }


# =========================================================
# WEEKLY PLAN BUILDER
# =========================================================

class WeeklyMealPlanBuilder:

    def build(

        self,

        daily_plan:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        return {

            "monday":
            daily_plan,

            "tuesday":
            daily_plan,

            "wednesday":
            daily_plan,

            "thursday":
            daily_plan,

            "friday":
            daily_plan,

            "saturday":
            daily_plan,

            "sunday":
            daily_plan,

        }


# =========================================================
# MONTHLY PLAN BUILDER
# =========================================================

class MonthlyMealPlanBuilder:

    def build(

        self,

        daily_plan:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        return {

            f"day_{day}":

            daily_plan

            for day

            in range(
                1,
                31,
            )

        }


# =========================================================
# SUMMARY ENGINE
# =========================================================

class MealPlanSummaryEngine:

    def build(

        self,

        profile: Dict[str, Any],

        nutrition_targets:
        Dict[str, Any],

        condition_plans:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        return {

            "goal":

            profile.get(
                "goals",
                [],
            ),

            "target_calories":

            nutrition_targets.get(
                "calories",
                0,
            ),

            "condition_support":

            list(
                condition_plans.keys()
            ),

        }


# =========================================================
# MASTER MEAL PLANNER ENGINE
# =========================================================

class MealPlannerEngine:

    def __init__(self):

        self.calorie_engine = (
            CalorieTargetEngine()
        )

        self.macro_engine = (
            MacroTargetEngine()
        )

        self.condition_analyzer = (
            MedicalConditionAnalyzer()
        )

        self.preference_analyzer = (
            DietPreferenceAnalyzer()
        )

        self.target_builder = (
            NutritionTargetBuilder()
        )

        self.breakfast_engine = (
            BreakfastEngine()
        )

        self.lunch_engine = (
            LunchEngine()
        )

        self.dinner_engine = (
            DinnerEngine()
        )

        self.snack_engine = (
            SnackEngine()
        )

        self.indian_engine = (
            IndianMealEngine()
        )

        self.vegetarian_engine = (
            VegetarianMealEngine()
        )

        self.nonveg_engine = (
            NonVegMealEngine()
        )

        self.vegan_engine = (
            VeganMealEngine()
        )

        self.condition_plan_engine = (
            ConditionPlanEngine()
        )

        self.budget_engine = (
            BudgetPlanner()
        )

        self.grocery_engine = (
            GroceryListEngine()
        )

        self.daily_builder = (
            DailyMealPlanBuilder()
        )

        self.weekly_builder = (
            WeeklyMealPlanBuilder()
        )

        self.monthly_builder = (
            MonthlyMealPlanBuilder()
        )

        self.summary_engine = (
            MealPlanSummaryEngine()
        )

    # =====================================================
    # MASTER ANALYSIS
    # =====================================================

    def analyze(

        self,

        profile: Dict[str, Any],

        metabolic_intelligence:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        calorie_targets = (

            self.calorie_engine.calculate(
                profile
            )

        )

        macro_targets = (

            self.macro_engine.calculate(

                profile,

                calorie_targets.get(
                    "target_calories",
                    2000,
                ),

            )

        )

        nutrition_targets = (

            self.target_builder.build(

                calorie_targets,

                macro_targets,

            )

        )

        breakfast = (

            self.breakfast_engine.generate(
                profile
            )

        )

        lunch = (

            self.lunch_engine.generate(
                profile
            )

        )

        dinner = (

            self.dinner_engine.generate(
                profile
            )

        )

        snacks = (

            self.snack_engine.generate(
                profile
            )

        )

        grocery_list = (

            self.grocery_engine.generate(

                breakfast,

                lunch,

                dinner,

                snacks,

            )

        )

        condition_plans = (

            self.condition_plan_engine.generate(

                profile,

                nutrition_targets,

                metabolic_intelligence,

            )

        )

        budget_plan = (

            self.budget_engine.generate(
                profile
            )

        )

        daily_plan = (

            self.daily_builder.build(

                breakfast,

                lunch,

                dinner,

                snacks,

                nutrition_targets,

                grocery_list,

            )

        )

        weekly_plan = (

            self.weekly_builder.build(
                daily_plan
            )

        )

        monthly_plan = (

            self.monthly_builder.build(
                daily_plan
            )

        )

        summary = (

            self.summary_engine.build(

                profile,

                nutrition_targets,

                condition_plans,

            )

        )

        return {

            "meal_planner_version":
            "1.0",

            "nutrition_targets":
            nutrition_targets,

            "daily_plan":
            daily_plan,

            "weekly_plan":
            weekly_plan,

            "monthly_plan":
            monthly_plan,

            "condition_plans":
            condition_plans,

            "budget_plan":
            budget_plan,

            "summary":
            summary,

        }


meal_planner_engine = (
    MealPlannerEngine()
)