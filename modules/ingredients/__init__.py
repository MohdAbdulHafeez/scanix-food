# ==========================================================
# SCANIX AI
# SYSTEM 2 – INGREDIENT INTELLIGENCE MODULE
# ELITE PRODUCTION GRADE – FINAL VERSION
# ==========================================================


from __future__ import annotations


# ==========================================================
# PARSER
# ==========================================================


from .parser import (
    IngredientParser,
    IngredientRecord,
    IngredientProfile,
)


# ==========================================================
# VERIFIER
# ==========================================================


from .verifier import (
    IngredientVerifier,
)


# ==========================================================
# ADDITIVE ENGINE
# ==========================================================


from .additive_engine import (
    AdditiveEngine,
    additive_engine,
)


# ==========================================================
# INGREDIENT FUNCTION ENGINE
# ==========================================================


from .ingredient_function_engine import (
    IngredientFunctionEngine,
    ingredient_function_engine,
)


# ==========================================================
# INGREDIENT RISK ENGINE
# ==========================================================


from .ingredient_risk_engine import (
    IngredientRiskEngine,
    ingredient_risk_engine,
)


# ==========================================================
# ADDITIVES REGISTRY
# ==========================================================


from .additives_registry import (
    ADDITIVES,
    RISK_TITLES,
    MESSAGES,
    get_additive_by_number,
    get_high_risk_additives,
    get_additives_by_risk,
    get_additives_by_function,
)


# ==========================================================
# SERVICE (MASTER ORCHESTRATOR)
# ==========================================================


from .service import (
    ingredient_intelligence_service,
    IngredientIntelligenceService,
)


# ==========================================================
# EXPORTS – ALL PUBLIC INTERFACES
# ==========================================================


__all__ = [
    # Parser
    "IngredientParser",
    "IngredientRecord",
    "IngredientProfile",
    # Verifier
    "IngredientVerifier",
    # Additive Engine
    "AdditiveEngine",
    "additive_engine",
    # Ingredient Function Engine
    "IngredientFunctionEngine",
    "ingredient_function_engine",
    # Ingredient Risk Engine
    "IngredientRiskEngine",
    "ingredient_risk_engine",
    # Additives Registry
    "ADDITIVES",
    "RISK_TITLES",
    "MESSAGES",
    "get_additive_by_number",
    "get_high_risk_additives",
    "get_additives_by_risk",
    "get_additives_by_function",
    # Service
    "ingredient_intelligence_service",
    "IngredientIntelligenceService",
]


# ==========================================================
# MODULE INITIALIZATION LOG
# ==========================================================


from core.logging import log


log.info(
    "System 2 – Ingredient Intelligence module initialized",
    parser_loaded=True,
    verifier_loaded=True,
    additive_engine_loaded=True,
    function_engine_loaded=True,
    risk_engine_loaded=True,
    registry_size=len(ADDITIVES) if ADDITIVES else 0,
)


# ==========================================================
# END OF FILE – __init__.py
# ==========================================================