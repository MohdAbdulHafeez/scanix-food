# ==========================================================
# SCANIX AI
# CORE DATABASE – ELITE PRODUCTION GRADE
# ==========================================================


from __future__ import annotations


from typing import Any
from typing import Dict
from typing import Generator
from typing import Optional


from sqlalchemy import (
    create_engine,
    text,
    event,
)
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import (
    Session,
    declarative_base,
    sessionmaker,
)


from core.config import get_settings
from core.logging import log


settings = get_settings()


# ==========================================================
# CONSTANTS
# ==========================================================


DEFAULT_POOL_SIZE: int = 5

DEFAULT_MAX_OVERFLOW: int = 10

DEFAULT_POOL_RECYCLE: int = 3600

DEFAULT_POOL_TIMEOUT: int = 30

DEFAULT_POOL_PRE_PING: bool = True


# ==========================================================
# VALIDATION
# ==========================================================


if not settings.DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is not configured in .env"
    )


# ==========================================================
# ENGINE SETUP
# ==========================================================


engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=DEFAULT_POOL_PRE_PING,
    pool_size=settings.DATABASE_POOL_SIZE or DEFAULT_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW or DEFAULT_MAX_OVERFLOW,
    pool_recycle=DEFAULT_POOL_RECYCLE,
    pool_timeout=DEFAULT_POOL_TIMEOUT,
    future=True,
    echo=settings.DEBUG if hasattr(settings, "DEBUG") else False,
)


# ==========================================================
# EVENT LISTENERS
# ==========================================================


@event.listens_for(engine, "connect")
def receive_connect(
    dbapi_connection: Any,
    connection_record: Any,
) -> None:
    """
    Event listener fired when a new database connection is created.
    """

    log.debug(
        "Database connection established",
        connection_id=id(dbapi_connection),
    )


@event.listens_for(engine, "checkout")
def receive_checkout(
    dbapi_connection: Any,
    connection_record: Any,
    connection_proxy: Any,
) -> None:
    """
    Event listener fired when a connection is checked out from pool.
    """

    log.debug(
        "Database connection checked out",
        connection_id=id(dbapi_connection),
    )


@event.listens_for(engine, "close")
def receive_close(
    dbapi_connection: Any,
    connection_record: Any,
) -> None:
    """
    Event listener fired when a database connection is closed.
    """

    log.debug(
        "Database connection closed",
        connection_id=id(dbapi_connection),
    )


# ==========================================================
# SESSION FACTORY
# ==========================================================


SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=Session,
)


# ==========================================================
# BASE MODEL CLASS
# ==========================================================


Base = declarative_base()


# ==========================================================
# DATABASE UTILITIES
# ==========================================================


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function for FastAPI to get database session.

    Usage:
        @router.get("/items")
        async def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()

    Yields:
        Database session
    """

    db = SessionLocal()

    try:

        yield db

        db.commit()

    except Exception as e:

        db.rollback()

        log.exception(
            f"Database transaction failed: {e}"
        )

        raise

    finally:

        db.close()


def get_db_session() -> Session:
    """
    Get a new database session directly (not for dependency injection).

    Returns:
        Database session

    Example:
        db = get_db_session()
        try:
            result = db.query(User).filter_by(id=user_id).first()
            db.commit()
        finally:
            db.close()
    """

    return SessionLocal()


def check_database_connection() -> bool:
    """
    Check if database connection is working.

    Returns:
        True if connection successful, False otherwise
    """

    try:

        with engine.connect() as conn:

            conn.execute(
                text("SELECT 1")
            )

        log.info(
            "Database connection established successfully"
        )

        return True

    except SQLAlchemyError as e:

        log.exception(
            f"Database connection failed: {e}"
        )

        return False

    except Exception as e:

        log.exception(
            f"Unexpected database connection error: {e}"
        )

        return False


def initialize_database() -> None:
    """
    Create all database tables from SQLAlchemy models.
    """

    try:

        Base.metadata.create_all(
            bind=engine
        )

        log.info(
            "Database initialized successfully"
        )

    except SQLAlchemyError as e:

        log.exception(
            f"Database initialization failed: {e}"
        )

        raise

    except Exception as e:

        log.exception(
            f"Unexpected database initialization error: {e}"
        )

        raise


def drop_database() -> None:
    """
    Drop all database tables (development only).
    WARNING: This will delete all data.
    """

    if settings.DEBUG:

        try:

            Base.metadata.drop_all(
                bind=engine
            )

            log.warning(
                "Database tables dropped (development mode)"
            )

        except SQLAlchemyError as e:

            log.exception(
                f"Database drop failed: {e}"
            )

            raise

    else:

        log.error(
            "Attempted to drop database outside development mode"
        )

        raise RuntimeError(
            "Cannot drop database in production mode"
        )


def get_engine() -> Engine:
    """
    Get the SQLAlchemy engine instance.

    Returns:
        SQLAlchemy engine
    """

    return engine


def get_session() -> Session:
    """
    Get a new database session.

    Returns:
        Database session
    """

    return SessionLocal()


def get_session_factory() -> sessionmaker:
    """
    Get the session factory.

    Returns:
        SQLAlchemy sessionmaker
    """

    return SessionLocal


def health_check() -> Dict[str, Any]:
    """
    Comprehensive database health check.

    Returns:
        Dictionary with health status and details
    """

    try:

        with engine.connect() as conn:

            result = conn.execute(
                text("SELECT 1 as is_healthy, version() as db_version, current_database() as db_name")
            )

            row = result.fetchone()

        return {

            "success": True,

            "database": "connected",

            "engine": "postgresql",

            "db_name": row.db_name if row else "unknown",

            "db_version": row.db_version if row else "unknown",

            "pool_size": engine.pool.size(),

            "pool_checked_in": engine.pool.checkedin(),

            "pool_overflow": engine.pool.overflow(),

            "pool_total": engine.pool.total(),

        }

    except SQLAlchemyError as e:

        return {

            "success": False,

            "database": "disconnected",

            "error": str(e),

            "error_type": "SQLAlchemyError",

        }

    except Exception as e:

        return {

            "success": False,

            "database": "disconnected",

            "error": str(e),

            "error_type": type(e).__name__,

        }


def get_pool_status() -> Dict[str, Any]:
    """
    Get database connection pool status.

    Returns:
        Dictionary with pool statistics
    """

    return {

        "pool_size": engine.pool.size(),

        "pool_checked_in": engine.pool.checkedin(),

        "pool_overflow": engine.pool.overflow(),

        "pool_total": engine.pool.total(),

        "pool_timeout": DEFAULT_POOL_TIMEOUT,

        "pool_recycle": DEFAULT_POOL_RECYCLE,

    }


def execute_raw_sql(
    query: str,
    params: Optional[Dict[str, Any]] = None,
) -> Any:
    """
    Execute raw SQL query (use with caution).

    Args:
        query: Raw SQL query string
        params: Query parameters

    Returns:
        Query result
    """

    try:

        with engine.connect() as conn:

            result = conn.execute(
                text(query),
                params or {},
            )

            conn.commit()

            return result

    except SQLAlchemyError as e:

        log.exception(
            f"Raw SQL execution failed: {e}"
        )

        raise


# ==========================================================
# INITIALIZATION LOG
# ==========================================================


log.info(
    "Database module initialized",
    database_url="***" + settings.DATABASE_URL[-20:] if len(settings.DATABASE_URL) > 20 else "***",
    pool_size=settings.DATABASE_POOL_SIZE or DEFAULT_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW or DEFAULT_MAX_OVERFLOW,
    pool_recycle=DEFAULT_POOL_RECYCLE,
)


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [
    "engine",
    "SessionLocal",
    "Base",
    "get_db",
    "get_db_session",
    "check_database_connection",
    "initialize_database",
    "drop_database",
    "get_engine",
    "get_session",
    "get_session_factory",
    "health_check",
    "get_pool_status",
    "execute_raw_sql",
]


# ==========================================================
# END OF FILE – database.py
# ==========================================================