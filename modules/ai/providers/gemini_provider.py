from __future__ import annotations

import json
import logging

from typing import Dict
from typing import Any

import google.genai as genai

from core.config import settings


log = logging.getLogger(__name__)


class GeminiProvider:

    def __init__(self):

        self.api_key = (
            settings.GEMINI_API_KEY
        )

        if not self.api_key:

            raise ValueError(
                "GEMINI_API_KEY missing"
            )

        genai.configure(
            api_key=self.api_key
        )

    # =====================================================
    # GENERATE
    # =====================================================

    def generate(

        self,

        prompt: str,

        system_prompt: str = "",

        temperature: float = 0.2,

        max_tokens: int = 2048,

        model: str | None = None,

    ) -> Dict[str, Any]:

        model_name = (

            model

            or

            settings.AI_PRIMARY_MODEL

        )

        try:

            full_prompt = (

                f"{system_prompt}\n\n"

                f"{prompt}"

            )

            llm = genai.GenerativeModel(
                model_name
            )

            response = llm.generate_content(

                full_prompt,

                generation_config={

                    "temperature":
                    temperature,

                    "max_output_tokens":
                    max_tokens,

                },

            )

            content = ""

            if (

                hasattr(
                    response,
                    "text"
                )

                and

                response.text

            ):

                content = (
                    response.text
                )

            return {

                "success":
                True,

                "provider":
                "gemini",

                "model":
                model_name,

                "content":
                content,

                "usage": {

                    "input_tokens":
                    None,

                    "output_tokens":
                    None,

                },

            }

        except Exception as e:

            log.exception(

                f"Gemini generation failed: {e}"

            )

            raise

    # =====================================================
    # GENERATE JSON
    # =====================================================

    def generate_json(

        self,

        prompt: str,

        system_prompt: str = "",

        temperature: float = 0.1,

        max_tokens: int = 4096,

        model: str | None = None,

    ) -> Dict[str, Any]:

        json_prompt = f"""

Return ONLY valid JSON.

No markdown.

No explanations.

No code fences.

{prompt}

"""

        response = self.generate(

            prompt=
            json_prompt,

            system_prompt=
            system_prompt,

            temperature=
            temperature,

            max_tokens=
            max_tokens,

            model=
            model,

        )

        content = (
            response.get(
                "content",
                "",
            )
        )

        try:

            parsed = json.loads(
                content
            )

            return {

                "success":
                True,

                "data":
                parsed,

                "provider":
                "gemini",

                "model":
                response.get(
                    "model"
                ),

            }

        except Exception:

            return {

                "success":
                False,

                "data": {},

                "raw":
                content,

                "provider":
                "gemini",

                "model":
                response.get(
                    "model"
                ),

            }

    # =====================================================
    # HEALTH CHECK
    # =====================================================

    def health_check(

        self,

    ) -> bool:

        try:

            response = self.generate(

                prompt=
                "Reply with OK",

                max_tokens=10,

            )

            return bool(

                response.get(
                    "content"
                )

            )

        except Exception:

            return False