from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status

from app.api.endpoints import register
from app.api_docs_responses.user import CREATE_AUTH, DELETE_USER, LOGOUT_USER
from app.api_docs_responses.utils_docs import USER_VALUE
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

login_auth_route_responses = router.routes[0].responses = CREATE_AUTH
logout_auth_route = router.routes[1].responses = LOGOUT_USER

# Эндпоинты пользователя
# me_get_route = router.routes[3]
# me_patch_route = router.routes[4]
# users_id_get_route = router.routes[5]
# users_id_patch_route = router.routes[6]


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
