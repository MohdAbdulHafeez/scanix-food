# ============================================================
# ELITE PART A
#
# ORGAN IMPACT ENGINE FOUNDATION
#
# Shared Models
# Shared Utilities
# Organ Verdict Logic
# Organ Risk Utilities
#
# Used By:
#
# Heart Engine
# Liver Engine
# Kidney Engine
# Pancreas Engine
# Gut Engine
# Brain Engine
# Blood Vessel Engine
# Immune Engine
# ============================================================

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List


# ============================================================
# ORGAN CONSTANTS
# ============================================================

class OrganConstants:

    MAX_SCORE = 100

    MIN_SCORE = 0

    PROTECTED_THRESHOLD = 80

    MODERATE_THRESHOLD = 60

    HIGH_RISK_THRESHOLD = 70

    MODERATE_RISK_THRESHOLD = 40


# ============================================================
# ORGAN SCORE UTILITIES
# ============================================================

class OrganMath:

    @staticmethod
    def clamp(
        value: float,
        minimum: float = 0,
        maximum: float = 100
    ) -> float:

        return max(
            minimum,
            min(
                value,
                maximum
            )
        )

    @staticmethod
    def inverse_score(
        burden: float
    ) -> float:

        return OrganMath.clamp(
            100 - burden
        )

    @staticmethod
    def weighted_average(
        values: List[float],
        weights: List[float]
    ) -> float:

        if not values:
            return 0

        numerator = sum(
            v * w
            for v, w in zip(
                values,
                weights
            )
        )

        denominator = sum(weights)

        if denominator == 0:
            return 0

        return numerator / denominator


# ============================================================
# ORGAN VERDICT ENGINE
# ============================================================

class OrganVerdictEngine:

    @staticmethod
    def generate(
        score: float
    ) -> str:

        if score >= 80:

            return "PROTECTED"

        if score >= 60:

            return "MODERATE"

        return "STRESSED"


# ============================================================
# ORGAN RISK ENGINE
# ============================================================

class OrganRiskEngine:

    @staticmethod
    def risk_level(
        value: float
    ) -> str:

        if value >= 70:

            return "HIGH"

        if value >= 40:

            return "MODERATE"

        return "LOW"


# ============================================================
# ORGAN OUTPUT MODEL
# ============================================================

@dataclass
class OrganImpactResult:

    organ: str

    score: float

    burden: float

    verdict: str


# ============================================================
# ORGAN HEALTH AGGREGATOR HELPERS
# ============================================================

class OrganAggregatorUtils:

    @staticmethod
    def extract_scores(
        organ_results: Dict[str, Dict]
    ) -> List[float]:

        scores = []

        for result in organ_results.values():

            score_key = next(
                (
                    key
                    for key in result
                    if key.endswith("_score")
                ),
                None
            )

            if score_key is not None:
                scores.append(
                    result[score_key]
                )

        return scores

    @staticmethod
    def most_stressed(
        organ_results: Dict[str, Dict]
    ) -> str:

        stressed_organ = None

        lowest_score = 999

        for organ, result in organ_results.items():

            score_key = next(
                (
                    key
                    for key in result
                    if key.endswith("_score")
                ),
                None
            )

            if score_key is not None:

                score = result[score_key]

                if score < lowest_score:

                    lowest_score = score

                    stressed_organ = organ

        return stressed_organ.upper() if stressed_organ else "UNKNOWN"

    @staticmethod
    def most_protected(
        organ_results: Dict[str, Dict]
    ) -> str:

        protected_organ = None

        highest_score = -1

        for organ, result in organ_results.items():

            score_key = next(
                (
                    key
                    for key in result
                    if key.endswith("_score")
                ),
                None
            )

            if score_key is not None:

                score = result[score_key]

                if score > highest_score:

                    highest_score = score

                    protected_organ = organ

        return protected_organ.upper() if protected_organ else "UNKNOWN"


# ============================================================
# SHARED CARDIOMETABOLIC BURDEN MODEL
# ============================================================

class CardioMetabolicBurdenModel:

    @staticmethod
    def calculate(
        sugar: float,
        inflammation: float,
        metabolic_stress: float
    ) -> float:

        burden = (

            sugar * 0.50

            +

            inflammation * 0.30

            +

            metabolic_stress * 0.20

        )

        return OrganMath.clamp(
            burden
        )


# ============================================================
# SHARED PROCESSING BURDEN MODEL
# ============================================================

class ProcessingBurdenModel:

    @staticmethod
    def calculate(
        processing_score: float
    ) -> float:

        burden = (

            processing_score *
            0.85

        )

        return OrganMath.clamp(
            burden
        )


# ============================================================
# SHARED INFLAMMATION BURDEN MODEL
# ============================================================

class InflammationBurdenModel:

    @staticmethod
    def calculate(
        inflammation_score: float
    ) -> float:

        return OrganMath.clamp(
            inflammation_score
        )


# ============================================================
# SHARED ADDITIVE BURDEN MODEL
# ============================================================

class AdditiveBurdenModel:

    @staticmethod
    def calculate(
        additive_score: float
    ) -> float:

        burden = (

            additive_score *
            0.90

        )

        return OrganMath.clamp(
            burden
        )


# ============================================================
# SHARED SODIUM BURDEN MODEL
# ============================================================

class SodiumBurdenModel:

    @staticmethod
    def calculate(
        sodium_mg: float
    ) -> float:

        burden = (

            sodium_mg / 20

        )

        return OrganMath.clamp(
            burden
        )


# ============================================================
# PART A REGISTRATION
# ============================================================

class OrganFoundation:

    def __init__(self):

        self.verdict_engine = (
            OrganVerdictEngine()
        )

        self.risk_engine = (
            OrganRiskEngine()
        )


        # ============================================================
# HEART IMPACT ENGINE
# LIVER IMPACT ENGINE
#
# Depends On:
# - PhysiologicalState
# - FoodExposure
# - OrganMath
# ============================================================


# ============================================================
# HEART MODELS
# ============================================================

class BloodPressureLoadModel:

    @staticmethod
    def calculate(
        sodium_mg: float,
        metabolic_stress: float
    ) -> float:

        pressure_load = 0

        pressure_load += (
            sodium_mg / 20
        )

        pressure_load += (
            metabolic_stress * 0.35
        )

        return OrganMath.clamp(
            pressure_load,
            0,
            100
        )


class AtherosclerosisRiskModel:

    @staticmethod
    def calculate(
        trans_fat: float,
        saturated_fat: float,
        sugar: float,
        inflammation: float
    ) -> float:

        risk = 0

        risk += (
            trans_fat * 18
        )

        risk += (
            saturated_fat * 1.8
        )

        risk += (
            sugar * 0.45
        )

        risk += (
            inflammation * 0.35
        )

        return OrganMath.clamp(
            risk,
            0,
            100
        )


class CardiovascularRiskModel:

    @staticmethod
    def calculate(
        blood_pressure_load: float,
        atherosclerosis_risk: float
    ) -> float:

        risk = (

            blood_pressure_load * 0.45

            +

            atherosclerosis_risk * 0.55

        )

        return OrganMath.clamp(
            risk,
            0,
            100
        )


# ============================================================
# HEART IMPACT ENGINE
# ============================================================

class HeartImpactEngine:

    def calculate(
        self,
        sodium_mg: float,
        trans_fat: float,
        saturated_fat: float,
        sugar: float,
        inflammation_score: float,
        metabolic_stress_score: float
    ) -> Dict:

        blood_pressure_load = (

            BloodPressureLoadModel
            .calculate(
                sodium_mg,
                metabolic_stress_score
            )

        )

        atherosclerosis_risk = (

            AtherosclerosisRiskModel
            .calculate(
                trans_fat,
                saturated_fat,
                sugar,
                inflammation_score
            )

        )

        cardiovascular_risk = (

            CardiovascularRiskModel
            .calculate(
                blood_pressure_load,
                atherosclerosis_risk
            )

        )

        heart_score = (

            100 -
            cardiovascular_risk

        )

        heart_score = OrganMath.clamp(
            heart_score,
            0,
            100
        )

        if heart_score >= 80:

            verdict = "PROTECTED"

        elif heart_score >= 60:

            verdict = "MODERATE"

        else:

            verdict = "STRESSED"

        return {

            "heart_score":
                round(
                    heart_score,
                    2
                ),

            "blood_pressure_load":
                round(
                    blood_pressure_load,
                    2
                ),

            "atherosclerosis_risk":
                round(
                    atherosclerosis_risk,
                    2
                ),

            "cardiovascular_risk":
                round(
                    cardiovascular_risk,
                    2
                ),

            "heart_verdict":
                verdict
        }


# ============================================================
# LIVER MODELS
# ============================================================

class FattyLiverRiskModel:

    @staticmethod
    def calculate(
        sugar: float,
        hfcs: float,
        fructose: float,
        fat_storage_score: float
    ) -> float:

        risk = 0

        risk += (
            sugar * 0.60
        )

        risk += (
            hfcs * 1.20
        )

        risk += (
            fructose * 0.90
        )

        risk += (
            fat_storage_score * 0.50
        )

        return OrganMath.clamp(
            risk,
            0,
            100
        )


class HepaticStressModel:

    @staticmethod
    def calculate(
        processing_score: float,
        inflammation_score: float
    ) -> float:

        stress = 0

        stress += (
            processing_score * 0.60
        )

        stress += (
            inflammation_score * 0.40
        )

        return OrganMath.clamp(
            stress,
            0,
            100
        )


class LiverBurdenModel:

    @staticmethod
    def calculate(
        fatty_liver_risk: float,
        hepatic_stress: float
    ) -> float:

        burden = (

            fatty_liver_risk * 0.55

            +

            hepatic_stress * 0.45

        )

        return OrganMath.clamp(
            burden,
            0,
            100
        )


# ============================================================
# LIVER IMPACT ENGINE
# ============================================================

class LiverImpactEngine:

    def calculate(
        self,
        sugar: float,
        hfcs: float,
        fructose: float,
        processing_score: float,
        fat_storage_score: float,
        inflammation_score: float
    ) -> Dict:

        fatty_liver_risk = (

            FattyLiverRiskModel
            .calculate(
                sugar,
                hfcs,
                fructose,
                fat_storage_score
            )

        )

        hepatic_stress = (

            HepaticStressModel
            .calculate(
                processing_score,
                inflammation_score
            )

        )

        liver_burden = (

            LiverBurdenModel
            .calculate(
                fatty_liver_risk,
                hepatic_stress
            )

        )

        liver_score = (

            100 -
            liver_burden

        )

        liver_score = OrganMath.clamp(
            liver_score,
            0,
            100
        )

        if liver_score >= 80:

            verdict = "PROTECTED"

        elif liver_score >= 60:

            verdict = "MODERATE"

        else:

            verdict = "STRESSED"

        return {

            "liver_score":
                round(
                    liver_score,
                    2
                ),

            "fatty_liver_risk":
                round(
                    fatty_liver_risk,
                    2
                ),

            "hepatic_stress":
                round(
                    hepatic_stress,
                    2
                ),

            "liver_burden":
                round(
                    liver_burden,
                    2
                ),

            "liver_verdict":
                verdict
        }


# ============================================================
# PART B REGISTRATION
# ============================================================

class OrganCardioHepaticLayer:

    def __init__(self):

        self.heart = (
            HeartImpactEngine()
        )

        self.liver = (
            LiverImpactEngine()
        )


        # ============================================================
# ELITE PART C
#
# KIDNEY IMPACT ENGINE
# PANCREAS IMPACT ENGINE
#
# Depends On:
# - OrganMath
# - OrganVerdictEngine
# - OrganRiskEngine
# ============================================================


# ============================================================
# KIDNEY MODELS
# ============================================================

class SodiumBurdenRiskModel:

    @staticmethod
    def calculate(
        sodium_mg: float
    ) -> float:

        burden = (

            sodium_mg / 25

        )

        return OrganMath.clamp(
            burden
        )


class FluidRetentionRiskModel:

    @staticmethod
    def calculate(
        sodium_mg: float,
        hydration_score: float
    ) -> float:

        sodium_component = (
            sodium_mg / 30
        )

        hydration_component = (
            (100 - hydration_score)
            * 0.60
        )

        risk = (

            sodium_component

            +

            hydration_component

        )

        return OrganMath.clamp(
            risk
        )


class ProteinLoadModel:

    @staticmethod
    def calculate(
        protein_g: float
    ) -> float:

        stress = (

            protein_g * 0.80

        )

        return OrganMath.clamp(
            stress
        )


class BloodPressureKidneyModel:

    @staticmethod
    def calculate(
        blood_pressure_load: float
    ) -> float:

        return OrganMath.clamp(
            blood_pressure_load
        )


class RenalStressModel:

    @staticmethod
    def calculate(
        sodium_burden: float,
        fluid_retention_risk: float,
        protein_load: float,
        blood_pressure_signal: float
    ) -> float:

        stress = (

            sodium_burden * 0.30

            +

            fluid_retention_risk * 0.25

            +

            protein_load * 0.15

            +

            blood_pressure_signal * 0.30

        )

        return OrganMath.clamp(
            stress
        )


# ============================================================
# KIDNEY IMPACT ENGINE
# ============================================================

class KidneyImpactEngine:

    def calculate(
        self,
        sodium_mg: float,
        hydration_score: float,
        protein_g: float,
        blood_pressure_load: float
    ) -> Dict:

        sodium_burden = (

            SodiumBurdenRiskModel
            .calculate(
                sodium_mg
            )

        )

        fluid_retention_risk = (

            FluidRetentionRiskModel
            .calculate(
                sodium_mg,
                hydration_score
            )

        )

        protein_load = (

            ProteinLoadModel
            .calculate(
                protein_g
            )

        )

        renal_stress = (

            RenalStressModel
            .calculate(
                sodium_burden,
                fluid_retention_risk,
                protein_load,
                blood_pressure_load
            )

        )

        kidney_score = (

            100 -
            renal_stress

        )

        kidney_score = OrganMath.clamp(
            kidney_score
        )

        return {

            "kidney_score":
                round(
                    kidney_score,
                    2
                ),

            "sodium_burden":
                round(
                    sodium_burden,
                    2
                ),

            "fluid_retention_risk":
                round(
                    fluid_retention_risk,
                    2
                ),

            "renal_stress":
                round(
                    renal_stress,
                    2
                ),

            "kidney_verdict":

                OrganVerdictEngine
                .generate(
                    kidney_score
                )
        }


# ============================================================
# PANCREAS MODELS
# ============================================================

class InsulinStressModel:

    @staticmethod
    def calculate(
        glycemic_load: float,
        insulin_load: float
    ) -> float:

        stress = (

            glycemic_load * 1.20

            +

            insulin_load * 1.40

        )

        return OrganMath.clamp(
            stress
        )


class BetaCellBurdenModel:

    @staticmethod
    def calculate(
        insulin_stress: float,
        hba1c: float
    ) -> float:

        burden = (

            insulin_stress * 0.70

            +

            max(
                0,
                hba1c - 5.0
            ) * 12

        )

        return OrganMath.clamp(
            burden
        )


class GlucosePeakModel:

    @staticmethod
    def calculate(
        peak_glucose: float
    ) -> float:

        risk = (

            max(
                0,
                peak_glucose - 100
            )

            * 0.80

        )

        return OrganMath.clamp(
            risk
        )


class DiabetesProgressionModel:

    @staticmethod
    def calculate(
        beta_cell_burden: float,
        glucose_peak_risk: float
    ) -> float:

        progression = (

            beta_cell_burden * 0.60

            +

            glucose_peak_risk * 0.40

        )

        return OrganMath.clamp(
            progression
        )


# ============================================================
# PANCREAS IMPACT ENGINE
# ============================================================

class PancreasImpactEngine:

    def calculate(
        self,
        glycemic_load: float,
        insulin_load: float,
        hba1c: float,
        peak_glucose: float
    ) -> Dict:

        insulin_stress = (

            InsulinStressModel
            .calculate(
                glycemic_load,
                insulin_load
            )

        )

        beta_cell_burden = (

            BetaCellBurdenModel
            .calculate(
                insulin_stress,
                hba1c
            )

        )

        glucose_peak_risk = (

            GlucosePeakModel
            .calculate(
                peak_glucose
            )

        )

        diabetes_progression_risk = (

            DiabetesProgressionModel
            .calculate(
                beta_cell_burden,
                glucose_peak_risk
            )

        )

        pancreas_score = (

            100 -
            diabetes_progression_risk

        )

        pancreas_score = OrganMath.clamp(
            pancreas_score
        )

        return {

            "pancreas_score":
                round(
                    pancreas_score,
                    2
                ),

            "insulin_stress":
                round(
                    insulin_stress,
                    2
                ),

            "beta_cell_burden":
                round(
                    beta_cell_burden,
                    2
                ),

            "diabetes_progression_risk":
                round(
                    diabetes_progression_risk,
                    2
                ),

            "pancreas_verdict":

                OrganVerdictEngine
                .generate(
                    pancreas_score
                )
        }


# ============================================================
# PART C REGISTRATION
# ============================================================

class OrganRenalPancreaticLayer:

    def __init__(self):

        self.kidney = (
            KidneyImpactEngine()
        )

        self.pancreas = (
            PancreasImpactEngine()
        )


        # ============================================================
# ELITE PART D
#
# GUT IMPACT ENGINE
# BRAIN IMPACT ENGINE
#
# Depends On:
# - OrganMath
# - OrganVerdictEngine
# ============================================================


# ============================================================
# GUT MODELS
# ============================================================

class MicrobiomeSupportModel:

    @staticmethod
    def calculate(
        fiber_g: float,
        processing_score: float
    ) -> float:

        support = 50

        support += (
            fiber_g * 4.0
        )

        support -= (
            processing_score * 0.35
        )

        return OrganMath.clamp(
            support
        )


class AdditiveGutBurdenModel:

    @staticmethod
    def calculate(
        additive_score: float,
        emulsifier_score: float
    ) -> float:

        burden = (

            additive_score * 0.60

            +

            emulsifier_score * 0.40

        )

        return OrganMath.clamp(
            burden
        )


class GutInflammationModel:

    @staticmethod
    def calculate(
        processing_score: float,
        additive_score: float,
        emulsifier_score: float
    ) -> float:

        inflammation = (

            processing_score * 0.40

            +

            additive_score * 0.35

            +

            emulsifier_score * 0.25

        )

        return OrganMath.clamp(
            inflammation
        )


class DigestiveQualityModel:

    @staticmethod
    def calculate(
        fiber_g: float,
        processing_score: float,
        gut_inflammation: float
    ) -> float:

        quality = 60

        quality += (
            fiber_g * 3.0
        )

        quality -= (
            processing_score * 0.25
        )

        quality -= (
            gut_inflammation * 0.35
        )

        return OrganMath.clamp(
            quality
        )


# ============================================================
# GUT IMPACT ENGINE
# ============================================================

class GutImpactEngine:

    def calculate(
        self,
        fiber_g: float,
        additive_score: float,
        emulsifier_score: float,
        processing_score: float
    ) -> Dict:

        microbiome_support = (

            MicrobiomeSupportModel
            .calculate(
                fiber_g,
                processing_score
            )

        )

        gut_inflammation = (

            GutInflammationModel
            .calculate(
                processing_score,
                additive_score,
                emulsifier_score
            )

        )

        digestive_quality = (

            DigestiveQualityModel
            .calculate(
                fiber_g,
                processing_score,
                gut_inflammation
            )

        )

        additive_burden = (

            AdditiveGutBurdenModel
            .calculate(
                additive_score,
                emulsifier_score
            )

        )

        gut_burden = (

            gut_inflammation * 0.40

            +

            additive_burden * 0.25

            +

            (
                100 -
                microbiome_support
            ) * 0.35

        )

        gut_burden = OrganMath.clamp(
            gut_burden
        )

        gut_score = (

            100 -
            gut_burden

        )

        gut_score = OrganMath.clamp(
            gut_score
        )

        return {

            "gut_score":
                round(
                    gut_score,
                    2
                ),

            "microbiome_support":
                round(
                    microbiome_support,
                    2
                ),

            "gut_inflammation":
                round(
                    gut_inflammation,
                    2
                ),

            "digestive_quality":
                round(
                    digestive_quality,
                    2
                ),

            "gut_verdict":

                OrganVerdictEngine
                .generate(
                    gut_score
                )
        }


# ============================================================
# BRAIN MODELS
# ============================================================

class FocusScoreModel:

    @staticmethod
    def calculate(
        energy_stability: float,
        sugar_g: float,
        processing_score: float
    ) -> float:

        focus = 70

        focus += (
            energy_stability * 0.25
        )

        focus -= (
            sugar_g * 0.50
        )

        focus -= (
            processing_score * 0.20
        )

        return OrganMath.clamp(
            focus
        )


class MentalEnergyModel:

    @staticmethod
    def calculate(
        energy_stability: float,
        inflammation_score: float
    ) -> float:

        energy = 70

        energy += (
            energy_stability * 0.30
        )

        energy -= (
            inflammation_score * 0.35
        )

        return OrganMath.clamp(
            energy
        )


class BrainFogRiskModel:

    @staticmethod
    def calculate(
        sugar_g: float,
        inflammation_score: float,
        processing_score: float
    ) -> float:

        risk = (

            sugar_g * 0.50

            +

            inflammation_score * 0.30

            +

            processing_score * 0.20

        )

        return OrganMath.clamp(
            risk
        )


class NeuroInflammationModel:

    @staticmethod
    def calculate(
        inflammation_score: float,
        processing_score: float
    ) -> float:

        neuro_load = (

            inflammation_score * 0.65

            +

            processing_score * 0.35

        )

        return OrganMath.clamp(
            neuro_load
        )


# ============================================================
# BRAIN IMPACT ENGINE
# ============================================================

class BrainImpactEngine:

    def calculate(
        self,
        sugar_g: float,
        inflammation_score: float,
        energy_stability: float,
        processing_score: float
    ) -> Dict:

        focus_score = (

            FocusScoreModel
            .calculate(
                energy_stability,
                sugar_g,
                processing_score
            )

        )

        mental_energy_score = (

            MentalEnergyModel
            .calculate(
                energy_stability,
                inflammation_score
            )

        )

        brain_fog_risk = (

            BrainFogRiskModel
            .calculate(
                sugar_g,
                inflammation_score,
                processing_score
            )

        )

        neuro_inflammation = (

            NeuroInflammationModel
            .calculate(
                inflammation_score,
                processing_score
            )

        )

        brain_burden = (

            brain_fog_risk * 0.45

            +

            neuro_inflammation * 0.35

            +

            (
                100 -
                focus_score
            ) * 0.20

        )

        brain_burden = OrganMath.clamp(
            brain_burden
        )

        brain_score = (

            100 -
            brain_burden

        )

        brain_score = OrganMath.clamp(
            brain_score
        )

        return {

            "brain_score":
                round(
                    brain_score,
                    2
                ),

            "focus_score":
                round(
                    focus_score,
                    2
                ),

            "mental_energy_score":
                round(
                    mental_energy_score,
                    2
                ),

            "brain_fog_risk":
                round(
                    brain_fog_risk,
                    2
                ),

            "brain_verdict":

                OrganVerdictEngine
                .generate(
                    brain_score
                )
        }


# ============================================================
# PART D REGISTRATION
# ============================================================

class OrganGutBrainLayer:

    def __init__(self):

        self.gut = (
            GutImpactEngine()
        )

        self.brain = (
            BrainImpactEngine()
        )


        # ============================================================
# ELITE PART E
#
# BLOOD VESSEL IMPACT ENGINE
# IMMUNE SYSTEM IMPACT ENGINE
#
# Depends On:
# - OrganMath
# - OrganVerdictEngine
# ============================================================


# ============================================================
# BLOOD VESSEL MODELS
# ============================================================

class EndothelialStressModel:

    @staticmethod
    def calculate(
        sugar_g: float,
        inflammation_score: float
    ) -> float:

        stress = (

            sugar_g * 0.55

            +

            inflammation_score * 0.45

        )

        return OrganMath.clamp(
            stress
        )


class VascularInflammationModel:

    @staticmethod
    def calculate(
        inflammation_score: float,
        sodium_mg: float
    ) -> float:

        inflammation = (

            inflammation_score * 0.70

            +

            (sodium_mg / 30) * 0.30

        )

        return OrganMath.clamp(
            inflammation
        )


class ArterialPressureModel:

    @staticmethod
    def calculate(
        blood_pressure_signal: float,
        sodium_mg: float
    ) -> float:

        pressure = (

            blood_pressure_signal * 0.75

            +

            (sodium_mg / 25) * 0.25

        )

        return OrganMath.clamp(
            pressure
        )


class VascularBurdenModel:

    @staticmethod
    def calculate(
        endothelial_stress: float,
        vascular_inflammation: float,
        arterial_pressure: float
    ) -> float:

        burden = (

            endothelial_stress * 0.40

            +

            vascular_inflammation * 0.35

            +

            arterial_pressure * 0.25

        )

        return OrganMath.clamp(
            burden
        )


# ============================================================
# BLOOD VESSEL IMPACT ENGINE
# ============================================================

class BloodVesselImpactEngine:

    def calculate(
        self,
        sugar_g: float,
        inflammation_score: float,
        sodium_mg: float,
        blood_pressure_signal: float
    ) -> Dict:

        endothelial_stress = (

            EndothelialStressModel
            .calculate(
                sugar_g,
                inflammation_score
            )

        )

        vascular_inflammation = (

            VascularInflammationModel
            .calculate(
                inflammation_score,
                sodium_mg
            )

        )

        arterial_pressure = (

            ArterialPressureModel
            .calculate(
                blood_pressure_signal,
                sodium_mg
            )

        )

        vascular_burden = (

            VascularBurdenModel
            .calculate(
                endothelial_stress,
                vascular_inflammation,
                arterial_pressure
            )

        )

        vascular_score = (

            100 -
            vascular_burden

        )

        vascular_score = OrganMath.clamp(
            vascular_score
        )

        return {

            "vascular_score":
                round(
                    vascular_score,
                    2
                ),

            "endothelial_stress":
                round(
                    endothelial_stress,
                    2
                ),

            "vascular_inflammation":
                round(
                    vascular_inflammation,
                    2
                ),

            "arterial_pressure":
                round(
                    arterial_pressure,
                    2
                ),

            "vascular_verdict":

                OrganVerdictEngine
                .generate(
                    vascular_score
                )
        }


# ============================================================
# IMMUNE SYSTEM MODELS
# ============================================================

class ImmuneSupportModel:

    @staticmethod
    def calculate(
        fiber_g: float,
        micronutrient_score: float
    ) -> float:

        support = 40

        support += (
            fiber_g * 3.5
        )

        support += (
            micronutrient_score * 0.60
        )

        return OrganMath.clamp(
            support
        )


class ImmuneStressModel:

    @staticmethod
    def calculate(
        inflammation_score: float,
        processing_score: float,
        additive_score: float
    ) -> float:

        stress = (

            inflammation_score * 0.45

            +

            processing_score * 0.30

            +

            additive_score * 0.25

        )

        return OrganMath.clamp(
            stress
        )


class GutImmuneAxisModel:

    @staticmethod
    def calculate(
        fiber_g: float,
        processing_score: float
    ) -> float:

        axis_score = 60

        axis_score += (
            fiber_g * 2.5
        )

        axis_score -= (
            processing_score * 0.30
        )

        return OrganMath.clamp(
            axis_score
        )


class ImmuneBurdenModel:

    @staticmethod
    def calculate(
        immune_stress: float,
        immune_support: float,
        gut_immune_axis: float
    ) -> float:

        burden = (

            immune_stress * 0.55

            +

            (
                100 -
                immune_support
            ) * 0.25

            +

            (
                100 -
                gut_immune_axis
            ) * 0.20

        )

        return OrganMath.clamp(
            burden
        )


# ============================================================
# IMMUNE SYSTEM IMPACT ENGINE
# ============================================================

class ImmuneSystemImpactEngine:

    def calculate(
        self,
        inflammation_score: float,
        processing_score: float,
        additive_score: float,
        fiber_g: float,
        micronutrient_score: float
    ) -> Dict:

        immune_support = (

            ImmuneSupportModel
            .calculate(
                fiber_g,
                micronutrient_score
            )

        )

        immune_stress = (

            ImmuneStressModel
            .calculate(
                inflammation_score,
                processing_score,
                additive_score
            )

        )

        gut_immune_axis = (

            GutImmuneAxisModel
            .calculate(
                fiber_g,
                processing_score
            )

        )

        immune_burden = (

            ImmuneBurdenModel
            .calculate(
                immune_stress,
                immune_support,
                gut_immune_axis
            )

        )

        immune_score = (

            100 -
            immune_burden

        )

        immune_score = OrganMath.clamp(
            immune_score
        )

        return {

            "immune_score":
                round(
                    immune_score,
                    2
                ),

            "immune_support":
                round(
                    immune_support,
                    2
                ),

            "immune_stress":
                round(
                    immune_stress,
                    2
                ),

            "gut_immune_axis":
                round(
                    gut_immune_axis,
                    2
                ),

            "immune_verdict":

                OrganVerdictEngine
                .generate(
                    immune_score
                )
        }


# ============================================================
# PART E REGISTRATION
# ============================================================

class OrganVascularImmuneLayer:

    def __init__(self):

        self.blood_vessels = (
            BloodVesselImpactEngine()
        )

        self.immune_system = (
            ImmuneSystemImpactEngine()
        )


        # ============================================================
# ELITE PART F
#
# FINAL ORGAN AGGREGATOR
#
# ORGAN HEALTH SCORE
# MOST STRESSED ORGAN
# MOST PROTECTED ORGAN
# OVERALL ORGAN VERDICT
#
# MASTER ORGAN IMPACT ENGINE
# ============================================================


# ============================================================
# ORGAN HEALTH SCORE ENGINE
# ============================================================

class OrganHealthScoreEngine:

    @staticmethod
    def calculate(
        organ_results: Dict[str, Dict]
    ) -> float:

        scores = []

        for result in organ_results.values():

            score_key = next(
                (
                    key
                    for key in result
                    if key.endswith("_score")
                ),
                None
            )

            if score_key is not None:
                scores.append(
                    result[score_key]
                )

        if not scores:
            return 0.0

        return round(
            sum(scores) / len(scores),
            2
        )


# ============================================================
# MOST STRESSED ORGAN ENGINE
# ============================================================

class MostStressedOrganEngine:

    @staticmethod
    def identify(
        organ_results: Dict[str, Dict]
    ) -> str:

        stressed_organ = None

        lowest_score = 999

        for organ, result in organ_results.items():

            score_key = next(
                (
                    key
                    for key in result
                    if key.endswith("_score")
                ),
                None
            )

            if score_key is not None:

                score = result[score_key]

                if score < lowest_score:

                    lowest_score = score

                    stressed_organ = organ

        return stressed_organ.upper() if stressed_organ else "UNKNOWN"


# ============================================================
# MOST PROTECTED ORGAN ENGINE
# ============================================================

class MostProtectedOrganEngine:

    @staticmethod
    def identify(
        organ_results: Dict[str, Dict]
    ) -> str:

        protected_organ = None

        highest_score = -1

        for organ, result in organ_results.items():

            score_key = next(
                (
                    key
                    for key in result
                    if key.endswith("_score")
                ),
                None
            )

            if score_key is not None:

                score = result[score_key]

                if score > highest_score:

                    highest_score = score

                    protected_organ = organ

        return protected_organ.upper() if protected_organ else "UNKNOWN"


# ============================================================
# ORGAN VERDICT AGGREGATOR
# ============================================================

class OverallOrganVerdictEngine:

    @staticmethod
    def generate(
        organ_health_score: float
    ) -> str:

        if organ_health_score >= 90:

            return (
                "EXCELLENT"
            )

        if organ_health_score >= 80:

            return (
                "GOOD"
            )

        if organ_health_score >= 65:

            return (
                "MODERATE"
            )

        if organ_health_score >= 50:

            return (
                "POOR"
            )

        return (
            "HIGH RISK"
        )


# ============================================================
# ORGAN HEATMAP ENGINE
# ============================================================

class OrganHeatmapEngine:

    @staticmethod
    def generate(
        organ_results: Dict[str, Dict]
    ) -> Dict:

        heatmap = {}

        for organ, result in organ_results.items():

            score_key = next(
                (
                    key
                    for key in result
                    if key.endswith("_score")
                ),
                None
            )

            if score_key is not None:

                score = result[score_key]

                if score >= 90:

                    zone = "DARK_GREEN"

                elif score >= 80:

                    zone = "GREEN"

                elif score >= 65:

                    zone = "YELLOW"

                elif score >= 50:

                    zone = "ORANGE"

                else:

                    zone = "RED"

                heatmap[organ] = {

                    "score":
                        score,

                    "zone":
                        zone
                }

        return heatmap


# ============================================================
# MASTER ORGAN IMPACT ENGINE
# ============================================================

class OrganImpactEngine:

    def __init__(self):

        self.heart_engine = (
            HeartImpactEngine()
        )

        self.liver_engine = (
            LiverImpactEngine()
        )

        self.kidney_engine = (
            KidneyImpactEngine()
        )

        self.pancreas_engine = (
            PancreasImpactEngine()
        )

        self.gut_engine = (
            GutImpactEngine()
        )

        self.brain_engine = (
            BrainImpactEngine()
        )

        self.vascular_engine = (
            BloodVesselImpactEngine()
        )

        self.immune_engine = (
            ImmuneSystemImpactEngine()
        )

    def analyze(
        self,
        organ_inputs: Dict
    ) -> Dict:

        # ====================================================
        # INPUT VALIDATION LAYER
        # ====================================================

        required_fields = [

            "sodium_mg",
            "trans_fat",
            "saturated_fat",
            "sugar",
            "inflammation_score",
            "metabolic_stress_score",
            "hfcs",
            "fructose",
            "processing_score",
            "fat_storage_score",
            "hydration_score",
            "protein_g",
            "glycemic_load",
            "insulin_load",
            "hba1c",
            "peak_glucose",
            "fiber_g",
            "additive_score",
            "emulsifier_score",
            "energy_stability",
            "micronutrient_score"

        ]

        missing = [

            field

            for field in required_fields

            if field not in organ_inputs

        ]

        if missing:

           for field in missing:

                    organ_inputs[field] = 0

        # ====================================================
        # HEART
        # ====================================================

        heart = (

            self.heart_engine
            .calculate(

                sodium_mg=
                    organ_inputs["sodium_mg"],

                trans_fat=
                    organ_inputs["trans_fat"],

                saturated_fat=
                    organ_inputs["saturated_fat"],

                sugar=
                    organ_inputs["sugar"],

                inflammation_score=
                    organ_inputs["inflammation_score"],

                metabolic_stress_score=
                    organ_inputs[
                        "metabolic_stress_score"
                    ]
            )
        )

        # ====================================================
        # LIVER
        # ====================================================

        liver = (

            self.liver_engine
            .calculate(

                sugar=
                    organ_inputs["sugar"],

                hfcs=
                    organ_inputs["hfcs"],

                fructose=
                    organ_inputs["fructose"],

                processing_score=
                    organ_inputs[
                        "processing_score"
                    ],

                fat_storage_score=
                    organ_inputs[
                        "fat_storage_score"
                    ],

                inflammation_score=
                    organ_inputs[
                        "inflammation_score"
                    ]
            )
        )

        # ====================================================
        # KIDNEY
        # ====================================================

        kidney = (

            self.kidney_engine
            .calculate(

                sodium_mg=
                    organ_inputs["sodium_mg"],

                hydration_score=
                    organ_inputs[
                        "hydration_score"
                    ],

                protein_g=
                    organ_inputs["protein_g"],

                blood_pressure_load=
                    heart[
                        "blood_pressure_load"
                    ]
            )
        )

        # ====================================================
        # PANCREAS
        # ====================================================

        pancreas = (

            self.pancreas_engine
            .calculate(

                glycemic_load=
                    organ_inputs[
                        "glycemic_load"
                    ],

                insulin_load=
                    organ_inputs[
                        "insulin_load"
                    ],

                hba1c=
                    organ_inputs[
                        "hba1c"
                    ],

                peak_glucose=
                    organ_inputs[
                        "peak_glucose"
                    ]
            )
        )

        # ====================================================
        # GUT
        # ====================================================

        gut = (

            self.gut_engine
            .calculate(

                fiber_g=
                    organ_inputs["fiber_g"],

                additive_score=
                    organ_inputs[
                        "additive_score"
                    ],

                emulsifier_score=
                    organ_inputs[
                        "emulsifier_score"
                    ],

                processing_score=
                    organ_inputs[
                        "processing_score"
                    ]
            )
        )

        # ====================================================
        # BRAIN
        # ====================================================

        brain = (

            self.brain_engine
            .calculate(

                sugar_g=
                    organ_inputs["sugar"],

                inflammation_score=
                    organ_inputs[
                        "inflammation_score"
                    ],

                energy_stability=
                    organ_inputs[
                        "energy_stability"
                    ],

                processing_score=
                    organ_inputs[
                        "processing_score"
                    ]
            )
        )

        # ====================================================
        # BLOOD VESSELS
        # ====================================================

        blood_vessels = (

            self.vascular_engine
            .calculate(

                sugar_g=
                    organ_inputs["sugar"],

                inflammation_score=
                    organ_inputs[
                        "inflammation_score"
                    ],

                sodium_mg=
                    organ_inputs["sodium_mg"],

                blood_pressure_signal=
                    heart[
                        "blood_pressure_load"
                    ]
            )
        )

        # ====================================================
        # IMMUNE SYSTEM
        # ====================================================

        immune_system = (

            self.immune_engine
            .calculate(

                inflammation_score=
                    organ_inputs[
                        "inflammation_score"
                    ],

                processing_score=
                    organ_inputs[
                        "processing_score"
                    ],

                additive_score=
                    organ_inputs[
                        "additive_score"
                    ],

                fiber_g=
                    organ_inputs["fiber_g"],

                micronutrient_score=
                    organ_inputs[
                        "micronutrient_score"
                    ]
            )
        )

        # ====================================================
        # AGGREGATION
        # ====================================================

        organ_results = {

            "heart":
                heart,

            "liver":
                liver,

            "kidney":
                kidney,

            "pancreas":
                pancreas,

            "gut":
                gut,

            "brain":
                brain,

            "blood_vessels":
                blood_vessels,

            "immune_system":
                immune_system
        }

        organ_health_score = (

            OrganHealthScoreEngine
            .calculate(
                organ_results
            )

        )

        most_stressed_organ = (

            MostStressedOrganEngine
            .identify(
                organ_results
            )

        )

        most_protected_organ = (

            MostProtectedOrganEngine
            .identify(
                organ_results
            )

        )

        overall_organ_verdict = (

            OverallOrganVerdictEngine
            .generate(
                organ_health_score
            )

        )

        heatmap = (

            OrganHeatmapEngine
            .generate(
                organ_results
            )

        )

        return {

            **organ_results,

            "organ_health_score":
                organ_health_score,

            "most_stressed_organ":
                most_stressed_organ,

            "most_protected_organ":
                most_protected_organ,

            "overall_organ_verdict":
                overall_organ_verdict,

            "body_organ_heatmap":
                heatmap
        }


# ============================================================
# SINGLETON EXPORT
# ============================================================

organ_impact_engine = (
    OrganImpactEngine()
)