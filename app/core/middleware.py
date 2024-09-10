import json
import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import Message

from app.core.config import logger_settings

logger = logging.getLogger(__name__)

MIN_CHAR_FOR_HIDE = 12
STAR_MULTIPLIER = 8

HIDDEN_FIELDS: list[str] = [
    "password",
    "token",
]


def get_request_data(request: Request, json_body: dict) -> dict:
    data = {}
    if request.query_params:
        data["query_params"] = str(request.query_params)
    if request.path_params:
        data["path_params"] = request.path_params
    if json_body:
        data["body"] = json_body
    return data


def hide_details(json_body: dict) -> None:
    if not logger_settings.HIDE_DETAILS:
        return

    for key in (
        key
        for hidden_field in HIDDEN_FIELDS
        for key in json_body
        if hidden_field.lower() in key.lower()
    ):
        stars = '*' * STAR_MULTIPLIER
        if len(json_body[key]) >= MIN_CHAR_FOR_HIDE:
            json_body[
                key
            ] = f"{json_body[key][:4]}{stars}{json_body[key][-2:]}"
        else:
            json_body[key] = stars


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        json_body = await self._get_request_json(request)
        start_time = time.time()
        response = await call_next(request)

        response_time = round(time.time() - start_time, 5)
        hide_details(json_body)
        data = json.dumps(
            get_request_data(request, json_body),
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

    async def _get_request_json(self, request: Request) -> dict:
        await self._set_body(request)
        json_body = {}
        try:
            json_body = await request.json()
        except json.decoder.JSONDecodeError as e:
            logger.exception("Decoder json failed\n%s", e)
        except Exception as e:
            logger.exception("Get json from request failed\n%s", e)
        return json_body

    async def _set_body(self, request: Request) -> None:
        receive_ = await request._receive()

        async def receive() -> Message:
            return receive_

        request._receive = receive
