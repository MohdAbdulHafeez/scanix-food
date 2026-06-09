from functools import lru_cache
from typing import List
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    PROJECT: str = "SCANIX AI"
    APP_NAME: str = "SCANIX AI"
    VERSION: str = "1.0.0"

    ENV: str = "development"
    DEBUG: bool = True

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    LOG_LEVEL: str = "INFO"

    SECRET_KEY: str = ""
    JWT_SECRET: str = ""

    JWT_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    DATABASE_URL: str = ""

    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""

    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 40

    # ==========================================================
    # AI PROVIDERS
    # ==========================================================

    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"

    GROQ_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    TAVILY_API_KEY: str = ""

    AI_DEFAULT_PROVIDER: str = "gemini"
    AI_FALLBACK_PROVIDER: str = "groq"

    DEFAULT_MODEL: str = "gemini-2.5-flash"

    AI_TIMEOUT_SECONDS: int = 60
    AI_MAX_RETRIES: int = 3

    # ==========================================================
    # SEARCH PROVIDERS (SYSTEM 7)
    # ==========================================================

    GOOGLE_CSE_API_KEY: str = ""
    GOOGLE_CSE_ID: str = ""

    USDA_API_KEY: str = ""

    # ==========================================================
    # FOOD DATA APIS
    # ==========================================================

    OPENFOODFACTS_URL: str = "https://world.openfoodfacts.org"
    OPENFOODFACTS_TIMEOUT: int = 10
    OPENFOODFACTS_CACHE_TTL: int = 86400

    SPOONACULAR_API_KEY: str = ""
    APININJAS_API_KEY: str = ""

    # ==========================================================
    # FATSECRET API
    # ==========================================================

    FATSECRET_CLIENT_ID: str = ""
    FATSECRET_CONSUMER_KEY: str = ""
    FATSECRET_CONSUMER_SECRET: str = ""

    # ==========================================================
    # RESEARCH APIS
    # ==========================================================

    PUBMED_EMAIL: str = ""
    CROSSREF_BASE_URL: str = "https://api.crossref.org"
    CROSSREF_MAILTO: str = ""

    # ==========================================================
    # SAFETY APIS
    # ==========================================================

    OPENFDA_URL: str = "https://api.fda.gov"
    OPENFDA_ENABLED: bool = True

    # ==========================================================
    # CACHE
    # ==========================================================

    REDIS_URL: str = "redis://localhost:6379"
    CACHE_TTL: int = 3600

    # ==========================================================
    # VECTOR SEARCH / RAG
    # ==========================================================

    ENABLE_RAG: bool = True
    ENABLE_WEB_RAG: bool = True
    ENABLE_AGENT_MEMORY: bool = True
    ENABLE_VOICE_CHAT: bool = True
    ENABLE_MEAL_PLANNER: bool = True
    ENABLE_PRODUCT_COMPARISON: bool = True
    ENABLE_FOOD_EXPLAINER: bool = True
    ENABLE_NUTRITION_AGENT: bool = True

    VECTOR_DB: str = "qdrant"
    VECTOR_COLLECTION: str = "scanix_food"

    QDRANT_URL: str = ""
    QDRANT_API_KEY: str = ""

    RAG_MAX_RESULTS: int = 10
    RAG_MAX_SOURCES: int = 8
    RAG_SEARCH_TIMEOUT: int = 15
    RAG_CACHE_TTL: int = 86400

    # ==========================================================
    # VOICE
    # ==========================================================

    VOICE_PROVIDER: str = "edge"
    VOICE_MODE: str = "normal"
    VOICE_LANGUAGE: str = "en"
    VOICE_SPEED: float = 1.0
    VOICE_GENDER: str = "female"
    VOICE_NAME: str = "en-US-JennyNeural"
    WHISPER_MODEL: str = "small.en"
    VOICE_TIMEOUT: int = 30

    # ==========================================================
    # SCAN
    # ==========================================================

    MAX_SCAN_IMAGES: int = 4
    MAX_UPLOAD_MB: int = 10

    # ==========================================================
    # SCORE
    # ==========================================================

    DEFAULT_SCORE: int = 70

    # ==========================================================
    # BACKGROUND JOBS
    # ==========================================================

    CELERY_BROKER_URL: str = "redis://localhost:6379"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379"

    # ==========================================================
    # OBSERVABILITY
    # ==========================================================

    SENTRY_DSN: str = ""
    POSTHOG_API_KEY: str = ""

    # ==========================================================
    # DEPLOYMENT
    # ==========================================================

    FRONTEND_URL: str = "http://localhost:3000"
    BACKEND_URL: str = "http://localhost:8000"

    ALLOWED_HOSTS: str = "*"
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"]
    )

    # ==========================================================
    # RATE LIMITING
    # ==========================================================

    API_RATE_LIMIT_PER_MINUTE: int = 60
    API_RATE_LIMIT_PER_HOUR: int = 1000
    AI_REQUESTS_PER_MINUTE: int = 60
    AI_REQUESTS_PER_DAY: int = 5000

    # ==========================================================
    # AI TOKEN LIMITS
    # ==========================================================

    AI_MAX_INPUT_TOKENS: int = 32000
    AI_MAX_OUTPUT_TOKENS: int = 4096

    # ==========================================================
    # AI ROUTING
    # ==========================================================

    AI_PRIMARY_MODEL: str = "gemini-2.5-flash"
    AI_DEEP_MODEL: str = "gemini-2.5-flash"
    AI_EXPLAINER_MODEL: str = "gemini-2.5-flash"
    AI_AGENT_MODEL: str = "gemini-2.5-flash"
    AI_MEAL_MODEL: str = "gemini-2.5-flash"
    AI_PROVIDER_STRATEGY: str = "fallback"
    AI_PROVIDER_ORDER: str = "gemini,groq,openrouter"

    # ==========================================================
    # STORAGE
    # ==========================================================

    UPLOAD_DIR: str = "uploads"
    REPORTS_DIR: str = "reports"
    CACHE_DIR: str = "cache"

    # ==========================================================
    # FEATURE FLAGS
    # ==========================================================

    ENABLE_BARCODE_SCAN: bool = True
    ENABLE_CAMERA_SCAN: bool = True
    ENABLE_INGREDIENT_ANALYSIS: bool = True
    ENABLE_COMPLIANCE_ENGINE: bool = True
    ENABLE_HEALTH_SCORING: bool = True
    ENABLE_OPENFOODFACTS: bool = True

    # ==========================================================
    # SCAN HISTORY
    # ==========================================================

    SCAN_HISTORY_LIMIT: int = 100
    FAVORITES_LIMIT: int = 200

    # ==========================================================
    # OCR
    # ==========================================================

    OCR_PROVIDER: str = "tesseract"
    TESSERACT_PATH: str = ""

    # ==========================================================
    # HEALTH SCORE VERSION
    # ==========================================================

    HEALTH_SCORE_VERSION: str = "1.0"
    RECOMMENDATION_VERSION: str = "1.0"

    # ==========================================================
    # SUPABASE
    # ==========================================================

    SUPABASE_JWT_SECRET: str = ""


    # ==========================================================
    # EMAIL CONFIGURATION (System 8)
    # ==========================================================
    

    SENDGRID_API_KEY: str = ""
    FROM_EMAIL: str = "complaints@scanix.ai"


    # ==========================================================
    # PROPERTIES
    # ==========================================================

    @property
    def allowed_hosts_list(self) -> List[str]:

        if self.ALLOWED_HOSTS == "*":
            return ["*"]

        return [
            host.strip()
            for host in self.ALLOWED_HOSTS.split(",")
        ]

    @property
    def cors_origins_list(self) -> List[str]:

        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

        return self.CORS_ORIGINS

    @property
    def is_production(self) -> bool:

        return self.ENV == "production"

    @property
    def is_development(self) -> bool:

        return self.ENV == "development"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()