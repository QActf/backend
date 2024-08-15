import logging

from fastapi import Response
from fastapi_users import models
from fastapi_users.authentication import backend, Strategy

logger = logging.getLogger(__name__)


class AuthenticationBackendWithLogger(backend.AuthenticationBackend):
    async def login(
        self, strategy: Strategy[models.UP, models.ID], user: models.UP
    ) -> Response:
        response = await super().login(strategy, user)
        logger.info(f"Пользователь `{user.email}` вошел.")
        return response

    async def logout(
        self, strategy: Strategy[models.UP, models.ID], user: models.UP, token: str
    ) -> Response:
        response = await super().logout(strategy, user, token)
        logger.info(f"Пользователь `{user.email}` вышел.")
        return response
