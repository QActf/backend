from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints import register
from app.core.db import get_async_session
from app.api_docs_responses.user import (
    add_router_doc, USER_CONFIRM_DESCRIPTION)
from app.api_docs_responses.utils_docs import USER_VALUE
from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.crud.user import user_crud
from app.services.token_generator.tokens import token_generator

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)

router.include_router(
    register.get_register_router(
        UserRead,
        Annotated[UserCreate, Body(example=USER_VALUE)]
    ),
    prefix='/auth',
    tags=['auth'],
)

router.include_router(
    fastapi_users.get_users_router(
        UserRead,
        Annotated[UserUpdate, Body(example=USER_VALUE)]
    ),
    prefix='/users',
    tags=['users'],
)


@router.post(
    "/users/{user_id}/{confirm_code}",
    tags=['users'],
    status_code=status.HTTP_200_OK,
    summary='Подтверждение почты и активация аккаунта.',
    description=USER_CONFIRM_DESCRIPTION,
)
async def confirm_email(
    user_id: int,
    confirm_code: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Подтверждение почты и активация аккаунта."""
    user = await user_crud.get(user_id, session)
    if not token_generator.check_token(
        user,
        confirm_code,
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Ошибка валидации аккаунта.',
        )
    await user_crud.update_id(user, 'is_verified', True, session)

add_router_doc(router)
