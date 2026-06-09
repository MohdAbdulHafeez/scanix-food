# ==========================================================
# SCANIX AI
# CORE LOGGING – ELITE PRODUCTION GRADE
# ==========================================================


# ==========================================================
# IMPORTS
# ==========================================================


from __future__ import annotations


import sys
import time
import asyncio
from pathlib import Path
from typing import Any
from typing import Dict , Optional
from functools import wraps


from loguru import logger

from core.config import get_settings

settings = get_settings()


# ==========================================================
# CONSTANTS
# ==========================================================


LOG_DIR_NAME: str = "logs"

LOG_FILE_NAME: str = "scanix.log"

LOG_ROTATION_SIZE: str = "10 MB"

LOG_RETENTION_DAYS: str = "30 days"

LOG_COMPRESSION_FORMAT: str = "zip"

CONSOLE_LOG_LEVEL: str = settings.LOG_LEVEL

FILE_LOG_LEVEL: str = settings.LOG_LEVEL


# ==========================================================
# LOG DIRECTORY SETUP
# ==========================================================


LOG_DIR = Path(
    LOG_DIR_NAME
)

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


LOG_FILE = (
    LOG_DIR
    / LOG_FILE_NAME
)


# ==========================================================
# REMOVE DEFAULT LOGURU HANDLER
# ==========================================================


logger.remove()


# ==========================================================
# CONSOLE LOGGER (STDOUT) – FOR DEVELOPMENT
# ==========================================================


logger.add(
    sys.stdout,
    level=CONSOLE_LOG_LEVEL,
    colorize=True,
    backtrace=True,
    diagnose=False,
    enqueue=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:"
        "<cyan>{function}</cyan>:"
        "<cyan>{line}</cyan> | "
        "{message}"
    ),
)


# ==========================================================
# FILE LOGGER (ROTATING) – FOR PRODUCTION
# ==========================================================


logger.add(
    LOG_FILE,
    level=FILE_LOG_LEVEL,
    rotation=LOG_ROTATION_SIZE,
    retention=LOG_RETENTION_DAYS,
    compression=LOG_COMPRESSION_FORMAT,
    enqueue=True,
    backtrace=True,
    diagnose=False,
    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level} | "
        "{name}:{function}:{line} | "
        "{message}"
    ),
)


# ==========================================================
# CONTEXT MANAGER FOR REQUEST LOGGING
# ==========================================================


class RequestLoggerContext:
    """
    Context manager for request-scoped logging.

    Usage:
        with RequestLoggerContext(request_id="req_123", user_id="user_456"):
            log.info("Processing request")
    """

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:

        self.context = kwargs

    def __enter__(self) -> None:

        self.bound_logger = logger.bind(
            **self.context
        )

        self.original_log = log._LoggerManager__get_logger()

        # Not modifying global log, just providing bound version

    def __exit__(
        self,
        exc_type: Any,
        exc_val: Any,
        exc_tb: Any,
    ) -> None:

        pass

    def get_logger(self) -> Any:

        return self.bound_logger


# ==========================================================
# LOGGER MANAGER CLASS
# ==========================================================


class LoggerManager:
    """
    Central logging facade for Scanix AI.

    Provides consistent logging across all 9 systems with:
    - Automatic file rotation
    - Console coloring
    - Structured logging support
    - Exception capture with stack traces
    - Request context binding

    Usage:

        from core.logging import log

        log.info("User logged in", user_id="123", email="user@example.com")
        log.exception("Failed to process scan", scan_id="scan_123")
        log.debug("OCR completed", confidence=0.85, text_length=120)
    """

    @staticmethod
    def debug(
        message: str,
        **kwargs: Any,
    ) -> None:
        """
        Log debug message with optional structured data.

        Args:
            message: Log message
            **kwargs: Additional structured data to bind

        Example:
            log.debug("OCR processing", confidence=0.92, word_count=45)
        """

        logger.bind(
            **kwargs
        ).debug(message)

    @staticmethod
    def info(
        message: str,
        **kwargs: Any,
    ) -> None:
        """
        Log info message with optional structured data.

        Args:
            message: Log message
            **kwargs: Additional structured data to bind

        Example:
            log.info("Scan completed", scan_id="scan_123", processing_time_ms=450)
        """

        logger.bind(
            **kwargs
        ).info(message)

    @staticmethod
    def warning(
        message: str,
        **kwargs: Any,
    ) -> None:
        """
        Log warning message with optional structured data.

        Args:
            message: Log message
            **kwargs: Additional structured data to bind

        Example:
            log.warning("Low OCR confidence", confidence=0.45, threshold=0.70)
        """

        logger.bind(
            **kwargs
        ).warning(message)

    @staticmethod
    def error(
        message: str,
        **kwargs: Any,
    ) -> None:
        """
        Log error message with optional structured data.

        Args:
            message: Log message
            **kwargs: Additional structured data to bind

        Example:
            log.error("OpenFoodFacts API failed", status_code=500, barcode="890123456789")
        """

        logger.bind(
            **kwargs
        ).error(message)

    @staticmethod
    def critical(
        message: str,
        **kwargs: Any,
    ) -> None:
        """
        Log critical message with optional structured data.

        Args:
            message: Log message
            **kwargs: Additional structured data to bind

        Example:
            log.critical("Database connection lost", service="supabase", retry_count=3)
        """

        logger.bind(
            **kwargs
        ).critical(message)

    @staticmethod
    def exception(
        message: str,
        **kwargs: Any,
    ) -> None:
        """
        Log exception with stack trace and optional structured data.

        Args:
            message: Log message
            **kwargs: Additional structured data to bind

        Example:
            try:
                result = await scan_product(file)
            except Exception as e:
                log.exception("Scan failed", file_name=file.filename)
        """

        logger.bind(
            **kwargs
        ).exception(message)

    @staticmethod
    def bind(
        **kwargs: Any,
    ) -> Any:
        """
        Create a bound logger with persistent context.

        Args:
            **kwargs: Context data to bind to all future logs

        Returns:
            Bound logger instance

        Example:
            request_logger = log.bind(request_id="req_123", user_id="user_456")
            request_logger.info("Processing request")
            request_logger.info("Request completed")
        """

        return logger.bind(
            **kwargs
        )

    @staticmethod
    def success(
        message: str,
        **kwargs: Any,
    ) -> None:
        """
        Log success message (info level with success marker).

        Args:
            message: Success message
            **kwargs: Additional structured data

        Example:
            log.success("Product scanned successfully", product_name="Maggi Noodles")
        """

        logger.bind(
            **kwargs
        ).info(
            f"✅ {message}"
        )

    @staticmethod
    def fail(
        message: str,
        **kwargs: Any,
    ) -> None:
        """
        Log failure message (error level with failure marker).

        Args:
            message: Failure message
            **kwargs: Additional structured data

        Example:
            log.fail("Barcode validation failed", barcode="1234567890123")
        """

        logger.bind(
            **kwargs
        ).error(
            f"❌ {message}"
        )

    @staticmethod
    def log_time(
        operation: str,
        start_time: float,
        **kwargs: Any,
    ) -> None:
        """
        Log operation execution time.

        Args:
            operation: Name of the operation
            start_time: Start time in seconds (from time.time())
            **kwargs: Additional structured data

        Example:
            start = time.time()
            result = await process()
            log.log_time("OCR processing", start, image_size=1024)
        """

        elapsed_ms = int(
            (time.time() - start_time) * 1000
        )

        logger.bind(
            operation=operation,
            elapsed_ms=elapsed_ms,
            **kwargs,
        ).info(
            f"{operation} completed in {elapsed_ms}ms"
        )

    @staticmethod
    def get_logger(self) -> Any:

        return logger

    @staticmethod
    def get_log_file_path() -> Path:

        return LOG_FILE


# ==========================================================
# DECORATORS FOR AUTO LOGGING
# ==========================================================


def log_function_call(
    log_args: bool = True,
    log_result: bool = False,
    log_level: str = "debug",
) -> Any:
    """
    Decorator to automatically log function calls.

    Args:
        log_args: Whether to log function arguments
        log_result: Whether to log return value
        log_level: Log level to use

    Example:
        @log_function_call(log_args=True, log_result=True)
        async def scan_product(file: UploadFile) -> Dict:
            ...
    """

    def decorator(
        func: Any,
    ) -> Any:

        @wraps(func)
        async def async_wrapper(
            *args: Any,
            **kwargs: Any,
        ) -> Any:

            func_name = func.__name__

            module_name = func.__module__

            if log_args:

                logger.bind(
                    function=func_name,
                    module=module_name,
                    args=str(args)[:200],
                    kwargs=str(kwargs)[:200],
                ).log(
                    log_level,
                    f"Calling {func_name}",
                )

            else:

                logger.bind(
                    function=func_name,
                    module=module_name,
                ).log(
                    log_level,
                    f"Calling {func_name}",
                )

            start_time = time.time()

            try:

                result = await func(
                    *args,
                    **kwargs,
                )

                elapsed_ms = int(
                    (time.time() - start_time) * 1000
                )

                if log_result:

                    logger.bind(
                        function=func_name,
                        elapsed_ms=elapsed_ms,
                        result=str(result)[:200],
                    ).log(
                        log_level,
                        f"{func_name} completed",
                    )

                else:

                    logger.bind(
                        function=func_name,
                        elapsed_ms=elapsed_ms,
                    ).log(
                        log_level,
                        f"{func_name} completed",
                    )

                return result

            except Exception as e:

                elapsed_ms = int(
                    (time.time() - start_time) * 1000
                )

                logger.bind(
                    function=func_name,
                    elapsed_ms=elapsed_ms,
                    error=str(e),
                ).exception(
                    f"{func_name} failed"
                )

                raise

        @wraps(func)
        def sync_wrapper(
            *args: Any,
            **kwargs: Any,
        ) -> Any:

            func_name = func.__name__

            module_name = func.__module__

            if log_args:

                logger.bind(
                    function=func_name,
                    module=module_name,
                    args=str(args)[:200],
                    kwargs=str(kwargs)[:200],
                ).log(
                    log_level,
                    f"Calling {func_name}",
                )

            else:

                logger.bind(
                    function=func_name,
                    module=module_name,
                ).log(
                    log_level,
                    f"Calling {func_name}",
                )

            start_time = time.time()

            try:

                result = func(
                    *args,
                    **kwargs,
                )

                elapsed_ms = int(
                    (time.time() - start_time) * 1000
                )

                if log_result:

                    logger.bind(
                        function=func_name,
                        elapsed_ms=elapsed_ms,
                        result=str(result)[:200],
                    ).log(
                        log_level,
                        f"{func_name} completed",
                    )

                else:

                    logger.bind(
                        function=func_name,
                        elapsed_ms=elapsed_ms,
                    ).log(
                        log_level,
                        f"{func_name} completed",
                    )

                return result

            except Exception as e:

                elapsed_ms = int(
                    (time.time() - start_time) * 1000
                )

                logger.bind(
                    function=func_name,
                    elapsed_ms=elapsed_ms,
                    error=str(e),
                ).exception(
                    f"{func_name} failed"
                )

                raise

        if asyncio.iscoroutinefunction(func):

            return async_wrapper

        return sync_wrapper

    return decorator


def log_async_function_call(
    func: Any,
) -> Any:
    """
    Simplified decorator for async functions.

    Example:
        @log_async_function_call
        async def scan_product(file):
            ...
    """

    @wraps(func)
    async def wrapper(
        *args: Any,
        **kwargs: Any,
    ) -> Any:

        func_name = func.__name__

        logger.debug(
            f"⏳ Starting {func_name}"
        )

        start_time = time.time()

        try:

            result = await func(
                *args,
                **kwargs,
            )

            elapsed_ms = int(
                (time.time() - start_time) * 1000
            )

            logger.debug(
                f"✅ {func_name} completed in {elapsed_ms}ms"
            )

            return result

        except Exception as e:

            elapsed_ms = int(
                (time.time() - start_time) * 1000
            )

            logger.error(
                f"❌ {func_name} failed after {elapsed_ms}ms: {e}"
            )

            raise

    return wrapper


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================


def get_logger() -> Any:
    """
    Get the underlying loguru logger for advanced use.

    Returns:
        loguru logger instance
    """

    return logger


def get_log_stats() -> Dict[str, Any]:
    """
    Get logging statistics.

    Returns:
        Dictionary with log file information
    """

    if LOG_FILE.exists():

        file_size_bytes = LOG_FILE.stat().st_size

        file_size_mb = round(
            file_size_bytes / (1024 * 1024),
            2,
        )

    else:

        file_size_bytes = 0

        file_size_mb = 0

    return {

        "log_file": str(LOG_FILE),

        "log_file_exists": LOG_FILE.exists(),

        "log_file_size_bytes": file_size_bytes,

        "log_file_size_mb": file_size_mb,

        "log_rotation": LOG_ROTATION_SIZE,

        "log_retention": LOG_RETENTION_DAYS,

        "console_level": CONSOLE_LOG_LEVEL,

        "file_level": FILE_LOG_LEVEL,
    }


async def flush_logs() -> None:
    """
    Force flush all log handlers.
    Useful before application shutdown.
    """

    logger.complete()


# ==========================================================
# SINGLETON INSTANCE
# ==========================================================


log = LoggerManager()


# ==========================================================
# INITIALIZATION LOG
# ==========================================================


log.info(
    "Logging system initialized",
    log_level=settings.LOG_LEVEL,
    log_file=str(LOG_FILE),
    log_rotation=LOG_ROTATION_SIZE,
    log_retention=LOG_RETENTION_DAYS,
)


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [
    "log",
    "logger",
    "LoggerManager",
    "RequestLoggerContext",
    "log_function_call",
    "log_async_function_call",
    "get_logger",
    "get_log_stats",
    "flush_logs",
]


# ==========================================================
# END OF FILE – logging.py
# ==========================================================