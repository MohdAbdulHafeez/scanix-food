from __future__ import annotations

import os
import uuid
import asyncio
import tempfile
import logging

from pathlib import Path

from typing import Any
from typing import Dict
from typing import Optional

from faster_whisper import WhisperModel

import edge_tts

from .service import (
    nutritionist_service,
)


log = logging.getLogger(__name__)


# =========================================================
# VOICE PROFILES
# =========================================================

VOICE_PROFILES = {

    "female": {

        "voice":
        "en-US-JennyNeural",

        "gender":
        "female",

    },

    "male": {

        "voice":
        "en-US-GuyNeural",

        "gender":
        "male",

    },

    "coach": {

        "voice":
        "en-US-AriaNeural",

        "gender":
        "female",

    },

    "doctor": {

        "voice":
        "en-US-DavisNeural",

        "gender":
        "male",

    },

}


# =========================================================
# VOICE ENGINE
# =========================================================

class VoiceEngine:

    def __init__(self) -> None:

        self.whisper_model = None

        self.whisper_model_name = (

            os.getenv(

                "WHISPER_MODEL",

                "small.en",

            )

        )

        self.voice_name = (

            os.getenv(

                "VOICE_NAME",

                "en-US-JennyNeural",

            )

        )

        self.voice_timeout = int(

            os.getenv(

                "VOICE_TIMEOUT",

                "30",

            )

        )

    # =====================================================
    # WHISPER LAZY LOADER
    # =====================================================

    def get_whisper_model(

        self,

    ) -> WhisperModel:

        if self.whisper_model is None:

            log.info(

                f"Loading Whisper Model: "

                f"{self.whisper_model_name}"

            )

            self.whisper_model = (

                WhisperModel(

                    self.whisper_model_name,

                    device="cpu",

                    compute_type="int8",

                )

            )

        return self.whisper_model

    # =====================================================
    # SAFE HELPERS
    # =====================================================

    def _safe_string(

        self,

        value: Any,

    ) -> str:

        if value is None:

            return ""

        return str(value)

    def _file_exists(

        self,

        path: str,

    ) -> bool:

        if not path:

            return False

        return Path(path).exists()

    # =====================================================
    # AUDIO VALIDATION
    # =====================================================

    SUPPORTED_FORMATS = {

        ".wav",

        ".mp3",

        ".m4a",

        ".ogg",

        ".flac",

        ".aac",

    }

    def validate_audio(

        self,

        audio_path: str,

    ) -> Dict[str, Any]:

        if not audio_path:

            return {

                "valid": False,

                "error":
                "EMPTY_AUDIO_PATH",

            }

        if not self._file_exists(

            audio_path

        ):

            return {

                "valid": False,

                "error":
                "FILE_NOT_FOUND",

            }

        suffix = (

            Path(audio_path)
            .suffix
            .lower()

        )

        if suffix not in (

            self.SUPPORTED_FORMATS

        ):

            return {

                "valid": False,

                "error":
                "UNSUPPORTED_AUDIO_FORMAT",

            }

        return {

            "valid": True,

            "format":
            suffix,

        }

    # =====================================================
    # VOICE PROFILE MANAGEMENT
    # =====================================================

    def set_voice_profile(

        self,

        profile: str,

    ) -> bool:

        profile = (

            self._safe_string(
                profile
            )
            .lower()
        )

        if profile not in (

            VOICE_PROFILES

        ):

            return False

        self.voice_name = (

            VOICE_PROFILES

            [profile]

            ["voice"]

        )

        return True

    def get_voice_profile(

        self,

    ) -> Dict[str, Any]:

        return {

            "voice":
            self.voice_name,

            "available_profiles":

            list(

                VOICE_PROFILES
                .keys()

            ),

        }

    # =====================================================
    # TEMP FILES
    # =====================================================

    def create_audio_output_path(

        self,

    ) -> str:

        return os.path.join(

            tempfile.gettempdir(),

            f"{uuid.uuid4()}.mp3",

        )
    

        # =====================================================
    # SPEECH TO TEXT
    # =====================================================

    def speech_to_text(

        self,

        audio_path: str,

    ) -> Dict[str, Any]:

        validation = (

            self.validate_audio(

                audio_path

            )

        )

        if not validation.get(

            "valid",

            False,

        ):

            return {

                "success": False,

                "transcript": "",

                "language": "unknown",

                "confidence": 0,

                "error":

                validation.get(

                    "error"

                ),

            }

        try:

            model = (

                self.get_whisper_model()

            )

            segments, info = (

                model.transcribe(

                    audio_path,

                    beam_size=5,

                    vad_filter=True,

                )

            )

            transcript_parts = []

            segment_count = 0

            for segment in segments:

                text = (

                    self._safe_string(

                        segment.text

                    ).strip()

                )

                if text:

                    transcript_parts.append(

                        text

                    )

                    segment_count += 1

            transcript = " ".join(

                transcript_parts

            ).strip()

            probability = float(

                getattr(

                    info,

                    "language_probability",

                    0.90,

                )

            )

            confidence = int(

                probability * 100

            )

            confidence = max(

                0,

                min(

                    100,

                    confidence,

                ),

            )

            return {

                "success": True,

                "transcript":
                transcript,

                "language":

                getattr(

                    info,

                    "language",

                    "unknown",

                ),

                "confidence":
                confidence,

                "segments":
                segment_count,

            }

        except Exception as e:

            log.exception(

                f"Speech To Text Failed: {e}"

            )

            return {

                "success": False,

                "transcript": "",

                "language": "unknown",

                "confidence": 0,

                "error": str(e),

            }

    # =====================================================
    # INTERNAL TTS
    # =====================================================

    async def _generate_tts(

        self,

        text: str,

        output_path: str,

    ) -> None:

        communicate = (

            edge_tts.Communicate(

                text=text,

                voice=self.voice_name,

            )

        )

        await communicate.save(

            output_path

        )

    # =====================================================
    # TEXT TO SPEECH
    # =====================================================

    def text_to_speech(

        self,

        text: str,

    ) -> Dict[str, Any]:

        text = (

            self._safe_string(
                text
            ).strip()

        )

        if not text:

            return {

                "success": False,

                "audio_file": None,

                "error":
                "EMPTY_TEXT",

            }

        output_path = (

            self.create_audio_output_path()

        )

        try:

            asyncio.run(

                self._generate_tts(

                    text,

                    output_path,

                )

            )

            if not os.path.exists(

                output_path

            ):

                return {

                    "success": False,

                    "audio_file": None,

                    "error":
                    "TTS_OUTPUT_MISSING",

                }

            return {

                "success": True,

                "audio_file":
                output_path,

                "voice":
                self.voice_name,

            }

        except Exception as e:

            log.exception(

                f"TTS Failed: {e}"

            )

            return {

                "success": False,

                "audio_file": None,

                "error": str(e),

            }

    # =====================================================
    # TRANSCRIPT ANALYZER
    # =====================================================

    def analyze_transcript(

        self,

        transcript: str,

    ) -> Dict[str, Any]:

        transcript = (

            self._safe_string(
                transcript
            ).lower()

        )

        intent = "GENERAL"

        if any(

            keyword in transcript

            for keyword in [

                "meal plan",

                "diet plan",

                "weekly diet",

                "monthly diet",

            ]

        ):

            intent = "MEAL_PLANNING"

        elif any(

            keyword in transcript

            for keyword in [

                "can i eat",

                "is this healthy",

                "should i eat",

            ]

        ):

            intent = "PRODUCT_GUIDANCE"

        elif any(

            keyword in transcript

            for keyword in [

                "muscle gain",

                "weight loss",

                "fat loss",

            ]

        ):

            intent = "GOAL_COACHING"

        elif any(

            keyword in transcript

            for keyword in [

                "diabetes",

                "pcos",

                "thyroid",

                "hypertension",

            ]

        ):

            intent = "MEDICAL_NUTRITION"

        return {

            "intent":
            intent,

            "query":
            transcript,

        }

    # =====================================================
    # VOICE RESPONSE FORMATTER
    # =====================================================

    def build_voice_response(

        self,

        transcript_result:
        Dict[str, Any],

        nutrition_response:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        voice_response = (

            nutrition_response.get(

                "voice_response",

                {},

            )

        )

        return {

            "transcript":

            transcript_result.get(

                "transcript",

                "",

            ),

            "language":

            transcript_result.get(

                "language",

                "unknown",

            ),

            "stt_confidence":

            transcript_result.get(

                "confidence",

                0,

            ),

            "response_text":

            voice_response.get(

                "response_text",

                "",

            ),

            "voice_text":

            voice_response.get(

                "voice_text",

                "",

            ),

            "nutrition_confidence":

            nutrition_response.get(

                "confidence",

                0,

            ),

        }
    

        # =====================================================
    # NUTRITIONIST PIPELINE
    # =====================================================

    def run_nutritionist(

        self,

        transcript: str,

        profile: Dict[str, Any],

        product: Dict[str, Any],

        nutrition: Dict[str, Any],

        claims: list,

        ocr_text: str,

        serving_size: str,

        scan_quality: Dict[str, Any],

        ingredient_intelligence: Dict[str, Any],

        metabolic_intelligence: Dict[str, Any],

        consumer_intelligence: Dict[str, Any],

        body_intelligence: Dict[str, Any],

        scan_history: list,

        conversation_history: list,

    ) -> Dict[str, Any]:

        return (

            nutritionist_service
            .analyze(

                profile=
                profile,

                product=
                product,

                nutrition=
                nutrition,

                claims=
                claims,

                ocr_text=
                ocr_text,

                serving_size=
                serving_size,

                scan_quality=
                scan_quality,

                ingredient_intelligence=
                ingredient_intelligence,

                metabolic_intelligence=
                metabolic_intelligence,

                consumer_intelligence=
                consumer_intelligence,

                body_intelligence=
                body_intelligence,

                scan_history=
                scan_history,

                conversation_history=
                conversation_history,

                user_query=
                transcript,

            )

        )

    # =====================================================
    # VOICE CHAT
    # =====================================================

    def voice_chat(

        self,

        audio_path: str,

        profile: Dict[str, Any],

        product: Dict[str, Any],

        nutrition: Dict[str, Any],

        claims: list,

        ocr_text: str,

        serving_size: str,

        scan_quality: Dict[str, Any],

        ingredient_intelligence: Dict[str, Any],

        metabolic_intelligence: Dict[str, Any],

        consumer_intelligence: Dict[str, Any],

        body_intelligence: Dict[str, Any],

        scan_history: list,

        conversation_history: list,

    ) -> Dict[str, Any]:

        # =================================
        # STT
        # =================================

        transcript_result = (

            self.speech_to_text(

                audio_path

            )

        )

        if not transcript_result.get(

            "success",

            False,

        ):

            return {

                "success": False,

                "error":

                transcript_result.get(

                    "error"

                ),

                "transcript": "",

            }

        transcript = (

            transcript_result.get(

                "transcript",

                "",

            )

        )

        # =================================
        # INTENT
        # =================================

        intent_analysis = (

            self.analyze_transcript(

                transcript

            )

        )

        # =================================
        # NUTRITIONIST
        # =================================

        nutrition_response = (

            self.run_nutritionist(

                transcript=
                transcript,

                profile=
                profile,

                product=
                product,

                nutrition=
                nutrition,

                claims=
                claims,

                ocr_text=
                ocr_text,

                serving_size=
                serving_size,

                scan_quality=
                scan_quality,

                ingredient_intelligence=
                ingredient_intelligence,

                metabolic_intelligence=
                metabolic_intelligence,

                consumer_intelligence=
                consumer_intelligence,

                body_intelligence=
                body_intelligence,

                scan_history=
                scan_history,

                conversation_history=
                conversation_history,

            )

        )

        # =================================
        # RESPONSE EXTRACTION
        # =================================

        voice_response = (

            nutrition_response.get(

                "voice_response",

                {},

            )

        )

        voice_text = (

            voice_response.get(

                "voice_text",

                ""

            )

        )

        # =================================
        # TTS
        # =================================

        tts_result = (

            self.text_to_speech(

                voice_text

            )

        )

        # =================================
        # FINAL
        # =================================

        return {

            "success": True,

            "transcript":

            transcript,

            "intent":

            intent_analysis.get(

                "intent",

                "GENERAL",

            ),

            "language":

            transcript_result.get(

                "language",

                "unknown",

            ),

            "stt_confidence":

            transcript_result.get(

                "confidence",

                0,

            ),

            "nutrition_response":

            nutrition_response,

            "voice_response":

            voice_response,

            "audio_file":

            tts_result.get(

                "audio_file"

            ),

            "tts_success":

            tts_result.get(

                "success",

                False,

            ),

        }

    # =====================================================
    # PRODUCT VOICE ANALYSIS
    # =====================================================

    def analyze_product_by_voice(

        self,

        audio_path: str,

        **kwargs,

    ) -> Dict[str, Any]:

        return self.voice_chat(

            audio_path=
            audio_path,

            **kwargs,

        )

    # =====================================================
    # MEAL PLANNER VOICE
    # =====================================================

    def generate_meal_plan_by_voice(

        self,

        audio_path: str,

        **kwargs,

    ) -> Dict[str, Any]:

        return self.voice_chat(

            audio_path=
            audio_path,

            **kwargs,

        )

    # =====================================================
    # FOOD EXPLAINER VOICE
    # =====================================================

    def explain_food_by_voice(

        self,

        audio_path: str,

        **kwargs,

    ) -> Dict[str, Any]:

        return self.voice_chat(

            audio_path=
            audio_path,

            **kwargs,

        )

    # =====================================================
    # HEALTH COACH VOICE
    # =====================================================

    def health_coach_voice(

        self,

        audio_path: str,

        **kwargs,

    ) -> Dict[str, Any]:

        return self.voice_chat(

            audio_path=
            audio_path,

            **kwargs,

        )
    

        # =====================================================
    # AUDIO CLEANUP
    # =====================================================

    def cleanup_audio(

        self,

        audio_path: Optional[str],

    ) -> bool:

        try:

            if (

                audio_path

                and

                os.path.exists(
                    audio_path
                )

            ):

                os.remove(
                    audio_path
                )

                return True

        except Exception as e:

            log.warning(

                f"Audio Cleanup Failed: {e}"

            )

        return False

    # =====================================================
    # MEMORY HOOK
    # =====================================================

    def build_memory_record(

        self,

        transcript: str,

        nutrition_response:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        return {

            "query":
            transcript,

            "timestamp":

            str(
                uuid.uuid4()
            ),

            "goal":

            nutrition_response
            .get(
                "summary",
                {},
            )
            .get(
                "goal",
                "GENERAL_HEALTH",
            ),

            "confidence":

            nutrition_response.get(
                "confidence",
                0,
            ),

        }

    # =====================================================
    # VOICE METADATA
    # =====================================================

    def build_voice_metadata(

        self,

        transcript_result:
        Dict[str, Any],

        nutrition_response:
        Dict[str, Any],

        tts_result:
        Dict[str, Any],

    ) -> Dict[str, Any]:

        return {

            "stt_language":

            transcript_result.get(
                "language",
                "unknown",
            ),

            "stt_confidence":

            transcript_result.get(
                "confidence",
                0,
            ),

            "nutrition_confidence":

            nutrition_response.get(
                "confidence",
                0,
            ),

            "voice":

            self.voice_name,

            "tts_success":

            tts_result.get(
                "success",
                False,
            ),

        }

    # =====================================================
    # FULL VOICE SESSION
    # =====================================================

    def voice_session(

        self,

        audio_path: str,

        profile: Dict[str, Any],

        product: Dict[str, Any],

        nutrition: Dict[str, Any],

        claims: list,

        ocr_text: str,

        serving_size: str,

        scan_quality: Dict[str, Any],

        ingredient_intelligence:
        Dict[str, Any],

        metabolic_intelligence:
        Dict[str, Any],

        consumer_intelligence:
        Dict[str, Any],

        body_intelligence:
        Dict[str, Any],

        scan_history: list,

        conversation_history: list,

        cleanup_audio: bool = False,

    ) -> Dict[str, Any]:

        result = (

            self.voice_chat(

                audio_path=
                audio_path,

                profile=
                profile,

                product=
                product,

                nutrition=
                nutrition,

                claims=
                claims,

                ocr_text=
                ocr_text,

                serving_size=
                serving_size,

                scan_quality=
                scan_quality,

                ingredient_intelligence=
                ingredient_intelligence,

                metabolic_intelligence=
                metabolic_intelligence,

                consumer_intelligence=
                consumer_intelligence,

                body_intelligence=
                body_intelligence,

                scan_history=
                scan_history,

                conversation_history=
                conversation_history,

            )

        )

        if not result.get(

            "success",

            False,

        ):

            return result

        transcript = (

            result.get(
                "transcript",
                "",
            )

        )

        nutrition_response = (

            result.get(
                "nutrition_response",
                {},
            )

        )

        memory_record = (

            self.build_memory_record(

                transcript,

                nutrition_response,

            )

        )

        metadata = (

            self.build_voice_metadata(

                {

                    "language":

                    result.get(
                        "language",
                        "unknown",
                    ),

                    "confidence":

                    result.get(
                        "stt_confidence",
                        0,
                    ),

                },

                nutrition_response,

                {

                    "success":

                    result.get(
                        "tts_success",
                        False,
                    ),

                },

            )

        )

        result["memory_record"] = (
            memory_record
        )

        result["metadata"] = (
            metadata
        )

        if cleanup_audio:

            self.cleanup_audio(
                audio_path
            )

        return result

    # =====================================================
    # HEALTH CHECK
    # =====================================================

    def health_check(

        self,

    ) -> Dict[str, Any]:

        return {

            "voice_engine":
            "healthy",

            "whisper_model":

            self.whisper_model_name,

            "voice":

            self.voice_name,

            "tts_provider":
            "edge_tts",

            "stt_provider":
            "faster_whisper",

        }


voice_engine = (
    VoiceEngine()
)