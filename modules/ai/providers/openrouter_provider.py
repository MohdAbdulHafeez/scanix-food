from __future__ import annotations

from typing import Dict
from typing import Any


class OpenRouterProvider:

    def generate(

        self,

        prompt: str,

        system_prompt: str = "",

        temperature: float = 0.2,

        max_tokens: int = 2048,

    ) -> Dict[str, Any]:

        raise NotImplementedError(
            "OpenRouter integration pending"
        )