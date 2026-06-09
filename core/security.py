# ==========================================================
# SCANIX AI
# CORE SECURITY – ELITE PRODUCTION GRADE
# ==========================================================


from __future__ import annotations


import hashlib
import hmac
import re
import secrets
import string
from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union


from jose import jwt
from jose import JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from pydantic import field_validator


from core.config import get_settings
from core.logging import log


settings = get_settings()


# ==========================================================
# CONSTANTS
# ==========================================================


PASSWORD_CONTEXT = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

ALGORITHM = "HS256"

DEFAULT_JWT_EXPIRE_MINUTES = 60

DEFAULT_REFRESH_EXPIRE_DAYS = 30

MIN_PASSWORD_LENGTH = 8

MAX_PASSWORD_LENGTH = 128

EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)

PHONE_REGEX = re.compile(
    r"^(\+91|91|0)?[6-9]\d{9}$"
)

FSSAI_LICENSE_REGEX = re.compile(
    r"^\d{14}$"
)

BARCODE_REGEX = re.compile(
    r"^\d{8,14}$"
)

ALLOWED_IMAGE_TYPES = [
    "image/jpeg",
    "image/png",
    "image/jpg",
    "image/webp",
]

MAX_IMAGE_SIZE_MB = 10

MAX_IMAGE_SIZE_BYTES = MAX_IMAGE_SIZE_MB * 1024 * 1024


# ==========================================================
# PYDANTIC MODELS
# ==========================================================


class TokenData(BaseModel):
    """
    JWT token payload data.
    """

    model_config = {
        "extra": "forbid",
    }

    sub: str = Field(
        ...,
        description="Subject (user ID)",
    )

    email: EmailStr = Field(
        ...,
        description="User email",
    )

    exp: datetime = Field(
        ...,
        description="Expiration timestamp",
    )

    iat: datetime = Field(
        ...,
        description="Issued at timestamp",
    )

    iss: str = Field(
        default="scanix-ai",
        description="Issuer",
    )

    aud: str = Field(
        default="scanix-frontend",
        description="Audience",
    )

    type: str = Field(
        default="access",
        description="Token type (access/refresh)",
    )


class TokenResponse(BaseModel):
    """
    Token response for authentication.
    """

    model_config = {
        "extra": "forbid",
    }

    access_token: str = Field(
        ...,
        description="JWT access token",
    )

    refresh_token: str = Field(
        ...,
        description="JWT refresh token",
    )

    token_type: str = Field(
        default="bearer",
        description="Token type",
    )

    expires_in: int = Field(
        ...,
        description="Seconds until expiration",
    )


class LoginRequest(BaseModel):
    """
    Login request model.
    """

    model_config = {
        "extra": "forbid",
    }

    email: EmailStr = Field(
        ...,
        description="User email",
    )

    password: str = Field(
        ...,
        min_length=MIN_PASSWORD_LENGTH,
        max_length=MAX_PASSWORD_LENGTH,
        description="User password",
    )


class PasswordResetRequest(BaseModel):
    """
    Password reset request model.
    """

    model_config = {
        "extra": "forbid",
    }

    email: EmailStr = Field(
        ...,
        description="User email",
    )


class PasswordResetConfirm(BaseModel):
    """
    Password reset confirmation model.
    """

    model_config = {
        "extra": "forbid",
    }

    token: str = Field(
        ...,
        description="Reset token",
    )

    new_password: str = Field(
        ...,
        min_length=MIN_PASSWORD_LENGTH,
        max_length=MAX_PASSWORD_LENGTH,
        description="New password",
    )


class ChangePasswordRequest(BaseModel):
    """
    Change password request model.
    """

    model_config = {
        "extra": "forbid",
    }

    current_password: str = Field(
        ...,
        description="Current password",
    )

    new_password: str = Field(
        ...,
        min_length=MIN_PASSWORD_LENGTH,
        max_length=MAX_PASSWORD_LENGTH,
        description="New password",
    )


# ==========================================================
# SECURITY UTILITIES
# ==========================================================


class SecurityUtils:
    """
    Utility functions for security operations.
    """

    @staticmethod
    def generate_secure_token(
        length: int = 32,
    ) -> str:
        """
        Generate a cryptographically secure random token.

        Args:
            length: Token length in bytes (default: 32)

        Returns:
            Hexadecimal token string
        """

        return secrets.token_hex(length)

    @staticmethod
    def generate_api_key(
        prefix: str = "sk",
        length: int = 32,
    ) -> str:
        """
        Generate a secure API key.

        Args:
            prefix: Key prefix (e.g., "sk" for secret key)
            length: Key length in bytes

        Returns:
            API key string
        """

        random_part = secrets.token_hex(length)

        return f"{prefix}_{random_part}"

    @staticmethod
    def generate_otp(
        length: int = 6,
    ) -> str:
        """
        Generate a numeric OTP (One Time Password).

        Args:
            length: Number of digits (default: 6)

        Returns:
            OTP string
        """

        return "".join(
            secrets.choice(string.digits)
            for _ in range(length)
        )

    @staticmethod
    def hash_string(
        value: str,
        algorithm: str = "sha256",
    ) -> str:
        """
        Hash a string using specified algorithm.

        Args:
            value: String to hash
            algorithm: Hash algorithm (sha256, sha512, md5)

        Returns:
            Hexadecimal hash string
        """

        if algorithm == "sha256":

            return hashlib.sha256(
                value.encode()
            ).hexdigest()

        if algorithm == "sha512":

            return hashlib.sha512(
                value.encode()
            ).hexdigest()

        if algorithm == "md5":

            return hashlib.md5(
                value.encode()
            ).hexdigest()

        raise ValueError(
            f"Unsupported algorithm: {algorithm}"
        )

    @staticmethod
    def verify_hash(
        value: str,
        hashed: str,
        algorithm: str = "sha256",
    ) -> bool:
        """
        Verify a string against its hash.

        Args:
            value: Plain string
            hashed: Hash to compare against
            algorithm: Hash algorithm used

        Returns:
            True if hash matches
        """

        return SecurityUtils.hash_string(
            value,
            algorithm,
        ) == hashed

    @staticmethod
    def create_hmac(
        message: str,
        secret: Optional[str] = None,
    ) -> str:
        """
        Create HMAC signature for a message.

        Args:
            message: Message to sign
            secret: Secret key (uses settings if not provided)

        Returns:
            HMAC signature
        """

        if secret is None:

            secret = settings.JWT_SECRET

        return hmac.new(
            secret.encode(),
            message.encode(),
            hashlib.sha256,
        ).hexdigest()

    @staticmethod
    def verify_hmac(
        message: str,
        signature: str,
        secret: Optional[str] = None,
    ) -> bool:
        """
        Verify HMAC signature.

        Args:
            message: Original message
            signature: Signature to verify
            secret: Secret key used

        Returns:
            True if signature is valid
        """

        expected = SecurityUtils.create_hmac(
            message,
            secret,
        )

        return hmac.compare_digest(
            expected,
            signature,
        )


# ==========================================================
# PASSWORD MANAGEMENT
# ==========================================================


class PasswordManager:
    """
    Secure password hashing and verification.
    Uses bcrypt with automatic salt generation.
    """

    @staticmethod
    def hash_password(
        password: str,
    ) -> str:
        """
        Hash a password using bcrypt.

        Args:
            password: Plain text password

        Returns:
            Bcrypt hash string
        """

        return PASSWORD_CONTEXT.hash(
            password
        )

    @staticmethod
    def verify_password(
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        """
        Verify a password against its hash.

        Args:
            plain_password: Plain text password
            hashed_password: Bcrypt hash

        Returns:
            True if password matches
        """

        return PASSWORD_CONTEXT.verify(
            plain_password,
            hashed_password,
        )

    @staticmethod
    def needs_rehash(
        hashed_password: str,
    ) -> bool:
        """
        Check if password hash needs rehashing.

        Args:
            hashed_password: Existing hash

        Returns:
            True if rehashing is needed
        """

        return PASSWORD_CONTEXT.needs_update(
            hashed_password
        )

    @staticmethod
    def validate_password_strength(
        password: str,
    ) -> Tuple[bool, List[str]]:
        """
        Validate password strength against security rules.

        Args:
            password: Password to validate

        Returns:
            Tuple of (is_valid, list_of_issues)
        """

        issues = []

        if len(password) < MIN_PASSWORD_LENGTH:

            issues.append(
                f"Password must be at least {MIN_PASSWORD_LENGTH} characters"
            )

        if len(password) > MAX_PASSWORD_LENGTH:

            issues.append(
                f"Password must be at most {MAX_PASSWORD_LENGTH} characters"
            )

        if not re.search(
            r"[A-Z]",
            password,
        ):

            issues.append(
                "Password must contain at least one uppercase letter"
            )

        if not re.search(
            r"[a-z]",
            password,
        ):

            issues.append(
                "Password must contain at least one lowercase letter"
            )

        if not re.search(
            r"\d",
            password,
        ):

            issues.append(
                "Password must contain at least one number"
            )

        if not re.search(
            r"[!@#$%^&*(),.?\":{}|<>]",
            password,
        ):

            issues.append(
                "Password must contain at least one special character"
            )

        common_passwords = [
            "password",
            "12345678",
            "qwerty123",
            "admin123",
            "letmein123",
        ]

        if password.lower() in common_passwords:

            issues.append(
                "Password is too common"
            )

        return len(issues) == 0, issues


# ==========================================================
# JWT TOKEN MANAGEMENT
# ==========================================================


class JWTManager:
    """
    JWT token creation, verification, and refresh.
    """

    @staticmethod
    def create_access_token(
        user_id: str,
        email: str,
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        """
        Create a new JWT access token.

        Args:
            user_id: User identifier
            email: User email
            expires_delta: Custom expiration (uses settings if None)

        Returns:
            JWT token string
        """

        if expires_delta:

            expire = datetime.utcnow() + expires_delta

        else:

            expire = datetime.utcnow() + timedelta(
                minutes=settings.JWT_EXPIRE_MINUTES or DEFAULT_JWT_EXPIRE_MINUTES
            )

        payload = {

            "sub": user_id,

            "email": email,

            "exp": expire,

            "iat": datetime.utcnow(),

            "iss": "scanix-ai",

            "aud": "scanix-frontend",

            "type": "access",
        }

        token = jwt.encode(
            payload,
            settings.JWT_SECRET,
            algorithm=ALGORITHM,
        )

        return token

    @staticmethod
    def create_refresh_token(
        user_id: str,
        email: str,
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        """
        Create a new JWT refresh token.

        Args:
            user_id: User identifier
            email: User email
            expires_delta: Custom expiration

        Returns:
            JWT refresh token string
        """

        if expires_delta:

            expire = datetime.utcnow() + expires_delta

        else:

            expire = datetime.utcnow() + timedelta(
                days=DEFAULT_REFRESH_EXPIRE_DAYS
            )

        payload = {

            "sub": user_id,

            "email": email,

            "exp": expire,

            "iat": datetime.utcnow(),

            "iss": "scanix-ai",

            "aud": "scanix-frontend",

            "type": "refresh",
        }

        token = jwt.encode(
            payload,
            settings.JWT_SECRET,
            algorithm=ALGORITHM,
        )

        return token

    @staticmethod
    def decode_token(
        token: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Decode and verify a JWT token.

        Args:
            token: JWT token string

        Returns:
            Decoded payload if valid, None otherwise
        """

        try:

            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[ALGORITHM],
                audience="scanix-frontend",
                issuer="scanix-ai",
            )

            return payload

        except JWTError as e:

            log.debug(
                f"JWT decode failed: {e}"
            )

            return None

    @staticmethod
    def verify_token(
        token: str,
        token_type: str = "access",
    ) -> Optional[TokenData]:
        """
        Verify a JWT token and return token data.

        Args:
            token: JWT token string
            token_type: Expected token type (access/refresh)

        Returns:
            TokenData if valid, None otherwise
        """

        payload = JWTManager.decode_token(
            token
        )

        if not payload:

            return None

        if payload.get("type") != token_type:

            log.warning(
                f"Invalid token type. Expected {token_type}, got {payload.get('type')}"
            )

            return None

        return TokenData(
            sub=payload.get("sub"),
            email=payload.get("email"),
            exp=datetime.fromtimestamp(
                payload.get("exp")
            ),
            iat=datetime.fromtimestamp(
                payload.get("iat")
            ),
            iss=payload.get("iss", "scanix-ai"),
            aud=payload.get("aud", "scanix-frontend"),
            type=payload.get("type", "access"),
        )

    @staticmethod
    def refresh_access_token(
        refresh_token: str,
    ) -> Optional[str]:
        """
        Generate a new access token from a refresh token.

        Args:
            refresh_token: Valid refresh token

        Returns:
            New access token or None if invalid
        """

        token_data = JWTManager.verify_token(
            refresh_token,
            token_type="refresh",
        )

        if not token_data:

            return None

        return JWTManager.create_access_token(
            token_data.sub,
            token_data.email,
        )

    @staticmethod
    def get_token_expiry_seconds(
        token: str,
    ) -> int:
        """
        Get remaining seconds until token expiry.

        Args:
            token: JWT token

        Returns:
            Seconds remaining (0 if expired)
        """

        payload = JWTManager.decode_token(
            token
        )

        if not payload:

            return 0

        exp = payload.get("exp")

        if not exp:

            return 0

        remaining = exp - int(
            datetime.utcnow().timestamp()
        )

        return max(remaining, 0)


# ==========================================================
# INPUT VALIDATION
# ==========================================================


class InputValidator:
    """
    Validate and sanitize user inputs.
    """

    @staticmethod
    def validate_email(
        email: str,
    ) -> bool:
        """
        Validate email format.

        Args:
            email: Email string to validate

        Returns:
            True if email format is valid
        """

        return bool(
            EMAIL_REGEX.match(email)
        )

    @staticmethod
    def validate_phone(
        phone: str,
    ) -> bool:
        """
        Validate Indian phone number format.

        Args:
            phone: Phone number string

        Returns:
            True if phone number format is valid
        """

        return bool(
            PHONE_REGEX.match(phone)
        )

    @staticmethod
    def validate_fssai_license(
        license_number: str,
    ) -> bool:
        """
        Validate FSSAI license number format.

        Args:
            license_number: 14-digit FSSAI number

        Returns:
            True if format is valid
        """

        return bool(
            FSSAI_LICENSE_REGEX.match(license_number)
        )

    @staticmethod
    def validate_barcode(
        barcode: str,
    ) -> bool:
        """
        Validate barcode format.

        Args:
            barcode: 8-14 digit barcode

        Returns:
            True if barcode format is valid
        """

        return bool(
            BARCODE_REGEX.match(barcode)
        )

    @staticmethod
    def validate_image(
        content_type: str,
        file_size: int,
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate image file.

        Args:
            content_type: MIME type of the image
            file_size: Size of the file in bytes

        Returns:
            Tuple of (is_valid, error_message)
        """

        if content_type not in ALLOWED_IMAGE_TYPES:

            return False, (
                f"Invalid image type. Allowed: {', '.join(ALLOWED_IMAGE_TYPES)}"
            )

        if file_size > MAX_IMAGE_SIZE_BYTES:

            return False, (
                f"Image size exceeds {MAX_IMAGE_SIZE_MB}MB limit"
            )

        return True, None

    @staticmethod
    def sanitize_string(
        text: str,
        max_length: int = 1000,
        allow_html: bool = False,
    ) -> str:
        """
        Sanitize string input.

        Args:
            text: Input string
            max_length: Maximum allowed length
            allow_html: Whether to allow HTML tags

        Returns:
            Sanitized string
        """

        if not text:

            return ""

        # Truncate to max length
        if len(text) > max_length:

            text = text[:max_length]

        # Remove control characters
        text = re.sub(
            r"[\x00-\x1f\x7f-\x9f]",
            "",
            text,
        )

        # Remove HTML tags if not allowed
        if not allow_html:

            text = re.sub(
                r"<[^>]*>",
                "",
                text,
            )

        # Normalize whitespace
        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    @staticmethod
    def sanitize_filename(
        filename: str,
    ) -> str:
        """
        Sanitize filename to prevent path traversal.

        Args:
            filename: Original filename

        Returns:
            Sanitized filename
        """

        # Remove path separators
        filename = filename.replace("/", "_")

        filename = filename.replace("\\", "_")

        # Remove parent directory references
        filename = filename.replace("..", "_")

        # Allow only alphanumeric, dot, dash, underscore
        filename = re.sub(
            r"[^a-zA-Z0-9._-]",
            "_",
            filename,
        )

        return filename


# ==========================================================
# SECURITY HEADERS
# ==========================================================


class SecurityHeaders:
    """
    Generate security headers for HTTP responses.
    """

    @staticmethod
    def get_headers(
        is_https: bool = False,
    ) -> Dict[str, str]:
        """
        Get security headers for API responses.

        Args:
            is_https: Whether connection is HTTPS

        Returns:
            Dictionary of security headers
        """

        headers = {

            "X-Content-Type-Options": "nosniff",

            "X-Frame-Options": "DENY",

            "X-XSS-Protection": "1; mode=block",

            "Referrer-Policy": "strict-origin-when-cross-origin",

            "Cross-Origin-Resource-Policy": "same-origin",

            "Cross-Origin-Opener-Policy": "same-origin",
        }

        if is_https:

            headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )

        return headers


# ==========================================================
# RATE LIMITING HELPERS
# ==========================================================


class RateLimitKeyGenerator:
    """
    Generate rate limit keys for different scenarios.
    """

    @staticmethod
    def for_user(
        user_id: str,
        endpoint: str,
    ) -> str:
        """
        Generate rate limit key for user.

        Args:
            user_id: User identifier
            endpoint: API endpoint name

        Returns:
            Rate limit key string
        """

        return f"ratelimit:user:{user_id}:{endpoint}"

    @staticmethod
    def for_ip(
        ip_address: str,
        endpoint: str,
    ) -> str:
        """
        Generate rate limit key for IP address.

        Args:
            ip_address: Client IP address
            endpoint: API endpoint name

        Returns:
            Rate limit key string
        """

        return f"ratelimit:ip:{ip_address}:{endpoint}"

    @staticmethod
    def for_api_key(
        api_key_prefix: str,
        endpoint: str,
    ) -> str:
        """
        Generate rate limit key for API key.

        Args:
            api_key_prefix: Prefix of the API key
            endpoint: API endpoint name

        Returns:
            Rate limit key string
        """

        return f"ratelimit:apikey:{api_key_prefix}:{endpoint}"


# ==========================================================
# SINGLETON INSTANCES
# ==========================================================


security_utils = SecurityUtils()

password_manager = PasswordManager()

jwt_manager = JWTManager()

input_validator = InputValidator()

security_headers = SecurityHeaders()

rate_limit_key_gen = RateLimitKeyGenerator()


# ==========================================================
# INITIALIZATION LOG
# ==========================================================


log.info(
    "Security module initialized",
    jwt_algorithm=ALGORITHM,
    min_password_length=MIN_PASSWORD_LENGTH,
    max_image_size_mb=MAX_IMAGE_SIZE_MB,
)


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [
    "TokenData",
    "TokenResponse",
    "LoginRequest",
    "PasswordResetRequest",
    "PasswordResetConfirm",
    "ChangePasswordRequest",
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
    "validate_email",
    "validate_password_strength",
    "hash_password",
    "verify_password",
    "create_access_token",
    "verify_token",
]


# ==========================================================
# BACKWARD COMPATIBILITY FUNCTIONS
# ==========================================================


def validate_email(
    email: str,
) -> bool:
    """
    Backward compatibility function for email validation.

    Args:
        email: Email to validate

    Returns:
        True if valid
    """

    return InputValidator.validate_email(email)


def validate_password_strength(
    password: str,
) -> Tuple[bool, List[str]]:
    """
    Backward compatibility function for password validation.

    Args:
        password: Password to validate

    Returns:
        Tuple of (is_valid, issues)
    """

    return PasswordManager.validate_password_strength(password)


def hash_password(
    password: str,
) -> str:
    """
    Backward compatibility function for password hashing.

    Args:
        password: Plain text password

    Returns:
        Hashed password
    """

    return PasswordManager.hash_password(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Backward compatibility function for password verification.

    Args:
        plain_password: Plain text password
        hashed_password: Hashed password

    Returns:
        True if matches
    """

    return PasswordManager.verify_password(
        plain_password,
        hashed_password,
    )


def create_access_token(
    user_id: str,
    email: str,
) -> str:
    """
    Backward compatibility function for access token creation.

    Args:
        user_id: User identifier
        email: User email

    Returns:
        JWT access token
    """

    return JWTManager.create_access_token(
        user_id,
        email,
    )


def verify_token(
    token: str,
) -> Optional[Dict[str, Any]]:
    """
    Backward compatibility function for token verification.

    Args:
        token: JWT token

    Returns:
        Decoded payload or None
    """

    return JWTManager.decode_token(token)


# ==========================================================
# END OF FILE – security.py
# ==========================================================