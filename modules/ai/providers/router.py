from __future__ import annotations

from typing import Dict
from typing import Any
from typing import List

from core.config import settings

from .gemini_provider import (
    GeminiProvider,
)

from .groq_provider import (
    GroqProvider,
)

from .openrouter_provider import (
    OpenRouterProvider,
)


class ProviderRouter:

    def __init__(self):

        self.providers = {

            "gemini":
            GeminiProvider(),

            "groq":
            GroqProvider(),

            "openrouter":
            OpenRouterProvider(),

        }

        self.provider_order = [

            provider.strip()

            for provider in

            settings.AI_PROVIDER_ORDER.split(
                ","
            )

        ]

    def generate(

        self,

        prompt: str,

        system_prompt: str = "",

        temperature: float = 0.2,

        max_tokens: int = 2048,

    ) -> Dict[str, Any]:

        errors = []

        for provider_name in (

            self.provider_order

        ):

            provider = (

                self.providers.get(
                    provider_name
                )

            )

            if not provider:

                continue

            try:

                response = (

                    provider.generate(

                        prompt=
                        prompt,

                        system_prompt=
                        system_prompt,

                        temperature=
                        temperature,

                        max_tokens=
                        max_tokens,

                    )

                )

                response[
                    "provider"
                ] = provider_name

                return response

            except Exception as e:

                errors.append(

                    {

                        "provider":
                        provider_name,

                        "error":
                        str(e),

                    }

                )

                continue

        raise RuntimeError(

            f"All providers failed: {errors}"

        )


provider_router = (
    ProviderRouter()
)