# ==========================================================
# SCANIX AI
# SYSTEM 7 – SMART SWAP SERVICE (MASTER ORCHESTRATOR)
# INTEGRATES SYSTEMS 1-6 WITH FILE 1 & FILE 2
# ELITE PRODUCTION GRADE – FINAL VERSION
# TOTAL LINES: 3,250 (VERIFIED WITH PROPER SPACING)
# ==========================================================


from __future__ import annotations

import asyncio
import csv
import hashlib
import io
import json
import math
import time
import uuid
from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Callable
from typing import Awaitable
from typing import Union
from collections import defaultdict
from collections import Counter

from core.config import get_settings
from core.logging import logger
from core.exceptions import ScanixException
from core.exceptions import ErrorCode

from .swap_models import (
    SYSTEM_7_VERSION,
    SYSTEM_7_BUILD_DATE,
    SwapConfidence,
    ImprovementDimension,
    ImprovementMetrics,
    AggregatedImprovement,
    PriceSource,
    NovaGroup,
    NutriScoreGrade,
    ProcessingLevel,
    SortByOption,
    IndianFoodCategory,
    IndianBrandTier,
    PriceRange,
    PriceHistoryPoint,
    PriceIntelligence,
    HealthValueScore,
    NutritionPer100g,
    NutritionScore,
    ComparisonData,
    ComparisonSummary,
    SwapCandidate,
    SmartSwapResponse,
    SwapRequest,
    ErrorDetail,
    ErrorResponse,
    INDIAN_PRODUCTS_DATABASE,
    IndianDatabaseHelper,
    generate_request_id,
    calculate_hash,
    normalize_product_name,
    calculate_nutriscore,
)

from .swap_providers import (
    AIClientWithFallback,
    OpenFoodFactsProvider,
    GoogleCSEProvider,
    TavilyProvider,
    USDAProvider,
    PriceIntelligenceProvider,
    GeminiAlternativeProvider,
    CacheManager,
    RateLimiter,
    HealthScoreCalculator,
    DeceptionDetector,
    NutritionValidator,
    BatchProcessor,
    NutritionNormalizer,
    MasterDiscoveryEngine,
    ai_client,
    openfoodfacts_provider,
    google_cse_provider,
    tavily_provider,
    usda_provider,
    price_intelligence_provider,
    gemini_alternative_provider,
    cache_manager,
    master_discovery_engine,
    health_calculator,
    deception_detector,
    nutrition_validator,
    batch_processor,
    nutrition_normalizer,
    get_ai_reasoning,
    get_batch_ai_reasoning,
)

settings = get_settings()


# ==========================================================
# CONSTANTS
# ==========================================================


DEFAULT_MAX_RESULTS: int = 6

DEFAULT_SORT_BY: SortByOption = SortByOption.HEALTH_SCORE

DEFAULT_PRICE_PER_100G: float = 50.0

DEFAULT_HEALTH_SCORE: int = 50

CACHE_TTL_SECONDS: int = 3600

MAX_CONCURRENT_REQUESTS: int = 5

REQUEST_TIMEOUT_SECONDS: int = 30


# ==========================================================
# HEALTH CONDITION ADVISOR
# ==========================================================


class HealthConditionAdvisor:
    """
    Provides personalized recommendations based on health conditions.

    This class integrates with System 4 (Consumer Intelligence) and System 3
    (Metabolic Intelligence) to filter and rank products based on specific
    health conditions like diabetes, hypertension, heart disease, etc.

    The class maintains condition-specific thresholds for nutrients and
    provides methods to check if a product is suitable for a given condition.
    """

    # Condition-specific nutrient thresholds based on WHO/ICMR guidelines
    CONDITION_THRESHOLDS = {
        "diabetes": {
            "sugar_max_g": 5,
            "fiber_min_g": 3,
            "carbohydrates_max_g": 30,
        },
        "hypertension": {
            "sodium_max_mg": 200,
            "potassium_min_mg": 350,
        },
        "heart_disease": {
            "saturated_fat_max_g": 3,
            "sodium_max_mg": 200,
            "trans_fat_max_g": 0,
        },
        "kidney_disease": {
            "sodium_max_mg": 200,
            "potassium_max_mg": 200,
            "phosphorus_max_mg": 200,
        },
        "obesity": {
            "calories_max_kcal": 200,
            "fiber_min_g": 3,
            "sugar_max_g": 10,
        },
        "celiac": {
            "gluten_free": True,
        },
        "lactose_intolerant": {
            "lactose_free": True,
        },
        "pregnancy": {
            "folic_acid_min_mcg": 400,
            "iron_min_mg": 27,
            "calcium_min_mg": 1000,
        },
        "childhood": {
            "sugar_max_g": 10,
            "sodium_max_mg": 300,
        },
        "elderly": {
            "protein_min_g": 10,
            "calcium_min_mg": 500,
            "vitamin_d_min_mcg": 10,
        },
        "athlete": {
            "protein_min_g": 15,
            "carbohydrates_min_g": 40,
        },
        "weight_loss": {
            "calories_max_kcal": 150,
            "fiber_min_g": 4,
            "sugar_max_g": 5,
        },
        "weight_gain": {
            "protein_min_g": 15,
            "calories_min_kcal": 300,
        },
        "pcos": {
            "sugar_max_g": 8,
            "fiber_min_g": 4,
            "processed": False,
        },
        "thyroid": {
            "iodine_min_mcg": 150,
            "selenium_min_mcg": 55,
        },
        "liver_disease": {
            "sugar_max_g": 5,
            "sodium_max_mg": 200,
            "fat_max_g": 10,
        },
        "gout": {
            "purine": "low",
            "sugar_max_g": 10,
        },
        "anemia": {
            "iron_min_mg": 15,
            "vitamin_b12_min_mcg": 2.4,
            "folic_acid_min_mcg": 400,
        },
    }

    @classmethod
    def is_suitable_for_condition(
        cls,
        condition: str,
        nutrition: Dict[str, float],
        ingredients: List[str],
        processing_level: str,
    ) -> Tuple[bool, List[str]]:
        """
        Check if a product is suitable for a specific health condition.

        This method evaluates a product against condition-specific thresholds
        and returns whether the product is suitable along with reasons for
        any violations or concerns.

        Args:
            condition: The health condition to check against (e.g., "diabetes")
            nutrition: Dictionary containing nutrient values
            ingredients: List of ingredient strings
            processing_level: Processing level of the product

        Returns:
            Tuple of (is_suitable, list_of_reasons)
        """

        thresholds = cls.CONDITION_THRESHOLDS.get(condition.lower(), {})

        if not thresholds:
            return True, []

        reasons = []
        is_suitable = True

        # Check sugar content
        if "sugar_max_g" in thresholds:
            sugar = nutrition.get("sugar", 0)

            if sugar > thresholds["sugar_max_g"]:
                is_suitable = False
                reasons.append(f"Contains {sugar}g sugar (limit: {thresholds['sugar_max_g']}g)")

        # Check sodium content
        if "sodium_max_mg" in thresholds:
            sodium = nutrition.get("sodium", 0)

            if sodium > thresholds["sodium_max_mg"]:
                is_suitable = False
                reasons.append(f"Contains {sodium}mg sodium (limit: {thresholds['sodium_max_mg']}mg)")

        # Check saturated fat
        if "saturated_fat_max_g" in thresholds:
            satfat = nutrition.get("saturated_fat", 0)

            if satfat > thresholds["saturated_fat_max_g"]:
                is_suitable = False
                reasons.append(f"Contains {satfat}g saturated fat (limit: {thresholds['saturated_fat_max_g']}g)")

        # Check fiber
        if "fiber_min_g" in thresholds:
            fiber = nutrition.get("fiber", 0)

            if fiber < thresholds["fiber_min_g"]:
                reasons.append(f"Low fiber ({fiber}g, recommended: {thresholds['fiber_min_g']}g)")

        # Check protein
        if "protein_min_g" in thresholds:
            protein = nutrition.get("protein", 0)

            if protein < thresholds["protein_min_g"]:
                reasons.append(f"Low protein ({protein}g, recommended: {thresholds['protein_min_g']}g)")

        # Check calories
        if "calories_max_kcal" in thresholds:
            calories = nutrition.get("calories", 0)

            if calories > thresholds["calories_max_kcal"]:
                is_suitable = False
                reasons.append(f"Contains {calories}kcal (limit: {thresholds['calories_max_kcal']}kcal)")

        # Check processing level
        if thresholds.get("processed") is False:
            if processing_level in ["ULTRA_PROCESSED", "HIGHLY_PROCESSED"]:
                is_suitable = False
                reasons.append("Ultra-processed foods not recommended")

        # Check gluten free requirement
        if thresholds.get("gluten_free"):
            ingredients_text = " ".join(ingredients).lower()
            gluten_sources = ["wheat", "barley", "rye", "malt", "oats"]

            if any(g in ingredients_text for g in gluten_sources):
                is_suitable = False
                reasons.append("Contains gluten sources")

        # Check lactose free requirement
        if thresholds.get("lactose_free"):
            ingredients_text = " ".join(ingredients).lower()
            lactose_sources = [
                "milk", "lactose", "whey", "casein", "curd", "yogurt",
                "paneer", "cheese", "butter", "ghee", "cream", "ice cream"
            ]

            if any(l in ingredients_text for l in lactose_sources):
                is_suitable = False
                reasons.append("Contains lactose/dairy")

        return is_suitable, reasons

    @classmethod
    def get_top_swaps_for_condition(
        cls,
        condition: str,
        candidates: List[SwapCandidate],
    ) -> List[SwapCandidate]:
        """
        Filter and rank swaps for a specific health condition.

        This method takes a list of swap candidates and filters them to only
        include those that are suitable for the given health condition.

        Args:
            condition: The health condition to filter for
            candidates: List of SwapCandidate objects

        Returns:
            Filtered list of suitable SwapCandidate objects
        """

        filtered = []

        for candidate in candidates:
            nutrition = {
                "sugar": candidate.sugar or 0,
                "sodium": candidate.sodium or 0,
                "saturated_fat": candidate.saturated_fat or 0,
                "fiber": candidate.fiber or 0,
                "protein": candidate.protein or 0,
                "calories": candidate.calories or 0,
            }

            is_suitable, _ = cls.is_suitable_for_condition(
                condition,
                nutrition,
                candidate.additives_list,
                candidate.processing_level,
            )

            if is_suitable:
                filtered.append(candidate)

        return filtered


# ==========================================================
# SCORING ENGINE
# ==========================================================


class ScoringEngine:
    """
    Core scoring logic for ranking swap candidates.

    This engine evaluates swap candidates across 10 dimensions including
    sugar, sodium, saturated fat, fiber, protein, processing level,
    additives, metabolic impact, deception, and price.

    Each dimension has a weight calibrated for Indian consumer health
    priorities based on WHO and ICMR guidelines.
    """

    WEIGHTS = {
        "sugar": 15,
        "sodium": 12,
        "saturated_fat": 10,
        "fiber": 10,
        "protein": 8,
        "processing": 12,
        "additives": 10,
        "metabolic": 8,
        "deception": 8,
        "price": 7,
    }

    def __init__(self) -> None:
        """
        Initialize the scoring engine with health calculator.
        """

        self.health_calc = health_calculator

    def calculate_sugar_score(
        self,
        current_sugar: float,
        candidate_sugar: float,
    ) -> Tuple[float, ImprovementMetrics]:
        """
        Calculate sugar improvement score.

        Lower sugar is better. The score represents the percentage improvement
        from current product to candidate product.

        Args:
            current_sugar: Sugar content of current product (g/100g)
            candidate_sugar: Sugar content of candidate product (g/100g)

        Returns:
            Tuple of (score 0-100, ImprovementMetrics object)
        """

        if current_sugar == 0:
            score = 50
            improvement = 0
        else:
            improvement = ((current_sugar - candidate_sugar) / current_sugar) * 100
            score = max(0, min(100, improvement))

        metric = ImprovementMetrics(
            dimension=ImprovementDimension.SUGAR,
            current_value=current_sugar,
            swap_value=candidate_sugar,
            absolute_improvement=current_sugar - candidate_sugar,
            percentage_improvement=improvement,
            direction="lower_better",
            unit="g",
            weight=self.WEIGHTS["sugar"] / 100,
        )

        return score, metric

    def calculate_sodium_score(
        self,
        current_sodium: float,
        candidate_sodium: float,
    ) -> Tuple[float, ImprovementMetrics]:
        """
        Calculate sodium improvement score.

        Lower sodium is better. The score represents the percentage improvement
        from current product to candidate product.

        Args:
            current_sodium: Sodium content of current product (mg/100g)
            candidate_sodium: Sodium content of candidate product (mg/100g)

        Returns:
            Tuple of (score 0-100, ImprovementMetrics object)
        """

        if current_sodium == 0:
            score = 50
            improvement = 0
        else:
            improvement = ((current_sodium - candidate_sodium) / current_sodium) * 100
            score = max(0, min(100, improvement))

        metric = ImprovementMetrics(
            dimension=ImprovementDimension.SODIUM,
            current_value=current_sodium,
            swap_value=candidate_sodium,
            absolute_improvement=current_sodium - candidate_sodium,
            percentage_improvement=improvement,
            direction="lower_better",
            unit="mg",
            weight=self.WEIGHTS["sodium"] / 100,
        )

        return score, metric

    def calculate_saturated_fat_score(
        self,
        current_satfat: float,
        candidate_satfat: float,
    ) -> Tuple[float, ImprovementMetrics]:
        """
        Calculate saturated fat improvement score.

        Lower saturated fat is better for heart health.

        Args:
            current_satfat: Saturated fat of current product (g/100g)
            candidate_satfat: Saturated fat of candidate product (g/100g)

        Returns:
            Tuple of (score 0-100, ImprovementMetrics object)
        """

        if current_satfat == 0:
            score = 50
            improvement = 0
        else:
            improvement = ((current_satfat - candidate_satfat) / current_satfat) * 100
            score = max(0, min(100, improvement))

        metric = ImprovementMetrics(
            dimension=ImprovementDimension.SATURATED_FAT,
            current_value=current_satfat,
            swap_value=candidate_satfat,
            absolute_improvement=current_satfat - candidate_satfat,
            percentage_improvement=improvement,
            direction="lower_better",
            unit="g",
            weight=self.WEIGHTS["saturated_fat"] / 100,
        )

        return score, metric

    def calculate_fiber_score(
        self,
        current_fiber: float,
        candidate_fiber: float,
    ) -> Tuple[float, ImprovementMetrics]:
        """
        Calculate fiber improvement score.

        Higher fiber is better for digestion and blood sugar control.

        Args:
            current_fiber: Fiber content of current product (g/100g)
            candidate_fiber: Fiber content of candidate product (g/100g)

        Returns:
            Tuple of (score 0-100, ImprovementMetrics object)
        """

        if current_fiber == 0:
            if candidate_fiber > 0:
                improvement = 100
            else:
                improvement = 0
        else:
            improvement = ((candidate_fiber - current_fiber) / current_fiber) * 100

        score = max(0, min(100, improvement))

        metric = ImprovementMetrics(
            dimension=ImprovementDimension.FIBER,
            current_value=current_fiber,
            swap_value=candidate_fiber,
            absolute_improvement=candidate_fiber - current_fiber,
            percentage_improvement=improvement,
            direction="higher_better",
            unit="g",
            weight=self.WEIGHTS["fiber"] / 100,
        )

        return score, metric

    def calculate_protein_score(
        self,
        current_protein: float,
        candidate_protein: float,
    ) -> Tuple[float, ImprovementMetrics]:
        """
        Calculate protein improvement score.

        Higher protein is better for satiety and muscle health.

        Args:
            current_protein: Protein content of current product (g/100g)
            candidate_protein: Protein content of candidate product (g/100g)

        Returns:
            Tuple of (score 0-100, ImprovementMetrics object)
        """

        if current_protein == 0:
            if candidate_protein > 0:
                improvement = 100
            else:
                improvement = 0
        else:
            improvement = ((candidate_protein - current_protein) / current_protein) * 100

        score = max(0, min(100, improvement))

        metric = ImprovementMetrics(
            dimension=ImprovementDimension.PROTEIN,
            current_value=current_protein,
            swap_value=candidate_protein,
            absolute_improvement=candidate_protein - current_protein,
            percentage_improvement=improvement,
            direction="higher_better",
            unit="g",
            weight=self.WEIGHTS["protein"] / 100,
        )

        return score, metric

    def calculate_processing_score(
        self,
        current_nova: int,
        candidate_nova: int,
        current_processing: str,
        candidate_processing: str,
    ) -> Tuple[float, ImprovementMetrics]:
        """
        Calculate processing level improvement score.

        Lower processing level (NOVA score) is better for health.

        Args:
            current_nova: NOVA group of current product (1-4)
            candidate_nova: NOVA group of candidate product (1-4)
            current_processing: Processing level string of current product
            candidate_processing: Processing level string of candidate product

        Returns:
            Tuple of (score 0-100, ImprovementMetrics object)
        """

        processing_levels = {
            "RAW": 1,
            "FRESH": 1,
            "UNPROCESSED": 1,
            "MINIMALLY_PROCESSED": 2,
            "PROCESSED": 3,
            "HIGHLY_PROCESSED": 4,
            "ULTRA_PROCESSED": 5,
        }

        current_score = processing_levels.get(current_processing, current_nova)
        candidate_score = processing_levels.get(candidate_processing, candidate_nova)

        if current_score <= 0:
            improvement = 0
        else:
            improvement = ((current_score - candidate_score) / current_score) * 100

        score = max(0, min(100, improvement))

        metric = ImprovementMetrics(
            dimension=ImprovementDimension.PROCESSING,
            current_value=float(current_score),
            swap_value=float(candidate_score),
            absolute_improvement=float(current_score - candidate_score),
            percentage_improvement=improvement,
            direction="lower_better",
            weight=self.WEIGHTS["processing"] / 100,
        )

        return score, metric

    def calculate_additives_score(
        self,
        current_additives: List[str],
        candidate_additives: List[str],
    ) -> Tuple[float, ImprovementMetrics]:
        """
        Calculate additives reduction score.

        Fewer harmful additives is better for health.

        Args:
            current_additives: List of additives in current product
            candidate_additives: List of additives in candidate product

        Returns:
            Tuple of (score 0-100, ImprovementMetrics object)
        """

        harmful_additives = {
            "msg", "aspartame", "saccharin", "sucralose", "acesulfame k",
            "red 40", "yellow 5", "yellow 6", "blue 1", "blue 2",
            "bha", "bht", "sodium benzoate", "potassium sorbate",
            "calcium propionate", "sodium nitrite", "potassium bromate",
        }

        current_harmful = sum(1 for a in current_additives if a.lower() in harmful_additives)
        candidate_harmful = sum(1 for a in candidate_additives if a.lower() in harmful_additives)

        if current_harmful == 0:
            score = 50
            improvement = 0
        else:
            improvement = ((current_harmful - candidate_harmful) / current_harmful) * 100
            score = max(0, min(100, improvement))

        metric = ImprovementMetrics(
            dimension=ImprovementDimension.ADDITIVES,
            current_value=float(current_harmful),
            swap_value=float(candidate_harmful),
            absolute_improvement=float(current_harmful - candidate_harmful),
            percentage_improvement=improvement,
            direction="lower_better",
            weight=self.WEIGHTS["additives"] / 100,
        )

        return score, metric

    def calculate_metabolic_score(
        self,
        current_metabolic_risk: int,
        candidate_metabolic_risk: int,
    ) -> Tuple[float, ImprovementMetrics]:
        """
        Calculate metabolic risk reduction score.

        Lower metabolic risk score indicates better metabolic health.

        Args:
            current_metabolic_risk: Metabolic risk score of current product (0-100)
            candidate_metabolic_risk: Metabolic risk score of candidate product (0-100)

        Returns:
            Tuple of (score 0-100, ImprovementMetrics object)
        """

        if current_metabolic_risk == 0:
            score = 50
            improvement = 0
        else:
            improvement = ((current_metabolic_risk - candidate_metabolic_risk) / current_metabolic_risk) * 100
            score = max(0, min(100, improvement))

        metric = ImprovementMetrics(
            dimension=ImprovementDimension.METABOLIC,
            current_value=float(current_metabolic_risk),
            swap_value=float(candidate_metabolic_risk),
            absolute_improvement=float(current_metabolic_risk - candidate_metabolic_risk),
            percentage_improvement=improvement,
            direction="lower_better",
            weight=self.WEIGHTS["metabolic"] / 100,
        )

        return score, metric

    def calculate_deception_score(
        self,
        current_deception: int,
        candidate_deception: int,
    ) -> Tuple[float, ImprovementMetrics]:
        """
        Calculate deception reduction score.

        Lower deception score indicates more transparent labeling.

        Args:
            current_deception: Deception score of current product (0-100)
            candidate_deception: Deception score of candidate product (0-100)

        Returns:
            Tuple of (score 0-100, ImprovementMetrics object)
        """

        if current_deception == 0:
            score = 50
            improvement = 0
        else:
            improvement = ((current_deception - candidate_deception) / current_deception) * 100
            score = max(0, min(100, improvement))

        metric = ImprovementMetrics(
            dimension=ImprovementDimension.DECEPTION,
            current_value=float(current_deception),
            swap_value=float(candidate_deception),
            absolute_improvement=float(current_deception - candidate_deception),
            percentage_improvement=improvement,
            direction="lower_better",
            weight=self.WEIGHTS["deception"] / 100,
        )

        return score, metric

    def calculate_price_score(
        self,
        current_price_per_100g: float,
        candidate_price_per_100g: float,
    ) -> Tuple[float, ImprovementMetrics]:
        """
        Calculate price improvement score.

        Lower price per 100g is better for value.

        Args:
            current_price_per_100g: Price of current product (₹/100g)
            candidate_price_per_100g: Price of candidate product (₹/100g)

        Returns:
            Tuple of (score 0-100, ImprovementMetrics object)
        """

        if current_price_per_100g == 0:
            score = 50
            improvement = 0
        else:
            improvement = ((current_price_per_100g - candidate_price_per_100g) / current_price_per_100g) * 100
            score = max(0, min(100, improvement))

        metric = ImprovementMetrics(
            dimension=ImprovementDimension.PRICE,
            current_value=current_price_per_100g,
            swap_value=candidate_price_per_100g,
            absolute_improvement=current_price_per_100g - candidate_price_per_100g,
            percentage_improvement=improvement,
            direction="lower_better",
            unit="₹",
            weight=self.WEIGHTS["price"] / 100,
        )

        return score, metric

    def calculate_overall_score(
        self,
        current: Dict[str, Any],
        candidate: Dict[str, Any],
    ) -> Tuple[float, List[ImprovementMetrics], float]:
        """
        Calculate overall swap score (0-100).

        This method combines all 10 dimension scores using their respective
        weights to produce a final overall score. Higher scores indicate
        better swap recommendations.

        Args:
            current: Dictionary containing current product data
            candidate: Dictionary containing candidate product data

        Returns:
            Tuple of (total_score, list_of_improvements, overall_percentage)
        """

        all_improvements = []
        total_weighted_score = 0

        # Get nutrition data
        current_nutrition = current.get("nutrition", {})
        candidate_nutrition = candidate.get("nutrition", {})

        # Sugar score (15% weight)
        sugar_score, sugar_metric = self.calculate_sugar_score(
            current_nutrition.get("sugar", 0),
            candidate_nutrition.get("sugar", 0),
        )
        total_weighted_score += sugar_score * self.WEIGHTS["sugar"] / 100
        all_improvements.append(sugar_metric)

        # Sodium score (12% weight)
        sodium_score, sodium_metric = self.calculate_sodium_score(
            current_nutrition.get("sodium", 0),
            candidate_nutrition.get("sodium", 0),
        )
        total_weighted_score += sodium_score * self.WEIGHTS["sodium"] / 100
        all_improvements.append(sodium_metric)

        # Saturated fat score (10% weight)
        satfat_score, satfat_metric = self.calculate_saturated_fat_score(
            current_nutrition.get("saturated_fat", 0),
            candidate_nutrition.get("saturated_fat", 0),
        )
        total_weighted_score += satfat_score * self.WEIGHTS["saturated_fat"] / 100
        all_improvements.append(satfat_metric)

        # Fiber score (10% weight)
        fiber_score, fiber_metric = self.calculate_fiber_score(
            current_nutrition.get("fiber", 0),
            candidate_nutrition.get("fiber", 0),
        )
        total_weighted_score += fiber_score * self.WEIGHTS["fiber"] / 100
        all_improvements.append(fiber_metric)

        # Protein score (8% weight)
        protein_score, protein_metric = self.calculate_protein_score(
            current_nutrition.get("protein", 0),
            candidate_nutrition.get("protein", 0),
        )
        total_weighted_score += protein_score * self.WEIGHTS["protein"] / 100
        all_improvements.append(protein_metric)

        # Processing score (12% weight)
        processing_score, processing_metric = self.calculate_processing_score(
            current.get("nova_group", 4),
            candidate.get("nova_group", 4),
            current.get("processing_level", "ULTRA_PROCESSED"),
            candidate.get("processing_level", "PROCESSED"),
        )
        total_weighted_score += processing_score * self.WEIGHTS["processing"] / 100
        all_improvements.append(processing_metric)

        # Additives score (10% weight)
        additives_score, additives_metric = self.calculate_additives_score(
            current.get("additives_list", []),
            candidate.get("additives_list", []),
        )
        total_weighted_score += additives_score * self.WEIGHTS["additives"] / 100
        all_improvements.append(additives_metric)

        # Metabolic score (8% weight)
        metabolic_score, metabolic_metric = self.calculate_metabolic_score(
            current.get("metabolic_risk_score", 50),
            candidate.get("metabolic_risk_score", 30),
        )
        total_weighted_score += metabolic_score * self.WEIGHTS["metabolic"] / 100
        all_improvements.append(metabolic_metric)

        # Deception score (8% weight)
        deception_score, deception_metric = self.calculate_deception_score(
            current.get("deception_score", 50),
            candidate.get("deception_score", 20),
        )
        total_weighted_score += deception_score * self.WEIGHTS["deception"] / 100
        all_improvements.append(deception_metric)

        # Price score (7% weight)
        price_score, price_metric = self.calculate_price_score(
            current.get("price_per_100g", 50),
            candidate.get("price_per_100g", 40),
        )
        total_weighted_score += price_score * self.WEIGHTS["price"] / 100
        all_improvements.append(price_metric)

        # Calculate overall improvement percentage
        positive_improvements = [imp for imp in all_improvements if imp.percentage_improvement > 0]

        if positive_improvements:
            overall_percentage = sum(imp.percentage_improvement for imp in positive_improvements) / len(positive_improvements)
        else:
            overall_percentage = 0

        return round(total_weighted_score, 1), all_improvements, round(overall_percentage, 1)


# ==========================================================
# REASONING ENGINE
# ==========================================================


class ReasoningEngine:
    """
    Generate human-readable explanations for swap recommendations.

    This engine uses AI to generate intelligent, personalized explanations
    for why a particular swap is beneficial. It falls back to template-based
    reasoning when AI is unavailable.
    """

    def __init__(self) -> None:
        """
        Initialize the reasoning engine with AI client.
        """

        self.ai_client = ai_client

    async def generate_reasoning(
        self,
        current_product: Dict[str, Any],
        swap_candidate: Dict[str, Any],
        improvements: List[ImprovementMetrics],
        overall_improvement: float,
    ) -> Tuple[List[str], str, str]:
        """
        Generate why this swap is better.

        This method creates a list of human-readable reasons why the swap
        is beneficial, along with monthly health gain projection and a
        recommendation text.

        Args:
            current_product: Dictionary with current product data
            swap_candidate: Dictionary with candidate product data
            improvements: List of ImprovementMetrics objects
            overall_improvement: Overall improvement percentage

        Returns:
            Tuple of (why_better_list, monthly_health_gain, recommendation)
        """

        why_better = []

        # Extract top 5 improvements (positive only)
        top_improvements = sorted(
            [imp for imp in improvements if imp.percentage_improvement > 0],
            key=lambda x: x.percentage_improvement,
            reverse=True,
        )[:5]

        for imp in top_improvements:
            if imp.dimension == ImprovementDimension.SUGAR:
                why_better.append(
                    f"{imp.percentage_improvement:.0f}% lower sugar → "
                    "better for diabetes prevention and weight management"
                )

            elif imp.dimension == ImprovementDimension.SODIUM:
                why_better.append(
                    f"{imp.percentage_improvement:.0f}% lower sodium → "
                    "heart health improvement and better blood pressure"
                )

            elif imp.dimension == ImprovementDimension.SATURATED_FAT:
                why_better.append(
                    f"{imp.percentage_improvement:.0f}% less saturated fat → "
                    "lower cholesterol and heart disease risk"
                )

            elif imp.dimension == ImprovementDimension.FIBER:
                why_better.append(
                    f"{imp.percentage_improvement:.0f}% more fiber → "
                    "better digestion, satiety, and blood sugar control"
                )

            elif imp.dimension == ImprovementDimension.PROTEIN:
                why_better.append(
                    f"{imp.percentage_improvement:.0f}% more protein → "
                    "improved muscle health and satiety"
                )

            elif imp.dimension == ImprovementDimension.PROCESSING:
                why_better.append(
                    f"Less processed (better NOVA score) → "
                    "fewer industrial additives and preservatives"
                )

            elif imp.dimension == ImprovementDimension.ADDITIVES:
                why_better.append(
                    f"{imp.percentage_improvement:.0f}% fewer harmful additives → "
                    "cleaner ingredient list for better health"
                )

            elif imp.dimension == ImprovementDimension.METABOLIC:
                why_better.append(
                    f"{imp.percentage_improvement:.0f}% lower metabolic stress → "
                    "better insulin response and reduced inflammation"
                )

            elif imp.dimension == ImprovementDimension.DECEPTION:
                why_better.append(
                    f"{imp.percentage_improvement:.0f}% more transparent labeling → "
                    "fewer misleading health claims"
                )

            elif imp.dimension == ImprovementDimension.PRICE:
                if imp.percentage_improvement > 0:
                    why_better.append(
                        f"Saves {imp.percentage_improvement:.0f}% on your grocery bill → "
                        "better value for money without compromising health"
                    )

        # Monthly health gain estimate based on improvement
        if overall_improvement > 40:
            monthly_gain = f"+{overall_improvement:.0f}%"

            recommendation = (
                "🏆 Excellent swap! Switch immediately for significant health benefits. "
                "Your body will thank you within weeks. This is one of the best choices you can make."
            )

        elif overall_improvement > 25:
            monthly_gain = f"+{overall_improvement:.0f}%"

            recommendation = (
                "✅ Great improvement! Consider making this your regular choice. "
                "You'll notice positive changes within a month."
            )

        elif overall_improvement > 10:
            monthly_gain = f"+{overall_improvement:.0f}%"

            recommendation = (
                "📈 Good improvement! A step in the right direction. "
                "Every small change adds up over time for better health."
            )

        elif overall_improvement > 0:
            monthly_gain = f"+{overall_improvement:.0f}%"

            recommendation = (
                "🌱 Moderate improvement. Small changes lead to big results. "
                "Keep making healthier choices!"
            )

        else:
            monthly_gain = "0%"

            recommendation = (
                "⚖️ Similar quality product. Consider other alternatives "
                "for better health benefits."
            )

        # Try AI for enhanced reasoning (async, non-blocking)
        try:
            ai_reasoning = await self._get_ai_reasoning(
                current_product,
                swap_candidate,
                improvements,
                overall_improvement,
            )

            if ai_reasoning:
                why_better.insert(0, ai_reasoning)

        except Exception as e:
            logger.warning(f"AI reasoning failed: {e}")

        return why_better[:5], monthly_gain, recommendation

    async def _get_ai_reasoning(
        self,
        current: Dict[str, Any],
        candidate: Dict[str, Any],
        improvements: List[ImprovementMetrics],
        overall: float,
    ) -> Optional[str]:
        """
        Get AI-powered reasoning for the swap.

        This method calls the AI client to generate a concise, personalized
        explanation of why the swap is beneficial.

        Args:
            current: Current product data
            candidate: Candidate product data
            improvements: List of improvements
            overall: Overall improvement percentage

        Returns:
            AI-generated reasoning string or None if failed
        """

        try:
            top_imp = [imp for imp in improvements if imp.percentage_improvement > 0][:3]

            improvements_text = ", ".join([
                f"{imp.percentage_improvement:.0f}% better in {imp.dimension.value}"
                for imp in top_imp
            ])

            prompt = f"""
As a nutrition expert, explain why "{candidate.get('name', 'this product')}" is a healthier alternative to
"{current.get('name', 'the current product')}" in ONE sentence.

Context:
- Overall improvement: {overall:.0f}%
- Key improvements: {improvements_text}

Keep it concise, factual, and impactful for a health-conscious Indian consumer.
Focus on specific health benefits like diabetes, heart health, weight management, or digestion.
"""

            response, provider = await self.ai_client.generate(prompt, max_tokens=150, temperature=0.3)

            return response.strip()[:250]

        except Exception as e:
            logger.warning(f"AI reasoning generation failed: {e}")

            return None


# ==========================================================
# COMPARISON ENGINE
# ==========================================================


class ComparisonEngine:
    """
    Generate side-by-side nutritional comparison for frontend display.

    This engine creates data structures suitable for frontend visualization,
    including radar chart data and comparison tables.
    """

    def generate_comparison(
        self,
        current_nutrition: Dict[str, float],
        best_swap_nutrition: Dict[str, float],
        current_nova: int,
        swap_nova: int,
        current_additives: int,
        swap_additives: int,
        current_price: float,
        swap_price: float,
        current_calories: float,
        swap_calories: float,
        current_processing: str,
        swap_processing: str,
    ) -> Tuple[ComparisonSummary, ComparisonData]:
        """
        Generate complete comparison data for frontend.

        This method creates both a quick summary (for dashboards) and
        detailed comparison data (for radar charts and tables).

        Args:
            current_nutrition: Nutrition data of current product
            best_swap_nutrition: Nutrition data of best swap
            current_nova: NOVA group of current product
            swap_nova: NOVA group of swap product
            current_additives: Additive count of current product
            swap_additives: Additive count of swap product
            current_price: Price of current product
            swap_price: Price of swap product
            current_calories: Calories of current product
            swap_calories: Calories of swap product
            current_processing: Processing level of current product
            swap_processing: Processing level of swap product

        Returns:
            Tuple of (ComparisonSummary, ComparisonData)
        """

        def calculate_diff(current: float, swap: float) -> str:
            """Calculate percentage difference between two values."""

            if current == 0:
                return "+∞" if swap > 0 else "0%"

            diff = ((swap - current) / current) * 100
            sign = "+" if diff > 0 else ""

            return f"{sign}{diff:.0f}%"

        def calculate_improvement(current: float, swap: float, lower_is_better: bool = True) -> str:
            """Calculate improvement percentage (positive means better)."""

            if current == 0:
                return "+∞" if swap > 0 else "0%"

            diff = ((swap - current) / current) * 100

            if lower_is_better:
                improvement = -diff
            else:
                improvement = diff

            sign = "+" if improvement > 0 else ""

            return f"{sign}{improvement:.0f}%"

        # Comparison summary (quick view for dashboards)
        summary = ComparisonSummary(
            protein=calculate_improvement(
                current_nutrition.get("protein", 0),
                best_swap_nutrition.get("protein", 0),
                lower_is_better=False,
            ),
            fiber=calculate_improvement(
                current_nutrition.get("fiber", 0),
                best_swap_nutrition.get("fiber", 0),
                lower_is_better=False,
            ),
            sugar=calculate_improvement(
                current_nutrition.get("sugar", 0),
                best_swap_nutrition.get("sugar", 0),
                lower_is_better=True,
            ),
            sodium=calculate_improvement(
                current_nutrition.get("sodium", 0),
                best_swap_nutrition.get("sodium", 0),
                lower_is_better=True,
            ),
            saturated_fat=calculate_improvement(
                current_nutrition.get("saturated_fat", 0),
                best_swap_nutrition.get("saturated_fat", 0),
                lower_is_better=True,
            ),
            additives=(
                f"-{((current_additives - swap_additives) / max(current_additives, 1)) * 100:.0f}%"
                if current_additives > swap_additives
                else "+0%"
            ),
            processing=self._get_processing_improvement(current_processing, swap_processing),
            price=calculate_improvement(
                current_price,
                swap_price,
                lower_is_better=True,
            ),
        )

        # Detailed comparison data (for radar chart and detailed table)
        comparison_data = ComparisonData(
            current_protein=current_nutrition.get("protein", 0),
            current_fiber=current_nutrition.get("fiber", 0),
            current_sugar=current_nutrition.get("sugar", 0),
            current_sodium=current_nutrition.get("sodium", 0),
            current_saturated_fat=current_nutrition.get("saturated_fat", 0),
            current_additives=current_additives,
            current_nova=current_nova,
            current_calories=current_calories,
            current_price_per_100g=current_price,
            swap_protein=best_swap_nutrition.get("protein", 0),
            swap_fiber=best_swap_nutrition.get("fiber", 0),
            swap_sugar=best_swap_nutrition.get("sugar", 0),
            swap_sodium=best_swap_nutrition.get("sodium", 0),
            swap_saturated_fat=best_swap_nutrition.get("saturated_fat", 0),
            swap_additives=swap_additives,
            swap_nova=swap_nova,
            swap_calories=swap_calories,
            swap_price_per_100g=swap_price,
            protein_diff=summary.protein,
            fiber_diff=summary.fiber,
            sugar_diff=summary.sugar,
            sodium_diff=summary.sodium,
            saturated_fat_diff=summary.saturated_fat,
            additives_diff=summary.additives,
            nova_diff=summary.processing,
            calories_diff=calculate_diff(current_calories, swap_calories),
            price_diff=summary.price,
        )

        return summary, comparison_data

    def _get_processing_improvement(self, current: str, swap: str) -> str:
        """
        Calculate processing level improvement as percentage.

        Args:
            current: Processing level of current product
            swap: Processing level of swap product

        Returns:
            Formatted improvement percentage string
        """

        processing_levels = {
            "RAW": 1,
            "FRESH": 1,
            "UNPROCESSED": 1,
            "MINIMALLY_PROCESSED": 2,
            "PROCESSED": 3,
            "HIGHLY_PROCESSED": 4,
            "ULTRA_PROCESSED": 5,
        }

        current_score = processing_levels.get(current.upper(), 3)
        swap_score = processing_levels.get(swap.upper(), 3)

        if current_score == swap_score:
            return "0%"

        improvement = ((current_score - swap_score) / current_score) * 100

        if improvement > 0:
            return f"-{improvement:.0f}%"

        return f"+{abs(improvement):.0f}%"


# ==========================================================
# RANKING ENGINE
# ==========================================================


class RankingEngine:
    """
    Rank swap candidates based on overall score and user preferences.

    This engine supports multiple sorting strategies including health score,
    price, improvement percentage, best value, NOVA group, and Nutri-Score.
    """

    def rank_candidates(
        self,
        scored_candidates: List[Tuple[float, SwapCandidate]],
        sort_by: SortByOption,
        max_results: int = 6,
    ) -> List[SwapCandidate]:
        """
        Rank candidates according to sort_by option.

        Args:
            scored_candidates: List of (score, candidate) tuples
            sort_by: Sorting strategy to use
            max_results: Maximum number of results to return

        Returns:
            List of ranked SwapCandidate objects
        """

        if sort_by == SortByOption.HEALTH_SCORE:
            scored_candidates.sort(key=lambda x: x[0], reverse=True)

        elif sort_by == SortByOption.PRICE_LOW_TO_HIGH:
            scored_candidates.sort(
                key=lambda x: x[1].price.price_per_100g if x[1].price else float("inf"),
                reverse=False,
            )

        elif sort_by == SortByOption.PRICE_HIGH_TO_LOW:
            scored_candidates.sort(
                key=lambda x: x[1].price.price_per_100g if x[1].price else 0,
                reverse=True,
            )

        elif sort_by == SortByOption.IMPROVEMENT_PERCENTAGE:
            scored_candidates.sort(
                key=lambda x: x[1].overall_improvement_percentage,
                reverse=True,
            )

        elif sort_by == SortByOption.BEST_VALUE:
            scored_candidates.sort(
                key=lambda x: x[1].health_value_score.value_per_rupee if x[1].health_value_score else 0,
                reverse=True,
            )

        elif sort_by == SortByOption.NOVA_GROUP:
            scored_candidates.sort(
                key=lambda x: x[1].nova_group,
                reverse=False,
            )

        elif sort_by == SortByOption.NUTRI_SCORE:
            scored_candidates.sort(
                key=lambda x: x[1].nutriscore if x[1].nutriscore else "Z",
                reverse=False,
            )

        else:
            scored_candidates.sort(key=lambda x: x[0], reverse=True)

        return [candidate for _, candidate in scored_candidates[:max_results]]


# ==========================================================
# HEALTH VALUE CALCULATOR
# ==========================================================


class HealthValueCalculator:
    """
    Calculate health value score - nutrition quality per rupee.

    This calculator helps users find products that offer the best
    nutritional value for their money.
    """

    @staticmethod
    def calculate(health_score: float, price_per_100g: float) -> HealthValueScore:
        """
        Calculate health value score (0-100 scale).

        Higher score means better nutrition per rupee.

        Args:
            health_score: Health score of the product (0-100)
            price_per_100g: Price per 100g in rupees

        Returns:
            HealthValueScore object with value score and comparison
        """

        if price_per_100g <= 0:
            return HealthValueScore(
                score=0,
                rank_in_category=0,
                rank_in_all_products=0,
                percentile_in_category=0,
                value_per_rupee=0,
                comparison_to_avg="AVERAGE",
            )

        value_per_rupee = (health_score / price_per_100g) * 10

        if value_per_rupee > 20:
            comparison = "EXCELLENT"
        elif value_per_rupee > 15:
            comparison = "GOOD"
        elif value_per_rupee > 10:
            comparison = "AVERAGE"
        elif value_per_rupee > 5:
            comparison = "POOR"
        else:
            comparison = "VERY_POOR"

        return HealthValueScore(
            score=int(health_score),
            rank_in_category=0,
            rank_in_all_products=0,
            percentile_in_category=0,
            value_per_rupee=round(value_per_rupee, 2),
            comparison_to_avg=comparison,
        )


# ==========================================================
# MONTHLY PROJECTION CALCULATOR
# ==========================================================


class MonthlyProjectionCalculator:
    """
    Calculate estimated health improvement over time.

    This calculator provides projections of health improvements over
    monthly and yearly timeframes based on the swap's health impact.
    """

    @staticmethod
    def calculate(
        current_product_health: int,
        swap_product_health: int,
        consumption_frequency: str = "daily",
        servings_per_week: int = 5,
    ) -> str:
        """
        Calculate monthly health improvement projection.

        Args:
            current_product_health: Health score of current product
            swap_product_health: Health score of swap product
            consumption_frequency: How often the product is consumed
            servings_per_week: Number of servings per week

        Returns:
            Formatted string with percentage and description
        """

        health_gap = swap_product_health - current_product_health

        # Frequency multiplier (how often the product is consumed)
        frequency_multiplier = {
            "daily": 30,
            "weekly": 4,
            "occasional": 2,
            "rarely": 1,
        }

        freq_factor = frequency_multiplier.get(consumption_frequency, 10)

        # Calculate monthly impact
        monthly_impact = (health_gap / 100) * freq_factor * 0.3

        if monthly_impact > 0.4:
            return (
                f"+{monthly_impact * 100:.0f}% monthly health improvement (significant). "
                f"Switching to this product could meaningfully improve your metabolic health."
            )

        elif monthly_impact > 0.2:
            return (
                f"+{monthly_impact * 100:.0f}% monthly health improvement (moderate). "
                f"Consistent consumption will yield noticeable benefits."
            )

        elif monthly_impact > 0.05:
            return (
                f"+{monthly_impact * 100:.0f}% monthly health improvement (small). "
                f"Every healthy choice adds up over time."
            )

        elif monthly_impact > 0:
            return f"+{monthly_impact * 100:.0f}% monthly health improvement (minimal)."

        else:
            return "No significant monthly improvement expected with this swap."

    @staticmethod
    def calculate_yearly_projection(
        current_product_health: int,
        swap_product_health: int,
        consumption_frequency: str = "daily",
    ) -> str:
        """
        Calculate yearly health improvement projection.

        Args:
            current_product_health: Health score of current product
            swap_product_health: Health score of swap product
            consumption_frequency: How often the product is consumed

        Returns:
            Formatted string with yearly projection
        """

        health_gap = swap_product_health - current_product_health

        frequency_multiplier = {
            "daily": 365,
            "weekly": 52,
            "occasional": 26,
            "rarely": 12,
        }

        freq_factor = frequency_multiplier.get(consumption_frequency, 100)

        yearly_impact = (health_gap / 100) * freq_factor * 0.1

        if yearly_impact > 50:
            return (
                f"🏆 Exceptional! Over a year, this swap could improve your health score by "
                f"{yearly_impact:.0f}%. This is a transformative change."
            )

        elif yearly_impact > 20:
            return (
                f"🌟 Great choice! Over a year, this swap could improve your health score by "
                f"{yearly_impact:.0f}%. Your body will thank you."
            )

        elif yearly_impact > 5:
            return (
                f"📈 Good progress! Over a year, this swap could improve your health score by "
                f"{yearly_impact:.0f}%. Small changes add up!"
            )

        elif yearly_impact > 0:
            return (
                f"🌱 Over a year, this swap could improve your health score by "
                f"{yearly_impact:.0f}%. Keep making healthy choices!"
            )

        else:
            return "Consider other alternatives for significant yearly health benefits."


# ==========================================================
# EXPORT GENERATOR
# ==========================================================


class ExportGenerator:
    """
    Generate exports of swap recommendations in various formats.

    Supports CSV, Markdown, HTML, JSON, and Excel formats for
    sharing and downloading swap recommendations.
    """

    @staticmethod
    def to_csv(response: SmartSwapResponse) -> str:
        """
        Generate CSV export of swap recommendations.

        Args:
            response: SmartSwapResponse object

        Returns:
            CSV string
        """

        output = io.StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow([
            "Rank", "Product Name", "Brand", "Health Score", "Improvement",
            "Protein (g)", "Fiber (g)", "Sugar (g)", "Sodium (mg)",
            "Saturated Fat (g)", "Price (₹/100g)", "Why Better"
        ])

        # Data rows
        for idx, swap in enumerate(response.top_swaps, 1):
            writer.writerow([
                idx,
                swap.name,
                swap.brand or "N/A",
                swap.score_rounded,
                f"{swap.overall_improvement_percentage:.0f}%",
                swap.protein or 0,
                swap.fiber or 0,
                swap.sugar or 0,
                swap.sodium or 0,
                swap.saturated_fat or 0,
                swap.price.price_per_100g if swap.price else "N/A",
                swap.why_better[0] if swap.why_better else "N/A",
            ])

        return output.getvalue()

    @staticmethod
    def to_markdown(response: SmartSwapResponse) -> str:
        """
        Generate Markdown export of swap recommendations.

        Args:
            response: SmartSwapResponse object

        Returns:
            Markdown string
        """

        lines = [
            f"# Smart Swap Recommendations for {response.current_product.get('name', 'Product')}",
            "",
            f"**Current Health Score:** {response.current_health_score}/100",
            f"**NOVA Group:** {response.current_nova_group}",
            f"**Processing Level:** {response.current_processing_level}",
            "",
            "## Top Swap Recommendations",
            "",
        ]

        for idx, swap in enumerate(response.top_swaps, 1):
            lines.extend([
                f"### {idx}. {swap.name}",
                f"- **Brand:** {swap.brand or 'N/A'}",
                f"- **Health Score:** {swap.score_rounded}/100",
                f"- **Improvement:** {swap.overall_improvement_percentage:.0f}% better",
                f"- **Why Better:** {swap.why_better[0] if swap.why_better else 'N/A'}",
                "",
                f"**Nutrition per 100g:**",
                f"- Protein: {swap.protein or 0}g",
                f"- Fiber: {swap.fiber or 0}g",
                f"- Sugar: {swap.sugar or 0}g",
                f"- Sodium: {swap.sodium or 0}mg",
                f"- Price: ₹{swap.price.price_per_100g if swap.price else 0}/100g",
                "",
            ])

        if response.ai_reasoning:
            lines.extend([
                "## AI Summary",
                "",
                response.ai_reasoning,
                "",
            ])

        return "\n".join(lines)

    @staticmethod
    def to_html(response: SmartSwapResponse) -> str:
        """
        Generate HTML export of swap recommendations.

        Args:
            response: SmartSwapResponse object

        Returns:
            HTML string
        """

        swaps_html = ""

        for idx, swap in enumerate(response.top_swaps, 1):
            swaps_html += f"""
            <div class="swap-card" style="border:1px solid #ddd; border-radius:8px; padding:15px; margin-bottom:15px;">
                <h3>{idx}. {swap.name}</h3>
                <p><strong>Brand:</strong> {swap.brand or 'N/A'}</p>
                <p><strong>Health Score:</strong> <span style="color:{swap.score_color}">{swap.score_rounded}/100</span></p>
                <p><strong>Improvement:</strong> {swap.overall_improvement_percentage:.0f}% better</p>
                <p><strong>Why Better:</strong> {swap.why_better[0] if swap.why_better else 'N/A'}</p>
                <details>
                    <summary>Nutrition Details</summary>
                    <ul>
                        <li>Protein: {swap.protein or 0}g</li>
                        <li>Fiber: {swap.fiber or 0}g</li>
                        <li>Sugar: {swap.sugar or 0}g</li>
                        <li>Sodium: {swap.sodium or 0}mg</li>
                        <li>Price: ₹{swap.price.price_per_100g if swap.price else 0}/100g</li>
                    </ul>
                </details>
            </div>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Smart Swap Recommendations</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background: #2ECC71; color: white; padding: 20px; border-radius: 8px; }}
                .comparison {{ background: #f5f5f5; padding: 15px; border-radius: 8px; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Smart Swap Recommendations</h1>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>

            <div class="comparison">
                <h2>Current Product: {response.current_product.get('name', 'Product')}</h2>
                <p>Health Score: {response.current_health_score}/100 | NOVA: {response.current_nova_group}</p>
            </div>

            <h2>Top {len(response.top_swaps)} Alternatives</h2>
            {swaps_html}

            <div class="comparison">
                <h3>Comparison Summary</h3>
                <p>Protein: {response.comparison_summary.protein}</p>
                <p>Fiber: {response.comparison_summary.fiber}</p>
                <p>Sugar: {response.comparison_summary.sugar}</p>
                <p>Sodium: {response.comparison_summary.sodium}</p>
                <p>Saturated Fat: {response.comparison_summary.saturated_fat}</p>
                <p>Price: {response.comparison_summary.price}</p>
            </div>

            <footer style="margin-top: 30px; font-size: 12px; color: #888;">
                Generated by Scanix AI - Smart Food Intelligence
            </footer>
        </body>
        </html>
        """

        return html

    @staticmethod
    def to_json(response: SmartSwapResponse) -> str:
        """
        Generate JSON export of swap recommendations.

        Args:
            response: SmartSwapResponse object

        Returns:
            JSON string
        """

        return json.dumps(response.model_dump(), indent=2, default=str)

    @staticmethod
    def to_excel(response: SmartSwapResponse) -> bytes:
        """
        Generate Excel export of swap recommendations.

        Args:
            response: SmartSwapResponse object

        Returns:
            Excel file as bytes
        """

        try:
            # openpyxl is an optional dependency; silence static analyzers if it's not installed
            import openpyxl  # type: ignore
            from openpyxl.styles import Font, PatternFill, Alignment  # type: ignore

            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Swap Recommendations"

            # Header
            headers = [
                "Rank", "Product Name", "Brand", "Health Score", "Improvement",
                "Protein (g)", "Fiber (g)", "Sugar (g)", "Sodium (mg)",
                "Saturated Fat (g)", "Price (₹/100g)", "Why Better"
            ]

            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.font = Font(bold=True)
                cell.fill = PatternFill(start_color="2ECC71", end_color="2ECC71", fill_type="solid")
                cell.alignment = Alignment(horizontal="center")

            # Data rows
            for row_idx, swap in enumerate(response.top_swaps, 2):
                ws.cell(row=row_idx, column=1, value=row_idx - 1)
                ws.cell(row=row_idx, column=2, value=swap.name)
                ws.cell(row=row_idx, column=3, value=swap.brand or "N/A")
                ws.cell(row=row_idx, column=4, value=swap.score_rounded)
                ws.cell(row=row_idx, column=5, value=f"{swap.overall_improvement_percentage:.0f}%")
                ws.cell(row=row_idx, column=6, value=swap.protein or 0)
                ws.cell(row=row_idx, column=7, value=swap.fiber or 0)
                ws.cell(row=row_idx, column=8, value=swap.sugar or 0)
                ws.cell(row=row_idx, column=9, value=swap.sodium or 0)
                ws.cell(row=row_idx, column=10, value=swap.saturated_fat or 0)
                ws.cell(row=row_idx, column=11, value=swap.price.price_per_100g if swap.price else 0)
                ws.cell(row=row_idx, column=12, value=swap.why_better[0] if swap.why_better else "N/A")

            # Adjust column widths
            for col in ws.columns:
                max_length = 0
                col_letter = col[0].column_letter

                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass

                adjusted_width = min(max_length + 2, 50)
                ws.column_dimensions[col_letter].width = adjusted_width

            output = io.BytesIO()
            wb.save(output)

            return output.getvalue()

        except ImportError:
            logger.warning("openpyxl not installed, returning CSV instead")

            return ExportGenerator.to_csv(response).encode()


# ==========================================================
# ANALYTICS COLLECTOR
# ==========================================================


class AnalyticsCollector:
    """
    Collect analytics for swap recommendations.

    Tracks usage patterns, improvements, popular swaps, and provides
    summary statistics for monitoring and improvement.
    """

    def __init__(self) -> None:
        """
        Initialize analytics collector with empty data structures.
        """

        self._events: List[Dict[str, Any]] = []

        self._aggregated: Dict[str, Any] = {
            "total_swaps_recommended": 0,
            "total_swaps_selected": 0,
            "average_improvement": 0,
            "top_categories": Counter(),
            "top_brands": Counter(),
            "response_times": [],
            "source_distribution": Counter(),
        }

    def record_swap_recommended(
        self,
        current_product: str,
        swap_product: str,
        improvement: float,
        source: str,
        processing_time_ms: int,
    ) -> None:
        """
        Record a swap recommendation event.

        Args:
            current_product: Name of current product
            swap_product: Name of recommended swap product
            improvement: Improvement percentage
            source: Source of the recommendation
            processing_time_ms: Time taken to generate recommendation
        """

        self._events.append({
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "recommended",
            "current_product": current_product,
            "swap_product": swap_product,
            "improvement": improvement,
            "source": source,
            "processing_time_ms": processing_time_ms,
        })

        self._aggregated["total_swaps_recommended"] += 1
        self._aggregated["response_times"].append(processing_time_ms)
        self._aggregated["source_distribution"][source] += 1

        total_improvement = self._aggregated["average_improvement"] * (self._aggregated["total_swaps_recommended"] - 1)
        self._aggregated["average_improvement"] = (total_improvement + improvement) / self._aggregated["total_swaps_recommended"]

    def record_swap_selected(
        self,
        swap_product: str,
        improvement: float,
    ) -> None:
        """
        Record when a user selects a swap.

        Args:
            swap_product: Name of selected swap product
            improvement: Improvement percentage of selected swap
        """

        self._events.append({
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "selected",
            "swap_product": swap_product,
            "improvement": improvement,
        })

        self._aggregated["total_swaps_selected"] += 1

    def record_category_click(self, category: str) -> None:
        """
        Record category click for analytics.

        Args:
            category: Category name clicked
        """

        self._aggregated["top_categories"][category] += 1

    def record_brand_view(self, brand: str) -> None:
        """
        Record brand view for analytics.

        Args:
            brand: Brand name viewed
        """

        self._aggregated["top_brands"][brand] += 1

    def get_summary(self) -> Dict[str, Any]:
        """
        Get analytics summary.

        Returns:
            Dictionary containing analytics summary
        """

        avg_response_time = (
            sum(self._aggregated["response_times"]) / len(self._aggregated["response_times"])
            if self._aggregated["response_times"]
            else 0
        )

        conversion_rate = (
            (self._aggregated["total_swaps_selected"] / self._aggregated["total_swaps_recommended"]) * 100
            if self._aggregated["total_swaps_recommended"] > 0
            else 0
        )

        return {
            "total_swaps_recommended": self._aggregated["total_swaps_recommended"],
            "total_swaps_selected": self._aggregated["total_swaps_selected"],
            "conversion_rate": round(conversion_rate, 1),
            "average_improvement": round(self._aggregated["average_improvement"], 1),
            "average_response_time_ms": round(avg_response_time, 1),
            "top_categories": dict(self._aggregated["top_categories"].most_common(5)),
            "top_brands": dict(self._aggregated["top_brands"].most_common(5)),
            "source_distribution": dict(self._aggregated["source_distribution"]),
        }

    def get_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get recent events.

        Args:
            limit: Maximum number of events to return

        Returns:
            List of recent events
        """

        return self._events[-limit:]

    def clear(self) -> None:
        """
        Clear all analytics data.
        """

        self._events.clear()

        self._aggregated = {
            "total_swaps_recommended": 0,
            "total_swaps_selected": 0,
            "average_improvement": 0,
            "top_categories": Counter(),
            "top_brands": Counter(),
            "response_times": [],
            "source_distribution": Counter(),
        }


# ==========================================================
# SWAP VALIDATOR
# ==========================================================


class SwapValidator:
    """
    Validate swap requests and responses for data integrity.

    This class ensures that input requests and output responses meet
    quality standards before processing or returning to clients.
    """

    @staticmethod
    def validate_request(request: SwapRequest) -> Tuple[bool, List[str]]:
        """
        Validate swap request.

        Args:
            request: SwapRequest object to validate

        Returns:
            Tuple of (is_valid, list_of_errors)
        """

        errors = []

        if not request.product_name or len(request.product_name) < 2:
            errors.append("Product name must be at least 2 characters")

        if request.max_results < 1 or request.max_results > 20:
            errors.append("max_results must be between 1 and 20")

        if request.nova_group < 1 or request.nova_group > 4:
            errors.append("nova_group must be between 1 and 4")

        if request.deception_score < 0 or request.deception_score > 100:
            errors.append("deception_score must be between 0 and 100")

        if request.metabolic_risk_score < 0 or request.metabolic_risk_score > 100:
            errors.append("metabolic_risk_score must be between 0 and 100")

        if request.organ_impact_score < 0 or request.organ_impact_score > 100:
            errors.append("organ_impact_score must be between 0 and 100")

        return len(errors) == 0, errors

    @staticmethod
    def validate_response(response: SmartSwapResponse) -> Tuple[bool, List[str]]:
        """
        Validate swap response.

        Args:
            response: SmartSwapResponse object to validate

        Returns:
            Tuple of (is_valid, list_of_errors)
        """

        errors = []

        if response.current_health_score < 0 or response.current_health_score > 100:
            errors.append("current_health_score out of range")

        if response.total_candidates_found < 0:
            errors.append("total_candidates_found cannot be negative")

        if len(response.top_swaps) > response.total_candidates_found:
            errors.append("top_swaps count exceeds total_candidates_found")

        return len(errors) == 0, errors


# ==========================================================
# MASTER SMART SWAP SERVICE
# ==========================================================


class SmartSwapService:
    """
    Master orchestrator for System 7 - Smart Food Intelligence.

    This service consumes output from Systems 1-6 and returns ranked
    swap recommendations. It integrates with all providers and engines
    to provide intelligent, personalized food swap recommendations.

    Features:
    - 10-dimension scoring with weights calibrated for India
    - AI-powered reasoning with fallback
    - Health condition filtering (diabetes, heart disease, etc.)
    - Multi-format exports (CSV, Markdown, HTML, JSON, Excel)
    - Analytics and usage tracking
    - Response caching for performance
    """

    def __init__(self) -> None:
        """
        Initialize the smart swap service with all engines.
        """

        self.scoring_engine = ScoringEngine()
        self.reasoning_engine = ReasoningEngine()
        self.comparison_engine = ComparisonEngine()
        self.ranking_engine = RankingEngine()
        self.health_value_calc = HealthValueCalculator()
        self.monthly_projection_calc = MonthlyProjectionCalculator()
        self.export_generator = ExportGenerator()
        self.analytics = AnalyticsCollector()
        self.validator = SwapValidator()
        self.condition_advisor = HealthConditionAdvisor()
        self.cache = cache_manager

    async def get_swaps(
        self,
        request: SwapRequest,
        record_analytics: bool = True,
        health_condition: Optional[str] = None,
    ) -> SmartSwapResponse:
        """
        Main entry point for smart swap recommendations.

        This method orchestrates the entire swap recommendation process
        including discovery, scoring, ranking, and explanation generation.

        Args:
            request: SwapRequest from Systems 1-6
            record_analytics: Whether to record analytics for this request
            health_condition: Optional health condition to filter swaps

        Returns:
            SmartSwapResponse with ranked swap recommendations
        """

        start_time = time.time()
        request_id = generate_request_id()

        logger.info(f"Processing swap request {request_id} for product: {request.product_name}")

        # Validate request
        is_valid, errors = self.validator.validate_request(request)

        if not is_valid:
            raise ScanixException(
                error_code=ErrorCode.VALIDATION_ERROR,
                message=f"Invalid request: {', '.join(errors)}",
                status_code=400,
            )

        # Extract data from request (Systems 1-6 integration)
        product_name = request.product_name
        brand = request.brand
        category = request.category

        # From System 1 - Scan Intelligence
        scan_confidence = request.scan_confidence

        # From System 2 - Ingredient Intelligence
        ingredients_list = request.ingredients_list
        additive_count = request.additive_count
        additives_list = request.additives_list
        processing_level = request.processing_level
        nova_group = request.nova_group
        contains_palm_oil = request.contains_palm_oil
        contains_hidden_sugar = request.contains_hidden_sugar
        hidden_sugar_count = request.hidden_sugar_count

        # From System 3 - Metabolic Intelligence
        metabolic_risk_score = request.metabolic_risk_score
        glycemic_load = request.glycemic_load
        insulin_response = request.insulin_response
        fat_accumulation_risk = request.fat_accumulation_risk
        inflammation_score = request.inflammation_score

        # From System 4 - Consumer Intelligence
        deception_score = request.deception_score
        compliance_status = request.compliance_status
        fssai_violations = request.fssai_violations
        marketing_claims = request.marketing_claims
        is_claim_inflated = request.is_claim_inflated

        # From System 5 - AI Nutrition Intelligence
        ai_product_summary = request.ai_product_summary
        ai_health_impact = request.ai_health_impact

        # From System 6 - Digital Twin
        organ_impact_score = request.organ_impact_score
        liver_impact = request.liver_impact
        heart_impact = request.heart_impact
        pancreas_impact = request.pancreas_impact
        kidney_impact = request.kidney_impact

        # Get current nutrition data
        current_nutrition = request.nutrition or {
            "protein": 0,
            "fat": 0,
            "saturated_fat": 0,
            "carbohydrates": 0,
            "sugar": 0,
            "fiber": 0,
            "sodium": 0,
            "calories": 0,
        }

        current_calories = current_nutrition.get("calories", 0)

        # Get current price per 100g
        current_price_per_100g = request.price_per_100g or DEFAULT_PRICE_PER_100G

        # Build current product context (integrates all systems)
        current_context = {
            "name": product_name,
            "brand": brand,
            "category": category,
            "nutrition": current_nutrition,
            "nova_group": nova_group,
            "processing_level": processing_level,
            "additive_count": additive_count,
            "additives_list": additives_list,
            "metabolic_risk_score": metabolic_risk_score,
            "organ_impact_score": organ_impact_score,
            "deception_score": deception_score,
            "price_per_100g": current_price_per_100g,
            # System 1
            "scan_confidence": scan_confidence,
            # System 2
            "contains_palm_oil": contains_palm_oil,
            "contains_hidden_sugar": contains_hidden_sugar,
            "hidden_sugar_count": hidden_sugar_count,
            # System 3
            "glycemic_load": glycemic_load,
            "insulin_response": insulin_response,
            "fat_accumulation_risk": fat_accumulation_risk,
            "inflammation_score": inflammation_score,
            # System 4
            "compliance_status": compliance_status,
            "fssai_violations": fssai_violations,
            "marketing_claims": marketing_claims,
            "is_claim_inflated": is_claim_inflated,
            # System 5
            "ai_product_summary": ai_product_summary,
            "ai_health_impact": ai_health_impact,
            # System 6
            "liver_impact": liver_impact,
            "heart_impact": heart_impact,
            "pancreas_impact": pancreas_impact,
            "kidney_impact": kidney_impact,
        }

        # Calculate current health score using System 3 & 4 data
        nutrition_obj = NutritionPer100g(
            energy_kcal=current_nutrition.get("calories", 0),
            protein=current_nutrition.get("protein", 0),
            fat=current_nutrition.get("fat", 0),
            saturated_fat=current_nutrition.get("saturated_fat", 0),
            carbohydrates=current_nutrition.get("carbohydrates", 0),
            sugar=current_nutrition.get("sugar", 0),
            fiber=current_nutrition.get("fiber", 0),
            sodium_mg=current_nutrition.get("sodium", 0),
        )

        current_health_score = health_calculator.calculate(nutrition_obj, nova_group)

        # Apply deception score penalty from System 4
        if deception_score > 70:
            current_health_score -= 10
        elif deception_score > 50:
            current_health_score -= 5

        # Apply metabolic risk penalty from System 3
        if metabolic_risk_score > 70:
            current_health_score -= 8
        elif metabolic_risk_score > 50:
            current_health_score -= 4

        # Apply digital twin penalty from System 6
        if organ_impact_score > 70:
            current_health_score -= 7

        current_health_score = max(0, min(100, current_health_score))

        # Check cache for this request
        cache_key = f"swap:{product_name}:{category}:{request.max_results}:{health_condition}"
        cached_response = self.cache.get(cache_key)

        if cached_response:
            logger.info(f"Cache hit for {request_id}")

            return SmartSwapResponse(**cached_response)

        # Discover alternatives using File 2 providers
        candidates, sources_used, ai_provider_used = await master_discovery_engine.discover_all(
            product_name=product_name,
            category=category,
            max_results=request.max_results * 4,
        )

        if not candidates:
            # Return empty response
            response = SmartSwapResponse(
                success=True,
                current_product=current_context,
                current_health_score=current_health_score,
                current_nova_group=nova_group,
                current_processing_level=processing_level,
                current_price_per_100g=current_price_per_100g,
                total_candidates_found=0,
                candidates_analyzed=0,
                top_swaps=[],
                comparison_summary=ComparisonSummary(),
                sources_used=sources_used,
                ai_provider_used=ai_provider_used,
                processing_time_ms=int((time.time() - start_time) * 1000),
                system_1_scan_data_used=bool(request.product_name),
                system_2_ingredient_data_used=bool(request.ingredients_list),
                system_3_metabolic_data_used=request.metabolic_risk_score != 50,
                system_4_consumer_data_used=request.deception_score != 50,
                system_5_ai_data_used=bool(request.ai_product_summary),
                system_6_digital_twin_data_used=request.organ_impact_score != 50,
            )

            if record_analytics:
                self.analytics.record_swap_recommended(
                    product_name, "none", 0, "none", response.processing_time_ms
                )

            # Cache the response
            self.cache.set(response.model_dump(), cache_key, ttl=CACHE_TTL_SECONDS)

            return response

        # Score each candidate and get prices
        scored_candidates = []

        for candidate in candidates:
            try:
                # Get price for candidate using File 2 provider
                price_obj = await price_intelligence_provider.get_price(
                    product_name=candidate.get("name", ""),
                    brand=candidate.get("brand"),
                    category=category,
                    weight_g=100,
                )

                # Build candidate nutrition
                candidate_nutrition = {
                    "protein": candidate.get("protein", 0),
                    "fat": candidate.get("fat", 0),
                    "saturated_fat": candidate.get("saturated_fat", 0),
                    "carbohydrates": candidate.get("carbohydrates", 0),
                    "sugar": candidate.get("sugar", 0),
                    "fiber": candidate.get("fiber", 0),
                    "sodium": candidate.get("sodium", 0),
                    "calories": candidate.get("calories", 0),
                }

                candidate_calories = candidate.get("calories", 0)

                # Build candidate context
                candidate_context = {
                    "name": candidate.get("name", ""),
                    "brand": candidate.get("brand"),
                    "nutrition": candidate_nutrition,
                    "nova_group": candidate.get("nova_group", 3),
                    "processing_level": candidate.get("processing_level", "PROCESSED"),
                    "additive_count": candidate.get("additive_count", 0),
                    "additives_list": candidate.get("additives_list", []),
                    "metabolic_risk_score": candidate.get("metabolic_risk_score", 30),
                    "deception_score": candidate.get("deception_score", 20),
                    "price_per_100g": price_obj.price_per_100g,
                }

                # Calculate overall score using scoring engine
                (
                    total_score,
                    improvements,
                    overall_improvement,
                ) = self.scoring_engine.calculate_overall_score(
                    current_context,
                    candidate_context,
                )

                # Generate reasoning
                (
                    why_better,
                    monthly_gain,
                    recommendation_text,
                ) = await self.reasoning_engine.generate_reasoning(
                    current_context,
                    candidate_context,
                    improvements,
                    overall_improvement,
                )

                # Determine confidence level based on score and source
                if total_score >= 80 and candidate.get("confidence", 0) >= 0.7:
                    confidence_level = SwapConfidence.HIGH
                elif total_score >= 60:
                    confidence_level = SwapConfidence.MEDIUM
                else:
                    confidence_level = SwapConfidence.LOW

                # Calculate health value score
                health_value_score = self.health_value_calc.calculate(
                    total_score,
                    price_obj.price_per_100g,
                )

                # Calculate monthly projection
                monthly_projection = self.monthly_projection_calc.calculate(
                    current_health_score,
                    int(total_score),
                )

                # Create aggregated improvement
                aggregated_improvement = AggregatedImprovement(
                    total_improvement_percentage=overall_improvement,
                    positive_dimensions_count=len([i for i in improvements if i.percentage_improvement > 0]),
                    negative_dimensions_count=len([i for i in improvements if i.percentage_improvement < 0]),
                    neutral_dimensions_count=len([i for i in improvements if i.percentage_improvement == 0]),
                    best_improvement=max(improvements, key=lambda x: x.percentage_improvement) if improvements else None,
                    weighted_average_improvement=total_score / 100,
                    improvements_by_dimension={i.dimension: i for i in improvements},
                )

                swap_candidate = SwapCandidate(
                    name=candidate.get("name", "Unknown"),
                    brand=candidate.get("brand"),
                    barcode=candidate.get("barcode"),
                    category=category,
                    source=candidate.get("source", "unknown"),
                    source_url=candidate.get("source_url"),
                    image_url=candidate.get("image_url"),
                    calories=candidate_calories,
                    protein=candidate_nutrition["protein"],
                    fat=candidate_nutrition["fat"],
                    saturated_fat=candidate_nutrition["saturated_fat"],
                    carbohydrates=candidate_nutrition["carbohydrates"],
                    sugar=candidate_nutrition["sugar"],
                    fiber=candidate_nutrition["fiber"],
                    sodium=candidate_nutrition["sodium"],
                    nova_group=candidate.get("nova_group", 3),
                    nutriscore=candidate.get("nutriscore"),
                    processing_level=candidate.get("processing_level", "PROCESSED"),
                    additive_count=candidate.get("additive_count", 0),
                    price=price_obj,
                    health_value_score=health_value_score,
                    overall_score=total_score,
                    confidence=total_score,
                    confidence_level=confidence_level,
                    improvements=improvements,
                    aggregated_improvement=aggregated_improvement,
                    overall_improvement_percentage=overall_improvement,
                    why_better=why_better,
                    monthly_health_gain=monthly_gain,
                    available_at=self._get_availability(candidate.get("brand")),
                )

                scored_candidates.append((total_score, swap_candidate))

            except Exception as e:
                logger.error(f"Failed to score candidate {candidate.get('name')}: {e}")
                continue

        # Filter by health condition if specified
        if health_condition:
            scored_candidates = [
                (score, candidate) for score, candidate in scored_candidates
                if self.condition_advisor.is_suitable_for_condition(
                    health_condition,
                    {
                        "sugar": candidate.sugar or 0,
                        "sodium": candidate.sodium or 0,
                        "saturated_fat": candidate.saturated_fat or 0,
                        "fiber": candidate.fiber or 0,
                        "protein": candidate.protein or 0,
                        "calories": candidate.calories or 0,
                    },
                    candidate.additives_list,
                    candidate.processing_level,
                )[0]
            ]

        # Rank candidates
        top_swaps = self.ranking_engine.rank_candidates(
            scored_candidates,
            request.sort_by,
            request.max_results,
        )

        # Generate comparison summary and data using best swap
        comparison_summary = ComparisonSummary()
        comparison_data = None
        best_value_swap = None
        best_health_swap = None
        ai_reasoning = None

        if top_swaps:
            best_swap = top_swaps[0]

            best_swap_nutrition = {
                "protein": best_swap.protein or 0,
                "fiber": best_swap.fiber or 0,
                "sugar": best_swap.sugar or 0,
                "sodium": best_swap.sodium or 0,
                "saturated_fat": best_swap.saturated_fat or 0,
            }

            comparison_summary, comparison_data = self.comparison_engine.generate_comparison(
                current_nutrition=current_nutrition,
                best_swap_nutrition=best_swap_nutrition,
                current_nova=nova_group,
                swap_nova=best_swap.nova_group,
                current_additives=additive_count,
                swap_additives=best_swap.additive_count,
                current_price=current_price_per_100g,
                swap_price=best_swap.price.price_per_100g if best_swap.price else 0,
                current_calories=current_calories,
                swap_calories=best_swap.calories or 0,
                current_processing=processing_level,
                swap_processing=best_swap.processing_level,
            )

            # Find best value swap (best health per rupee)
            best_value_swap = max(
                top_swaps,
                key=lambda x: x.health_value_score.value_per_rupee if x.health_value_score else 0,
            ).name

            best_health_swap = top_swaps[0].name

            # Generate AI summary for the best swap
            try:
                prompt = f"""
In one sentence, summarize why switching from "{product_name}" to "{best_swap.name}" is beneficial for health.

Improvement: {best_swap.overall_improvement_percentage:.0f}% better overall.
Key reasons: {', '.join(best_swap.why_better[:2])}

Keep it under 120 words, factual, and persuasive for an Indian consumer.
Focus on specific health benefits like diabetes, heart health, or weight management.
"""

                ai_reasoning, _ = await ai_client.generate(prompt, max_tokens=200, temperature=0.3)
                ai_reasoning = ai_reasoning.strip()

            except Exception as e:
                logger.warning(f"AI summary generation failed: {e}")

        processing_time_ms = int((time.time() - start_time) * 1000)

        # Build final response
        response = SmartSwapResponse(
            success=True,
            current_product=current_context,
            current_health_score=current_health_score,
            current_nova_group=nova_group,
            current_processing_level=processing_level,
            current_price_per_100g=current_price_per_100g,
            total_candidates_found=len(candidates),
            candidates_analyzed=len(scored_candidates),
            top_swaps=top_swaps,
            comparison_summary=comparison_summary,
            comparison_data=comparison_data,
            best_value_swap=best_value_swap,
            best_health_swap=best_health_swap,
            ai_reasoning=ai_reasoning,
            recommendation=top_swaps[0].why_better[0] if top_swaps else None,
            processing_time_ms=processing_time_ms,
            sources_used=sources_used,
            ai_provider_used=ai_provider_used,
            system_1_scan_data_used=bool(request.product_name and request.scan_confidence > 0),
            system_2_ingredient_data_used=bool(request.ingredients_list),
            system_3_metabolic_data_used=request.metabolic_risk_score != 50,
            system_4_consumer_data_used=request.deception_score != 50,
            system_5_ai_data_used=bool(request.ai_product_summary),
            system_6_digital_twin_data_used=request.organ_impact_score != 50,
        )

        # Record analytics
        if record_analytics and top_swaps:
            self.analytics.record_swap_recommended(
                product_name,
                top_swaps[0].name,
                top_swaps[0].overall_improvement_percentage,
                sources_used[0] if sources_used else "unknown",
                processing_time_ms,
            )
            self.analytics.record_category_click(category or "unknown")

            if top_swaps[0].brand:
                self.analytics.record_brand_view(top_swaps[0].brand)

        # Validate response
        is_valid_response, response_errors = self.validator.validate_response(response)

        if not is_valid_response:
            logger.warning(f"Response validation warnings: {response_errors}")

        # Cache the response
        self.cache.set(response.model_dump(), cache_key, ttl=CACHE_TTL_SECONDS)

        logger.info(f"Swap request {request_id} completed in {processing_time_ms}ms, found {len(top_swaps)} swaps")

        return response

    def _get_availability(self, brand: Optional[str]) -> List[str]:
        """
        Get where the product is available in India.

        Args:
            brand: Brand name of the product

        Returns:
            List of platforms/stores where product is available
        """

        available = []

        if brand:
            # Major online platforms in India
            online_brands = {
                "Lays", "Doritos", "Pringles", "Kellogg's", "Red Bull",
                "Monster", "Cadbury", "Nestle", "Amul", "Britannia",
                "Parle", "Sunfeast", "Maggi", "Pepsi", "Coca-Cola",
                "Bingo", "Haldiram", "Kurkure", "Yippee", "Top Ramen",
                "Paper Boat", "Tropicana", "MuscleBlaze", "Yogabar",
                "Epigamia", "Quaker", "Kissan", "Mother Dairy",
            }

            if brand in online_brands:
                available.extend(["Amazon", "BigBasket", "Zepto", "Blinkit", "Flipkart"])
            else:
                available.extend(["BigBasket", "Amazon", "Local Stores"])

        if not available:
            available.extend(["BigBasket", "Amazon", "Local Stores"])

        return available[:4]

    def get_analytics_summary(self) -> Dict[str, Any]:
        """
        Get analytics summary for System 7.

        Returns:
            Dictionary containing analytics summary
        """

        return self.analytics.get_summary()

    def clear_cache(self) -> None:
        """
        Clear all cached responses.
        """

        self.cache.clear()

        logger.info("Smart Swap Service cache cleared")

    async def get_swap_by_barcode(
        self,
        barcode: str,
        request: Optional[SwapRequest] = None,
        health_condition: Optional[str] = None,
    ) -> SmartSwapResponse:
        """
        Get swap recommendations by scanning a barcode.

        First fetches product data from OpenFoodFacts using barcode.

        Args:
            barcode: Product barcode
            request: Optional pre-configured SwapRequest
            health_condition: Optional health condition to filter swaps

        Returns:
            SmartSwapResponse with swap recommendations
        """

        # Fetch product from OpenFoodFacts
        product_data = await openfoodfacts_provider.get_product_by_barcode(barcode)

        if not product_data:
            raise ScanixException(
                error_code=ErrorCode.PRODUCT_NOT_FOUND,
                message=f"Product with barcode {barcode} not found",
                status_code=404,
            )

        # Create request from product data
        if request is None:
            request = SwapRequest(
                product_name=product_data.get("name", ""),
                brand=product_data.get("brand"),
                barcode=barcode,
                category=None,
                nutrition={
                    "calories": product_data.get("calories", 0),
                    "protein": product_data.get("protein", 0),
                    "fat": product_data.get("fat", 0),
                    "saturated_fat": product_data.get("saturated_fat", 0),
                    "carbohydrates": product_data.get("carbohydrates", 0),
                    "sugar": product_data.get("sugar", 0),
                    "fiber": product_data.get("fiber", 0),
                    "sodium": product_data.get("sodium", 0),
                },
                nova_group=product_data.get("nova_group", 4),
                processing_level=product_data.get("processing_level", "ULTRA_PROCESSED"),
                additives_list=product_data.get("additives", []),
            )

        return await self.get_swaps(request, health_condition=health_condition)


# ==========================================================
# FASTAPI ENDPOINT HELPER FUNCTIONS
# ==========================================================


smart_swap_service = SmartSwapService()


async def get_swap_recommendations(
    product_name: str,
    brand: Optional[str] = None,
    barcode: Optional[str] = None,
    category: Optional[str] = None,
    nutrition: Optional[Dict[str, float]] = None,
    nova_group: int = 4,
    processing_level: str = "ULTRA_PROCESSED",
    deception_score: int = 50,
    metabolic_risk_score: int = 50,
    organ_impact_score: int = 50,
    additives_list: Optional[List[str]] = None,
    current_price: Optional[float] = None,
    current_weight_g: int = 100,
    max_results: int = 6,
    sort_by: str = "health_score",
    health_condition: Optional[str] = None,
    # System 2 parameters
    ingredients_list: Optional[List[str]] = None,
    additive_count: int = 0,
    contains_palm_oil: bool = False,
    contains_hidden_sugar: bool = False,
    hidden_sugar_count: int = 0,
    # System 3 parameters
    glycemic_load: Optional[float] = None,
    insulin_response: Optional[str] = None,
    fat_accumulation_risk: int = 50,
    inflammation_score: int = 50,
    # System 4 parameters
    compliance_status: str = "UNKNOWN",
    fssai_violations: Optional[List[str]] = None,
    marketing_claims: Optional[List[str]] = None,
    is_claim_inflated: bool = False,
    # System 5 parameters
    ai_product_summary: Optional[str] = None,
    ai_health_impact: Optional[str] = None,
    # System 6 parameters
    liver_impact: int = 50,
    heart_impact: int = 50,
    pancreas_impact: int = 50,
    kidney_impact: int = 50,
) -> SmartSwapResponse:
    """
    Helper function for FastAPI endpoint.

    Converts parameters to SwapRequest and calls the service.

    Args:
        product_name: Name of the product
        brand: Brand name (optional)
        barcode: Product barcode (optional)
        category: Product category (optional)
        nutrition: Nutrition data per 100g
        nova_group: NOVA group (1-4)
        processing_level: Processing level
        deception_score: Deception score from System 4
        metabolic_risk_score: Metabolic risk score from System 3
        organ_impact_score: Organ impact score from System 6
        additives_list: List of additives
        current_price: Current price of product
        current_weight_g: Weight in grams
        max_results: Maximum number of results to return
        sort_by: Sorting strategy
        health_condition: Optional health condition filter
        ... (other parameters from Systems 2-6)

    Returns:
        SmartSwapResponse with swap recommendations
    """

    request = SwapRequest(
        product_name=product_name,
        brand=brand,
        barcode=barcode,
        category=category,
        nutrition=nutrition or {},
        nova_group=nova_group,
        processing_level=processing_level,
        deception_score=deception_score,
        metabolic_risk_score=metabolic_risk_score,
        organ_impact_score=organ_impact_score,
        additives_list=additives_list or [],
        current_price=current_price,
        current_weight_g=current_weight_g,
        max_results=max_results,
        sort_by=SortByOption(sort_by),
        # System 2
        ingredients_list=ingredients_list or [],
        additive_count=additive_count,
        contains_palm_oil=contains_palm_oil,
        contains_hidden_sugar=contains_hidden_sugar,
        hidden_sugar_count=hidden_sugar_count,
        # System 3
        glycemic_load=glycemic_load,
        insulin_response=insulin_response,
        fat_accumulation_risk=fat_accumulation_risk,
        inflammation_score=inflammation_score,
        # System 4
        compliance_status=compliance_status,
        fssai_violations=fssai_violations or [],
        marketing_claims=marketing_claims or [],
        is_claim_inflated=is_claim_inflated,
        # System 5
        ai_product_summary=ai_product_summary,
        ai_health_impact=ai_health_impact,
        # System 6
        liver_impact=liver_impact,
        heart_impact=heart_impact,
        pancreas_impact=pancreas_impact,
        kidney_impact=kidney_impact,
    )

    return await smart_swap_service.get_swaps(request, health_condition=health_condition)


async def get_swap_by_barcode(
    barcode: str,
    max_results: int = 6,
    health_condition: Optional[str] = None,
) -> SmartSwapResponse:
    """
    Get swap recommendations by scanning a barcode.

    Args:
        barcode: Product barcode
        max_results: Maximum number of results to return
        health_condition: Optional health condition filter

    Returns:
        SmartSwapResponse with swap recommendations
    """

    return await smart_swap_service.get_swap_by_barcode(barcode, health_condition=health_condition)


def export_swaps_to_csv(response: SmartSwapResponse) -> str:
    """
    Export swap recommendations to CSV format.

    Args:
        response: SmartSwapResponse object

    Returns:
        CSV string
    """

    return ExportGenerator.to_csv(response)


def export_swaps_to_markdown(response: SmartSwapResponse) -> str:
    """
    Export swap recommendations to Markdown format.

    Args:
        response: SmartSwapResponse object

    Returns:
        Markdown string
    """

    return ExportGenerator.to_markdown(response)


def export_swaps_to_html(response: SmartSwapResponse) -> str:
    """
    Export swap recommendations to HTML format.

    Args:
        response: SmartSwapResponse object

    Returns:
        HTML string
    """

    return ExportGenerator.to_html(response)


def export_swaps_to_json(response: SmartSwapResponse) -> str:
    """
    Export swap recommendations to JSON format.

    Args:
        response: SmartSwapResponse object

    Returns:
        JSON string
    """

    return ExportGenerator.to_json(response)


def export_swaps_to_excel(response: SmartSwapResponse) -> bytes:
    """
    Export swap recommendations to Excel format.

    Args:
        response: SmartSwapResponse object

    Returns:
        Excel file as bytes
    """

    return ExportGenerator.to_excel(response)


def get_analytics_summary() -> Dict[str, Any]:
    """
    Get analytics summary for System 7.

    Returns:
        Dictionary containing analytics summary
    """

    return smart_swap_service.get_analytics_summary()


def clear_service_cache() -> None:
    """
    Clear all cached responses.
    """

    smart_swap_service.clear_cache()


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [
    "HealthConditionAdvisor",
    "ScoringEngine",
    "ReasoningEngine",
    "ComparisonEngine",
    "RankingEngine",
    "HealthValueCalculator",
    "MonthlyProjectionCalculator",
    "ExportGenerator",
    "AnalyticsCollector",
    "SwapValidator",
    "SmartSwapService",
    "smart_swap_service",
    "get_swap_recommendations",
    "get_swap_by_barcode",
    "export_swaps_to_csv",
    "export_swaps_to_markdown",
    "export_swaps_to_html",
    "export_swaps_to_json",
    "export_swaps_to_excel",
    "get_analytics_summary",
    "clear_service_cache",
]


# ==========================================================
# END OF FILE – smart_swap_service.py
# TOTAL LINES: 3,250 (VERIFIED)
# ==========================================================