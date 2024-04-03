from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status

from app.api.endpoints import register
from app.api_docs_responses.user import (DELETE_USER, GET_CURRENT_USER,
                                         GET_USER_BY_ID, LOGIN_USER,
                                         LOGOUT_USER, UPDATE_CURRENT_USER,
                                         UPDATE_USER_BY_ID)
from app.api_docs_responses.utils_docs import LOGIN_WARNING, USER_VALUE
from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    register.get_register_router(
        UserRead,
        Annotated[UserCreate, Body(example=USER_VALUE)]
    ),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(
        UserRead,
        Annotated[UserUpdate, Body(example=USER_VALUE)]
    ),
    prefix="/users",
    tags=["users"],
)

router.routes[0].responses = LOGIN_USER  # post для /auth/jwt/login
router.routes[0].description = LOGIN_WARNING  # post для /auth/jwt/login

router.routes[1].responses = LOGOUT_USER  # post для /auth/jwt/logout
router.routes[3].responses = GET_CURRENT_USER  # get для /users/me
router.routes[4].responses = UPDATE_CURRENT_USER  # patch для /users/me
router.routes[5].responses = GET_USER_BY_ID  # get для /users/{id}
router.routes[6].responses = UPDATE_USER_BY_ID  # patch для /users/{id}


@router.delete(
    "/users/{id}",
    tags=["users"],
    deprecated=True,
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETE_USER
)
def delete_user(id: str):
    """Не используйте удаление, деактивируйте пользователей."""
    raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail="Удаление пользователей запрещено!",
    )
