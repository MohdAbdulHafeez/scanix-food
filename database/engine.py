# database/engine.py


from typing import Generator
from typing import Dict
from typing import Any


from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker


from core.config import settings
from core.logging import log


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
# EVENT LISTENERS
# ==========================================================


@event.listens_for(engine, "connect")
def receive_connect(
    dbapi_connection,
    connection_record,
) -> None:

    log.debug(
        "Database connection established"
    )


@event.listens_for(engine, "checkout")
def receive_checkout(
    dbapi_connection,
    connection_record,
    connection_proxy,
) -> None:

    log.debug(
        "Database connection checked out"
    )


# ==========================================================
# DEPENDENCY FUNCTIONS
# ==========================================================


def get_db() -> Generator[Session, None, None]:

    db = SessionLocal()

    try:

        yield db

        db.commit()

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


def get_db_session() -> Session:

    return SessionLocal()


def check_database_connection() -> bool:

    try:

        with engine.connect() as conn:

            conn.execute(
                text("SELECT 1")
            )

        log.info(
            "Database connection established successfully"
        )

        return True

    except Exception as e:

        log.error(
            f"Database connection failed: {e}"
        )

        return False


def get_engine():

    return engine


def get_session():

    return SessionLocal()


def get_session_factory():

    return SessionLocal


def health_check() -> Dict[str, Any]:

    try:

        with engine.connect() as conn:

            result = conn.execute(
                text("SELECT 1 as is_healthy, version() as db_version")
            )

            row = result.fetchone()

        return {

            "success": True,

            "database": "connected",

            "db_version": row.db_version if row else "unknown",

            "pool_size": engine.pool.size(),

        }

    except Exception as e:

        return {

            "success": False,

            "database": "disconnected",

            "error": str(e),

        }


def get_pool_status() -> Dict[str, Any]:

    return {

        "pool_size": engine.pool.size(),

        "pool_checked_in": engine.pool.checkedin(),

        "pool_overflow": engine.pool.overflow(),

        "pool_total": engine.pool.total(),

    }