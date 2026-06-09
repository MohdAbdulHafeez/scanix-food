# ==========================================================
# SCANIX AI
# SYSTEM 1 - SCAN ENGINE
# PART A1 (ELITE UPGRADED V6 - FINAL FREEZE)
# ==========================================================


import os
import re
import uuid
import json
import time
import gc
import hashlib
import tempfile
import asyncio

from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import cv2
import easyocr
import httpx

from cachetools import TTLCache
from fastapi import UploadFile, HTTPException
from pyzbar.pyzbar import decode
from rapidfuzz import fuzz
from tenacity import retry, stop_after_attempt, wait_exponential

from core.logging import log

from modules.scan.constants import (
    ADDITIVES,
    ALLERGENS,
    ALLERGEN_ALIASES,
    ARTIFICIAL_INGREDIENTS,
    BRANDS,
    CATEGORY_KEYWORDS,
    MARKETING_CLAIMS,
    NEGATIVE_INGREDIENTS,
    POSITIVE_INGREDIENTS,
    PRESERVATIVES,
    PRODUCT_IMAGES,
    HIDDEN_SUGARS,
    RISK_KEYWORDS,
    SECTION_KEYWORDS,
    OCR_CORRECTIONS,
)


from modules.consumer.service import (
    ConsumerIntelligenceService
)

from modules.ai.food_explainer.service import (
    food_explainer_service,
)

from modules.ai.nutritionist.service import (
    nutritionist_service,
)

from modules.digital_twin.service import (
    digital_twin_service,
)

from modules.smart_food import (
    smart_swap_service,
    SwapRequest,
    SortByOption,
)


# ==========================================================
# CONSTANTS
# ==========================================================

DEFAULT_OCR_TIMEOUT: float = 30.0
DEFAULT_OFF_TIMEOUT: float = 10.0
MAX_SCAN_HISTORY: int = 100
MAX_IMAGE_SIZE_MB: int = 10
OCR_CONFIDENCE_THRESHOLD: float = 0.70

# HTTP Connection Pool
_http_client: Optional[httpx.AsyncClient] = None

async def get_http_client() -> httpx.AsyncClient:
    global _http_client
    if _http_client is None or _http_client.is_closed:
        _http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(DEFAULT_OFF_TIMEOUT),
            limits=httpx.Limits(max_keepalive_connections=20, max_connections=100),
        )
    return _http_client


# ==========================================================
# GLOBAL MEMORY (PERSISTED)
# ==========================================================


SCAN_HISTORY_FILE = "scanix_scan_history.json"

FAVORITES_FILE = "scanix_favorites.json"

SCAN_HISTORY: List[Dict[str, Any]] = []

FAVORITES: List[Dict[str, Any]] = []


# ==========================================================
# UTILITIES
# ==========================================================


class ScanUtils:

    @staticmethod
    def generate_scan_id() -> str:

        return f"scan_{uuid.uuid4().hex}"

    @staticmethod
    def current_timestamp() -> str:

        return datetime.utcnow().isoformat()

    @staticmethod
    def clean_text(
        text: str,
    ) -> str:

        text = text.lower()

        text = re.sub(
            r"[^a-z0-9\s]",
            " ",
            text,
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    @staticmethod
    def create_hash(
        text: str,
    ) -> str:

        return hashlib.sha256(
            text.encode()
        ).hexdigest()

    @staticmethod
    def calculate_average(
        values: List[float],
    ) -> float:

        if not values:

            return 0.0

        return round(
            sum(values) / len(values),
            2,
        )


# ==========================================================
# MEMORY ENGINE
# ==========================================================


class MemoryEngine:

    @staticmethod
    def _load_data():

        global SCAN_HISTORY
        global FAVORITES

        try:

            if os.path.exists(SCAN_HISTORY_FILE):

                with open(SCAN_HISTORY_FILE, "r") as f:

                    SCAN_HISTORY = json.load(f)

        except Exception:

            SCAN_HISTORY = []

        try:

            if os.path.exists(FAVORITES_FILE):

                with open(FAVORITES_FILE, "r") as f:

                    FAVORITES = json.load(f)

        except Exception:

            FAVORITES = []

    @staticmethod
    def _save_history():

        try:

            with open(SCAN_HISTORY_FILE, "w") as f:

                json.dump(SCAN_HISTORY, f)

        except Exception:

            pass

    @staticmethod
    def _save_favorites():

        try:

            with open(FAVORITES_FILE, "w") as f:

                json.dump(FAVORITES, f)

        except Exception:

            pass

    @staticmethod
    def save_scan(
        scan_data: Dict[str, Any],
    ) -> bool:

        try:

            SCAN_HISTORY.insert(
                0,
                scan_data,
            )

            SCAN_HISTORY[:] = (
                SCAN_HISTORY[:MAX_SCAN_HISTORY]
            )

            MemoryEngine._save_history()

            return True

        except Exception as e:

            log.exception(
                f"Failed to save scan: {e}"
            )

            return False

    @staticmethod
    def get_history() -> List[Dict]:

        return SCAN_HISTORY

    @staticmethod
    def clear_history() -> bool:

        try:

            SCAN_HISTORY.clear()

            MemoryEngine._save_history()

            return True

        except Exception:

            return False

    @staticmethod
    def add_favorite(
        product: Dict[str, Any],
    ) -> bool:

        try:

            brand = product.get(
                "brand"
            )

            if not brand:

                return False

            exists = any(

                item.get("brand") == brand

                for item in FAVORITES

            )

            if not exists:

                FAVORITES.append(
                    product
                )

                MemoryEngine._save_favorites()

            return True

        except Exception as e:

            log.exception(
                f"Favorite error: {e}"
            )

            return False

    @staticmethod
    def get_favorites() -> List[Dict]:

        return FAVORITES


# Initialize memory on import
MemoryEngine._load_data()


# ==========================================================
# OCR CORRECTION ENGINE
# ==========================================================


class OCRCorrectionEngine:

    def apply_corrections(
        self,
        text: str,
    ) -> str:

        corrected_text = text

        for wrong, right in (
            OCR_CORRECTIONS.items()
        ):

            pattern = re.compile(
                rf"\b{re.escape(wrong)}\b",
                re.IGNORECASE,
            )

            corrected_text = pattern.sub(
                right,
                corrected_text,
            )

        corrected_text = re.sub(
            r"\s+",
            " ",
            corrected_text,
        )

        return corrected_text.strip()


# ==========================================================
# OCR ENGINE
# ==========================================================


ocr_correction_engine = OCRCorrectionEngine()


class OCREngine:

    def __init__(self):

        self._reader = None
        self._last_used = None

        # Support for Indian languages
        self.supported_languages = [
            "en",      # English
            "hi",      # Hindi
            "ta",      # Tamil
            "te",      # Telugu
            "kn",      # Kannada
            "ml",      # Malayalam
            "mr",      # Marathi
            "bn",      # Bengali
            "gu",      # Gujarati
            "pa",      # Punjabi
            "or",      # Odia
        ]

    def _get_languages(self) -> List[str]:
        """
        Detect languages based on text pattern or default to English + Hindi.
        """
        # Always include English as fallback
        return ["en", "hi"]  # English + Hindi for best coverage

    @property
    def reader(self):

        if self._reader is None:

            gc.collect()

            self._reader = easyocr.Reader(
                self._get_languages(),
                gpu=False,
                verbose=False,
                model_storage_directory=None,
                download_enabled=True,
            )

            self._last_used = time.time()

        return self._reader

    def cleanup(self):

        if self._reader:

            self._reader = None

    def cleanup_if_idle(self) -> None:
        if self._reader and self._last_used:
            if time.time() - self._last_used > 300:  # 5 minutes
                self._reader = None
                self._last_used = None
                gc.collect()
                log.debug("OCR reader cleaned up due to idle timeout")

    def _get_empty_ocr_result(self) -> Dict[str, Any]:
        return {
            "raw_text": "",
            "text": "",
            "blocks": [],
            "confidence": [],
            "average_confidence": 0,
            "temp_image_path": None,
        }

    async def extract_text(
        self,
        file: UploadFile,
    ) -> Dict[str, Any]:

        temp_path = None

        try:

            with tempfile.NamedTemporaryFile(

                delete=False,

                suffix=".jpg",

            ) as temp:

                content = await file.read()

                temp.write(content)

                temp_path = temp.name

            await file.seek(0)

            # Run OCR with timeout
            try:
                results = await asyncio.wait_for(
                    asyncio.to_thread(self.reader.readtext, temp_path),
                    timeout=DEFAULT_OCR_TIMEOUT
                )
            except asyncio.TimeoutError:
                log.error(f"OCR timeout after {DEFAULT_OCR_TIMEOUT} seconds")
                return self._get_empty_ocr_result()

            text_blocks = []

            confidence_values = []

            extracted_text = []

            for result in results:

                text_blocks.append(
                    result[1]
                )

                confidence_values.append(

                    round(
                        result[2],
                        2,
                    )

                )

                extracted_text.append(
                    result[1]
                )

            raw_merged_text = (
                "\n".join(
                    extracted_text
                )
            )

            corrected_text = (
                ocr_correction_engine.apply_corrections(
                    raw_merged_text
                )
            )

            return {

                "raw_text":
                raw_merged_text,

                "text":
                corrected_text,

                "blocks":
                text_blocks,

                "confidence":
                confidence_values,

                "average_confidence":
                ScanUtils.calculate_average(
                    confidence_values
                ),

                "temp_image_path":
                temp_path,

            }

        except Exception as e:

            log.exception(
                f"OCR failed: {e}"
            )

            return self._get_empty_ocr_result()

    def calculate_density_score(
        self,
        text: str,
    ) -> int:

        words = len(
            text.split()
        )

        score = min(
            words * 2,
            100,
        )

        return score

    def calculate_readability_score(
        self,
        text: str,
    ) -> int:

        if not text:

            return 0

        alpha_chars = sum(

            1

            for c in text

            if c.isalpha()

        )

        score = min(

            alpha_chars // 3,

            100,

        )

        return score

    def calculate_ocr_quality(
        self,
        confidence: List[float],
    ) -> int:

        if not confidence:

            return 0

        avg = (
            sum(confidence)
            / len(confidence)
        )

        return int(
            avg * 100
        )


# ==========================================================
# BARCODE ENGINE
# ==========================================================


class BarcodeEngine:

    def decode_barcode_from_image(
        self,
        image_path: str,
    ) -> Optional[str]:

        try:

            if not image_path:
                return None

            image = cv2.imread(image_path)

            if image is None:
                return None

            # Try original image
            decoded = decode(image)

            if decoded:
                return decoded[0].data.decode()

            # Try grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            decoded = decode(gray)

            if decoded:
                return decoded[0].data.decode()

            # Try thresholded
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            decoded = decode(thresh)

            if decoded:
                return decoded[0].data.decode()

        except Exception as e:
            log.debug(f"Barcode decode failed: {e}")

        return None

    def extract_barcode(
        self,
        text: str,
    ) -> Optional[str]:

        if not text:

            return None

        candidates = re.findall(
            r"\b\d{8,14}\b",
            text,
        )

        ignore_prefixes = [
            "lic",
            "license",
            "fssai",
            "tel",
        ]

        normalized = text.lower()

        lines = normalized.split("\n")

        for candidate in candidates:

            if not self.validate_barcode(candidate):

                continue

            for line in lines:

                if candidate in line:

                    line_lower = line.lower()

                    if any(
                        prefix in line_lower
                        for prefix in ignore_prefixes
                    ):

                        continue

                    if any(
                        keyword in line_lower
                        for keyword in [
                            "barcode",
                            "ean",
                            "upc",
                            "scan",
                        ]
                    ):

                        return candidate

        for candidate in candidates:

            if self.validate_barcode(candidate):

                related_line = ""

                for line in lines:

                    if candidate in line:

                        related_line = line.lower()

                        break

                if any(
                    prefix in related_line
                    for prefix in ignore_prefixes
                ):

                    continue

                return candidate

        return None

    def validate_ean8(
        self,
        barcode: str,
    ) -> bool:

        if len(barcode) != 8:

            return False

        return self._mod10_checksum(barcode)

    def validate_ean13(
        self,
        barcode: str,
    ) -> bool:

        if len(barcode) != 13:

            return False

        return self._mod10_checksum(barcode)

    def validate_upc(
        self,
        barcode: str,
    ) -> bool:

        if len(barcode) != 12:

            return False

        return self._mod10_checksum(barcode)

    def validate_gtin14(
        self,
        barcode: str,
    ) -> bool:

        if len(barcode) != 14:

            return False

        return self._mod10_checksum(barcode)

    def _mod10_checksum(
        self,
        barcode: str,
    ) -> bool:

        digits = [
            int(x)
            for x in barcode
        ]

        checksum = digits.pop()

        digits.reverse()

        total = sum(

            d * 3

            if i % 2 == 0

            else d

            for i, d in enumerate(digits)

        )

        expected_checksum = (
            (10 - (total % 10))
            % 10
        )

        return expected_checksum == checksum

    def validate_barcode(
        self,
        barcode: Optional[str],
    ) -> bool:

        if not barcode:

            return False

        if not barcode.isdigit():

            return False

        length = len(barcode)

        if length == 8:

            return self.validate_ean8(barcode)

        if length == 12:

            return self.validate_upc(barcode)

        if length == 13:

            return self.validate_ean13(barcode)

        if length == 14:

            return self.validate_gtin14(barcode)

        return False

    def barcode_confidence(
        self,
        barcode: Optional[str],
    ) -> int:

        if not barcode:

            return 0

        if self.validate_barcode(
            barcode
        ):

            return 95

        return 25


# ==========================================================
# PRODUCT ENGINE
# ==========================================================


class ProductEngine:

    def detect_brand(
        self,
        text: str,
    ) -> Optional[str]:

        normalized_text = (
            text.lower()
        )

        best_brand = None

        highest_score = 0

        for brand, aliases in (
            BRANDS.items()
        ):

            for alias in aliases:

                score = (

                    fuzz.partial_ratio(
                        alias.lower(),
                        normalized_text,
                    )

                )

                if score > 90:

                    if score > highest_score:

                        highest_score = score

                        best_brand = brand

        return best_brand

    def detect_category(
        self,
        text: str,
    ) -> Optional[str]:

        normalized_text = (
            ScanUtils.clean_text(
                text
            )
        )

        scores = {}

        for (
            category,
            data,
        ) in CATEGORY_KEYWORDS.items():

            score = 0

            if isinstance(data, dict):

                keywords = data.get("keywords", [])

                weight = data.get("weight", 1)

            else:

                keywords = data

                weight = 1

            for keyword in keywords:

                if (
                    keyword.lower()
                    in normalized_text
                ):

                    score += weight

            scores[
                category
            ] = score

        if not scores:

            return None

        best_category = max(
            scores,
            key=scores.get,
        )

        if (
            scores[
                best_category
            ]
            == 0
        ):

            return None

        return best_category

    def detect_product_name(
        self,
        text: str,
        brand: Optional[str],
        external_data: Optional[Dict] = None,
    ) -> Optional[str]:

        off_name = None

        if external_data:

            off_name = external_data.get(
                "product_name"
            )

        lines = [

            x.strip()

            for x in text.splitlines()

            if x.strip()

        ]

        candidates = []

        for line in lines[:50]:

            l = line.lower()

            if any(

                bad in l

                for bad in [

                    "ingredient",
                    "nutrition",
                    "fssai",
                    "manufactured",
                    "marketed",
                    "customer care",
                    "consumer care",
                    "email",
                    "phone",
                    "barcode",
                    "net qty",
                    "mrp",
                    "batch",
                    "nutritional information",
                    "nutrition facts",
                    "serving size",
                    "per serving",
                    "net weight",
                    "net quantity",

                ]

            ):

                continue

            if len(line) > 60:

                continue

            score = 0

            if brand and brand.lower() in l:

                score += 100

            if any(

                x in l

                for x in [

                    "cream",
                    "onion",
                    "masala",
                    "cheese",
                    "tomato",
                    "salted",
                    "classic",
                    "spicy",
                    "flavour",
                    "flavor",

                ]

            ):

                score += 30

            score += len(line)

            candidates.append(
                (score, line)
            )

        candidates.sort(
            reverse=True
        )

        ocr_name = (
            candidates[0][1] if candidates else None
        )

        if off_name:

            if brand and brand.lower() in off_name.lower():

                return off_name

        return ocr_name or off_name or brand

    def get_product_image(
        self,
        brand: Optional[str],
        barcode: Optional[str] = None,
        off_image: Optional[str] = None,
    ) -> str:

        if off_image:

            return off_image

        if brand and brand in PRODUCT_IMAGES:

            return PRODUCT_IMAGES[brand]

        return (
            "https://images.openfoodfacts.org/"
        )

    def calculate_identity_confidence(
        self,
        brand: Optional[str],
        category: Optional[str],
        barcode: Optional[str],
    ) -> int:

        score = 0

        if brand:

            score += 40

        if category:

            score += 25

        if barcode:

            score += 35

        if brand and barcode:

            score += 10

        return min(
            score,
            100,
        )


# ==========================================================
# PRODUCT FUSION ENGINE
# ==========================================================


class ProductFusionEngine:

    def build_identity(
        self,
        text: str,
    ) -> Dict[str, Any]:

        brand = (
            product_engine.detect_brand(
                text
            )
        )

        category = (
            product_engine.detect_category(
                text
            )
        )

        barcode = (
            barcode_engine.extract_barcode(
                text
            )
        )

        product_name = (
            product_engine.detect_product_name(
                text,
                brand,
            )
        )

        confidence = (

            product_engine.calculate_identity_confidence(

                brand,

                category,

                barcode,

            )

        )

        matched_by = []

        if brand:

            matched_by.append(
                "ocr_brand"
            )

        if category:

            matched_by.append(
                "ocr_category"
            )

        if barcode:

            matched_by.append(
                "barcode"
            )

        return {

            "product_name":
            product_name,

            "brand":
            brand,

            "category":
            category,

            "barcode":
            barcode,

            "image_url":
            product_engine.get_product_image(
                brand,
                barcode,
            ),

            "identity_confidence":
            confidence,

            "matched_by":
            matched_by,

        }


# ==========================================================
# IMAGE QUALITY ENGINE
# ==========================================================


class ImageQualityEngine:

    def calculate_blur_score(
        self,
        gray: Any,
    ) -> int:

        variance = (
            cv2.Laplacian(
                gray,
                cv2.CV_64F,
            ).var()
        )

        score = min(

            int(
                variance
            ),

            100,

        )

        return score

    def calculate_brightness_score(
        self,
        gray: Any,
    ) -> int:

        mean_val = cv2.mean(gray)[0]

        diff = abs(127 - mean_val)

        score = max(

            0,

            100 - int(diff * 0.78),

        )

        return score

    def calculate_contrast_score(
        self,
        gray: Any,
    ) -> int:

        std_val = gray.std()

        score = min(

            100,

            int(std_val * 2),

        )

        return score

    def calculate_glare_score(
        self,
        gray: Any,
    ) -> int:

        mask = gray > 240

        glare_ratio = mask.sum() / mask.size

        score = max(

            0,

            100 - int(glare_ratio * 1000),

        )

        return score

    def calculate_image_quality(
        self,
        image_path: str,
    ) -> int:

        try:

            if not image_path:

                return 50

            image = cv2.imread(
                image_path
            )

            if image is None:

                return 50

            gray = (
                cv2.cvtColor(
                    image,
                    cv2.COLOR_BGR2GRAY,
                )
            )

            blur_score = (
                self.calculate_blur_score(
                    gray
                )
            )

            brightness_score = (
                self.calculate_brightness_score(
                    gray
                )
            )

            contrast_score = (
                self.calculate_contrast_score(
                    gray
                )
            )

            glare_score = (
                self.calculate_glare_score(
                    gray
                )
            )

            overall_quality = (
                blur_score * 0.4
                + brightness_score * 0.2
                + contrast_score * 0.2
                + glare_score * 0.2
            )

            return max(

                min(
                    int(overall_quality),
                    100,
                ),

                0,

            )

        except Exception:

            return 50


# ==========================================================
# OPEN FOOD FACTS ENGINE
# ==========================================================


class OpenFoodFactsEngine:

    BASE_URL = (
        "https://world.openfoodfacts.org/api/v2/product"
    )

    def __init__(self):

        self._cache = TTLCache(
            maxsize=5000,
            ttl=86400,
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        reraise=False
    )
    async def lookup_product(
        self,
        barcode: Optional[str],
        product_name: Optional[str] = None,
        brand: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:

        try:

            if not barcode:

                return None

            if barcode in self._cache:

                return self._cache[barcode]

            url = (
                f"{self.BASE_URL}/{barcode}.json"
            )

            client = await get_http_client()
            response = await client.get(url)

            if response.status_code != 200:

                return None

            data = response.json()

            if data.get("status") != 1:

                return None

            product = data.get(
                "product",
                {},
            )

            raw_brand = product.get(
                "brands"
            )

            normalized_brand = raw_brand

            if raw_brand:

                normalized_brand = (
                    product_engine.detect_brand(
                        raw_brand
                    )
                    or raw_brand
                )

            result = {

                "barcode":
                barcode,

                "off_code":
                str(
                    product.get("code", "")
                ),

                "product_name":
                product.get(
                    "product_name"
                ),

                "brand":
                normalized_brand,

                "image_url":
                product.get(
                    "image_url"
                ),

                "ingredients_text":
                product.get(
                    "ingredients_text"
                ),

                "nutriscore":
                product.get(
                    "nutriscore_grade"
                ),

                "nova":
                product.get(
                    "nova_group"
                ),

                "categories":
                product.get(
                    "categories"
                ),

                "source":
                "openfoodfacts",

            }

            self._cache[barcode] = result

            return result

        except Exception as e:

            log.exception(
                f"OpenFoodFacts lookup failed: {e}"
            )

            return None


# ==========================================================
# TRUST ENGINE
# ==========================================================


class TrustEngine:

    def calculate_source_reliability(
        self,
        external_data: Optional[Dict],
    ) -> int:

        if external_data:

            return 95

        return 40

    def calculate_data_confidence(
        self,
        ocr_confidence: float,
        barcode_verified: bool,
    ) -> int:

        score = int(
            ocr_confidence * 100
        )

        if barcode_verified:

            score += 10

        return min(
            score,
            100,
        )

    def calculate_evidence_strength(
        self,
        matched_by: List[str],
    ) -> int:

        score = len(
            matched_by
        ) * 30

        return min(
            score,
            100,
        )

    def calculate_trust_score(
        self,
        source_reliability: int,
        data_confidence: int,
        evidence_strength: int,
    ) -> int:

        score = (
            source_reliability * 0.20
            + data_confidence * 0.55
            + evidence_strength * 0.25
        )

        return max(
            25,
            min(
                int(score),
                100,
            ),
        )


# ==========================================================
# VERIFICATION ENGINE
# ==========================================================


class VerificationEngine:

    def barcode_verified(
        self,
        barcode: Optional[str],
    ) -> bool:

        return (
            barcode_engine.validate_barcode(
                barcode
            )
        )

    def ocr_verified(
        self,
        average_confidence: float,
    ) -> bool:

        return (
            average_confidence >= OCR_CONFIDENCE_THRESHOLD
        )

    def source_verified(
        self,
        external_data: Optional[Dict],
    ) -> bool:

        return external_data is not None

    def verification_level(
        self,
        barcode_verified: bool,
        ocr_verified: bool,
        source_verified: bool,
    ) -> str:

        score = 0

        if barcode_verified:

            score += 40

        if ocr_verified:

            score += 40

        if source_verified:

            score += 30

        if score >= 80:

            return "HIGH"

        if score >= 40:

            return "MEDIUM"

        return "LOW"


# ==========================================================
# PRODUCT ENRICHMENT ENGINE
# ==========================================================


class ProductEnrichmentEngine:

    def enrich_product(
        self,
        identity: Dict[str, Any],
        external_data: Optional[Dict],
    ) -> Dict[str, Any]:

        if not external_data:

            return identity

        off_barcode = str(

            external_data.get(
                "off_code",
                ""
            )

        )

        scanned_barcode = str(

            identity.get(
                "barcode",
                ""
            )

        )

        verified_image = None

        if (

            off_barcode

            and

            scanned_barcode

            and

            off_barcode == scanned_barcode

        ):

            verified_image = external_data.get(
                "image_url"
            )

        image_url = product_engine.get_product_image(

            identity.get("brand"),

            scanned_barcode,

            verified_image,

        )

        return {

            "product_name":

            external_data.get(
                "product_name"
            )

            or

            identity.get(
                "product_name"
            ),

            "brand":

            external_data.get(
                "brand"
            )

            or

            identity.get(
                "brand"
            ),

            "category":

            identity.get(
                "category"
            )

            or

            external_data.get(
                "categories"
            ),

            "barcode":

            identity.get(
                "barcode"
            ),

            "image_url":

            image_url,

            "identity_confidence":

            min(

                identity.get(
                    "identity_confidence",
                    0,
                )
                + 15,

                100,

            ),

            "matched_by":

            identity.get(
                "matched_by",
                [],
            )
            +
            [
                "openfoodfacts"
            ],

            "nutriscore":

            external_data.get(
                "nutriscore"
            ),

            "nova":

            external_data.get(
                "nova"
            ),

        }


# ==========================================================
# PRODUCT FUSION V2
# ==========================================================


class ProductFusionV2:

    async def fuse(
        self,
        text: str,
        average_confidence: float,
        image_barcode: Optional[str] = None,
    ) -> Dict[str, Any]:

        identity = (

            fusion_engine.build_identity(
                text
            )

        )

        if image_barcode:

            identity["barcode"] = image_barcode

            matched = identity.get(
                "matched_by",
                []
            )

            if "barcode" not in matched:

                matched.append(
                    "barcode"
                )

            identity["matched_by"] = matched

        barcode = identity.get(
            "barcode"
        )

        external_barcode = barcode

        external_data = (

            await openfoodfacts_engine.lookup_product(
                barcode,
                identity.get("product_name"),
                identity.get("brand"),
            )

        )

        if external_data:

            off_name = external_data.get(
                "product_name"
            )

            if not off_name:

                external_data = None

        enriched = (

            enrichment_engine.enrich_product(

                identity,

                external_data,

            )

        )

        if not external_data:

            enriched["identity_confidence"] = max(
                40,
                enriched.get(
                    "identity_confidence",
                    0
                ) - 10
            )

        barcode_ok = (

            verification_engine.barcode_verified(
                barcode
            )

        )

        ocr_ok = (

            verification_engine.ocr_verified(
                average_confidence
            )

        )

        source_ok = (

            verification_engine.source_verified(
                external_data
            )

        )

        source_reliability = (

            trust_engine.calculate_source_reliability(
                external_data
            )

        )

        data_confidence = (

            trust_engine.calculate_data_confidence(

                average_confidence,

                barcode_ok,

            )

        )

        evidence_strength = (

            trust_engine.calculate_evidence_strength(

                enriched.get(
                    "matched_by",
                    [],
                )

            )

        )

        trust_score = (

            trust_engine.calculate_trust_score(

                source_reliability,

                data_confidence,

                evidence_strength,

            )

        )

        return {

            "product":
            enriched,

            "trust": {

                "trust_score":
                trust_score,

                "source_reliability":
                source_reliability,

                "evidence_strength":
                evidence_strength,

                "data_confidence":
                data_confidence,

            },

            "verification": {

                "barcode_verified":
                bool(barcode_ok),

                "ocr_verified":
                bool(ocr_ok),

                "source_verified":
                bool(source_ok),

                "verification_level":

                verification_engine.verification_level(

                    barcode_ok,

                    ocr_ok,

                    source_ok,

                ),

            },

        }


# ==========================================================
# E-NUMBER EXTRACTOR ENGINE
# ==========================================================


class ENumberExtractorEngine:

    def extract(
        self,
        text: str,
    ) -> List[str]:

        normalized = text.upper()

        e_numbers = re.findall(
            r"\b[E]\d{3,4}[a-z]?\b",
            normalized,
            re.IGNORECASE,
        )

        ins_numbers = re.findall(
            r"\bINS\s?\d{3,4}[a-z]?\b",
            normalized,
            re.IGNORECASE,
        )

        return list(
            set(
                e_numbers + ins_numbers
            )
        )


# ==========================================================
# POSITIVE ENGINE
# ==========================================================


class PositiveEngine:

    def detect(
        self,
        text: str,
        nutrition_data: Dict[str, Any] = None,
    ) -> List[Dict[str, Any]]:

        positives = []

        normalized = text.lower()

        if nutrition_data and nutrition_data.get("sugar", 0) > 15:

            high_sugar_penalty = True

        else:

            high_sugar_penalty = False

        protein_match = re.search(

            r"protein[:\s]+(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*g",

            normalized,

        )

        if protein_match and not high_sugar_penalty:

            protein_value = (
                protein_match.group(1)
            )

            if float(protein_value) >= 5.0:

                positives.append(

                    {

                        "title":
                        "Protein Source",

                        "value":
                        f"{protein_value}g",

                        "reason":
                        "Protein detected in nutrition facts",

                    }

                )

        fiber_match = re.search(

            r"(?:dietary\s+)?fib(?:er|re)[:\s]+(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*g",

            normalized,

        )

        if fiber_match:

            fiber_value = (
                fiber_match.group(1)
            )

            if float(fiber_value) >= 3.0:

                positives.append(

                    {

                        "title":
                        "High Fiber",

                        "value":
                        f"{fiber_value}g",

                        "reason":
                        "Dietary fiber detected",

                    }

                )

        calcium_match = re.search(

            r"calcium[:\s]+(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*mg",

            normalized,

        )

        if calcium_match:

            calcium_value = (
                calcium_match.group(1)
            )

            positives.append(

                {

                    "title":
                    "Calcium Source",

                    "value":
                    f"{calcium_value}mg",

                    "reason":
                    "Calcium detected",

                }

            )

        return positives


# ==========================================================
# NEGATIVE ENGINE
# ==========================================================


class NegativeEngine:

    def detect(
        self,
        text: str,
    ) -> List[Dict]:

        negatives = []

        normalized = (
            text.lower()
        )

        for ingredient, title in (

            NEGATIVE_INGREDIENTS.items()

        ):

            if ingredient in normalized:

                negatives.append(

                    {

                        "title":
                        title,

                        "reason":
                        f"Detected {ingredient}",

                        "severity":
                        "MEDIUM",

                    }

                )

        return negatives


# ==========================================================
# ALLERGEN ENGINE
# ==========================================================


class AllergenEngine:

    def detect(
        self,
        text: str,
    ) -> List[Dict]:

        results = []

        normalized = (
            text.lower()
        )

        detected_set = set()

        for allergen, aliases in (
            ALLERGEN_ALIASES.items()
        ):

            for alias in aliases:

                pattern = rf"\b{re.escape(alias.lower())}\b"

                if re.search(pattern, normalized):

                    if allergen not in detected_set:

                        results.append(

                            {

                                "allergen":
                                allergen,

                                "severity":
                                "HIGH",

                            }

                        )

                        detected_set.add(
                            allergen
                        )

        return results


# ==========================================================
# CLAIM ENGINE
# ==========================================================


class ClaimEngine:

    def detect_claims(
        self,
        text: str,
    ) -> List[str]:

        claims = []

        normalized = (
            text.lower()
        )

        for claim in MARKETING_CLAIMS:

            if claim in normalized:

                claims.append(
                    claim
                )

        return claims


# ==========================================================
# RISK ENGINE
# ==========================================================


class RiskEngine:

    def detect_hidden_sugars(
        self,
        text: str,
    ) -> List[str]:

        results = []

        normalized = text.lower()

        for sugar in HIDDEN_SUGARS:

            pattern = rf"\b{re.escape(sugar)}\b"

            if re.search(pattern, normalized) or sugar in normalized:

                results.append(
                    sugar
                )

        return results

    def detect_risks(
        self,
        text: str,
        nutrition_data: Dict[str, Any] = None,
    ) -> Dict[str, Any]:

        risks = []

        normalized = text.lower()

        hidden_sugars = (
            self.detect_hidden_sugars(
                normalized
            )
        )

        if hidden_sugars:

            risks.append(
                "Hidden Sugar"
            )

        if nutrition_data:

            if nutrition_data.get("sugar", 0) > 22.5:

                risks.append(
                    "High Sugar Profile"
                )

            if nutrition_data.get("sodium", 0) > 400:

                risks.append(
                    "High Sodium Profile"
                )

            if nutrition_data.get("saturated_fat", 0) > 5.0:

                risks.append(
                    "High Saturated Fat"
                )

        for keyword, risk in (

            RISK_KEYWORDS.items()

        ):

            if keyword in normalized:

                risks.append(
                    risk
                )

        overall_risk = "LOW"

        if len(risks) >= 4:

            overall_risk = "HIGH"

        elif len(risks) >= 2:

            overall_risk = "MEDIUM"

        return {

            "risks":
            list(
                set(risks)
            ),

            "overall_risk":
            overall_risk,

            "hidden_sugars":
            hidden_sugars,

        }


# ==========================================================
# SECTION ENGINE
# ==========================================================


class SectionEngine:

    def detect_sections(
        self,
        text: str,
    ) -> Dict[str, bool]:

        normalized = text.lower()

        detected = {

            "nutrition_table":
            False,

            "ingredients_section":
            False,

            "barcode_section":
            False,

            "claims_section":
            False,

            "front_label_section":
            True,

        }

        ingredient_fuzzies = [
            "ingredients",
            "ingredicnts",
            "ingredents",
            "ingrdients",
            "ingredients list",
        ]

        for fuzzy in ingredient_fuzzies:

            if fuzzy in normalized:

                detected[
                    "ingredients_section"
                ] = True

                break

        for section, keywords in (

            SECTION_KEYWORDS.items()

        ):

            for keyword in keywords:

                if keyword in normalized:

                    if section == "barcode":

                        detected[
                            "barcode_section"
                        ] = True

                    elif section == "claims":

                        detected[
                            "claims_section"
                        ] = True

                    elif section == "nutrition_table":

                        detected[
                            "nutrition_table"
                        ] = True

        return {

            key: bool(value)

            for key, value in detected.items()

        }


# ==========================================================
# COVERAGE ENGINE
# ==========================================================


class CoverageEngine:

    def calculate_coverage(
        self,
        sections: Dict[str, bool],
    ) -> int:

        weights = {
            "nutrition_table": 35,
            "ingredients_section": 25,
            "barcode_section": 20,
            "claims_section": 10,
            "front_label_section": 10,
        }

        score = 0

        for key, value in sections.items():

            if value:

                score += weights.get(key, 0)

        return min(score, 100)

    def calculate_completeness(
        self,
        ingredient_count: int,
        barcode_found: bool,
        nutrition_found: bool,
    ) -> int:

        score = 0

        if nutrition_found:

            score += 60

        if ingredient_count > 0:

            score += 25

        if barcode_found:

            score += 15

        return min(score, 100)


# ==========================================================
# SCAN QUALITY ENGINE
# ==========================================================


class ScanQualityEngine:

    def calculate_quality(
        self,
        ocr_quality: int,
        readability: int,
        image_quality: int,
        coverage: int,
    ) -> int:

        return int(

            (
                ocr_quality
                +
                readability
                +
                image_quality
                +
                coverage
            )

            / 4

        )

    def calculate_reliability(
        self,
        quality: int,
        verification_level: str,
    ) -> int:

        bonus_map = {

            "LOW": 0,

            "MEDIUM": 7,

            "HIGH": 15,

        }

        bonus = bonus_map.get(
            verification_level,
            0,
        )

        return min(

            quality + bonus,

            100,

        )


# ==========================================================
# RECOMMENDATION ENGINE
# ==========================================================


class RecommendationEngine:

    def build_recommendation(
        self,
        trust_score: int,
        overall_risk: str,
        nutrition_data: Dict[str, Any] = None,
        processing_level: str = "UNKNOWN",
    ) -> Dict[str, Any]:

        sugar = 0
        protein = 0
        fiber = 0

        if nutrition_data:

            sugar = nutrition_data.get("sugar", 0)
            protein = nutrition_data.get("protein", 0)
            fiber = nutrition_data.get("fiber", 0)

        if overall_risk == "HIGH":

            return {

                "recommendation": "AVOID",

                "reason": "Multiple health risks detected",

                "best_for": [],

            }

        if (
            processing_level == "ULTRA_PROCESSED"
            and
            sugar >= 15
        ):

            return {

                "recommendation": "AVOID",

                "reason": "Ultra processed and high sugar",

                "best_for": [],

            }

        if (
            sugar >= 15
            and
            protein < 5
            and
            fiber < 3
        ):

            return {

                "recommendation": "AVOID",

                "reason": "Poor nutritional profile",

                "best_for": [],

            }

        if (
            trust_score >= 70
            and
            overall_risk == "LOW"
        ):

            return {

                "recommendation": "DAILY",

                "reason": "Good overall profile",

                "best_for": ["General Consumers"],

            }

        return {

            "recommendation": "OCCASIONAL",

            "reason": "Moderate consumption recommended",

            "best_for": ["General Consumers"],

        }


# ==========================================================
# CLAIM VERIFICATION ENGINE
# ==========================================================


class ClaimVerificationEngine:

    def verify_claims(
        self,
        claims: List[str],
    ) -> List[Dict[str, Any]]:

        results = []

        for claim in claims:

            results.append(

                {

                    "claim": claim,

                    "detected": True,

                    "verification_status":
                    "UNVERIFIED",

                }

            )

        return results


# ==========================================================
# PRODUCT BADGE ENGINE
# ==========================================================


class ProductBadgeEngine:

    def generate_badges(
        self,
        positives: List[Dict],
        negatives: List[Dict],
        risks: List[str],
    ) -> List[str]:

        badges = []

        if len(positives) >= 3:

            badges.append(
                "NUTRITION_PLUS"
            )

        if len(negatives) >= 3:

            badges.append(
                "ULTRA_PROCESSED"
            )

        if "Hidden Sugar" in risks or "High Sugar Profile" in risks:

            badges.append(
                "HIDDEN_SUGAR"
            )

        if not badges:

            badges.append(
                "STANDARD_PRODUCT"
            )

        return badges


# ==========================================================
# TRUST CLASSIFICATION ENGINE
# ==========================================================


class TrustClassificationEngine:

    def classify(
        self,
        trust_score: int,
    ) -> str:

        if trust_score >= 85:

            return "HIGH"

        if trust_score >= 60:

            return "MEDIUM"

        return "LOW"


# ==========================================================
# NUTRITION SNAPSHOT ENGINE
# ==========================================================


class NutritionSnapshotEngine:

    def _extract_serving_size(
        self,
        text: str,
    ) -> Tuple[float, str]:
        """
        Extract serving size from label text.

        Args:
            text: OCR extracted text

        Returns:
            Tuple of (serving_size_in_grams, serving_unit)
        """

        text_lower = text.lower()

        patterns = [
            r"per\s+serving\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*(g|ml|gm|gram)",
            r"serving\s+size\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*(g|ml|gm|gram)",
            r"each\s+serving\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*(g|ml|gm|gram)",
            r"serving\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*(g|ml|gm|gram)",
            r"(\d+(?:\.\d+)?)\s*(g|ml|gm|gram)\s+per\s+serving",
        ]

        for pattern in patterns:

            match = re.search(pattern, text_lower)

            if match:

                value = float(match.group(1))

                unit = match.group(2).lower()

                if unit == "gm":
                    unit = "g"

                return value, unit

        # Default to 100g if no serving size found
        return 100.0, "g"

    def _convert_to_per_100g(
        self,
        value: float,
        serving_size_g: float,
    ) -> float:
        """
        Convert nutrient value from serving size to per 100g.

        Args:
            value: Nutrient value on label
            serving_size_g: Serving size in grams

        Returns:
            Nutrient value per 100g
        """

        if serving_size_g <= 0 or serving_size_g == 100:
            return value

        return round(
            (value * 100) / serving_size_g,
            2,
        )

    def _parse_table_coordinates(
        self,
        blocks: List[str],
    ) -> Dict[str, float]:

        nutrition = {}

        if not blocks:

            return nutrition

        keywords = {
            "protein": "protein",
            "fat": "fat",
            "sugar": "sugar",
            "sodium": "sodium",
            "energy": "calories",
            "calories": "calories",
        }

        for i, block in enumerate(blocks):

            text = block.lower()

            for keyword_key, keyword_val in keywords.items():

                if keyword_key in text:

                    search_range = 8 if keyword_val == "sodium" else 5

                    if keyword_val == "calories":

                        found_kcal = False

                        for j in range(0, search_range):

                            if i + j < len(blocks):

                                target_text = blocks[i + j].lower()

                                kcal_match = re.search(r"(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*kcal", target_text)

                                if kcal_match:

                                    nutrition[keyword_val] = float(kcal_match.group(1))

                                    found_kcal = True

                                    break

                        if not found_kcal:

                            for j in range(0, search_range):

                                if i + j < len(blocks):

                                    target_text = blocks[i + j].lower()

                                    kj_match = re.search(r"(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*kj", target_text)

                                    generic_match = re.search(r"(?<![a-zA-Z_])(\d+(?:\.\d+)?)", target_text)

                                    if kj_match:

                                        val = float(kj_match.group(1))

                                        nutrition[keyword_val] = round(val / 4.184, 1)

                                        break

                                    elif generic_match and j > 0:

                                        nutrition[keyword_val] = float(generic_match.group(1))

                                        break

                    else:

                        for j in range(0, search_range):

                            if i + j < len(blocks):

                                target_text = blocks[i + j].lower()

                                match = re.search(
                                    r"(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*(kcal|kj|g|mg)?",
                                    target_text
                                )

                                if match:

                                    nutrition[keyword_val] = float(match.group(1))

                                    break

        return nutrition

    def build(
        self,
        text: str,
        blocks: List[str] = None,
        ocr_confidence: float = 0.0,
        has_nutrition_table: bool = False,
    ) -> Dict[str, Any]:

        if not has_nutrition_table:

            return {

                "nutrition_detected": False,

                "nutrition_completeness": 0,

                "nutrition_confidence": 0,

                "nutrition_signals_detected": 0,

                "nutrition_signals_total": 8,

                "protein": 0.0,

                "fat": 0.0,

                "saturated_fat": 0.0,

                "sugar": 0.0,

                "sodium": 0.0,

                "carbohydrates": 0.0,

                "fiber": 0.0,

                "calories": 0.0,

            }

        normalized = text.lower()

        # Extract serving size and convert to per 100g
        serving_size_g, serving_unit = self._extract_serving_size(text)

        is_per_serving = (
            "per serving" in normalized
            or "serving size" in normalized
            or "each serving" in normalized
        )

        coord_nutrition = {}

        if blocks:

            coord_nutrition = (
                self._parse_table_coordinates(
                    blocks
                )
            )

        NUTRITION_FIELDS = {

            "protein": [

                r"protein\s*[|:.\-]*\s*(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*g?",

                r"protein\s*(?:per\s*serving)?\s*(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*g?",

            ],

            "fat": [

                r"total\s*fat\s*[|:.\-]*\s*(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*g?",

                r"fat\s*[|:.\-]*\s*(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*g?",

            ],

            "saturated_fat": [

                r"saturated\s*fat\s*[|:.\-]*\s*(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*g?",

            ],

            "sugar": [

                r"added\s*sugars?\s*[|:.\-]*\s*(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*g?",

                r"total\s*sugars?\s*[|:.\-]*\s*(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*g?",

                r"sugars?\s*[|:.\-]*\s*(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*g?",

            ],

            "sodium": [

                r"sodium\s*[|:.\-]*\s*(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*mg?",

                r"sodium\s*\(mg\)\s*[|:.\-]*\s*(?<![a-zA-Z_])(\d+(?:\.\d+)?)",

                r"na\s*[|:.\-]*\s*(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*mg?",

                r"salt\s*[|:.\-]*\s*(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*g?",

                r"salt\s*equivalent\s*[|:.\-]*\s*(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*g?",

            ],

            "carbohydrates": [

                r"carbohydrate[s]?\s*[|:.\-]*\s*(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*g?",

                r"carbs?\s*[|:.\-]*\s*(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*g?",

            ],

            "fiber": [

                r"(?:dietary\s*)?fiber\s*[|:.\-]*\s*(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*g?",

                r"(?:dietary\s*)?fibre\s*[|:.\-]*\s*(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*g?",

            ],

            "calories": [

                r"energy\s*[|:.\-]*\s*(?:\d+(?:\.\d+)?\s*kj\s*[\/|]?\s*)?(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*kcal",

                r"energy\s*[|:.\-]*\s*(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*kcal",

                r"(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*kcal",

                r"energy\s*[|:.\-]*\s*(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*kj",

                r"(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*kj",

                r"energy\s*[|:.\-]*\s*(?<![a-zA-Z_])(\d+(?:\.\d+)?)",

                r"calories?\s*[|:.\-]*\s*(?<![a-zA-Z_])(\d+(?:\.\d+)?)",

            ],

        }

        def extract_value(
            patterns,
            default=0.0,
            is_energy=False,
        ):

            for pattern in patterns:

                try:

                    match = re.search(
                        pattern,
                        normalized,
                        re.IGNORECASE,
                    )

                    if match:

                        val = float(
                            match.group(1)
                        )

                        match_text = match.group(0).lower()

                        if is_energy and "kj" in match_text and "kcal" not in match_text:

                            val = round(val / 4.184, 1)

                        return val

                except Exception:

                    continue

            return default

        nutrition_data = {}

        for field, patterns in (

            NUTRITION_FIELDS.items()

        ):

            if field in coord_nutrition:

                nutrition_data[field] = (
                    coord_nutrition[field]
                )

            else:

                is_energy = (field == "calories")

                nutrition_data[field] = (

                    extract_value(
                        patterns,
                        is_energy=is_energy,
                    )

                )

        def normalize_nutrition_values(
            data,
        ):

            for key in [
                "sugar",
                "protein",
                "fat",
                "saturated_fat",
                "fiber",
                "carbohydrates",
            ]:

                value = data.get(
                    key,
                    0,
                )

                if value > 100:

                    data[key] = round(
                        value / 100,
                        2,
                    )

            return data

        nutrition_data = (
            normalize_nutrition_values(
                nutrition_data
            )
        )

        if (
            nutrition_data.get("sodium", 0) == 0
            and "salt" in normalized
        ):

            salt_match = re.search(
                r"salt\s*[|:.\-]*\s*(?<![a-zA-Z_])(\d+(?:\.\d+)?)\s*g",
                normalized,
            )

            if salt_match:

                salt_g = float(
                    salt_match.group(1)
                )

                nutrition_data["sodium"] = round(
                    salt_g * 400,
                    0,
                )

        sodium = nutrition_data.get(
            "sodium",
            0,
        )

        if sodium > 5000:

            nutrition_data["sodium"] = (
                sodium / 10
            )

        fat = nutrition_data.get(
            "fat",
            0,
        )

        sat_fat = nutrition_data.get(
            "saturated_fat",
            0,
        )

        if sat_fat > fat:

            if sat_fat > 20:

                sat_fat = sat_fat / 10

            if sat_fat > fat:

                sat_fat = fat * 0.4

            nutrition_data["saturated_fat"] = round(sat_fat, 2)

        detected_count = sum(

            1

            for value in nutrition_data.values()

            if value > 0

        )

        if nutrition_data.get(
            "sodium",
            0
        ) > 0:

            detected_count += 1

        completeness = int(

            (
                detected_count
                /
                len(
                    NUTRITION_FIELDS
                )
            )

            * 100

        )

        confidence = int(
            (completeness * 0.7)
            +
            (ocr_confidence * 30)
        )

        # Convert to per 100g if serving size is not 100g
        if is_per_serving and serving_size_g != 100:

            for key in nutrition_data:

                if key in ["protein", "fat", "saturated_fat", "sugar", "carbohydrates", "fiber"]:

                    nutrition_data[key] = self._convert_to_per_100g(
                        nutrition_data[key],
                        serving_size_g,
                    )

                elif key == "sodium":

                    nutrition_data[key] = self._convert_to_per_100g(
                        nutrition_data[key],
                        serving_size_g,
                    )

                elif key == "calories":

                    nutrition_data[key] = self._convert_to_per_100g(
                        nutrition_data[key],
                        serving_size_g,
                    )

            # Store serving size info for reference
            nutrition_data["serving_size_g"] = serving_size_g
            nutrition_data["is_per_serving"] = True

        else:

            nutrition_data["serving_size_g"] = 100
            nutrition_data["is_per_serving"] = False

        return {
            "nutrition_detected":
            detected_count > 0,

            "nutrition_completeness":
            completeness,

            "nutrition_confidence":
            confidence,

            "nutrition_signals_detected":
            detected_count,

            "nutrition_signals_total":
            len(
                NUTRITION_FIELDS
            ),

            **nutrition_data,
        }


# ==========================================================
# MEMORY ANALYTICS ENGINE
# ==========================================================


class MemoryAnalyticsEngine:

    def analytics(
        self,
    ) -> Dict[str, Any]:

        return {

            "total_scans":

            len(
                SCAN_HISTORY
            ),

            "favorite_count":

            len(
                FAVORITES
            ),

        }


# ==========================================================
# DUPLICATE INTELLIGENCE ENGINE
# ==========================================================


class DuplicateIntelligenceEngine:

    def detect(
        self,
        barcode: Optional[str],
        brand: Optional[str],
        product_name: Optional[str],
    ) -> Dict[str, Any]:

        hash_source = f"{barcode}_{brand}_{product_name}"

        duplicate_hash = (

            hashlib.sha256(
                hash_source.encode()
            ).hexdigest()

        )

        for item in SCAN_HISTORY:

            hist_product = item.get("product", {})

            hist_barcode = hist_product.get("barcode")

            hist_brand = hist_product.get("brand")

            hist_name = hist_product.get("product_name")

            hist_source = f"{hist_barcode}_{hist_brand}_{hist_name}"

            hist_hash = (

                hashlib.sha256(
                    hist_source.encode()
                ).hexdigest()

            )

            if barcode and hist_barcode == barcode:

                return {

                    "duplicate":
                    True,

                    "duplicate_of":

                    item.get(
                        "metadata",
                        {},
                    ).get(
                        "scan_id"
                    ),

                }

            if brand and product_name and hist_brand and hist_name:

                brand_match = fuzz.token_set_ratio(
                    brand.lower(),
                    hist_brand.lower(),
                )

                name_match = fuzz.token_set_ratio(
                    product_name.lower(),
                    hist_name.lower(),
                )

                if brand_match > 85 and name_match > 85:

                    return {

                        "duplicate":
                        True,

                        "duplicate_of":

                        item.get(
                            "metadata",
                            {},
                        ).get(
                            "scan_id"
                        ),

                    }

        return {

            "duplicate":
            False,

            "duplicate_of":
            None,

        }


# ==========================================================
# CONSUMER PROFILE ENGINE
# ==========================================================


class ConsumerProfileEngine:

    def recommend_profile(
        self,
        positives: List[Dict],
        risks: List[str],
    ) -> List[str]:

        profiles = []

        if len(positives) >= 2:

            profiles.append(
                "Fitness Enthusiasts"
            )

        if "Hidden Sugar" not in risks and "High Sugar Profile" not in risks:

            profiles.append(
                "General Consumers"
            )

        if not profiles:

            profiles.append(
                "Occasional Consumers"
            )

        return profiles


# ==========================================================
# SINGLETONS
# ==========================================================


ocr_correction_engine = (
    OCRCorrectionEngine()
)

ocr_engine = (
    OCREngine()
)

memory_engine = (
    MemoryEngine()
)

barcode_engine = (
    BarcodeEngine()
)

product_engine = (
    ProductEngine()
)

fusion_engine = (
    ProductFusionEngine()
)

image_quality_engine = (
    ImageQualityEngine()
)

openfoodfacts_engine = (
    OpenFoodFactsEngine()
)

trust_engine = (
    TrustEngine()
)

verification_engine = (
    VerificationEngine()
)

enrichment_engine = (
    ProductEnrichmentEngine()
)

fusion_v2 = (
    ProductFusionV2()
)

enumber_extractor_engine = (
    ENumberExtractorEngine()
)

positive_engine = (
    PositiveEngine()
)

negative_engine = (
    NegativeEngine()
)

allergen_engine = (
    AllergenEngine()
)

claim_engine = (
    ClaimEngine()
)

risk_engine = (
    RiskEngine()
)

section_engine = (
    SectionEngine()
)

coverage_engine = (
    CoverageEngine()
)

scan_quality_engine = (
    ScanQualityEngine()
)

recommendation_engine = (
    RecommendationEngine()
)

claim_verification_engine = (
    ClaimVerificationEngine()
)

product_badge_engine = (
    ProductBadgeEngine()
)

trust_classification_engine = (
    TrustClassificationEngine()
)

nutrition_snapshot_engine = (
    NutritionSnapshotEngine()
)

memory_analytics_engine = (
    MemoryAnalyticsEngine()
)

duplicate_intelligence_engine = (
    DuplicateIntelligenceEngine()
)

consumer_profile_engine = (
    ConsumerProfileEngine()
)

consumer_intelligence_service = (
    ConsumerIntelligenceService()
)


# ==========================================================
# MULTI IMAGE FUSION ENGINE
# ==========================================================


class MultiImageFusionEngine:

    async def process_files(
        self,
        files: List[UploadFile],
    ) -> Dict[str, Any]:

        combined_raw_text = ""

        combined_text = ""

        all_blocks = []

        all_confidence = []

        processed_images = 0

        tasks = [

            ocr_engine.extract_text(file)

            for file in files

        ]

        results = await asyncio.gather(
            *tasks,
            return_exceptions=True,
        )

        for result in results:

            if isinstance(result, Exception):

                log.exception(
                    f"Fusion parallel OCR failed: {result}"
                )

                continue

            combined_raw_text += (
                result.get("raw_text", "")
                + "\n"
            )

            combined_text += (
                result.get("text", "")
                + "\n"
            )

            all_blocks.extend(

                result.get(
                    "blocks",
                    [],
                )

            )

            all_confidence.extend(

                result.get(
                    "confidence",
                    [],
                )

            )

            processed_images += 1

            temp_path = result.get(
                "temp_image_path"
            )

            if temp_path and os.path.exists(temp_path):

                try:

                    os.remove(temp_path)

                except Exception:

                    pass

        average_confidence = (

            ScanUtils.calculate_average(

                all_confidence

            )

        )

        return {

            "raw_text":
            combined_raw_text,

            "text":
            combined_text,

            "blocks":
            all_blocks,

            "confidence":
            all_confidence,

            "average_confidence":
            average_confidence,

            "images_processed":
            processed_images,

        }


multi_image_fusion_engine = (
    MultiImageFusionEngine()
)


# ==========================================================
# MASTER SCAN ENGINE
# ==========================================================


class MasterScanEngine:

    async def scan_product(
        self,
        file: UploadFile,
        user_id: Optional[str] = None,
    ) -> Dict[str, Any]:

        temp_image_path = None

        # ==========================================================
        # FILE VALIDATION
        # ==========================================================

        if not file or not file.filename:
            raise HTTPException(
                status_code=400,
                detail="No file provided"
            )

        # Check file size (max 10MB)
        max_size = MAX_IMAGE_SIZE_MB * 1024 * 1024
        file_size = 0

        if hasattr(file, "size"):
            file_size = file.size
        elif hasattr(file, "headers") and "content-length" in file.headers:
            file_size = int(file.headers["content-length"])

        if file_size > max_size:
            raise HTTPException(
                status_code=413,
                detail=f"File size exceeds {MAX_IMAGE_SIZE_MB}MB limit"
            )

        # Check content type
        allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]

        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=415,
                detail=f"Invalid image type. Allowed: {', '.join(allowed_types)}"
            )

        log.info(
            "Scan started",
            file_name=file.filename,
            file_size=file_size,
            content_type=file.content_type,
        )

        try:

            started = datetime.utcnow()

            scan_id = (
                ScanUtils.generate_scan_id()
            )

            ocr_result = (

                await ocr_engine.extract_text(
                    file
                )

            )

            text = ocr_result["text"]

            raw_text = ocr_result["raw_text"]

            temp_image_path = ocr_result.get("temp_image_path")

            image_quality = (

                image_quality_engine.calculate_image_quality(
                    temp_image_path
                )

            )

            barcode_from_image = (

                barcode_engine.decode_barcode_from_image(
                    temp_image_path
                )

            )

            fusion_task = asyncio.create_task(

                fusion_v2.fuse(

                    text,

                    ocr_result[
                        "average_confidence"
                    ],

                    image_barcode=barcode_from_image,

                )

            )

           
            fusion_result = await fusion_task

            e_numbers_extracted = (

                enumber_extractor_engine.extract(
                    text
                )

            )

            from modules.ingredients.service import ingredient_intelligence_service
            from modules.metabolism.service import metabolism_service


            ingredient_intelligence = (

                ingredient_intelligence_service
                .analyze(
                    text
                )

            )

            # Extract registry data from ingredient_intelligence
            registry = ingredient_intelligence.get(
                "registry",
                {},
            )

            # Extract ingredient functions
            ingredient_functions = ingredient_intelligence.get(
                "ingredient_functions",
                {},
            )

            # Extract ingredient risks
            ingredient_risks = ingredient_intelligence.get(
                "ingredient_risks",
                {},
            )

            # Extract ingredient summary with all new fields
            ingredient_summary = ingredient_intelligence.get(
                "ingredient_summary",
                {},
            )

            ingredient_data = {

                "ingredient_count":

                ingredient_intelligence.get(
                    "ingredient_profile", {}
                ).get(
                    "ingredient_count", 0
                ),

                "additive_count":

                len(

                    ingredient_intelligence.get(
                        "additives", {}
                    ).get(
                        "detected_additives", []
                    )

                    + e_numbers_extracted

                ),

                "preservative_count":
                ingredient_summary.get(
                    "preservatives", 0
                ),

                "artificial_count":

                ingredient_intelligence.get(
                    "ingredient_profile", {}
                ).get(
                    "artificial_count", 0
                ),

                "ingredients": [

                    item.get("name", "")

                    for item in

                    ingredient_intelligence.get(
                        "ingredients", []
                    )

                ],

                "e_numbers":
                e_numbers_extracted,

                # New fields from System 2 upgrades

                "stabilizers": ingredient_summary.get(
                    "stabilizers", 0
                ),

                "emulsifiers": ingredient_summary.get(
                    "emulsifiers", 0
                ),

                "thickeners": ingredient_summary.get(
                    "thickeners", 0
                ),

                "acidity_regulators": ingredient_summary.get(
                    "acidity_regulators", 0
                ),

                "anti_caking_agents": ingredient_summary.get(
                    "anti_caking_agents", 0
                ),

                "flavor_enhancers": ingredient_summary.get(
                    "flavor_enhancers", 0
                ),

                "artificial_sweeteners": ingredient_summary.get(
                    "artificial_sweeteners", 0
                ),

                "artificial_colors": ingredient_summary.get(
                    "artificial_colors", 0
                ),

            }

            sections = (

                section_engine
                .detect_sections(
                    text
                )

            )

            nutrition_snapshot = (

                nutrition_snapshot_engine
                .build(

                    text,

                    ocr_result["blocks"],

                    ocr_result["average_confidence"],

                    has_nutrition_table=sections.get("nutrition_table", False),

                )

            )

            positives = (

                positive_engine.detect(
                    text,
                    nutrition_data=nutrition_snapshot,
                )

            )

            negatives = (

                negative_engine.detect(
                    text
                )

            )

            allergens = (

                allergen_engine.detect(
                    text
                )

            )

            claims = (

                claim_engine
                .detect_claims(
                    text
                )

            )

            claim_verification = (

                claim_verification_engine
                .verify_claims(
                    claims
                )

            )

            risk_data = (

                risk_engine.detect_risks(
                    text,
                    nutrition_data=nutrition_snapshot,
                )

            )

            coverage_score = (

                coverage_engine
                .calculate_coverage(
                    sections
                )

            )

            completeness_score = (

                coverage_engine
                .calculate_completeness(

                    ingredient_data.get(
                        "ingredient_count",
                        0,
                    ),

                    fusion_result[
                        "verification"
                    ][
                        "barcode_verified"
                    ],

                    sections[
                        "nutrition_table"
                    ],

                )

            )

            ocr_quality = (

                ocr_engine
                .calculate_ocr_quality(

                    ocr_result[
                        "confidence"
                    ]

                )

            )

            readability = (

                ocr_engine
                .calculate_readability_score(
                    text
                )

            )

            scan_quality = (

                scan_quality_engine
                .calculate_quality(

                    ocr_quality,

                    readability,

                    image_quality,

                    coverage_score,

                )

            )

            reliability = (

                scan_quality_engine
                .calculate_reliability(

                    scan_quality,

                    fusion_result[
                        "verification"
                    ][
                        "verification_level"
                    ],

                )

            )

            recommendation = (

                recommendation_engine
                .build_recommendation(

                    fusion_result[
                        "trust"
                    ][
                        "trust_score"
                    ],

                    risk_data[
                        "overall_risk"
                    ],

                    nutrition_data=nutrition_snapshot,

                    processing_level=ingredient_intelligence.get("processing_analysis", {}).get("processing_level", "UNKNOWN"),

                )

            )

            nutrition_snapshot["category"] = (

                fusion_result
                .get(
                    "product",
                    {}
                )
                .get(
                    "category",
                    ""
                )

            )

            metabolic_intelligence = (

                metabolism_service.analyze(

                    nutrition=
                    nutrition_snapshot,

                    ingredient_intelligence=
                    ingredient_intelligence,

                    product=
                    fusion_result["product"],

                    scan_quality={

                        "scan_quality_score":
                        scan_quality

                    },

                )

            )

            consumer_intelligence = (

                consumer_intelligence_service.analyze(

                    claims=
                    claims,

                    nutrition=
                    nutrition_snapshot,

                    ingredient_intelligence=
                    ingredient_intelligence,

                    metabolic_intelligence=
                    metabolic_intelligence,

                    trust=
                    fusion_result["trust"],

                    ocr_text=
                    text,

                    product_category=

                    str(

                        fusion_result
                        .get(
                            "product",
                            {}
                        )
                        .get(
                            "category",
                            ""
                        )

                    ),

                )

            )

            digital_twin = (

                digital_twin_service.analyze({

                    "product":
                    fusion_result["product"],

                    "nutrition":
                    nutrition_snapshot,

                    "ingredient_intelligence":
                    ingredient_intelligence,

                    "metabolic_intelligence":
                    metabolic_intelligence,

                    "consumer_intelligence":
                    consumer_intelligence,

                    "claims":
                    claims,

                    "ocr_text":
                    text,

                })

            )


            # ==========================================================
            # SYSTEM 7 - SMART SWAP INTELLIGENCE
            # ==========================================================


            # Extract correct nutrition values from nutrition_snapshot
            swap_nutrition = {

                "calories": nutrition_snapshot.get("calories", 0),

                "protein": nutrition_snapshot.get("protein", 0),

                "fat": nutrition_snapshot.get("fat", 0),

                "saturated_fat": nutrition_snapshot.get("saturated_fat", 0),

                "carbohydrates": nutrition_snapshot.get("carbohydrates", 0),

                "sugar": nutrition_snapshot.get("sugar", 0),

                "fiber": nutrition_snapshot.get("fiber", 0),

                "sodium": nutrition_snapshot.get("sodium", 0),

            }

            # Build swap request from scan data with proper values
            swap_request = SwapRequest(

                product_name=fusion_result["product"].get("product_name", ""),

                brand=fusion_result["product"].get("brand", ""),

                category=fusion_result["product"].get("category", ""),

                nutrition=swap_nutrition,

                nova_group=fusion_result["product"].get("nova", 4),

                processing_level=ingredient_intelligence.get("processing_analysis", {}).get("processing_level", "ULTRA_PROCESSED"),

                deception_score=consumer_intelligence.get("deception", {}).get("deception_score", 50),

                metabolic_risk_score=metabolic_intelligence.get("verdict", {}).get("overall", {}).get("score", 50),

                organ_impact_score=float(digital_twin.get("organ_impact", {}).get("organ_health_score", 50)),

                additives_list=ingredient_data.get("e_numbers", []),

                max_results=6,

                sort_by=SortByOption.HEALTH_SCORE,

            )

            # Get swap recommendations
            swap_result = await smart_swap_service.get_swaps(swap_request)


                        # ==========================================================
            # SYSTEM 8 - TRUST INTELLIGENCE (Adulteration + Counterfeit + Claim Verifier)
            # ==========================================================

            from modules.trust import trust_service, TrustIntelligenceRequest

            # Build trust request from scan data
            trust_request = TrustIntelligenceRequest(

                product_name=fusion_result["product"].get("product_name", ""),

                brand=fusion_result["product"].get("brand", ""),

                fssai_number=consumer_intelligence.get("compliance", {}).get("fssai_license"),

                nutrition_data={
                    "protein": nutrition_snapshot.get("protein", 0),
                    "fat": nutrition_snapshot.get("fat", 0),
                    "saturated_fat": nutrition_snapshot.get("saturated_fat", 0),
                    "sugar": nutrition_snapshot.get("sugar", 0),
                    "sodium": nutrition_snapshot.get("sodium", 0),
                    "fiber": nutrition_snapshot.get("fiber", 0),
                    "carbohydrates": nutrition_snapshot.get("carbohydrates", 0),
                    "calories": nutrition_snapshot.get("calories", 0),
                },

                front_of_pack_claims=claims,

                ingredients=ingredient_data.get("ingredients", []),

                ingredient_text=text,

                serving_size_g=nutrition_snapshot.get("serving_size_g"),

                product_category=fusion_result["product"].get("category"),

                manufacturer=fusion_result["product"].get("manufacturer"),

                scan_quality_score=scan_quality,

                barcode=fusion_result["product"].get("barcode"),

            )

            # Get trust intelligence result
            trust_intelligence = await trust_service.analyze(trust_request)



            food_explainer = (

                food_explainer_service.analyze(

                    product=
                    fusion_result["product"],

                    nutrition=
                    nutrition_snapshot,

                    claims=
                    claims,

                    ocr_text=
                    text,

                    serving_size="",

                    ingredient_intelligence=
                    ingredient_intelligence,

                    metabolic_intelligence=
                    metabolic_intelligence,

                    consumer_intelligence=
                    consumer_intelligence,

                    digital_twin=
                    digital_twin,

                )

            )

            nutritionist = (

                nutritionist_service.analyze(

                    profile={},

                    product=
                    fusion_result["product"],

                    nutrition=
                    nutrition_snapshot,

                    claims=
                    claims,

                    ocr_text=
                    text,

                    serving_size="",

                    scan_quality={

                        "scan_quality_score":
                        scan_quality

                    },

                    ingredient_intelligence=
                    ingredient_intelligence,

                    metabolic_intelligence=
                    metabolic_intelligence,

                    consumer_intelligence=
                    consumer_intelligence,

                    body_intelligence=digital_twin,

                    scan_history=
                    SCAN_HISTORY,

                    conversation_history=[],

                    user_query="Analyze this food product",

                )

            )

            badges = (

                product_badge_engine
                .generate_badges(

                    positives,

                    negatives,

                    risk_data[
                        "risks"
                    ],

                )

            )

            duplicate = (

                duplicate_intelligence_engine
                .detect(

                    fusion_result["product"].get("barcode"),

                    fusion_result["product"].get("brand"),

                    fusion_result["product"].get("product_name"),

                )

            )

            consumer_profiles = (

                consumer_profile_engine
                .recommend_profile(

                    positives,

                    risk_data[
                        "risks"
                    ],

                )

            )

            completed = (
                datetime.utcnow()
            )

            processing_time = int(

                (
                    completed
                    - started
                ).total_seconds()

                * 1000

            )

            result = {

                "success": True,

                "metadata": {

                    "scan_id":
                    scan_id,

                    "timestamp":

                    ScanUtils.current_timestamp(),

                    "source":
                    "ocr+barcode+off",

                    "processing_time_ms":
                    processing_time,

                    "audit_trail": {

                        "ocr_raw":
                        raw_text,

                        "ocr_corrected":
                        text,

                    },

                },

                "product":

                fusion_result[
                    "product"
                ],

                "ocr": {

                    "extracted_text":
                    text,

                    "blocks":

                    ocr_result[
                        "blocks"
                    ],

                    "confidence_values":

                    ocr_result[
                        "confidence"
                    ],

                    "average_confidence":

                    ocr_result[
                        "average_confidence"
                    ],

                    "text_density_score":

                    ocr_engine
                    .calculate_density_score(
                        text
                    ),

                    "readability_score":
                    readability,

                    "ocr_quality_score":
                    ocr_quality,

                },

                "scan_quality": {

                    "coverage_score":
                    coverage_score,

                    "completeness_score":
                    completeness_score,

                    "image_quality_score":
                    image_quality,

                    "scan_quality_score":
                    scan_quality,

                    "scan_reliability_score":
                    reliability,

                },

                "ingredients":
                ingredient_data,

                "ingredient_intelligence":
                ingredient_intelligence,

                "ingredient_registry": {
                    "e_numbers": registry.get("e_numbers", []),
                    "high_risk_additives": registry.get("high_risk_additives", []),
                    "allergens": registry.get("allergens", []),
                    "contains_palm_oil": registry.get("contains_palm_oil", False),
                },

                "ingredient_functions":
                ingredient_functions,

                "ingredient_risks":
                ingredient_risks,

                "metabolic_intelligence":
                metabolic_intelligence,

                "consumer_intelligence":
                consumer_intelligence,

                "digital_twin":
                digital_twin,

                "smart_swaps":
                swap_result.model_dump(),


                "trust_intelligence": {
                    "overall_trust_score": trust_intelligence.overall_trust_score,
                    "overall_trust_level": trust_intelligence.overall_trust_level,
                    "is_fssai_valid": trust_intelligence.is_fssai_valid,
                    "fssai_validation": trust_intelligence.fssai_validation.model_dump() if trust_intelligence.fssai_validation else None,
                    "adulteration_detected": trust_intelligence.adulteration_detection.detected if trust_intelligence.adulteration_detection else False,
                    "adulteration_risk_level": trust_intelligence.adulteration_detection.risk_level.value if trust_intelligence.adulteration_detection else "none",
                    "counterfeit_risk_level": trust_intelligence.counterfeit_detection.risk_level.value if trust_intelligence.counterfeit_detection else "none",
                    "contradictions": [c.model_dump() for c in trust_intelligence.contradictions],
                    "label_anomalies": [a.model_dump() for a in trust_intelligence.label_anomalies],
                    "authenticity_score": trust_intelligence.authenticity_score.overall_score if trust_intelligence.authenticity_score else 0,
                    "authenticity_grade": trust_intelligence.authenticity_score.grade if trust_intelligence.authenticity_score else "F",
                    "brand_trust_score": trust_intelligence.brand_trust.trust_score if trust_intelligence.brand_trust else 50,
                    "warnings": trust_intelligence.warnings,
                    "recommendations": trust_intelligence.recommendations,
                },


                "food_explainer":
                food_explainer,

                "nutritionist":
                nutritionist,

                "claims": {

                    "claims_detected":
                    claims,

                    "claim_details":
                    claim_verification,

                },

                "sections":
                sections,

                "positives":
                positives,

                "negatives":
                negatives,

                "allergens":
                allergens,

                "risks":
                risk_data,

                "trust":

                fusion_result[
                    "trust"
                ],

                "verification":

                fusion_result[
                    "verification"
                ],

                "nutrition":
                nutrition_snapshot,

                "recommendation":
                recommendation,

                "badges":
                badges,

                "duplicate":
                duplicate,

                "consumer_profiles":
                consumer_profiles,

                "analytics":

                memory_analytics_engine
                .analytics(),

            }

            result["hash"] = (
                ScanUtils.create_hash(
                    text
                )
            )

            memory_engine.save_scan(
                result
            )

            result["analytics"] = (
                memory_analytics_engine
                .analytics()
            )

            # ==========================================================
            # SYSTEM 9 – USER INTELLIGENCE PLATFORM
            # ==========================================================

            try:
                from modules.user_intelligence.service import user_intelligence_service

                if user_id:
                    await user_intelligence_service.save_scan(user_id, result)
                    result["saved_to_history"] = True
                else:
                    result["saved_to_history"] = False

            except ImportError:
                result["saved_to_history"] = False

            except Exception as e:
                log.exception(f"Failed to save scan: {e}")
                result["saved_to_history"] = False

            # Clean up OCR reader if idle
            ocr_engine.cleanup_if_idle()

            return result

        finally:

            if temp_image_path and os.path.exists(temp_image_path):

                try:

                    os.remove(temp_image_path)

                except Exception as e:

                    log.exception(
                        f"Failed to cleanup temp file: {e}"
                    )

    async def multi_scan(
        self,
        files: List[UploadFile],
    ) -> Dict[str, Any]:

        fusion_data = (

            await multi_image_fusion_engine
            .process_files(
                files
            )

        )

        return fusion_data


master_scan_engine = (
    MasterScanEngine()
)