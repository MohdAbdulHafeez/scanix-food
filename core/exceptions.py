# ==========================================================
# SCANIX AI
# CORE EXCEPTIONS & ERROR CODES
# PRODUCTION GRADE – ELITE EDITION
# TOTAL LINES: 450+
# ==========================================================


from __future__ import annotations

from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Union
from enum import Enum
from enum import auto


# ==========================================================
# ERROR CODE ENUM
# ==========================================================


class ErrorCode(str, Enum):
    """
    Standardized error codes for all Scanix AI modules.
    
    Each error code follows the pattern: MODULE_XXXX
    where XXXX is a 4-digit number for specific errors.
    
    Ranges:
    1000-1999: System 1 - Scan Intelligence
    2000-2999: System 2 - Ingredient Intelligence
    3000-3999: System 3 - Metabolic Intelligence
    4000-4999: System 4 - Consumer Intelligence
    5000-5999: System 5 - AI Nutrition Intelligence
    6000-6999: System 6 - Digital Twin
    7000-7999: System 7 - Smart Food Intelligence
    8000-8999: System 8 - Truth & Trust Intelligence
    9000-9999: System 9 - FSSAI Complaint Generator
    """

    # ==================================================
    # System 1: Scan Intelligence (1000-1999)
    # ==================================================
    
    SCAN_BARCODE_NOT_FOUND = "SCAN_1001"
    SCAN_OCR_FAILED = "SCAN_1002"
    SCAN_INVALID_BARCODE = "SCAN_1003"
    SCAN_PRODUCT_NOT_FOUND = "SCAN_1004"
    SCAN_IMAGE_QUALITY_LOW = "SCAN_1005"
    SCAN_BARCODE_MISMATCH = "SCAN_1006"
    SCAN_MULTI_IMAGE_FAILED = "SCAN_1007"
    SCAN_NO_TEXT_EXTRACTED = "SCAN_1008"
    SCAN_CONFIDENCE_TOO_LOW = "SCAN_1009"
    
    # ==================================================
    # System 2: Ingredient Intelligence (2000-2999)
    # ==================================================
    
    INGREDIENT_PARSE_FAILED = "INGREDIENT_2001"
    INGREDIENT_INVALID_FORMAT = "INGREDIENT_2002"
    INGREDIENT_ENUMBER_NOT_FOUND = "INGREDIENT_2003"
    INGREDIENT_SUGAR_ALIAS_DETECTION_FAILED = "INGREDIENT_2004"
    INGREDIENT_ADDITIVE_DB_ERROR = "INGREDIENT_2005"
    INGREDIENT_ALLERGEN_DETECTION_FAILED = "INGREDIENT_2006"
    
    # ==================================================
    # System 3: Metabolic Intelligence (3000-3999)
    # ==================================================
    
    METABOLIC_GI_CALCULATION_FAILED = "METABOLIC_3001"
    METABOLIC_INSULIN_MODEL_ERROR = "METABOLIC_3002"
    METABOLIC_RISK_SCORE_FAILED = "METABOLIC_3003"
    METABOLIC_SIMULATION_ERROR = "METABOLIC_3004"
    METABOLIC_INVALID_PROFILE = "METABOLIC_3005"
    
    # ==================================================
    # System 4: Consumer Intelligence (4000-4999)
    # ==================================================
    
    CONSUMER_FSSAI_VALIDATION_FAILED = "CONSUMER_4001"
    CONSUMER_DECEPTION_DETECTION_FAILED = "CONSUMER_4002"
    CONSUMER_CLAIM_VERIFICATION_FAILED = "CONSUMER_4003"
    CONSUMER_ML_CLASSIFIER_ERROR = "CONSUMER_4004"
    CONSUMER_SUITABILITY_CHECK_FAILED = "CONSUMER_4005"
    CONSUMER_VERDICT_GENERATION_FAILED = "CONSUMER_4006"
    
    # ==================================================
    # System 5: AI Nutrition Intelligence (5000-5999)
    # ==================================================
    
    AI_GEMINI_API_ERROR = "AI_5001"
    AI_GROQ_API_ERROR = "AI_5002"
    AI_OPENROUTER_API_ERROR = "AI_5003"
    AI_ALL_PROVIDERS_FAILED = "AI_5004"
    AI_RAG_SEARCH_FAILED = "AI_5005"
    AI_EMBEDDING_FAILED = "AI_5006"
    AI_RESPONSE_PARSE_FAILED = "AI_5007"
    AI_AGENT_ROUTING_FAILED = "AI_5008"
    AI_VOICE_TRANSCRIPTION_FAILED = "AI_5009"
    AI_VOICE_SYNTHESIS_FAILED = "AI_5010"
    AI_TOKEN_LIMIT_EXCEEDED = "AI_5011"
    AI_RATE_LIMIT_EXCEEDED = "AI_5012"
    
    # ==================================================
    # System 6: Digital Twin (6000-6999)
    # ==================================================
    
    DIGITAL_TWIN_SIMULATION_FAILED = "DIGITAL_TWIN_6001"
    DIGITAL_TWIN_ORGAN_EVALUATION_FAILED = "DIGITAL_TWIN_6002"
    DIGITAL_TWIN_LIMIT_CALCULATION_FAILED = "DIGITAL_TWIN_6003"
    DIGITAL_TWIN_INVALID_USER_PROFILE = "DIGITAL_TWIN_6004"
    DIGITAL_TWIN_PROJECTION_ERROR = "DIGITAL_TWIN_6005"
    
    # ==================================================
    # System 7: Smart Food Intelligence (7000-7999)
    # ==================================================
    
    SWAP_DISCOVERY_FAILED = "SWAP_7001"
    SWAP_NO_ALTERNATIVES_FOUND = "SWAP_7002"
    SWAP_SCORING_FAILED = "SWAP_7003"
    SWAP_RANKING_FAILED = "SWAP_7004"
    SWAP_PRICE_FETCH_FAILED = "SWAP_7005"
    SWAP_COMPARISON_FAILED = "SWAP_7006"
    SWAP_OPENFOODFACTS_ERROR = "SWAP_7007"
    SWAP_GOOGLE_CSE_ERROR = "SWAP_7008"
    SWAP_TAVILY_ERROR = "SWAP_7009"
    SWAP_USDA_ERROR = "SWAP_7010"
    SWAP_CACHE_ERROR = "SWAP_7011"
    SWAP_INVALID_REQUEST = "SWAP_7012"
    SWAP_EXPORT_FAILED = "SWAP_7013"
    
    # ==================================================
    # System 8: Truth & Trust Intelligence (8000-8999)
    # ==================================================
    
    TRUST_FSSAI_LICENSE_INVALID = "TRUST_8001"
    TRUST_FSSAI_API_ERROR = "TRUST_8002"
    TRUST_CLAIM_CONTRADICTION_DETECTED = "TRUST_8003"
    TRUST_ML_CLASSIFICATION_FAILED = "TRUST_8004"
    TRUST_BRAND_SCORING_FAILED = "TRUST_8005"
    TRUST_LEADERBOARD_ERROR = "TRUST_8006"
    
    # ==================================================
    # System 9: FSSAI Complaint Generator (9000-9999)
    # ==================================================
    
    COMPLAINT_PDF_GENERATION_FAILED = "COMPLAINT_9001"
    COMPLAINT_INVALID_FSSAI_NUMBER = "COMPLAINT_9002"
    COMPLAINT_VIOLATION_NOT_FOUND = "COMPLAINT_9003"
    COMPLAINT_PG_PORTAL_SUBMISSION_FAILED = "COMPLAINT_9004"
    COMPLAINT_QR_GENERATION_FAILED = "COMPLAINT_9005"
    COMPLAINT_TEMPLATE_ERROR = "COMPLAINT_9006"
    
    # ==================================================
    # Database Errors (10000-10999)
    # ==================================================
    
    DB_CONNECTION_ERROR = "DB_10001"
    DB_QUERY_ERROR = "DB_10002"
    DB_RECORD_NOT_FOUND = "DB_10003"
    DB_DUPLICATE_RECORD = "DB_10004"
    DB_TRANSACTION_FAILED = "DB_10005"
    DB_MIGRATION_ERROR = "DB_10006"
    
    # ==================================================
    # Cache Errors (11000-11999)
    # ==================================================
    
    CACHE_CONNECTION_ERROR = "CACHE_11001"
    CACHE_OPERATION_FAILED = "CACHE_11002"
    CACHE_KEY_NOT_FOUND = "CACHE_11003"
    CACHE_SERIALIZATION_ERROR = "CACHE_11004"
    CACHE_TTL_INVALID = "CACHE_11005"
    
    # ==================================================
    # Authentication Errors (12000-12999)
    # ==================================================
    
    AUTH_UNAUTHORIZED = "AUTH_12001"
    AUTH_INVALID_TOKEN = "AUTH_12002"
    AUTH_TOKEN_EXPIRED = "AUTH_12003"
    AUTH_INVALID_CREDENTIALS = "AUTH_12004"
    AUTH_USER_NOT_FOUND = "AUTH_12005"
    AUTH_PERMISSION_DENIED = "AUTH_12006"
    
    # ==================================================
    # Validation Errors (13000-13999)
    # ==================================================
    
    VALIDATION_ERROR = "VALIDATION_13001"
    VALIDATION_INVALID_INPUT = "VALIDATION_13002"
    VALIDATION_MISSING_FIELD = "VALIDATION_13003"
    VALIDATION_INVALID_TYPE = "VALIDATION_13004"
    VALIDATION_OUT_OF_RANGE = "VALIDATION_13005"
    VALIDATION_PATTERN_MISMATCH = "VALIDATION_13006"
    
    # ==================================================
    # Rate Limiting Errors (14000-14999)
    # ==================================================
    
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_14001"
    RATE_LIMIT_PER_MINUTE_EXCEEDED = "RATE_LIMIT_14002"
    RATE_LIMIT_PER_HOUR_EXCEEDED = "RATE_LIMIT_14003"
    RATE_LIMIT_PER_DAY_EXCEEDED = "RATE_LIMIT_14004"
    
    # ==================================================
    # File Upload Errors (15000-15999)
    # ==================================================
    
    FILE_INVALID_TYPE = "FILE_15001"
    FILE_SIZE_EXCEEDED = "FILE_15002"
    FILE_CORRUPTED = "FILE_15003"
    FILE_UPLOAD_FAILED = "FILE_15004"
    FILE_NOT_FOUND = "FILE_15005"
    
    # ==================================================
    # External API Errors (16000-16999)
    # ==================================================
    
    EXTERNAL_API_TIMEOUT = "EXTERNAL_16001"
    EXTERNAL_API_RATE_LIMIT = "EXTERNAL_16002"
    EXTERNAL_API_INVALID_RESPONSE = "EXTERNAL_16003"
    EXTERNAL_API_SERVER_ERROR = "EXTERNAL_16004"
    EXTERNAL_API_AUTH_FAILED = "EXTERNAL_16005"
    
    # ==================================================
    # General Errors (90000-90999)
    # ==================================================
    
    UNKNOWN_ERROR = "GENERAL_90001"
    INTERNAL_SERVER_ERROR = "GENERAL_90002"
    SERVICE_UNAVAILABLE = "GENERAL_90003"
    OPERATION_TIMEOUT = "GENERAL_90004"
    NOT_IMPLEMENTED = "GENERAL_90005"


# ==========================================================
# BASE EXCEPTION CLASS
# ==========================================================


class ScanixException(Exception):
    """
    Base exception for all Scanix AI errors.
    
    This exception class provides standardized error handling
    across all modules with consistent error codes, messages,
    and status codes for HTTP responses.
    
    Attributes:
        error_code: ErrorCode enum value
        message: Human-readable error message
        status_code: HTTP status code for API responses
        details: Additional error context/details
        original_exception: Original exception if wrapped
    """

    def __init__(
        self,
        error_code: ErrorCode,
        message: str,
        status_code: int = 400,
        details: Optional[Dict[str, Any]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """
        Initialize ScanixException.

        Args:
            error_code: ErrorCode enum value
            message: Human-readable error message
            status_code: HTTP status code (default: 400)
            details: Additional error context
            original_exception: Original exception if wrapped
        """

        self.error_code = error_code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        self.original_exception = original_exception

        super().__init__(self.message)

    def __str__(self) -> str:
        """
        String representation of the exception.

        Returns:
            Formatted error string with code and message
        """

        return f"[{self.error_code}] {self.message}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert exception to dictionary for JSON responses.

        Returns:
            Dictionary with error details
        """

        result = {
            "error_code": self.error_code,
            "message": self.message,
            "status_code": self.status_code,
        }

        if self.details:
            result["details"] = self.details

        return result


# ==========================================================
# SYSTEM 1 EXCEPTIONS (Scan Intelligence)
# ==========================================================


class BarcodeNotFoundException(ScanixException):
    """
    Exception raised when a barcode is not found in any database.
    """

    def __init__(
        self,
        barcode: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize BarcodeNotFoundException.

        Args:
            barcode: The barcode that was not found
            details: Additional error details
        """

        super().__init__(
            error_code=ErrorCode.SCAN_BARCODE_NOT_FOUND,
            message=f"Product with barcode {barcode} not found in any database",
            status_code=404,
            details=details or {"barcode": barcode},
        )


class OCRFailedException(ScanixException):
    """
    Exception raised when OCR processing fails.
    """

    def __init__(
        self,
        message: str = "OCR processing failed",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize OCRFailedException.

        Args:
            message: Error message
            details: Additional error details
        """

        super().__init__(
            error_code=ErrorCode.SCAN_OCR_FAILED,
            message=message,
            status_code=422,
            details=details,
        )


class InvalidBarcodeException(ScanixException):
    """
    Exception raised when a barcode is invalid (checksum mismatch, wrong length).
    """

    def __init__(
        self,
        barcode: str,
        reason: Optional[str] = None,
    ) -> None:
        """
        Initialize InvalidBarcodeException.

        Args:
            barcode: The invalid barcode
            reason: Why the barcode is invalid
        """

        details = {"barcode": barcode, "reason": reason}

        super().__init__(
            error_code=ErrorCode.SCAN_INVALID_BARCODE,
            message=f"Invalid barcode: {barcode}. {reason or 'Checksum validation failed'}",
            status_code=400,
            details=details,
        )


class ProductNotFoundException(ScanixException):
    """
    Exception raised when a product is not found.
    """

    def __init__(
        self,
        product_identifier: str,
        identifier_type: str = "name",
    ) -> None:
        """
        Initialize ProductNotFoundException.

        Args:
            product_identifier: Product name or barcode
            identifier_type: Type of identifier (name, barcode, id)
        """

        details = {identifier_type: product_identifier}

        super().__init__(
            error_code=ErrorCode.SCAN_PRODUCT_NOT_FOUND,
            message=f"Product with {identifier_type} '{product_identifier}' not found",
            status_code=404,
            details=details,
        )


class LowImageQualityException(ScanixException):
    """
    Exception raised when uploaded image quality is too low.
    """

    def __init__(
        self,
        quality_score: int,
        threshold: int = 50,
    ) -> None:
        """
        Initialize LowImageQualityException.

        Args:
            quality_score: Detected quality score (0-100)
            threshold: Minimum acceptable threshold
        """

        details = {"quality_score": quality_score, "threshold": threshold}

        super().__init__(
            error_code=ErrorCode.SCAN_IMAGE_QUALITY_LOW,
            message=f"Image quality too low ({quality_score}/100). Please upload a clearer image.",
            status_code=400,
            details=details,
        )


# ==========================================================
# SYSTEM 2 EXCEPTIONS (Ingredient Intelligence)
# ==========================================================


class IngredientParseException(ScanixException):
    """
    Exception raised when ingredient parsing fails.
    """

    def __init__(
        self,
        raw_text: str,
        reason: Optional[str] = None,
    ) -> None:
        """
        Initialize IngredientParseException.

        Args:
            raw_text: The raw ingredient text that failed to parse
            reason: Why parsing failed
        """

        details = {"raw_text": raw_text[:200], "reason": reason}

        super().__init__(
            error_code=ErrorCode.INGREDIENT_PARSE_FAILED,
            message=f"Failed to parse ingredients: {reason or 'Invalid format'}",
            status_code=422,
            details=details,
        )


# ==========================================================
# SYSTEM 5 EXCEPTIONS (AI Nutrition Intelligence)
# ==========================================================


class GeminiAPIException(ScanixException):
    """
    Exception raised when Gemini API call fails.
    """

    def __init__(
        self,
        original_error: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize GeminiAPIException.

        Args:
            original_error: Original error message from API
            details: Additional error details
        """

        super().__init__(
            error_code=ErrorCode.AI_GEMINI_API_ERROR,
            message=f"Gemini API error: {original_error or 'Unknown error'}",
            status_code=503,
            details=details,
        )


class GroqAPIException(ScanixException):
    """
    Exception raised when Groq API call fails.
    """

    def __init__(
        self,
        original_error: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize GroqAPIException.

        Args:
            original_error: Original error message from API
            details: Additional error details
        """

        super().__init__(
            error_code=ErrorCode.AI_GROQ_API_ERROR,
            message=f"Groq API error: {original_error or 'Unknown error'}",
            status_code=503,
            details=details,
        )


class OpenRouterAPIException(ScanixException):
    """
    Exception raised when OpenRouter API call fails.
    """

    def __init__(
        self,
        original_error: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize OpenRouterAPIException.

        Args:
            original_error: Original error message from API
            details: Additional error details
        """

        super().__init__(
            error_code=ErrorCode.AI_OPENROUTER_API_ERROR,
            message=f"OpenRouter API error: {original_error or 'Unknown error'}",
            status_code=503,
            details=details,
        )


class AllAIProvidersFailedException(ScanixException):
    """
    Exception raised when all AI providers fail.
    """

    def __init__(
        self,
        failed_providers: List[str],
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize AllAIProvidersFailedException.

        Args:
            failed_providers: List of providers that failed
            details: Additional error details
        """

        super().__init__(
            error_code=ErrorCode.AI_ALL_PROVIDERS_FAILED,
            message=f"All AI providers failed. Failed: {', '.join(failed_providers)}",
            status_code=503,
            details=details or {"failed_providers": failed_providers},
        )


# ==========================================================
# SYSTEM 7 EXCEPTIONS (Smart Food Intelligence)
# ==========================================================


class SwapDiscoveryException(ScanixException):
    """
    Exception raised when alternative discovery fails.
    """

    def __init__(
        self,
        product_name: str,
        reason: Optional[str] = None,
    ) -> None:
        """
        Initialize SwapDiscoveryException.

        Args:
            product_name: Name of the product being searched
            reason: Why discovery failed
        """

        details = {"product_name": product_name, "reason": reason}

        super().__init__(
            error_code=ErrorCode.SWAP_DISCOVERY_FAILED,
            message=f"Failed to discover alternatives for '{product_name}': {reason or 'Unknown error'}",
            status_code=500,
            details=details,
        )


class NoAlternativesFoundException(ScanixException):
    """
    Exception raised when no alternatives are found.
    """

    def __init__(
        self,
        product_name: str,
        category: Optional[str] = None,
    ) -> None:
        """
        Initialize NoAlternativesFoundException.

        Args:
            product_name: Name of the product
            category: Product category (optional)
        """

        details = {"product_name": product_name, "category": category}

        super().__init__(
            error_code=ErrorCode.SWAP_NO_ALTERNATIVES_FOUND,
            message=f"No healthier alternatives found for '{product_name}'",
            status_code=404,
            details=details,
        )


class SwapScoringException(ScanixException):
    """
    Exception raised when scoring a swap candidate fails.
    """

    def __init__(
        self,
        candidate_name: str,
        reason: Optional[str] = None,
    ) -> None:
        """
        Initialize SwapScoringException.

        Args:
            candidate_name: Name of the candidate product
            reason: Why scoring failed
        """

        details = {"candidate": candidate_name, "reason": reason}

        super().__init__(
            error_code=ErrorCode.SWAP_SCORING_FAILED,
            message=f"Failed to score candidate '{candidate_name}': {reason or 'Unknown error'}",
            status_code=500,
            details=details,
        )


class PriceFetchException(ScanixException):
    """
    Exception raised when fetching product price fails.
    """

    def __init__(
        self,
        product_name: str,
        source: str = "unknown",
    ) -> None:
        """
        Initialize PriceFetchException.

        Args:
            product_name: Name of the product
            source: Price source that failed
        """

        details = {"product_name": product_name, "source": source}

        super().__init__(
            error_code=ErrorCode.SWAP_PRICE_FETCH_FAILED,
            message=f"Failed to fetch price for '{product_name}' from {source}",
            status_code=500,
            details=details,
        )


class ExportException(ScanixException):
    """
    Exception raised when exporting swap recommendations fails.
    """

    def __init__(
        self,
        format_type: str,
        reason: Optional[str] = None,
    ) -> None:
        """
        Initialize ExportException.

        Args:
            format_type: Export format (csv, pdf, html, etc.)
            reason: Why export failed
        """

        details = {"format": format_type, "reason": reason}

        super().__init__(
            error_code=ErrorCode.SWAP_EXPORT_FAILED,
            message=f"Failed to export as {format_type}: {reason or 'Unknown error'}",
            status_code=500,
            details=details,
        )


# ==========================================================
# DATABASE EXCEPTIONS
# ==========================================================


class DatabaseConnectionException(ScanixException):
    """
    Exception raised when database connection fails.
    """

    def __init__(
        self,
        original_error: Optional[str] = None,
    ) -> None:
        """
        Initialize DatabaseConnectionException.

        Args:
            original_error: Original error message
        """

        super().__init__(
            error_code=ErrorCode.DB_CONNECTION_ERROR,
            message=f"Database connection failed: {original_error or 'Check connection settings'}",
            status_code=503,
            details={"original_error": original_error},
        )


class DatabaseQueryException(ScanixException):
    """
    Exception raised when a database query fails.
    """

    def __init__(
        self,
        query: str,
        original_error: Optional[str] = None,
    ) -> None:
        """
        Initialize DatabaseQueryException.

        Args:
            query: The SQL query that failed
            original_error: Original error message
        """

        details = {"query": query[:200], "original_error": original_error}

        super().__init__(
            error_code=ErrorCode.DB_QUERY_ERROR,
            message=f"Database query failed: {original_error or 'Unknown error'}",
            status_code=500,
            details=details,
        )


class RecordNotFoundException(ScanixException):
    """
    Exception raised when a database record is not found.
    """

    def __init__(
        self,
        table: str,
        record_id: Any,
    ) -> None:
        """
        Initialize RecordNotFoundException.

        Args:
            table: Database table name
            record_id: Record identifier that was not found
        """

        details = {"table": table, "record_id": record_id}

        super().__init__(
            error_code=ErrorCode.DB_RECORD_NOT_FOUND,
            message=f"Record not found in {table} with ID: {record_id}",
            status_code=404,
            details=details,
        )


# ==========================================================
# CACHE EXCEPTIONS
# ==========================================================


class CacheConnectionException(ScanixException):
    """
    Exception raised when Redis/Cache connection fails.
    """

    def __init__(
        self,
        original_error: Optional[str] = None,
    ) -> None:
        """
        Initialize CacheConnectionException.

        Args:
            original_error: Original error message
        """

        super().__init__(
            error_code=ErrorCode.CACHE_CONNECTION_ERROR,
            message=f"Cache connection failed: {original_error or 'Check Redis configuration'}",
            status_code=503,
            details={"original_error": original_error},
        )


class CacheOperationException(ScanixException):
    """
    Exception raised when a cache operation fails.
    """

    def __init__(
        self,
        operation: str,
        key: str,
        original_error: Optional[str] = None,
    ) -> None:
        """
        Initialize CacheOperationException.

        Args:
            operation: Cache operation (get, set, delete)
            key: Cache key
            original_error: Original error message
        """

        details = {"operation": operation, "key": key, "original_error": original_error}

        super().__init__(
            error_code=ErrorCode.CACHE_OPERATION_FAILED,
            message=f"Cache {operation} failed for key '{key}': {original_error or 'Unknown error'}",
            status_code=500,
            details=details,
        )


# ==========================================================
# AUTHENTICATION EXCEPTIONS
# ==========================================================


class UnauthorizedException(ScanixException):
    """
    Exception raised when authentication is required but not provided.
    """

    def __init__(
        self,
        reason: str = "Authentication required",
    ) -> None:
        """
        Initialize UnauthorizedException.

        Args:
            reason: Reason for unauthorized access
        """

        super().__init__(
            error_code=ErrorCode.AUTH_UNAUTHORIZED,
            message=reason,
            status_code=401,
        )


class InvalidTokenException(ScanixException):
    """
    Exception raised when an authentication token is invalid.
    """

    def __init__(
        self,
        reason: str = "Invalid or malformed token",
    ) -> None:
        """
        Initialize InvalidTokenException.

        Args:
            reason: Why the token is invalid
        """

        super().__init__(
            error_code=ErrorCode.AUTH_INVALID_TOKEN,
            message=reason,
            status_code=401,
        )


class TokenExpiredException(ScanixException):
    """
    Exception raised when an authentication token has expired.
    """

    def __init__(
        self,
        expired_at: Optional[str] = None,
    ) -> None:
        """
        Initialize TokenExpiredException.

        Args:
            expired_at: Timestamp when token expired
        """

        details = {"expired_at": expired_at}

        super().__init__(
            error_code=ErrorCode.AUTH_TOKEN_EXPIRED,
            message="Authentication token has expired. Please login again.",
            status_code=401,
            details=details,
        )


class PermissionDeniedException(ScanixException):
    """
    Exception raised when user lacks required permissions.
    """

    def __init__(
        self,
        required_permission: str,
    ) -> None:
        """
        Initialize PermissionDeniedException.

        Args:
            required_permission: Permission that was required
        """

        details = {"required_permission": required_permission}

        super().__init__(
            error_code=ErrorCode.AUTH_PERMISSION_DENIED,
            message=f"Permission denied. Required: {required_permission}",
            status_code=403,
            details=details,
        )


# ==========================================================
# VALIDATION EXCEPTIONS
# ==========================================================


class ValidationException(ScanixException):
    """
    Exception raised when input validation fails.
    """

    def __init__(
        self,
        errors: List[Dict[str, Any]],
    ) -> None:
        """
        Initialize ValidationException.

        Args:
            errors: List of validation errors
        """

        super().__init__(
            error_code=ErrorCode.VALIDATION_ERROR,
            message="Request validation failed",
            status_code=422,
            details={"errors": errors},
        )


class MissingFieldException(ScanixException):
    """
    Exception raised when a required field is missing.
    """

    def __init__(
        self,
        field_name: str,
    ) -> None:
        """
        Initialize MissingFieldException.

        Args:
            field_name: Name of the missing field
        """

        details = {"missing_field": field_name}

        super().__init__(
            error_code=ErrorCode.VALIDATION_MISSING_FIELD,
            message=f"Required field '{field_name}' is missing",
            status_code=400,
            details=details,
        )


# ==========================================================
# RATE LIMIT EXCEPTIONS
# ==========================================================


class RateLimitExceededException(ScanixException):
    """
    Exception raised when rate limit is exceeded.
    """

    def __init__(
        self,
        limit: int,
        period: str,
        retry_after_seconds: int = 60,
    ) -> None:
        """
        Initialize RateLimitExceededException.

        Args:
            limit: Maximum allowed requests
            period: Time period (minute, hour, day)
            retry_after_seconds: Seconds to wait before retry
        """

        details = {
            "limit": limit,
            "period": period,
            "retry_after_seconds": retry_after_seconds,
        }

        super().__init__(
            error_code=ErrorCode.RATE_LIMIT_EXCEEDED,
            message=f"Rate limit exceeded. Maximum {limit} requests per {period}.",
            status_code=429,
            details=details,
        )


# ==========================================================
# FILE UPLOAD EXCEPTIONS
# ==========================================================


class InvalidFileTypeException(ScanixException):
    """
    Exception raised when file type is not allowed.
    """

    def __init__(
        self,
        file_type: str,
        allowed_types: List[str],
    ) -> None:
        """
        Initialize InvalidFileTypeException.

        Args:
            file_type: Detected file type
            allowed_types: List of allowed file types
        """

        details = {"detected_type": file_type, "allowed_types": allowed_types}

        super().__init__(
            error_code=ErrorCode.FILE_INVALID_TYPE,
            message=f"Invalid file type '{file_type}'. Allowed: {', '.join(allowed_types)}",
            status_code=400,
            details=details,
        )


class FileSizeExceededException(ScanixException):
    """
    Exception raised when file size exceeds limit.
    """

    def __init__(
        self,
        file_size_bytes: int,
        max_size_bytes: int,
    ) -> None:
        """
        Initialize FileSizeExceededException.

        Args:
            file_size_bytes: Actual file size
            max_size_bytes: Maximum allowed size
        """

        details = {
            "file_size_mb": round(file_size_bytes / (1024 * 1024), 2),
            "max_size_mb": round(max_size_bytes / (1024 * 1024), 2),
        }

        super().__init__(
            error_code=ErrorCode.FILE_SIZE_EXCEEDED,
            message=f"File size exceeds limit. Max: {details['max_size_mb']}MB",
            status_code=400,
            details=details,
        )


# ==========================================================
# SYSTEM 9 EXCEPTIONS (FSSAI Complaint Generator)
# ==========================================================


class InvalidFSSAIException(ScanixException):
    """
    Exception raised when FSSAI license number is invalid.
    """

    def __init__(
        self,
        fssai_number: str,
        reason: Optional[str] = None,
    ) -> None:
        """
        Initialize InvalidFSSAIException.

        Args:
            fssai_number: The invalid FSSAI number
            reason: Why it's invalid
        """

        details = {"fssai_number": fssai_number, "reason": reason}

        super().__init__(
            error_code=ErrorCode.COMPLAINT_INVALID_FSSAI_NUMBER,
            message=f"Invalid FSSAI license number: {fssai_number}. Must be 14 digits.",
            status_code=400,
            details=details,
        )


class PDFGenerationException(ScanixException):
    """
    Exception raised when PDF generation fails.
    """

    def __init__(
        self,
        reason: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize PDFGenerationException.

        Args:
            reason: Why PDF generation failed
            details: Additional error details
        """

        super().__init__(
            error_code=ErrorCode.COMPLAINT_PDF_GENERATION_FAILED,
            message=f"PDF generation failed: {reason or 'Unknown error'}",
            status_code=500,
            details=details,
        )


# ==========================================================
# EXCEPTION TO DICT UTILITY
# ==========================================================


def exception_to_dict(exception: Exception) -> Dict[str, Any]:
    """
    Convert any exception to a standardized dictionary.

    This utility function converts both ScanixException and
    standard Python exceptions to a consistent format for API responses.

    Args:
        exception: Exception to convert

    Returns:
        Dictionary with error details
    """

    if isinstance(exception, ScanixException):
        return {
            "success": False,
            "error": {
                "code": exception.error_code,
                "message": exception.message,
                "details": exception.details or None,
            },
            "status_code": exception.status_code,
        }

    # Handle standard Python exceptions
    return {
        "success": False,
        "error": {
            "code": ErrorCode.UNKNOWN_ERROR,
            "message": str(exception),
            "details": {
                "exception_type": type(exception).__name__,
            },
        },
        "status_code": 500,
    }


# ==========================================================
# EXCEPTION HANDLER DECORATOR
# ==========================================================


def handle_exceptions(
    default_error_code: ErrorCode = ErrorCode.INTERNAL_SERVER_ERROR,
    default_status_code: int = 500,
) -> Callable:
    """
    Decorator to wrap functions with exception handling.

    This decorator catches exceptions and converts them to
    ScanixException with the specified default error code.

    Args:
        default_error_code: Default ErrorCode if none is specified
        default_status_code: Default HTTP status code

    Returns:
        Decorated function
    """

    def decorator(func: Callable) -> Callable:

        async def async_wrapper(*args, **kwargs):

            try:

                return await func(*args, **kwargs)

            except ScanixException:
                raise

            except Exception as e:

                raise ScanixException(
                    error_code=default_error_code,
                    message=str(e),
                    status_code=default_status_code,
                    original_exception=e,
                )

        def sync_wrapper(*args, **kwargs):

            try:

                return func(*args, **kwargs)

            except ScanixException:
                raise

            except Exception as e:

                raise ScanixException(
                    error_code=default_error_code,
                    message=str(e),
                    status_code=default_status_code,
                    original_exception=e,
                )

        import asyncio

        if asyncio.iscoroutinefunction(func):

            return async_wrapper

        return sync_wrapper

    return decorator


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [
    "ErrorCode",
    "ScanixException",
    "BarcodeNotFoundException",
    "OCRFailedException",
    "InvalidBarcodeException",
    "ProductNotFoundException",
    "LowImageQualityException",
    "IngredientParseException",
    "GeminiAPIException",
    "GroqAPIException",
    "OpenRouterAPIException",
    "AllAIProvidersFailedException",
    "SwapDiscoveryException",
    "NoAlternativesFoundException",
    "SwapScoringException",
    "PriceFetchException",
    "ExportException",
    "DatabaseConnectionException",
    "DatabaseQueryException",
    "RecordNotFoundException",
    "CacheConnectionException",
    "CacheOperationException",
    "UnauthorizedException",
    "InvalidTokenException",
    "TokenExpiredException",
    "PermissionDeniedException",
    "ValidationException",
    "MissingFieldException",
    "RateLimitExceededException",
    "InvalidFileTypeException",
    "FileSizeExceededException",
    "InvalidFSSAIException",
    "PDFGenerationException",
    "exception_to_dict",
    "handle_exceptions",
]


# ==========================================================
# END OF FILE – exceptions.py
# TOTAL LINES: 850+
# ==========================================================