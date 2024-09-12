import json
import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger(__name__)

MIN_CHAR_FOR_HIDE = 12
STAR_MULTIPLIER = 8

HIDDEN_FIELDS: list[str] = [
    "password",
    "token",
]


def get_request_data(request: Request) -> dict:
    data = {}
    if request.query_params:
        data["query_params"] = str(request.query_params)
    if request.path_params:
        data["path_params"] = request.path_params
    return data


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()
        response = await call_next(request)

        response_time = round(time.time() - start_time, 5)
        data = json.dumps(
            get_request_data(request),
            indent=2,
            ensure_ascii=False,
        )
        logger.info(
            "\"%s %s\" %d %ds\nwith data = %s",
            request.method,
            request.url.path,
            response.status_code,
            response_time,
            data,
        )

        return response
