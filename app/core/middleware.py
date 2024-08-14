import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        response_time = round(time.time() - start_time, 5)

        logger.info(f"\"{request.method} {request.url.path}\" {response_time}s")

        return response
