from typing import Annotated


from fastapi import APIRouter, Body, Depends, Form, HTTPException, status
from fastapi_users import InvalidPasswordException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints import register
from app.api.validators import check_obj_exists
from app.api_docs_responses.user import (
    USER_CONFIRM_DESCRIPTION, add_router_doc,
)
from app.api_docs_responses.utils_docs import USER_VALUE
from app.core.db import get_async_session
from app.core.user import (
    UserManager, auth_backend_cookie, auth_backend_jwt, current_user,
    fastapi_users, get_user_manager,
)
from app.crud.hasher import Hasher
from app.crud.question import question_crud
from app.crud.user import user_crud
from app.models import User
from app.schemas.user import (
    UserChangePassword, UserCreate, UserRead, UserReadRegister, UserUpdate,
)
from app.services.token_generator.tokens import token_generator

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend_jwt),
    prefix='/auth/jwt',
    tags=['auth'],
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend_cookie),
    prefix='/auth/cookie',
    tags=['auth'],
)

router.include_router(
    register.get_register_router(
        UserReadRegister,
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
    '/users/send_message',
    tags=['users'],
    status_code=status.HTTP_201_CREATED,
    summary='Отправка сообщения от пользователя сервису.',
    dependencies=[Depends(current_user)]
)
async def send_message(
    email: str = Form(),
    message: str = Form(),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    if email != user.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проверьте, что вы правильно указали свою почту.'
        )
    await question_crud.create(email, message, session)
    return {'result': 'The message has been sent.'}


@router.post(
    '/users/{user_id}/{confirm_code}',
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
    obj = await user_crud.get_by_attr(
        attr_name='id',
        attr_value=user_id,
        session=session,
    )
    await check_obj_exists(obj=obj)

    if not token_generator.check_token(obj, confirm_code):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Ошибка валидации аккаунта.',
        )

    await user_crud.update_id(
        db_obj=obj,
        field='is_verified',
        field_value=True,
        session=session,
    )


@router.post(
    path='/auth/change-password',
    tags=['auth'],
    status_code=status.HTTP_200_OK,
    summary='Смена пароля пользователя.',
    dependencies=[Depends(current_user)],
)
async def change_password(
    old_password: str = Body(embed=True),
    new_password: str = Body(embed=True),
    confirm_new_password: str = Body(embed=True),
    user: User = Depends(current_user),
    user_manager: UserManager = Depends(get_user_manager),
):
    """Смена пароля пользователя."""
    old_password_is_correct: bool = Hasher.verify_password(
        plain_password=old_password,
        hashed_password=user.hashed_password,
    )
    if not old_password_is_correct:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Старый пароль неверен.',
        )
    elif new_password != confirm_new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Новый пароль и подтверждение не совпадают.',
        )
    elif new_password == old_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Вы уже используете данный пароль. Придумайте новый.',
        )

    try:
        user_update = UserChangePassword(password=new_password)
        await user_manager.update(
            user_update=user_update,
            user=user,
            safe=True,
        )
    except InvalidPasswordException as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error.reason,
        )

    return {'detail': 'Пароль был успешно изменен.'}

add_router_doc(router)
