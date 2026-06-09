# ==========================================================
# SCANIX AI
# SYSTEM 9 – GMAIL OAUTH AUTHENTICATION
# ELITE PRODUCTION GRADE – FINAL VERSION
# TOTAL LINES: 350
# ==========================================================


from __future__ import annotations


import os
from typing import Optional
from typing import Dict
from typing import Any
from datetime import datetime
from datetime import timedelta


import httpx
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import RedirectResponse
from jose import jwt
from jose import JWTError
from pydantic import EmailStr


from core.config import get_settings
from core.logging import logger


settings = get_settings()


# ==========================================================
# GOOGLE OAUTH CONSTANTS
# ==========================================================


GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


# ==========================================================
# GMAIL AUTH CLASS
# ==========================================================


class GmailAuth:
    """
    Google OAuth2 authentication handler for Gmail login.

    This class manages the complete OAuth2 flow:
    - Generating login URLs
    - Exchanging authorization codes for tokens
    - Fetching user information
    - Creating and verifying session tokens
    """

    def __init__(self) -> None:
        """
        Initialize Gmail authentication with credentials from .env.
        """

        self.client_id = getattr(
            settings,
            "GOOGLE_CLIENT_ID",
            None,
        )

        self.client_secret = getattr(
            settings,
            "GOOGLE_CLIENT_SECRET",
            None,
        )

        self.redirect_uri = getattr(
            settings,
            "GOOGLE_REDIRECT_URI",
            "http://localhost:8000/api/v1/user/auth/callback",
        )

        self.jwt_secret = getattr(
            settings,
            "JWT_SECRET",
            "scanix-secret-key-change-in-production",
        )

        if not self.client_id or not self.client_secret:

            logger.warning(
                "Google OAuth credentials not configured. "
                "Add GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET to .env"
            )

    def get_login_url(self) -> str:
        """
        Generate Google OAuth login URL.

        Returns:
            URL string for Google login page
        """

        if not self.client_id:

            raise HTTPException(
                status_code=500,
                detail="Google OAuth not configured. Add GOOGLE_CLIENT_ID to .env",
            )

        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "consent",
        }

        query = "&".join(
            f"{k}={v}"
            for k, v in params.items()
        )

        return f"{GOOGLE_AUTH_URL}?{query}"

    async def exchange_code(
        self,
        code: str,
    ) -> Dict[str, Any]:
        """
        Exchange authorization code for access and refresh tokens.

        Args:
            code: Authorization code from Google OAuth callback

        Returns:
            Dictionary containing access_token, refresh_token, etc.
        """

        if not self.client_id or not self.client_secret:

            raise HTTPException(
                status_code=500,
                detail="Google OAuth not configured",
            )

        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
        }

        try:

            async with httpx.AsyncClient(
                timeout=30.0,
            ) as client:

                response = await client.post(
                    GOOGLE_TOKEN_URL,
                    data=data,
                )

            if response.status_code != 200:

                logger.error(
                    f"Token exchange failed: {response.text}"
                )

                raise HTTPException(
                    status_code=400,
                    detail="Failed to exchange authorization code",
                )

            return response.json()

        except httpx.TimeoutException:

            logger.error("Token exchange timeout")

            raise HTTPException(
                status_code=504,
                detail="Google OAuth service timeout",
            )

        except Exception as e:

            logger.error(f"Token exchange error: {e}")

            raise HTTPException(
                status_code=500,
                detail=f"Authentication failed: {str(e)}",
            )

    async def get_user_info(
        self,
        access_token: str,
    ) -> Dict[str, Any]:
        """
        Fetch user information from Google.

        Args:
            access_token: Valid Google OAuth access token

        Returns:
            Dictionary with user email, name, picture, and ID
        """

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        try:

            async with httpx.AsyncClient(
                timeout=30.0,
            ) as client:

                response = await client.get(
                    GOOGLE_USERINFO_URL,
                    headers=headers,
                )

            if response.status_code != 200:

                logger.error(
                    f"User info failed: {response.text}"
                )

                raise HTTPException(
                    status_code=400,
                    detail="Failed to fetch user information",
                )

            return response.json()

        except httpx.TimeoutException:

            logger.error("User info timeout")

            raise HTTPException(
                status_code=504,
                detail="Google user info service timeout",
            )

        except Exception as e:

            logger.error(f"User info error: {e}")

            raise HTTPException(
                status_code=500,
                detail=f"Failed to get user info: {str(e)}",
            )

    def create_session_token(
        self,
        user_id: str,
        email: str,
    ) -> str:
        """
        Create JWT session token for authenticated user.

        Args:
            user_id: Internal user ID
            email: User's email address

        Returns:
            JWT token string
        """

        payload = {
            "user_id": user_id,
            "email": email,
            "exp": datetime.utcnow() + timedelta(days=7),
            "iat": datetime.utcnow(),
            "iss": "scanix-ai",
            "aud": "scanix-frontend",
        }

        token = jwt.encode(
            payload,
            self.jwt_secret,
            algorithm="HS256",
        )

        return token

    def verify_session_token(
        self,
        token: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Verify and decode JWT session token.

        Args:
            token: JWT token to verify

        Returns:
            Decoded payload if valid, None otherwise
        """

        try:

            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=["HS256"],
                audience="scanix-frontend",
                issuer="scanix-ai",
            )

            return payload

        except jwt.ExpiredSignatureError:

            logger.debug("Session token expired")

            return None

        except jwt.JWTError as e:

            logger.debug(f"Invalid session token: {e}")

            return None

    def create_logout_response(
        self,
        redirect_url: str = "http://localhost:3000",
    ) -> RedirectResponse:
        """
        Create logout response that clears the session cookie.

        Args:
            redirect_url: URL to redirect after logout

        Returns:
            RedirectResponse with cleared cookie
        """

        response = RedirectResponse(
            url=redirect_url,
        )

        response.delete_cookie(
            "session_token",
        )

        return response


# ==========================================================
# SINGLETON INSTANCE
# ==========================================================


gmail_auth = GmailAuth()


# ==========================================================
# DEPENDENCY FOR FASTAPI
# ==========================================================


def get_current_user(
    request: Request,
) -> Optional[str]:
    """
    FastAPI dependency to extract current user ID from session token.

    Args:
        request: FastAPI request object

    Returns:
        User ID if authenticated, None otherwise
    """

    token = request.cookies.get(
        "session_token",
    )

    if not token:

        return None

    payload = gmail_auth.verify_session_token(
        token,
    )

    if not payload:

        return None

    return payload.get("user_id")


# ==========================================================
# END OF FILE – auth.py
# ==========================================================