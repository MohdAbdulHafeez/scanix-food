# database/models.py


from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import JSON
from sqlalchemy import TIMESTAMP
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


from .base import Base


# ==========================================================
# USER MODEL
# ==========================================================


class User(Base):

    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
    )

    name = Column(
        String,
        nullable=True,
    )

    picture = Column(
        String,
        nullable=True,
    )

    gmail_id = Column(
        String,
        unique=True,
        nullable=True,
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
    )

    last_login = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
    )


# ==========================================================
# HEALTH PROFILE MODEL
# ==========================================================


class HealthProfile(Base):

    __tablename__ = "health_profiles"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    age = Column(
        Integer,
        nullable=True,
    )

    gender = Column(
        String,
        nullable=True,
    )

    weight_kg = Column(
        Float,
        nullable=True,
    )

    height_cm = Column(
        Float,
        nullable=True,
    )

    conditions = Column(
        JSON,
        nullable=True,
    )

    medications = Column(
        JSON,
        nullable=True,
    )

    allergies = Column(
        JSON,
        nullable=True,
    )

    dietary_preferences = Column(
        JSON,
        nullable=True,
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
    )


# ==========================================================
# USER SCAN MODEL
# ==========================================================


class UserScan(Base):

    __tablename__ = "user_scans"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    scan_id = Column(
        String,
        unique=True,
        nullable=False,
    )

    product_name = Column(
        String,
        nullable=True,
    )

    brand = Column(
        String,
        nullable=True,
    )

    barcode = Column(
        String,
        nullable=True,
    )

    health_score = Column(
        Integer,
        nullable=True,
    )

    sugar_score = Column(
        Float,
        nullable=True,
    )

    sodium_score = Column(
        Float,
        nullable=True,
    )

    fat_score = Column(
        Float,
        nullable=True,
    )

    nova_group = Column(
        Integer,
        nullable=True,
    )

    processing_level = Column(
        String,
        nullable=True,
    )

    deception_score = Column(
        Integer,
        nullable=True,
    )

    adulteration_risk = Column(
        String,
        nullable=True,
    )

    counterfeit_risk = Column(
        String,
        nullable=True,
    )

    trust_score = Column(
        Integer,
        nullable=True,
    )

    scan_data = Column(
        JSON,
        nullable=True,
    )

    scanned_at = Column(
        TIMESTAMP,
        server_default=func.now(),
    )


# ==========================================================
# USER PREFERENCES MODEL
# ==========================================================


class UserPreferences(Base):

    __tablename__ = "user_preferences"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    favorite_brands = Column(
        JSON,
        nullable=True,
    )

    avoided_ingredients = Column(
        JSON,
        nullable=True,
    )

    preferred_categories = Column(
        JSON,
        nullable=True,
    )

    price_sensitivity = Column(
        String,
        default="MEDIUM",
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
    )


# ==========================================================
# BRAND SCAN MODEL
# ==========================================================


class BrandScan(Base):

    __tablename__ = "brand_scans"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    brand_name = Column(
        String,
        nullable=False,
    )

    scan_date = Column(
        TIMESTAMP,
        server_default=func.now(),
    )

    authenticity_score = Column(
        Integer,
        nullable=True,
    )

    violations_count = Column(
        Integer,
        nullable=True,
    )

    is_adulterated = Column(
        Boolean,
        default=False,
    )

    is_counterfeit = Column(
        Boolean,
        default=False,
    )

    product_category = Column(
        String,
        nullable=True,
    )


# ==========================================================
# COMPLAINT MODEL
# ==========================================================


class Complaint(Base):

    __tablename__ = "complaints"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    complaint_id = Column(
        String,
        unique=True,
        nullable=False,
    )

    product_name = Column(
        String,
        nullable=True,
    )

    brand = Column(
        String,
        nullable=True,
    )

    manufacturer = Column(
        String,
        nullable=True,
    )

    fssai_number = Column(
        String,
        nullable=True,
    )

    violations = Column(
        JSON,
        nullable=True,
    )

    violations_count = Column(
        Integer,
        nullable=True,
    )

    severity_summary = Column(
        JSON,
        nullable=True,
    )

    pdf_url = Column(
        String,
        nullable=True,
    )

    qr_code_url = Column(
        String,
        nullable=True,
    )

    consumer_name = Column(
        String,
        nullable=True,
    )

    consumer_email = Column(
        String,
        nullable=True,
    )

    status = Column(
        String,
        default="generated",
    )

    submitted_at = Column(
        TIMESTAMP,
        nullable=True,
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
    )