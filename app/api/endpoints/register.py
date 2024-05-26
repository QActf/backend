from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi_users import exceptions, models, schemas
from fastapi_users.manager import BaseUserManager
from fastapi_users.router.common import ErrorCode
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_docs_responses.register import CREATE_REGISTER
from app.core.db import get_async_session
from app.core.user import get_user_manager
from app.crud import profile_crud
from app.schemas.profile import ProfileCreate


def get_register_router(
        user_schema,
        user_create_schema,
) -> APIRouter:
    """Generate a router with the register route."""
    router = APIRouter()

    @router.post(
        '/register',
        tags=['auth'],
        response_model=user_schema,
        status_code=status.HTTP_201_CREATED,
        name='register:register',
        responses=CREATE_REGISTER
    )
    async def register(
        request: Request,
        user_create: user_create_schema,
        user_manager: BaseUserManager[models.UP, models.ID] = Depends(
            get_user_manager
        ),
        session: AsyncSession = Depends(get_async_session)
    ):
        try:
            created_user = await user_manager.create(
                user_create, safe=True, request=request
            )

        except exceptions.UserAlreadyExists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.REGISTER_USER_ALREADY_EXISTS,
            )
        except exceptions.InvalidPasswordException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    'code': ErrorCode.REGISTER_INVALID_PASSWORD,
                    'reason': e.reason,
                },
            )
        response_schema = schemas.model_validate(user_schema, created_user)
        await profile_crud.create(
            ProfileCreate(
                user_id=created_user.id,
                first_name='',
                last_name='',
                age=0,
            ),
            session=session
        )
        return response_schema

    return router
