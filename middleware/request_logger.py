import time

from starlette.middleware.base import BaseHTTPMiddleware

from core.logging import log


class RequestLoggerMiddleware(
    BaseHTTPMiddleware
):

    async def dispatch(
        self,
        request,
        call_next,
    ):

        start_time = time.time()

        response = await call_next(
            request
        )

        duration = round(
            time.time() - start_time,
            3,
        )

        log.info(
            f"{request.method} "
            f"{request.url.path} "
            f"{response.status_code} "
            f"{duration}s"
        )

        return response