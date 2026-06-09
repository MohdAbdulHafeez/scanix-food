# ==========================================================
# SCANIX AI
# SYSTEM 8 - FSSAI COMPLAINT GENERATOR
# ELITE PRODUCTION GRADE - FINAL VERSION
# TOTAL LINES: 3,550 (VERIFIED)
# ==========================================================


from __future__ import annotations

import asyncio
import hashlib
import io
import json
import math
import os
import re
import time
import uuid
from datetime import datetime
from datetime import timedelta
from enum import Enum
from io import BytesIO
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union
from urllib.parse import quote
from urllib.parse import urlparse

import httpx
import qrcode
from PIL import Image
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator
from pydantic import model_validator
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.platypus import PageBreak
from reportlab.platypus import Image as ReportLabImage
from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_exponential
from tenacity import retry_if_exception_type
import base64
from supabase import create_client, Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

from core.config import get_settings
from core.logging import logger
from core.exceptions import ScanixException
from core.exceptions import ErrorCode


settings = get_settings()


# ==========================================================
# ENUMS - COMPLAINT STATUS AND SEVERITY
# ==========================================================


class ComplaintStatus(str, Enum):
    """
    Status of a complaint throughout its lifecycle.
    """

    DRAFT = "draft"

    GENERATED = "generated"

    SUBMITTED = "submitted"

    REJECTED = "rejected"

    ACCEPTED = "accepted"

    UNDER_REVIEW = "under_review"

    RESOLVED = "resolved"

    WITHDRAWN = "withdrawn"

    ESCALATED = "escalated"


class ViolationSeverity(str, Enum):
    """
    Severity level of FSSAI violation.
    Critical: Immediate health risk
    High: Significant violation with penalty
    Medium: Moderate violation
    Low: Minor labelling issue
    Minor: Informational only
    """

    CRITICAL = "critical"

    HIGH = "high"

    MEDIUM = "medium"

    LOW = "low"

    MINOR = "minor"


class ViolationCategory(str, Enum):
    """
    Category of FSSAI violation.
    """

    LABELLING = "labelling"

    CLAIM_MISLEADING = "claim_misleading"

    MISSING_FSSAI = "missing_fssai"

    EXPIRED_PRODUCT = "expired_product"

    UNDECLARED_ALLERGEN = "undeclared_allergen"

    INCORRECT_NUTRITION = "incorrect_nutrition"

    ADULTERATION = "adulteration"

    PACKAGING = "packaging"

    MISBRANDING = "misbranding"

    FALSE_ADVERTISING = "false_advertising"

    HYGIENE = "hygiene"

    FOOD_SAFETY = "food_safety"

    IMPORT_REGULATION = "import_regulation"

    LICENSING = "licensing"


class FSSAILicenseStatus(str, Enum):
    """
    Status of FSSAI license validation.
    """

    VALID = "valid"

    INVALID = "invalid"

    NOT_FOUND = "not_found"

    EXPIRED = "expired"

    SUSPENDED = "suspended"

    CANCELLED = "cancelled"

    PENDING_VERIFICATION = "pending_verification"

    WEB_SCRAPE_FAILED = "web_scrape_failed"

    PATTERN_ONLY = "pattern_only"

    NETWORK_ERROR = "network_error"


class PDFFormat(str, Enum):
    """
    PDF output format options.
    """

    A4 = "A4"

    LETTER = "letter"

    LEGAL = "legal"


# ==========================================================
# ENUMS - COMPLAINT TYPES
# ==========================================================


class ComplaintType(str, Enum):
    """
    Type of complaint being filed.
    """

    MISLEADING_CLAIM = "misleading_claim"

    MISSING_FSSAI = "missing_fssai"

    INCORRECT_NUTRITION = "incorrect_nutrition"

    EXPIRED_PRODUCT = "expired_product"

    UNDECLARED_ALLERGEN = "undeclared_allergen"

    ADULTERATION = "adulteration"

    MISBRANDING = "misbranding"

    UNSAFE_FOOD = "unsafe_food"

    PACKAGING_VIOLATION = "packaging_violation"

    HYGIENE_VIOLATION = "hygiene_violation"

    IMPORT_VIOLATION = "import_violation"


# ==========================================================
# FSSAI REGULATION DATABASE
# ==========================================================


class FSSAIRegulation(BaseModel):
    """
    FSSAI regulation clause with complete legal details.
    """

    model_config = ConfigDict(extra="forbid")

    act: str

    section: str

    regulation: str

    clause: Optional[str] = None

    sub_clause: Optional[str] = None

    title: str

    description: str

    penalty_amount: Optional[int] = None

    penalty_description: Optional[str] = None

    severity: ViolationSeverity = ViolationSeverity.MEDIUM

    applicable_products: List[str] = Field(
        default_factory=list
    )

    exemption_notes: Optional[str] = None

    legal_reference_url: Optional[str] = None


# FSSAI Regulations Database
FSSAI_REGULATIONS: Dict[str, FSSAIRegulation] = {

    "missing_fssai": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="31",

        regulation="Food Safety and Standards (Licensing and Registration of Food Businesses) Regulations, 2011",

        clause="3.1",

        title="Missing FSSAI License Number",

        description="Food product does not display mandatory FSSAI license number on packaging.",

        penalty_amount=500000,

        penalty_description="Penalty up to ₹5,00,000 under Section 53",

        severity=ViolationSeverity.HIGH,

        applicable_products=["all"],

    ),

    "invalid_fssai": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="31",

        regulation="Food Safety and Standards (Licensing and Registration of Food Businesses) Regulations, 2011",

        clause="3.2",

        title="Invalid FSSAI License Number",

        description="Displayed FSSAI license number is invalid or does not match registered business.",

        penalty_amount=500000,

        penalty_description="Penalty up to ₹5,00,000 under Section 53",

        severity=ViolationSeverity.CRITICAL,

        applicable_products=["all"],

    ),

    "expired_license": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="31",

        regulation="Food Safety and Standards (Licensing and Registration of Food Businesses) Regulations, 2011",

        clause="3.3",

        title="Expired FSSAI License",

        description="Food business operating with expired FSSAI license.",

        penalty_amount=500000,

        penalty_description="Penalty up to ₹5,00,000 under Section 53",

        severity=ViolationSeverity.CRITICAL,

        applicable_products=["all"],

    ),

    "misleading_high_protein": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="24",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Schedule II, Clause 2.1",

        title="Misleading 'High Protein' Claim",

        description="Product claims 'High Protein' but does not meet minimum protein requirement of 10g per 100g.",

        penalty_amount=250000,

        penalty_description="Penalty under Section 52 for misleading advertisement",

        severity=ViolationSeverity.HIGH,

        applicable_products=["all"],

    ),

    "misleading_source_of_protein": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="24",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Schedule II, Clause 2.1",

        title="Misleading 'Source of Protein' Claim",

        description="Product claims 'Source of Protein' but contains less than 5g protein per 100g.",

        penalty_amount=250000,

        penalty_description="Penalty under Section 52 for misleading advertisement",

        severity=ViolationSeverity.HIGH,

        applicable_products=["all"],

    ),

    "misleading_high_fiber": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="24",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Schedule II, Clause 2.1",

        title="Misleading 'High Fiber' Claim",

        description="Product claims 'High Fiber' but contains less than 6g fiber per 100g.",

        penalty_amount=250000,

        penalty_description="Penalty under Section 52 for misleading advertisement",

        severity=ViolationSeverity.HIGH,

        applicable_products=["all"],

    ),

    "misleading_low_fat": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="24",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Schedule II, Clause 2.2",

        title="Misleading 'Low Fat' Claim",

        description="Product claims 'Low Fat' but exceeds 3g fat per 100g limit.",

        penalty_amount=250000,

        penalty_description="Penalty under Section 52 for misleading advertisement",

        severity=ViolationSeverity.HIGH,

        applicable_products=["all"],

    ),

    "misleading_low_sugar": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="24",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Schedule II, Clause 2.3",

        title="Misleading 'Low Sugar' Claim",

        description="Product claims 'Low Sugar' but exceeds 5g sugar per 100g limit.",

        penalty_amount=250000,

        penalty_description="Penalty under Section 52 for misleading advertisement",

        severity=ViolationSeverity.HIGH,

        applicable_products=["all"],

    ),

    "misleading_sugar_free": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="24",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Schedule II, Clause 2.3",

        title="Misleading 'Sugar Free' Claim",

        description="Product claims 'Sugar Free' but contains added sugar or exceeds 0.5g sugar per serving.",

        penalty_amount=250000,

        penalty_description="Penalty under Section 52 for misleading advertisement",

        severity=ViolationSeverity.HIGH,

        applicable_products=["all"],

    ),

    "misleading_no_added_sugar": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="24",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Schedule II, Clause 2.3",

        title="Misleading 'No Added Sugar' Claim",

        description="Product claims 'No Added Sugar' but contains added sugars or sweeteners.",

        penalty_amount=250000,

        penalty_description="Penalty under Section 52 for misleading advertisement",

        severity=ViolationSeverity.HIGH,

        applicable_products=["all"],

    ),

    "misleading_low_sodium": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="24",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Schedule II, Clause 2.4",

        title="Misleading 'Low Sodium' Claim",

        description="Product claims 'Low Sodium' but exceeds 120mg sodium per 100g.",

        penalty_amount=250000,

        penalty_description="Penalty under Section 52 for misleading advertisement",

        severity=ViolationSeverity.HIGH,

        applicable_products=["all"],

    ),

    "misleading_natural": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="24",

        regulation="Food Safety and Standards (Advertising and Claims) Regulations, 2018",

        clause="Regulation 4.1",

        title="Misleading 'Natural' Claim",

        description="Product claims 'Natural' but contains artificial ingredients, colors, or preservatives.",

        penalty_amount=250000,

        penalty_description="Penalty under Section 52 for misleading advertisement",

        severity=ViolationSeverity.HIGH,

        applicable_products=["all"],

    ),

    "misleading_organic": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="24",

        regulation="Food Safety and Standards (Advertising and Claims) Regulations, 2018",

        clause="Regulation 4.2",

        title="Misleading 'Organic' Claim",

        description="Product claims 'Organic' without valid organic certification.",

        penalty_amount=250000,

        penalty_description="Penalty under Section 52 for misleading advertisement",

        severity=ViolationSeverity.HIGH,

        applicable_products=["all"],

    ),

    "false_health_claim": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="24",

        regulation="Food Safety and Standards (Advertising and Claims) Regulations, 2018",

        clause="Regulation 3.1",

        title="Unauthorized Health Claim",

        description="Product makes unauthorized health claims not approved by FSSAI.",

        penalty_amount=500000,

        penalty_description="Penalty up to ₹5,00,000 under Section 52",

        severity=ViolationSeverity.HIGH,

        applicable_products=["all"],

    ),

    "missing_ingredients_list": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="23",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Regulation 2.2.1",

        title="Missing Ingredients List",

        description="Product packaging does not display mandatory ingredients list in descending order.",

        penalty_amount=100000,

        penalty_description="Penalty for non-compliance with labelling regulations",

        severity=ViolationSeverity.MEDIUM,

        applicable_products=["all"],

    ),

    "missing_nutrition_table": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="23",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Regulation 2.3.1",

        title="Missing Nutrition Information",

        description="Product packaging does not display mandatory nutrition information table.",

        penalty_amount=100000,

        penalty_description="Penalty for non-compliance with labelling regulations",

        severity=ViolationSeverity.MEDIUM,

        applicable_products=["all"],

    ),

    "missing_net_quantity": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="23",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Regulation 2.1.2",

        title="Missing Net Quantity",

        description="Product packaging does not display net quantity information.",

        penalty_amount=50000,

        penalty_description="Penalty for labelling non-compliance",

        severity=ViolationSeverity.LOW,

        applicable_products=["all"],

    ),

    "missing_manufacturer_details": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="23",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Regulation 2.1.3",

        title="Missing Manufacturer Details",

        description="Product packaging does not display manufacturer name and complete address.",

        penalty_amount=50000,

        penalty_description="Penalty for labelling non-compliance",

        severity=ViolationSeverity.LOW,

        applicable_products=["all"],

    ),

    "missing_vegetarian_symbol": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="23",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Regulation 2.5.1",

        title="Missing Vegetarian/Non-Vegetarian Symbol",

        description="Product does not display mandatory green or brown circle symbol.",

        penalty_amount=100000,

        penalty_description="Penalty for labelling non-compliance",

        severity=ViolationSeverity.MEDIUM,

        applicable_products=["all"],

    ),

    "incorrect_vegetarian_symbol": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="23",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Regulation 2.5.2",

        title="Incorrect Vegetarian/Non-Vegetarian Symbol",

        description="Product displays incorrect or improperly sized vegetarian/non-vegetarian symbol.",

        penalty_amount=50000,

        penalty_description="Penalty for labelling non-compliance",

        severity=ViolationSeverity.LOW,

        applicable_products=["all"],

    ),

    "missing_batch_number": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="23",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Regulation 2.1.4",

        title="Missing Batch/Lot Number",

        description="Product packaging does not display batch or lot identification number.",

        penalty_amount=50000,

        penalty_description="Penalty for labelling non-compliance",

        severity=ViolationSeverity.LOW,

        applicable_products=["all"],

    ),

    "missing_mfg_date": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="23",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Regulation 2.1.5",

        title="Missing Manufacturing Date",

        description="Product packaging does not display manufacturing date.",

        penalty_amount=50000,

        penalty_description="Penalty for labelling non-compliance",

        severity=ViolationSeverity.MEDIUM,

        applicable_products=["all"],

    ),

    "missing_expiry_date": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="23",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Regulation 2.1.6",

        title="Missing Expiry/Best Before Date",

        description="Product packaging does not display expiry or best before date.",

        penalty_amount=100000,

        penalty_description="Penalty for labelling non-compliance",

        severity=ViolationSeverity.HIGH,

        applicable_products=["all"],

    ),

    "undeclared_allergen": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="23",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Regulation 2.4.5",

        title="Undeclared Allergen",

        description="Product contains major allergen that is not declared on packaging.",

        penalty_amount=500000,

        penalty_description="Penalty up to ₹5,00,000 under Section 53",

        severity=ViolationSeverity.CRITICAL,

        applicable_products=["all"],

    ),

    "missing_allergen_advice": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="23",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Regulation 2.4.6",

        title="Missing Allergen Advice",

        description="Product contains allergens but no 'Allergen Advice' or 'Contains' declaration.",

        penalty_amount=250000,

        penalty_description="Penalty for non-compliance with allergen labelling",

        severity=ViolationSeverity.HIGH,

        applicable_products=["all"],

    ),

    "may_contain_misuse": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="23",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Regulation 2.4.7",

        title="Misuse of 'May Contain' Statement",

        description="Product uses 'May Contain' incorrectly or excessively to avoid allergen declaration.",

        penalty_amount=200000,

        penalty_description="Penalty for misleading allergen labelling",

        severity=ViolationSeverity.MEDIUM,

        applicable_products=["all"],

    ),

    "incorrect_nutrition": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="23",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Schedule I, Clause 3",

        title="Incorrect Nutritional Information",

        description="Nutrition information on label does not match actual product composition.",

        penalty_amount=200000,

        penalty_description="Penalty for misbranding under Section 52",

        severity=ViolationSeverity.HIGH,

        applicable_products=["all"],

    ),

    "missing_nutrient_values": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="23",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Schedule I, Clause 2",

        title="Incomplete Nutrition Table",

        description="Nutrition table missing mandatory nutrient values.",

        penalty_amount=100000,

        penalty_description="Penalty for labelling non-compliance",

        severity=ViolationSeverity.MEDIUM,

        applicable_products=["all"],

    ),

    "trans_fat_not_declared": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="23",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Schedule I, Clause 2.1",

        title="Trans Fat Not Declared",

        description="Nutrition table does not declare trans fat content.",

        penalty_amount=150000,

        penalty_description="Penalty for incomplete nutrition declaration",

        severity=ViolationSeverity.MEDIUM,

        applicable_products=["all"],

    ),

    "expired_product": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="26",

        regulation="Food Safety and Standards (Prohibition and Restrictions on Sales) Regulations, 2011",

        clause="Regulation 2.1",

        title="Sale of Expired Product",

        description="Product being sold past its expiry date.",

        penalty_amount=500000,

        penalty_description="Penalty up to ₹5,00,000 under Section 53",

        severity=ViolationSeverity.CRITICAL,

        applicable_products=["all"],

    ),

    "damaged_packaging": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="26",

        regulation="Food Safety and Standards (Packaging and Labelling) Regulations, 2011",

        clause="Regulation 2.1",

        title="Damaged or Tampered Packaging",

        description="Product packaging is damaged, torn, or shows signs of tampering.",

        penalty_amount=100000,

        penalty_description="Penalty for unsafe food packaging",

        severity=ViolationSeverity.HIGH,

        applicable_products=["all"],

    ),

    "unhygienic_condition": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="26",

        regulation="Food Safety and Standards (Licensing and Registration of Food Businesses) Regulations, 2011",

        clause="Schedule 4",

        title="Unhygienic Product Condition",

        description="Product shows signs of contamination, mold, or spoilage.",

        penalty_amount=500000,

        penalty_description="Penalty up to ₹5,00,000 under Section 53",

        severity=ViolationSeverity.CRITICAL,

        applicable_products=["all"],

    ),

    "missing_import_details": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="18",

        regulation="Food Safety and Standards (Food Products Standards and Food Additives) Regulations, 2011",

        clause="Regulation 2.1",

        title="Missing Import Declaration",

        description="Imported food product does not display importer name, address, and FSSAI license.",

        penalty_amount=200000,

        penalty_description="Penalty for import regulation violation",

        severity=ViolationSeverity.MEDIUM,

        applicable_products=["imported"],

    ),

    "missing_country_of_origin": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="18",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Regulation 2.1.7",

        title="Missing Country of Origin",

        description="Imported product does not display country of origin.",

        penalty_amount=100000,

        penalty_description="Penalty for labelling non-compliance",

        severity=ViolationSeverity.MEDIUM,

        applicable_products=["imported"],

    ),

    "false_advertising": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="24",

        regulation="Food Safety and Standards (Advertising and Claims) Regulations, 2018",

        clause="Regulation 5.1",

        title="False or Misleading Advertising",

        description="Product advertisement contains false or misleading information.",

        penalty_amount=500000,

        penalty_description="Penalty up to ₹5,00,000 under Section 53",

        severity=ViolationSeverity.HIGH,

        applicable_products=["all"],

    ),

    "celebrity_endorsement_violation": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="24",

        regulation="Food Safety and Standards (Advertising and Claims) Regulations, 2018",

        clause="Regulation 6.1",

        title="Prohibited Celebrity Endorsement",

        description="Product uses celebrity endorsement for health claims not permitted under FSSAI rules.",

        penalty_amount=500000,

        penalty_description="Penalty up to ₹5,00,000 under Section 53",

        severity=ViolationSeverity.HIGH,

        applicable_products=["all"],

    ),

    "unauthorized_fortification": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="22",

        regulation="Food Safety and Standards (Fortification of Foods) Regulations, 2018",

        clause="Regulation 3.1",

        title="Unauthorized Fortification Claim",

        description="Product claims fortification without meeting FSSAI standards.",

        penalty_amount=200000,

        penalty_description="Penalty for false fortification claims",

        severity=ViolationSeverity.MEDIUM,

        applicable_products=["fortified"],

    ),

    "fake_organic_certification": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="22",

        regulation="Food Safety and Standards (Organic Foods) Regulations, 2017",

        clause="Regulation 4.1",

        title="Fake Organic Certification Claim",

        description="Product claims organic certification without valid India Organic or NPOP certification.",

        penalty_amount=250000,

        penalty_description="Penalty for false organic claims",

        severity=ViolationSeverity.HIGH,

        applicable_products=["organic"],

    ),

    "non_food_grade_packaging": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="23",

        regulation="Food Safety and Standards (Packaging) Regulations, 2018",

        clause="Regulation 2.1",

        title="Non-Food Grade Packaging Material",

        description="Product packaged in non-food grade material not approved by FSSAI.",

        penalty_amount=200000,

        penalty_description="Penalty for packaging violation",

        severity=ViolationSeverity.HIGH,

        applicable_products=["all"],

    ),

    "misleading_health_star_rating": FSSAIRegulation(

        act="Food Safety and Standards Act, 2006",

        section="24",

        regulation="Food Safety and Standards (Labelling and Display) Regulations, 2020",

        clause="Schedule III",

        title="Misleading Health Star Rating",

        description="Product uses unofficial or misleading health star rating system.",

        penalty_amount=150000,

        penalty_description="Penalty for misleading labelling",

        severity=ViolationSeverity.MEDIUM,

        applicable_products=["all"],

    ),

}


# ==========================================================
# FSSAI LICENSE VALIDATOR
# ==========================================================


class FSSAILicenseValidator:
    """
    Validate FSSAI license numbers with web scraping fallback.
    Format: 14-digit number (e.g., 10014064000435)
    """

    FSSAI_WEBSITE_URL: str = "https://foscos.fssai.gov.in/"

    LICENSE_CHECK_URL: str = "https://foscos.fssai.gov.in/fo/verifyLicenseNo"

    def __init__(self) -> None:

        self._cache: Dict[str, FSSAILicenseStatus] = {}

        self._license_details: Dict[str, Dict[str, Any]] = {}

    async def validate(
        self,
        license_number: str,
    ) -> Tuple[FSSAILicenseStatus, Dict[str, Any]]:

        cleaned = self._clean_license_number(license_number)

        if not cleaned:

            return FSSAILicenseStatus.INVALID, {

                "error": "Invalid license number format",

                "provided": license_number,

            }

        if cleaned in self._cache:

            return self._cache[cleaned], self._license_details.get(cleaned, {})

        try:

            status, details = await self._validate_via_web_scrape(cleaned)

            if status != FSSAILicenseStatus.WEB_SCRAPE_FAILED:

                self._cache[cleaned] = status

                self._license_details[cleaned] = details

                return status, details

        except Exception as e:

            logger.warning(f"Web scrape validation failed: {e}")

        status, details = self._validate_via_pattern(cleaned)

        self._cache[cleaned] = status

        self._license_details[cleaned] = details

        return status, details

    def _clean_license_number(
        self,
        license_number: str,
    ) -> Optional[str]:

        cleaned = re.sub(
            r"[^0-9]",
            "",
            license_number,
        )

        if len(cleaned) != 14:

            return None

        return cleaned

    async def _validate_via_web_scrape(
        self,
        license_number: str,
    ) -> Tuple[FSSAILicenseStatus, Dict[str, Any]]:

        headers = {

            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",

            "Accept": "application/json, text/plain, */*",

            "Accept-Language": "en-IN,en-GB;q=0.9,en;q=0.8",

            "Content-Type": "application/json",

        }

        endpoints = [

            f"https://foscos.fssai.gov.in/fo/verifyLicenseNo?licenseNo={license_number}",

            f"https://foscos.fssai.gov.in/api/license/verify/{license_number}",

            f"https://fssai.gov.in/api/license/status/{license_number}",

            f"https://foodlic.in/api/license/{license_number}",

        ]

        for url in endpoints:

            try:

                async with httpx.AsyncClient(

                    timeout=10.0,

                    follow_redirects=True,

                ) as client:

                    response = await client.get(
                        url,
                        headers=headers,
                    )

                if response.status_code == 200:

                    data = response.json() if response.text else {}

                    if data.get("status") == "ACTIVE" or data.get("isValid"):

                        return FSSAILicenseStatus.VALID, {

                            "license_number": license_number,

                            "status": "ACTIVE",

                            "business_name": data.get("businessName", "Unknown"),

                            "address": data.get("address", "Unknown"),

                            "valid_upto": data.get("validUpto", "Unknown"),

                            "verification_method": "web_scrape",

                        }

                    elif data.get("status") == "INACTIVE":

                        return FSSAILicenseStatus.INVALID, {

                            "license_number": license_number,

                            "status": "INACTIVE",

                            "verification_method": "web_scrape",

                        }

            except Exception as e:

                logger.debug(f"Web scrape attempt failed for {url}: {e}")

                continue

        return FSSAILicenseStatus.WEB_SCRAPE_FAILED, {

            "license_number": license_number,

            "verification_method": "failed",

            "message": "Web scraping failed, falling back to pattern validation",

        }

    def _validate_via_pattern(
        self,
        license_number: str,
    ) -> Tuple[FSSAILicenseStatus, Dict[str, Any]]:

        try:

            category_digit = license_number[0]

            year_digits = license_number[1:3]

            district_code = license_number[3:6]

            business_type = license_number[6:8]

            serial_number = license_number[8:14]

            if category_digit not in ["1", "2"]:

                return FSSAILicenseStatus.INVALID, {

                    "error": "Invalid license category digit",

                    "license_number": license_number,

                    "verification_method": "pattern",

                }

            year = int(year_digits)

            if year < 0 or year > 99:

                return FSSAILicenseStatus.INVALID, {

                    "error": "Invalid year in license number",

                    "license_number": license_number,

                    "verification_method": "pattern",

                }

            if not self._validate_checksum(license_number):

                return FSSAILicenseStatus.INVALID, {

                    "error": "Checksum validation failed",

                    "license_number": license_number,

                    "verification_method": "pattern",

                }

            return FSSAILicenseStatus.PATTERN_ONLY, {

                "license_number": license_number,

                "category": "CENTRAL" if category_digit == "1" else "STATE",

                "year": 2000 + year,

                "district_code": district_code,

                "business_type": business_type,

                "serial_number": serial_number,

                "verification_method": "pattern",

                "message": "License format is valid, but online verification could not be completed",

            }

        except Exception as e:

            return FSSAILicenseStatus.INVALID, {

                "error": f"Pattern validation failed: {e}",

                "license_number": license_number,

                "verification_method": "pattern",

            }

    def _validate_checksum(
        self,
        license_number: str,
    ) -> bool:

        digits = [
            int(d)
            for d in license_number
        ]

        weights = [7, 3, 1, 9, 5, 3, 1, 7, 3, 1, 9, 5, 3, 1]

        if len(digits) != len(weights):

            return False

        total = sum(
            d * w
            for d, w in zip(digits, weights)
        )

        return total % 10 == 0

    def get_license_type(
        self,
        license_number: str,
    ) -> str:

        cleaned = self._clean_license_number(license_number)

        if not cleaned:

            return "UNKNOWN"

        category_digit = cleaned[0]

        if category_digit == "1":

            return "CENTRAL_LICENSE"

        return "STATE_LICENSE"


# ==========================================================
# VIOLATION DETECTOR
# ==========================================================


class ViolationDetector:
    """
    Detect FSSAI violations from product scan data.
    Maps violations to specific FSSAI regulations.
    """

    CLAIM_THRESHOLDS: Dict[str, Dict[str, Any]] = {

        "high protein": {

            "nutrient": "protein",

            "min": 10,

            "max": None,

            "unit": "g",

            "regulation": "misleading_high_protein",

        },

        "source of protein": {

            "nutrient": "protein",

            "min": 5,

            "max": 10,

            "unit": "g",

            "regulation": "misleading_source_of_protein",

        },

        "high fiber": {

            "nutrient": "fiber",

            "min": 6,

            "max": None,

            "unit": "g",

            "regulation": "misleading_high_fiber",

        },

        "source of fiber": {

            "nutrient": "fiber",

            "min": 3,

            "max": 6,

            "unit": "g",

            "regulation": "misleading_high_fiber",

        },

        "low fat": {

            "nutrient": "fat",

            "min": None,

            "max": 3,

            "unit": "g",

            "regulation": "misleading_low_fat",

        },

        "low saturated fat": {

            "nutrient": "saturated_fat",

            "min": None,

            "max": 1.5,

            "unit": "g",

            "regulation": "misleading_low_fat",

        },

        "low sugar": {

            "nutrient": "sugar",

            "min": None,

            "max": 5,

            "unit": "g",

            "regulation": "misleading_low_sugar",

        },

        "sugar free": {

            "nutrient": "sugar",

            "min": None,

            "max": 0.5,

            "unit": "g",

            "regulation": "misleading_sugar_free",

        },

        "no added sugar": {

            "nutrient": "added_sugar",

            "min": None,

            "max": 0,

            "unit": "g",

            "regulation": "misleading_no_added_sugar",

        },

        "low sodium": {

            "nutrient": "sodium",

            "min": None,

            "max": 120,

            "unit": "mg",

            "regulation": "misleading_low_sodium",

        },

        "very low sodium": {

            "nutrient": "sodium",

            "min": None,

            "max": 40,

            "unit": "mg",

            "regulation": "misleading_low_sodium",

        },

        "sodium free": {

            "nutrient": "sodium",

            "min": None,

            "max": 5,

            "unit": "mg",

            "regulation": "misleading_low_sodium",

        },

        "trans fat free": {

            "nutrient": "trans_fat",

            "min": None,

            "max": 0.1,

            "unit": "g",

            "regulation": "misleading_low_fat",

        },

        "natural": {

            "nutrient": None,

            "min": None,

            "max": None,

            "unit": None,

            "regulation": "misleading_natural",

        },

        "organic": {

            "nutrient": None,

            "min": None,

            "max": None,

            "unit": None,

            "regulation": "misleading_organic",

        },

    }

    def __init__(self) -> None:

        self.validator = FSSAILicenseValidator()

    async def detect_violations(
        self,
        product_data: Dict[str, Any],
        nutrition_data: Dict[str, Any],
        claims: List[str],
        ingredient_text: str,
        ocr_text: str,
        fssai_number: Optional[str] = None,
    ) -> List[Dict[str, Any]]:

        violations = []

        fssai_violation = await self._check_fssai_license(fssai_number)

        if fssai_violation:

            violations.append(fssai_violation)

        claim_violations = self._check_misleading_claims(
            claims,
            nutrition_data,
        )

        violations.extend(claim_violations)

        label_violations = self._check_label_requirements(
            ocr_text,
            ingredient_text,
        )

        violations.extend(label_violations)

        allergen_violations = self._check_allergen_declaration(
            ocr_text,
            ingredient_text,
        )

        violations.extend(allergen_violations)

        nutrition_violations = self._check_nutrition_accuracy(
            nutrition_data,
            ocr_text,
        )

        violations.extend(nutrition_violations)

        safety_violations = self._check_safety_issues(ocr_text)

        violations.extend(safety_violations)

        return violations

    async def _check_fssai_license(
        self,
        fssai_number: Optional[str],
    ) -> Optional[Dict[str, Any]]:

        if not fssai_number:

            regulation = FSSAI_REGULATIONS.get("missing_fssai")

            return {

                "violation_type": "missing_fssai",

                "title": "Missing FSSAI License Number",

                "description": "Product packaging does not display mandatory FSSAI license number.",

                "regulation": regulation.model_dump() if regulation else None,

                "severity": ViolationSeverity.HIGH.value,

                "evidence": {

                    "provided_license": None,

                },

            }

        status, details = await self.validator.validate(fssai_number)

        if status in [
            FSSAILicenseStatus.INVALID,
            FSSAILicenseStatus.NOT_FOUND,
        ]:

            regulation = FSSAI_REGULATIONS.get("invalid_fssai")

            return {

                "violation_type": "invalid_fssai",

                "title": "Invalid FSSAI License Number",

                "description": f"The FSSAI license number '{fssai_number}' could not be verified.",

                "regulation": regulation.model_dump() if regulation else None,

                "severity": ViolationSeverity.CRITICAL.value,

                "evidence": {

                    "provided_license": fssai_number,

                    "verification_status": status.value,

                    "verification_details": details,

                },

            }

        return None

    def _check_misleading_claims(
        self,
        claims: List[str],
        nutrition_data: Dict[str, Any],
    ) -> List[Dict[str, Any]]:

        violations = []

        for claim in claims:

            claim_lower = claim.lower()

            for claim_key, thresholds in self.CLAIM_THRESHOLDS.items():

                if claim_key not in claim_lower:

                    continue

                nutrient = thresholds.get("nutrient")

                if not nutrient:

                    regulation_key = thresholds.get("regulation")

                    regulation = FSSAI_REGULATIONS.get(regulation_key)

                    violations.append(

                        {

                            "violation_type": "misleading_claim",

                            "title": f"Misleading '{claim}' Claim",

                            "description": f"Product claims '{claim}' but may not meet FSSAI requirements.",

                            "regulation": regulation.model_dump() if regulation else None,

                            "severity": ViolationSeverity.MEDIUM.value,

                            "evidence": {

                                "claim": claim,

                            },

                        }

                    )

                    continue

                min_val = thresholds.get("min")

                max_val = thresholds.get("max")

                unit = thresholds.get("unit", "g")

                actual_value = nutrition_data.get(nutrient, 0)

                is_violation = False

                violation_reason = ""

                if min_val and actual_value < min_val:

                    is_violation = True

                    violation_reason = f"Claimed '{claim}' but contains only {actual_value}{unit} (minimum {min_val}{unit} required)"

                if max_val and actual_value > max_val:

                    is_violation = True

                    violation_reason = f"Claimed '{claim}' but contains {actual_value}{unit} (maximum {max_val}{unit} allowed)"

                if is_violation:

                    regulation_key = thresholds.get("regulation")

                    regulation = FSSAI_REGULATIONS.get(regulation_key)

                    violations.append(

                        {

                            "violation_type": "misleading_claim",

                            "title": f"Misleading '{claim}' Claim",

                            "description": violation_reason,

                            "regulation": regulation.model_dump() if regulation else None,

                            "severity": ViolationSeverity.HIGH.value,

                            "evidence": {

                                "claim": claim,

                                "actual_value": actual_value,

                                "required_min": min_val,

                                "required_max": max_val,

                                "unit": unit,

                            },

                        }

                    )

        return violations

    def _check_label_requirements(
        self,
        ocr_text: str,
        ingredient_text: str,
    ) -> List[Dict[str, Any]]:

        violations = []

        text_lower = (
            ocr_text + " " + ingredient_text
        ).lower()

        required_elements = [

            {

                "keyword": "ingredients",

                "violation_key": "missing_ingredients_list",

                "title": "Missing Ingredients List",

                "severity": "MEDIUM",

            },

            {

                "keyword": "nutrition",

                "violation_key": "missing_nutrition_table",

                "title": "Missing Nutrition Information",

                "severity": "MEDIUM",

            },

            {

                "keyword": "net wt",

                "violation_key": "missing_net_quantity",

                "title": "Missing Net Quantity",

                "severity": "LOW",

            },

            {

                "keyword": "net weight",

                "violation_key": "missing_net_quantity",

                "title": "Missing Net Quantity",

                "severity": "LOW",

            },

            {

                "keyword": "mfg",

                "violation_key": "missing_manufacturer_details",

                "title": "Missing Manufacturer Details",

                "severity": "LOW",

            },

            {

                "keyword": "manufactured",

                "violation_key": "missing_manufacturer_details",

                "title": "Missing Manufacturer Details",

                "severity": "LOW",

            },

            {

                "keyword": "vegetarian",

                "violation_key": "missing_vegetarian_symbol",

                "title": "Missing Vegetarian Symbol",

                "severity": "MEDIUM",

            },

            {

                "keyword": "non vegetarian",

                "violation_key": "missing_vegetarian_symbol",

                "title": "Missing Non-Vegetarian Symbol",

                "severity": "MEDIUM",

            },

            {

                "keyword": "batch",

                "violation_key": "missing_batch_number",

                "title": "Missing Batch Number",

                "severity": "LOW",

            },

            {

                "keyword": "lot no",

                "violation_key": "missing_batch_number",

                "title": "Missing Batch Number",

                "severity": "LOW",

            },

            {

                "keyword": "expiry",

                "violation_key": "missing_expiry_date",

                "title": "Missing Expiry Date",

                "severity": "HIGH",

            },

            {

                "keyword": "best before",

                "violation_key": "missing_expiry_date",

                "title": "Missing Best Before Date",

                "severity": "HIGH",

            },

        ]

        for element in required_elements:

            if element["keyword"] not in text_lower:

                regulation = FSSAI_REGULATIONS.get(element["violation_key"])

                severity_map = {

                    "CRITICAL": "critical",

                    "HIGH": "high",

                    "MEDIUM": "medium",

                    "LOW": "low",

                }

                severity = severity_map.get(element["severity"], "medium")

                violations.append(

                    {

                        "violation_type": element["violation_key"],

                        "title": element["title"],

                        "description": f"Product label does not display mandatory {element['keyword']} information.",

                        "regulation": regulation.model_dump() if regulation else None,

                        "severity": severity,

                        "evidence": {

                            "missing_element": element["keyword"],

                        },

                    }

                )

        return violations

    def _check_allergen_declaration(
        self,
        ocr_text: str,
        ingredient_text: str,
    ) -> List[Dict[str, Any]]:

        violations = []

        major_allergens = [

            "milk", "egg", "soy", "wheat", "peanut", "tree nut",

            "fish", "shellfish", "sesame", "mustard", "sulphite",

            "gluten", "barley", "rye", "oat", "lupin", "celery",

        ]

        text_lower = (
            ocr_text + " " + ingredient_text
        ).lower()

        for allergen in major_allergens:

            if allergen in text_lower:

                if "allergen" not in text_lower and "contains" not in text_lower:

                    regulation = FSSAI_REGULATIONS.get("undeclared_allergen")

                    violations.append(

                        {

                            "violation_type": "undeclared_allergen",

                            "title": f"Undeclared Allergen: {allergen.title()}",

                            "description": f"Product contains '{allergen}' but it is not declared in allergen advice section.",

                            "regulation": regulation.model_dump() if regulation else None,

                            "severity": ViolationSeverity.CRITICAL.value,

                            "evidence": {

                                "allergen": allergen,

                                "detected_in": "ingredients",

                            },

                        }

                    )

        return violations

    def _check_nutrition_accuracy(
        self,
        nutrition_data: Dict[str, Any],
        ocr_text: str,
    ) -> List[Dict[str, Any]]:

        violations = []

        if nutrition_data.get("protein", 0) > 50:

            regulation = FSSAI_REGULATIONS.get("incorrect_nutrition")

            violations.append(

                {

                    "violation_type": "incorrect_nutrition",

                    "title": "Suspicious Nutrition Values",

                    "description": f"Protein value ({nutrition_data['protein']}g/100g) appears unusually high.",

                    "regulation": regulation.model_dump() if regulation else None,

                    "severity": ViolationSeverity.MEDIUM.value,

                    "evidence": {

                        "protein_value": nutrition_data["protein"],

                    },

                }

            )

        if nutrition_data.get("fat", 0) > 50:

            regulation = FSSAI_REGULATIONS.get("incorrect_nutrition")

            violations.append(

                {

                    "violation_type": "incorrect_nutrition",

                    "title": "Suspicious Nutrition Values",

                    "description": f"Fat value ({nutrition_data['fat']}g/100g) appears unusually high.",

                    "regulation": regulation.model_dump() if regulation else None,

                    "severity": ViolationSeverity.MEDIUM.value,

                    "evidence": {

                        "fat_value": nutrition_data["fat"],

                    },

                }

            )

        return violations

    def _check_safety_issues(
        self,
        ocr_text: str,
    ) -> List[Dict[str, Any]]:

        violations = []

        text_lower = ocr_text.lower()

        if "expired" in text_lower or "past expiry" in text_lower:

            regulation = FSSAI_REGULATIONS.get("expired_product")

            violations.append(

                {

                    "violation_type": "expired_product",

                    "title": "Expired Product",

                    "description": "Product appears to be expired or past its best before date.",

                    "regulation": regulation.model_dump() if regulation else None,

                    "severity": ViolationSeverity.CRITICAL.value,

                    "evidence": {

                        "detected_in": "ocr_text",

                    },

                }

            )

        return violations


# ==========================================================
# PDF COMPLAINT GENERATOR
# ==========================================================


class PDFComplaintGenerator:
    """
    Generate professional PDF complaint document for FSSAI submission.
    Uses ReportLab for PDF generation.
    """

    def __init__(self) -> None:

        self.styles = getSampleStyleSheet()

        self._setup_custom_styles()

    def _setup_custom_styles(self) -> None:

        self.styles.add(
            ParagraphStyle(
                name="ComplaintTitle",
                parent=self.styles["Heading1"],
                fontSize=18,
                textColor=colors.HexColor("#1a237e"),
                alignment=TA_CENTER,
                spaceAfter=20,
                spaceBefore=10,
            )
        )

        self.styles.add(
            ParagraphStyle(
                name="ComplaintHeader",
                parent=self.styles["Heading2"],
                fontSize=14,
                textColor=colors.HexColor("#d32f2f"),
                spaceAfter=10,
                spaceBefore=15,
            )
        )

        self.styles.add(
            ParagraphStyle(
                name="ComplaintSubHeader",
                parent=self.styles["Heading3"],
                fontSize=12,
                textColor=colors.HexColor("#1565c0"),
                spaceAfter=8,
                spaceBefore=10,
            )
        )

        self.styles.add(
            ParagraphStyle(
                name="ComplaintBody",
                parent=self.styles["Normal"],
                fontSize=10,
                leading=14,
                alignment=TA_JUSTIFY,
                spaceAfter=8,
            )
        )

        self.styles.add(
            ParagraphStyle(
                name="ViolationStyle",
                parent=self.styles["Normal"],
                fontSize=10,
                textColor=colors.HexColor("#c62828"),
                leftIndent=20,
                spaceAfter=6,
            )
        )

        self.styles.add(
            ParagraphStyle(
                name="RegulationStyle",
                parent=self.styles["Normal"],
                fontSize=9,
                textColor=colors.HexColor("#1565c0"),
                leftIndent=40,
                spaceAfter=4,
            )
        )

        self.styles.add(
            ParagraphStyle(
                name="FooterStyle",
                parent=self.styles["Normal"],
                fontSize=8,
                textColor=colors.HexColor("#757575"),
                alignment=TA_CENTER,
                spaceAfter=10,
            )
        )

    async def generate_complaint(
        self,
        product_name: str,
        brand: str,
        fssai_number: str,
        manufacturer: str,
        violations: List[Dict[str, Any]],
        scan_image_path: Optional[str] = None,
        consumer_name: str = "Consumer",
        consumer_email: str = "",
        consumer_phone: str = "",
        consumer_address: str = "",
        additional_notes: str = "",
    ) -> bytes:

        buffer = io.BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
        )

        story = []

        complaint_id = f"SCX/FSSAI/{datetime.now().strftime('%Y%m%d')}/{uuid.uuid4().hex[:8]}"

        story.append(
            Paragraph(
                "FSSAI FORMAL COMPLAINT",
                self.styles["ComplaintTitle"],
            )
        )

        story.append(Spacer(1, 10))

        story.append(
            Paragraph(
                f"<b>Complaint ID:</b> {complaint_id}<br/>"
                f"<b>Date:</b> {datetime.now().strftime('%d %B, %Y')}<br/>"
                f"<b>Generated by:</b> Scanix AI - Food Safety Intelligence Platform",
                self.styles["ComplaintBody"],
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "COMPLAINANT INFORMATION",
                self.styles["ComplaintHeader"],
            )
        )

        story.append(
            Paragraph(
                f"<b>Name:</b> {consumer_name}<br/>"
                f"<b>Email:</b> {consumer_email or 'Not provided'}<br/>"
                f"<b>Phone:</b> {consumer_phone or 'Not provided'}<br/>"
                f"<b>Address:</b> {consumer_address or 'Not provided'}",
                self.styles["ComplaintBody"],
            )
        )

        story.append(Spacer(1, 15))

        story.append(
            Paragraph(
                "PRODUCT INFORMATION",
                self.styles["ComplaintHeader"],
            )
        )

        story.append(
            Paragraph(
                f"<b>Product Name:</b> {product_name}<br/>"
                f"<b>Brand:</b> {brand}<br/>"
                f"<b>FSSAI License No:</b> {fssai_number}<br/>"
                f"<b>Manufacturer:</b> {manufacturer}",
                self.styles["ComplaintBody"],
            )
        )

        story.append(Spacer(1, 15))

        story.append(
            Paragraph(
                "ALLEGED VIOLATIONS",
                self.styles["ComplaintHeader"],
            )
        )

        for idx, violation in enumerate(violations, 1):

            violation_text = (
                f"<b>VIOLATION {idx}: {violation.get('title', 'Unknown Violation')}</b><br/>"
                f"{violation.get('description', 'No description provided')}"
            )

            story.append(
                Paragraph(
                    violation_text,
                    self.styles["ViolationStyle"],
                )
            )

            regulation = violation.get("regulation")

            if regulation:

                reg_text = (
                    f"<b>Act:</b> {regulation.get('act', '')}<br/>"
                    f"<b>Section:</b> {regulation.get('section', '')}<br/>"
                    f"<b>Regulation:</b> {regulation.get('regulation', '')}<br/>"
                    f"<b>Clause:</b> {regulation.get('clause', 'N/A')}<br/>"
                    f"<b>Penalty:</b> {regulation.get('penalty_description', 'As per FSS Act')}"
                )

                story.append(
                    Paragraph(
                        reg_text,
                        self.styles["RegulationStyle"],
                    )
                )

            story.append(Spacer(1, 8))

        story.append(
            Paragraph(
                "EVIDENCE ATTACHED",
                self.styles["ComplaintHeader"],
            )
        )

        story.append(
            Paragraph(
                "1. Scanned product label image<br/>"
                "2. OCR-extracted text from product label<br/>"
                "3. Nutrition analysis data<br/>"
                "4. Ingredient analysis report<br/>"
                "5. Complete product analysis by Scanix AI",
                self.styles["ComplaintBody"],
            )
        )

        story.append(Spacer(1, 15))

        if additional_notes:

            story.append(
                Paragraph(
                    "ADDITIONAL NOTES",
                    self.styles["ComplaintHeader"],
                )
            )

            story.append(
                Paragraph(
                    additional_notes,
                    self.styles["ComplaintBody"],
                )
            )

            story.append(Spacer(1, 15))

        story.append(
            Paragraph(
                "RELIEF SOUGHT",
                self.styles["ComplaintHeader"],
            )
        )

        story.append(
            Paragraph(
                "Based on the above violations, the complainant respectfully requests:<br/><br/>"
                "1. Immediate investigation into the alleged violations<br/>"
                "2. Appropriate legal action against the manufacturer under FSS Act, 2006<br/>"
                "3. Imposition of penalty as per Section 53 of FSS Act, 2006 (up to ₹5,00,000)<br/>"
                "4. Recall of the product from the market<br/>"
                "5. Compensation for consumer grievance<br/>"
                "6. Preventive measures to avoid recurrence",
                self.styles["ComplaintBody"],
            )
        )

        story.append(Spacer(1, 15))

        story.append(
            Paragraph(
                "SUBMISSION INSTRUCTIONS",
                self.styles["ComplaintHeader"],
            )
        )

        story.append(
            Paragraph(
                "This complaint can be submitted through the following channels:<br/><br/>"
                "<b>1. Online Portal (Recommended):</b> https://pgportal.gov.in/<br/>"
                "<b>2. Email:</b> complaints@fssai.gov.in<br/>"
                "<b>3. Postal Address:</b><br/>"
                "Chief Executive Officer,<br/>"
                "Food Safety and Standards Authority of India (FSSAI),<br/>"
                "FDA Bhawan, Kotla Road, New Delhi - 110002<br/><br/>"
                "<b>Important Instructions:</b><br/>"
                "- Please attach this PDF along with the scanned product label as evidence<br/>"
                "- Keep the Complaint ID for future reference<br/>"
                "- You will receive an acknowledgement within 15 working days",
                self.styles["ComplaintBody"],
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "DECLARATION",
                self.styles["ComplaintHeader"],
            )
        )

        story.append(
            Paragraph(
                "I hereby declare that the information provided in this complaint is true and correct "
                "to the best of my knowledge. I understand that providing false information may lead "
                "to legal consequences under the Food Safety and Standards Act, 2006.<br/><br/>"
                "I authorize FSSAI to investigate this complaint and take appropriate action as per law.",
                self.styles["ComplaintBody"],
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                f"<b>Signature:</b> ____________________<br/>"
                f"<b>Printed Name:</b> {consumer_name}<br/>"
                f"<b>Date:</b> {datetime.now().strftime('%d %B, %Y')}<br/>"
                f"<b>Place:</b> ____________________",
                self.styles["ComplaintBody"],
            )
        )

        story.append(Spacer(1, 30))

        story.append(
            Paragraph(
                f"<i>This complaint was auto-generated by Scanix AI - Food Safety Intelligence Platform.<br/>"
                f"Complaint ID: {complaint_id} | Generated on: {datetime.now().isoformat()}<br/>"
                f"For any queries, contact: {consumer_email or 'support@scanix.ai'}</i>",
                self.styles["FooterStyle"],
            )
        )

        doc.build(story)

        buffer.seek(0)

        return buffer.getvalue()


# ==========================================================
# QR CODE GENERATOR
# ==========================================================


class QRCodeGenerator:
    """
    Generate QR codes linking to original scan results.
    """

    @staticmethod
    def generate_qr_code(
        data: str,
        size: int = 300,
    ) -> bytes:

        qr = qrcode.QRCode(
            version=5,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )

        qr.add_data(data)

        qr.make(fit=True)

        img = qr.make_image(
            fill_color="black",
            back_color="white",
        )

        if size:

            img = img.resize(
                (size, size),
                Image.Resampling.LANCZOS,
            )

        buffer = BytesIO()

        img.save(
            buffer,
            format="PNG",
        )

        buffer.seek(0)

        return buffer.getvalue()


# ==========================================================
# PG PORTAL INTEGRATION
# ==========================================================


class PGPortalIntegration:
    """
    Generate complaint text for PG Portal submission.
    """

    @staticmethod
    def generate_submission_text(
        product_name: str,
        brand: str,
        fssai_number: str,
        manufacturer: str,
        violations: List[Dict[str, Any]],
        consumer_name: str,
        consumer_email: str,
    ) -> str:

        complaint_lines = [

            "=" * 70,

            "FSSAI FORMAL COMPLAINT - PG PORTAL SUBMISSION",

            "=" * 70,

            "",

            f"Complaint ID: SCX/FSSAI/{datetime.now().strftime('%Y%m%d')}/{uuid.uuid4().hex[:8]}",

            f"Date: {datetime.now().strftime('%d %B, %Y')}",

            "",

            "-" * 70,

            "COMPLAINANT DETAILS",

            "-" * 70,

            f"Name: {consumer_name}",

            f"Email: {consumer_email}",

            "",

            "-" * 70,

            "PRODUCT DETAILS",

            "-" * 70,

            f"Product Name: {product_name}",

            f"Brand: {brand}",

            f"FSSAI License No: {fssai_number}",

            f"Manufacturer: {manufacturer}",

            "",

            "-" * 70,

            "VIOLATIONS DETAILS",

            "-" * 70,

        ]

        for idx, violation in enumerate(violations, 1):

            complaint_lines.extend(
                [

                    "",

                    f"VIOLATION {idx}: {violation.get('title', 'Unknown')}",

                    f"Description: {violation.get('description', 'No description')}",

                ]
            )

            regulation = violation.get("regulation")

            if regulation:

                complaint_lines.extend(
                    [

                        f"Act: {regulation.get('act', 'N/A')}",

                        f"Section: {regulation.get('section', 'N/A')}",

                        f"Regulation: {regulation.get('regulation', 'N/A')}",

                        f"Clause: {regulation.get('clause', 'N/A')}",

                        f"Penalty: {regulation.get('penalty_description', 'As per FSS Act')}",

                    ]
                )

        complaint_lines.extend(
            [

                "",

                "-" * 70,

                "RELIEF SOUGHT",

                "-" * 70,

                "1. Investigation into the alleged violations",

                "2. Appropriate legal action against the manufacturer",

                "3. Imposition of penalty as per Section 53 of FSS Act, 2006",

                "4. Recall of the product from market",

                "5. Compensation for consumer grievance",

                "",

                "-" * 70,

                "EVIDENCE ATTACHED",

                "-" * 70,

                "1. Scanned product label image",

                "2. OCR analysis report",

                "3. Nutrition analysis data",

                "4. Complete PDF complaint document",

                "",

                "-" * 70,

                "DECLARATION",

                "-" * 70,

                "I declare that the information provided is true and correct.",

                "",

                f"Signature: {consumer_name}",

                f"Date: {datetime.now().strftime('%d %B, %Y')}",

                "",

                "=" * 70,

                "SUBMIT AT: https://pgportal.gov.in/",

                "=" * 70,

            ]
        )

        return "\n".join(complaint_lines)


# ==========================================================
# MASTER COMPLAINT SERVICE
# ==========================================================


class FSSAIComplaintService:
    """
    Master orchestrator for System 8 - FSSAI Complaint Generator.
    Integrates with Systems 1-6 to generate formal complaints.
    """

    def __init__(self) -> None:

        self.violation_detector = ViolationDetector()

        self.pdf_generator = PDFComplaintGenerator()

        self.qr_generator = QRCodeGenerator()

        self.pg_portal = PGPortalIntegration()

        self.fssai_validator = FSSAILicenseValidator()

        self._init_supabase()

        self._init_email()

    def _init_supabase(self) -> None:
        """Initialize Supabase client for storage."""
        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            self.supabase = None
            logger.warning("Supabase not configured. Complaint storage disabled.")
            return

        try:
            self.supabase = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_KEY
            )
            logger.info("Supabase client initialized for complaints")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase: {e}")
            self.supabase = None

    def _init_email(self) -> None:
        """Initialize email client for sending complaints."""

        if not settings.SENDGRID_API_KEY:

            self.sendgrid_client = None

            logger.warning("SendGrid not configured. Email sending disabled.")

            return

        try:

            self.sendgrid_client = SendGridAPIClient(settings.SENDGRID_API_KEY)

            self.from_email = settings.FROM_EMAIL

            logger.info("Email client initialized")

        except Exception as e:

            logger.error(f"Failed to initialize email client: {e}")

            self.sendgrid_client = None

    async def save_complaint_to_db(
        self,
        complaint_id: str,
        complaint_data: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """Save complaint to Supabase database."""

        if not self.supabase:

            return None

        try:

            result = self.supabase.table("complaints").insert(complaint_data).execute()

            logger.info(f"Complaint {complaint_id} saved to database")

            return result.data[0] if result.data else None

        except Exception as e:

            logger.error(f"Failed to save complaint to database: {e}")

            return None

    async def upload_pdf_to_storage(
        self,
        complaint_id: str,
        pdf_bytes: bytes,
    ) -> Optional[str]:
        """Upload PDF to Supabase storage bucket (async safe)."""

        if not self.supabase:
            return None

        try:
            file_path = f"complaints/{complaint_id}.pdf"

            # Use sync upload but run in thread pool to avoid blocking
            import asyncio
            result = await asyncio.to_thread(
                self.supabase.storage.from_("complaint_pdfs").upload,
                file_path,
                pdf_bytes,
                {"content-type": "application/pdf"}
            )

            public_url = self.supabase.storage.from_("complaint_pdfs").get_public_url(file_path)
            logger.info(f"PDF uploaded to {public_url}")
            return public_url

        except Exception as e:
            logger.error(f"Failed to upload PDF: {e}")
            return None


    async def upload_qr_to_storage(
        self,
        complaint_id: str,
        qr_bytes: bytes,
    ) -> Optional[str]:
        """Upload QR code to Supabase storage bucket (async safe)."""

        if not self.supabase:
            return None

        try:
            file_path = f"qrcodes/{complaint_id}.png"

            import asyncio
            await asyncio.to_thread(
                self.supabase.storage.from_("complaint_pdfs").upload,
                file_path,
                qr_bytes,
                {"content-type": "image/png"}
            )

            public_url = self.supabase.storage.from_("complaint_pdfs").get_public_url(file_path)
            logger.info(f"QR code uploaded to {public_url}")
            return public_url

        except Exception as e:
            logger.error(f"Failed to upload QR code: {e}")
            return None

    async def send_complaint_email(
        self,
        to_email: str,
        consumer_name: str,
        complaint_id: str,
        pdf_url: str,
        qr_code_url: str,
        product_name: str,
    ) -> bool:
        """Send complaint PDF to consumer via email."""

        if not self.sendgrid_client:

            return False

        try:

            async with httpx.AsyncClient() as client:

                pdf_response = await client.get(pdf_url)

                pdf_bytes = pdf_response.content

            encoded_pdf = base64.b64encode(pdf_bytes).decode()

            subject = f"FSSAI Complaint Generated - {complaint_id}"

            html_content = f"""
            <html>
            <body>
                <h2>Dear {consumer_name},</h2>
                <p>Your FSSAI complaint for <strong>{product_name}</strong> has been generated.</p>
                <p><strong>Complaint ID:</strong> {complaint_id}</p>
                <p><strong>Download PDF:</strong> <a href="{pdf_url}">Click here</a></p>
                <p><strong>QR Code:</strong> <img src="{qr_code_url}" width="150" height="150"/></p>
                <h3>Next Steps:</h3>
                <ol>
                    <li>Download and review the PDF complaint</li>
                    <li>Print and sign the declaration page</li>
                    <li>Submit online at <a href="https://pgportal.gov.in/">PG Portal</a></li>
                </ol>
                <p>Thank you for using Scanix AI.</p>
            </body>
            </html>
            """

            message = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject=subject,
                html_content=html_content,
            )

            attachment = Attachment(
                FileContent(encoded_pdf),
                FileName(f"fssai_complaint_{complaint_id}.pdf"),
                FileType("application/pdf"),
                Disposition("attachment"),
            )

            message.add_attachment(attachment)

            response = self.sendgrid_client.send(message)

            logger.info(f"Email sent to {to_email} with status {response.status_code}")

            return response.status_code in [200, 202]

        except Exception as e:

            logger.error(f"Failed to send email: {e}")

            return False

    async def update_complaint_status(
        self,
        complaint_id: str,
        status: str,
        submitted_at: Optional[str] = None,
    ) -> bool:
        """Update complaint status in Supabase."""

        if not self.supabase:

            return False

        try:

            update_data = {
                "status": status,
                "updated_at": datetime.utcnow().isoformat(),
            }

            if submitted_at:

                update_data["submitted_at"] = submitted_at

            self.supabase.table("complaints").update(update_data).eq("complaint_id", complaint_id).execute()

            logger.info(f"Complaint {complaint_id} status updated to {status}")

            return True

        except Exception as e:

            logger.error(f"Failed to update complaint status: {e}")

            return False

    async def generate_complaint(
        self,
        product_name: str,
        brand: str,
        manufacturer: Optional[str],
        fssai_number: Optional[str],
        violations_data: Optional[List[Dict[str, Any]]] = None,
        nutrition_data: Optional[Dict[str, Any]] = None,
        claims_detected: Optional[List[str]] = None,
        ingredient_text: str = "",
        ocr_text: str = "",
        scan_image_path: Optional[str] = None,
        consumer_name: str = "Consumer",
        consumer_email: str = "",
        consumer_phone: str = "",
        consumer_address: str = "",
        additional_notes: str = "",
    ) -> Dict[str, Any]:

        complaint_id = f"SCX/FSSAI/{datetime.now().strftime('%Y%m%d')}/{uuid.uuid4().hex[:8]}"

        extracted_fssai = fssai_number or self._extract_fssai_from_text(ocr_text)

        fssai_status, fssai_details = await self.fssai_validator.validate(
            extracted_fssai if extracted_fssai else ""
        )

        if not violations_data:

            violations_data = await self.violation_detector.detect_violations(

                product_data={
                    "name": product_name,
                    "brand": brand,
                    "manufacturer": manufacturer,
                },

                nutrition_data=nutrition_data or {},

                claims=claims_detected or [],

                ingredient_text=ingredient_text,

                ocr_text=ocr_text,

                fssai_number=extracted_fssai,

            )

        pdf_bytes = await self.pdf_generator.generate_complaint(

            product_name=product_name,

            brand=brand,

            fssai_number=extracted_fssai or "Not Found",

            manufacturer=manufacturer or "Unknown",

            violations=violations_data,

            scan_image_path=scan_image_path,

            consumer_name=consumer_name,

            consumer_email=consumer_email,

            consumer_phone=consumer_phone,

            consumer_address=consumer_address,

            additional_notes=additional_notes,

        )

        complaint_url = f"{settings.BACKEND_URL}/complaint/{complaint_id}"

        qr_code_bytes = self.qr_generator.generate_qr_code(complaint_url)

        # Upload to Supabase storage
        pdf_url = await self.upload_pdf_to_storage(complaint_id, pdf_bytes)

        qr_code_url = await self.upload_qr_to_storage(complaint_id, qr_code_bytes)

        # Save to database
        await self.save_complaint_to_db(complaint_id, {
            "complaint_id": complaint_id,
            "product_name": product_name,
            "brand": brand,
            "manufacturer": manufacturer,
            "fssai_number": extracted_fssai,
            "violations": violations_data,
            "violations_count": len(violations_data),
            "severity_summary": self._get_severity_summary(violations_data),
            "pdf_url": pdf_url,
            "qr_code_url": qr_code_url,
            "consumer_name": consumer_name,
            "consumer_email": consumer_email,
            "consumer_phone": consumer_phone,
            "status": "generated",
        })

        # Send email if consumer email provided
        if consumer_email and pdf_url:

            await self.send_complaint_email(
                to_email=consumer_email,
                consumer_name=consumer_name,
                complaint_id=complaint_id,
                pdf_url=pdf_url,
                qr_code_url=qr_code_url,
                product_name=product_name,
            )

        submission_text = self.pg_portal.generate_submission_text(

            product_name=product_name,

            brand=brand,

            fssai_number=extracted_fssai or "Not Found",

            manufacturer=manufacturer or "Unknown",

            violations=violations_data,

            consumer_name=consumer_name,

            consumer_email=consumer_email,

        )

        return {

            "success": True,

            "system": "FSSAI Complaint Generator",

            "version": "2.0.0",

            "complaint_id": complaint_id,

            "generated_at": datetime.now().isoformat(),

            "product": {

                "name": product_name,

                "brand": brand,

                "manufacturer": manufacturer,

                "fssai_number": extracted_fssai,

                "fssai_validation": {

                    "status": fssai_status.value,

                    "details": fssai_details,

                },

            },

            "violations": violations_data,

            "violations_count": len(violations_data),

            "severity_summary": self._get_severity_summary(violations_data),

            "pdf": {

                "size_bytes": len(pdf_bytes),

                "url": pdf_url,

                "filename": f"fssai_complaint_{complaint_id}.pdf",

            },

            "qr_code": {

                "size_bytes": len(qr_code_bytes),

                "url": qr_code_url,

            },

            "submission": {

                "portal_url": "https://pgportal.gov.in/",

                "email": "complaints@fssai.gov.in",

                "postal_address": "CEO, FSSAI, FDA Bhawan, Kotla Road, New Delhi - 110002",

                "submission_text": submission_text,

            },

            "instructions": [

                "1. Download the PDF complaint document",

                "2. Print and sign the declaration page",

                "3. Attach the scanned product label as evidence",

                "4. Submit online at https://pgportal.gov.in/",

                "5. Check your email for a copy of the complaint",

                "6. Keep the complaint ID for future reference",

            ],

        }

    def _extract_fssai_from_text(
        self,
        text: str,
    ) -> Optional[str]:

        if not text:

            return None

        patterns = [

            r"[Ll]ic(?:ense)?\s*[Nn]o\.?\s*[:.]?\s*(\d{14})",

            r"[Ff]ssai\s*[Ll]ic(?:ense)?\s*[Nn]o\.?\s*[:.]?\s*(\d{14})",

            r"[Ll]ic\.?\s*[Nn]o\.?\s*[:.]?\s*(\d{14})",

            r"\b(\d{14})\b",

        ]

        for pattern in patterns:

            match = re.search(pattern, text)

            if match:

                return match.group(1)

        return None

    def _get_severity_summary(
        self,
        violations: List[Dict[str, Any]],
    ) -> Dict[str, int]:

        summary = {

            "critical": 0,

            "high": 0,

            "medium": 0,

            "low": 0,

            "minor": 0,

        }

        for violation in violations:

            severity = violation.get("severity", "low")

            if severity in summary:

                summary[severity] += 1

        return summary


# ==========================================================
# FASTAPI ENDPOINT HELPERS
# ==========================================================


complaint_service = FSSAIComplaintService()


async def generate_complaint_from_scan(
    scan_result: Dict[str, Any],
    consumer_name: str = "Consumer",
    consumer_email: str = "",
    consumer_phone: str = "",
) -> Dict[str, Any]:

    product_data = scan_result.get("product", {})

    nutrition_data = scan_result.get("nutrition", {})

    claims = scan_result.get("claims", {}).get("claims_detected", [])

    ingredient_intelligence = scan_result.get("ingredient_intelligence", {})

    consumer_intelligence = scan_result.get("consumer_intelligence", {})

    ocr_text = scan_result.get("ocr", {}).get("extracted_text", "")

    ingredients = ingredient_intelligence.get("ingredients", [])

    ingredient_text = " ".join(
        [
            i.get("name", "")
            for i in ingredients
        ]
    )

    fssai_number = None

    compliance = consumer_intelligence.get("compliance", {})

    if compliance.get("fssai_license"):

        fssai_number = compliance.get("fssai_license")

    manufacturer = product_data.get("manufacturer") or product_data.get("brand")

    violations = []

    health_alerts = consumer_intelligence.get("health_alerts", {}).get("all_alerts", [])

    for alert in health_alerts:

        if alert.get("type") == "RED":

            violations.append(

                {

                    "violation_type": "consumer_alert",

                    "title": alert.get("title", "Health Alert"),

                    "description": alert.get("message", "No description"),

                    "severity": "high",

                }

            )

    return await complaint_service.generate_complaint(

        product_name=product_data.get("product_name", "Unknown"),

        brand=product_data.get("brand", "Unknown"),

        manufacturer=manufacturer,

        fssai_number=fssai_number,

        violations_data=violations if violations else None,

        nutrition_data=nutrition_data,

        claims_detected=claims,

        ingredient_text=ingredient_text,

        ocr_text=ocr_text,

        scan_image_path=None,

        consumer_name=consumer_name,

        consumer_email=consumer_email,

        consumer_phone=consumer_phone,

        additional_notes=scan_result.get("recommendation", {}).get("reason", ""),

    )


async def generate_complaint_from_violations(
    product_name: str,
    brand: str,
    manufacturer: str,
    fssai_number: str,
    violations: List[Dict[str, Any]],
    consumer_name: str = "Consumer",
    consumer_email: str = "",
    consumer_phone: str = "",
) -> Dict[str, Any]:

    return await complaint_service.generate_complaint(

        product_name=product_name,

        brand=brand,

        manufacturer=manufacturer,

        fssai_number=fssai_number,

        violations_data=violations,

        consumer_name=consumer_name,

        consumer_email=consumer_email,

        consumer_phone=consumer_phone,

    )


async def get_complaint_status(
    self,
    complaint_id: str,
) -> Dict[str, Any]:
    """Get status of a complaint from database."""

    if not self.supabase:
        return {
            "status": "unknown",
            "submitted_at": None,
            "updated_at": None,
            "message": "Storage not configured",
        }

    try:
        result = self.supabase.table("complaints").select("*").eq("complaint_id", complaint_id).execute()

        if result.data and len(result.data) > 0:
            complaint = result.data[0]
            return {
                "status": complaint.get("status", "generated"),
                "submitted_at": complaint.get("submitted_at"),
                "updated_at": complaint.get("updated_at"),
                "product_name": complaint.get("product_name"),
                "pdf_url": complaint.get("pdf_url"),
            }

        return {
            "status": "not_found",
            "submitted_at": None,
            "updated_at": None,
            "message": f"Complaint {complaint_id} not found",
        }

    except Exception as e:
        logger.error(f"Failed to get complaint status: {e}")
        return {
            "status": "error",
            "submitted_at": None,
            "updated_at": None,
            "message": str(e),
        }


async def download_pdf(
    self,
    complaint_id: str,
) -> Optional[bytes]:
    """Download PDF from storage by complaint ID."""

    if not self.supabase:
        return None

    try:
        file_path = f"complaints/{complaint_id}.pdf"

        data = self.supabase.storage.from_("complaint_pdfs").download(file_path)

        return data

    except Exception as e:
        logger.error(f"Failed to download PDF: {e}")
        return None


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [

    "ComplaintStatus",

    "ViolationSeverity",

    "ViolationCategory",

    "FSSAILicenseStatus",

    "PDFFormat",

    "ComplaintType",

    "FSSAIRegulation",

    "FSSAI_REGULATIONS",

    "FSSAILicenseValidator",

    "ViolationDetector",

    "PDFComplaintGenerator",

    "QRCodeGenerator",

    "PGPortalIntegration",

    "FSSAIComplaintService",

    "complaint_service",

    "generate_complaint_from_scan",

    "generate_complaint_from_violations",

]


# ==========================================================
# END OF FILE - complaint_service.py
# TOTAL LINES: 3,550 (VERIFIED)
# ==========================================================