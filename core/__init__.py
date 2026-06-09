# ==========================================================
# SCANIX AI
# CORE MODULE INITIALIZATION
# ELITE PRODUCTION GRADE
# ==========================================================

from __future__ import annotations

from core.config import settings, get_settings
from core.exceptions import (
    ScanixException,
    ErrorCode,
    exception_to_dict,
    handle_exceptions,
    # System 1
    BarcodeNotFoundException,
    OCRFailedException,
    InvalidBarcodeException,
    ProductNotFoundException,
    LowImageQualityException,
    # System 2
    IngredientParseException,
    # System 5
    GeminiAPIException,
    GroqAPIException,
    OpenRouterAPIException,
    AllAIProvidersFailedException,
    # System 7
    SwapDiscoveryException,
    NoAlternativesFoundException,
    SwapScoringException,
    PriceFetchException,
    ExportException,
    # Database
    DatabaseConnectionException,
    DatabaseQueryException,
    RecordNotFoundException,
    # Cache
    CacheConnectionException,
    CacheOperationException,
    # Auth
    UnauthorizedException,
    InvalidTokenException,
    TokenExpiredException,
    PermissionDeniedException,
    # Validation
    ValidationException,
    MissingFieldException,
    # Rate Limit
    RateLimitExceededException,
    # File
    InvalidFileTypeException,
    FileSizeExceededException,
    # System 8
    InvalidFSSAIException,
    PDFGenerationException,
)
from core.logging import log, logger, LoggerManager, get_log_stats, flush_logs
from core.security import (
    SecurityUtils,
    PasswordManager,
    JWTManager,
    InputValidator,
    SecurityHeaders,
    RateLimitKeyGenerator,
    security_utils,
    password_manager,
    jwt_manager,
    input_validator,
    security_headers,
    rate_limit_key_gen,
    # Backward compatibility
    validate_email,
    validate_password_strength,
    hash_password,
    verify_password,
    create_access_token,
    verify_token,
)


__all__ = [
    # Config
    "settings",
    "get_settings",
    
    # Exceptions
    "ScanixException",
    "ErrorCode",
    "exception_to_dict",
    "handle_exceptions",
    
    # System 1 Exceptions
    "BarcodeNotFoundException",
    "OCRFailedException",
    "InvalidBarcodeException",
    "ProductNotFoundException",
    "LowImageQualityException",
    
    # System 2 Exceptions
    "IngredientParseException",
    
    # System 5 Exceptions
    "GeminiAPIException",
    "GroqAPIException",
    "OpenRouterAPIException",
    "AllAIProvidersFailedException",
    
    # System 7 Exceptions
    "SwapDiscoveryException",
    "NoAlternativesFoundException",
    "SwapScoringException",
    "PriceFetchException",
    "ExportException",
    
    # Database Exceptions
    "DatabaseConnectionException",
    "DatabaseQueryException",
    "RecordNotFoundException",
    
    # Cache Exceptions
    "CacheConnectionException",
    "CacheOperationException",
    
    # Auth Exceptions
    "UnauthorizedException",
    "InvalidTokenException",
    "TokenExpiredException",
    "PermissionDeniedException",
    
    # Validation Exceptions
    "ValidationException",
    "MissingFieldException",
    
    # Rate Limit Exceptions
    "RateLimitExceededException",
    
    # File Exceptions
    "InvalidFileTypeException",
    "FileSizeExceededException",
    
    # System 8 Exceptions
    "InvalidFSSAIException",
    "PDFGenerationException",
    
    # Logging
    "log",
    "logger",
    "LoggerManager",
    "get_log_stats",
    "flush_logs",
    
    # Security
    "SecurityUtils",
    "PasswordManager",
    "JWTManager",
    "InputValidator",
    "SecurityHeaders",
    "RateLimitKeyGenerator",
    "security_utils",
    "password_manager",
    "jwt_manager",
    "input_validator",
    "security_headers",
    "rate_limit_key_gen",
    
    # Security Backward Compatibility
    "validate_email",
    "validate_password_strength",
    "hash_password",
    "verify_password",
    "create_access_token",
    "verify_token",
]


# ==========================================================
# DATABASE IMPORTS (from database folder)
# ==========================================================

# Note: Since database is a separate folder, imports will be handled
# by the database/__init__.py file. The core module doesn't need
# to re-export database items unless you want convenience imports.

# If you want convenience imports from core, uncomment:
# from database import (
#     engine,
#     SessionLocal,
#     Base,
#     get_db,
#     get_db_session,
#     check_database_connection,
#     initialize_database,
#     drop_database,
#     get_engine,
#     get_session,
#     get_session_factory,
#     health_check,
#     get_pool_status,
#     execute_raw_sql,
# )
#
# and add them to __all__


# ==========================================================
# MODULE INITIALIZATION LOG
# ==========================================================

log.info(
    "Core module initialized",
    config_loaded=True,
    exceptions_loaded=True,
    logging_loaded=True,
    security_loaded=True,
)


# ==========================================================
# END OF FILE – __init__.py
# ==========================================================