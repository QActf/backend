import json
import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Message

logger = logging.getLogger(__name__)


def get_data(request: Request, json_body) -> dict:
    data = {}
    if request.query_params:
        data["query_params"] = request.query_params
    if request.path_params:
        data["path_params"] = request.path_params
    if json_body:
        data["body"] = json_body
    return data


class LoggerMiddleware(BaseHTTPMiddleware):
    async def set_body(self, request: Request):
        receive_ = await request._receive()

        async def receive() -> Message:
            return receive_

        request._receive = receive

    async def dispatch(self, request: Request, call_next):
        await self.set_body(request)
        try:
            json_body = await request.json()
        except Exception as e:
            json_body = {}
            logger.exception("Request json failed\n%s", e)

        start_time = time.time()
        response = await call_next(request)
        response_time = round(time.time() - start_time, 5)

        data = json.dumps(
            get_data(request, json_body),
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
