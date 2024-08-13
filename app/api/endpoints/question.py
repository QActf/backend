from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from app.api.validators import check_obj_exists
from app.api_docs_responses.question import GET_QUESTION, GET_QUESTIONS
from app.core.db import get_async_session
from app.crud import question_crud
from app.schemas.question import QuestionRead

router = APIRouter()


@router.get(
    '/',
    response_model=list[QuestionRead],
    **GET_QUESTIONS,
)
async def get_all_questions(
    session: AsyncSession = Depends(get_async_session),
) -> list[QuestionRead]:
    """
    Получение всех часто задаваемых вопросов, которые есть в БД.
    """
    return await question_crud.get_multi(session)


@router.get(
    '/{question_id}',
    response_model=QuestionRead,
    **GET_QUESTION,
)
async def get_question(
    question_id: Annotated[int, Path(ge=0)],
    session: AsyncSession = Depends(get_async_session)
):
    """
    Получение вопроса по его id или
    получение ошибки 404 в случае отсутствия данного вопроса.
    """
    obj = await question_crud.get_by_attr(
        attr_name='id',
        attr_value=question_id,
        session=session,
    )
    await check_obj_exists(obj=obj)
    return obj
