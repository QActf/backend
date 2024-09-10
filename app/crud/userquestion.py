from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import UserQuestion


class CRUDUserQuestion(CRUDBase):
    async def create(
        self,
        from_user_email,
        message,
        session: AsyncSession,
    ):
        new_question = UserQuestion(
            from_user_email=from_user_email,
            message=message
        )
        session.add(new_question)
        await session.commit()
        await session.refresh(new_question)
        return new_question


user_question_crud = CRUDUserQuestion(UserQuestion)
