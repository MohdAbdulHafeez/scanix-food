# database/__init__.py


try:

    from .engine import (
        engine,
        SessionLocal,
        get_db,
        get_db_session,
        check_database_connection,
        get_engine,
        get_session,
        get_session_factory,
        health_check,
        get_pool_status,
    )

except ImportError:

    from database.engine import (
        engine,
        SessionLocal,
        get_db,
        get_db_session,
        check_database_connection,
        get_engine,
        get_session,
        get_session_factory,
        health_check,
        get_pool_status,
    )


from .base import Base

from .models import (
    User,
    HealthProfile,
    UserScan,
    UserPreferences,
    BrandScan,
    Complaint,
)


__all__ = [
    "engine",
    "SessionLocal",
    "get_db",
    "get_db_session",
    "check_database_connection",
    "get_engine",
    "get_session",
    "get_session_factory",
    "health_check",
    "get_pool_status",
    "Base",
    "User",
    "HealthProfile",
    "UserScan",
    "UserPreferences",
    "BrandScan",
    "Complaint",
]