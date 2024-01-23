from fastapi_users.authentication import JWTStrategy
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.core.db import AsyncSessionLocal
from app.core.user import get_jwt_strategy
from app.crud import user_crud


class AdminAuth(AuthenticationBackend):
    async def login(
            self,
            request: Request,
            session: AsyncSession = AsyncSessionLocal(),
            strategy: JWTStrategy = get_jwt_strategy()
    ) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        user = await user_crud.get_user_by_credentials(
            email, password, session
        )
        if not user:
            return False
        token = await strategy.write_token(user)
        request.session.update({"token": token})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(
            self,
            request: Request,
            session: AsyncSession = AsyncSessionLocal()
    ) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        return True
