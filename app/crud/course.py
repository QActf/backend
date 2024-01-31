from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models import Course, User


class CRUDCourse(CRUDBase):

    async def get_user_courses(
            self,
            user_id: int,
            session: AsyncSession
    ):
        """Получение курсов, относящихся к конкретному пользователю."""
        courses_with_user_select = (
            select(Course)
            .options(
                selectinload(Course.users)
            ).where(Course.users.any(User.id == user_id))
        )
        db_obj = await session.execute(courses_with_user_select)
        return db_obj.scalars().all()

    async def get_course(
            self,
            course_id: int,
            session: AsyncSession
    ):
        """Получение конкретного курса, который запрашивает пользователь."""
        course_query = (
            select(Course)
            .where(Course.id == course_id)
            .options(
                selectinload(Course.users)
            )
        )
        course = await session.execute(course_query)
        return course.scalars().first()

    async def add_user(
            self,
            course: Course,
            user: User,
            session: AsyncSession
    ):
        """Добавление к курсу пользователя."""
        course.users.append(user)
        session.add(course)
        await session.commit()
        await session.refresh(course)
        return course

    async def close_course(
            self,
            course: Course,
            session: AsyncSession
    ):
        """Закрытие курса по его id."""
        course.is_closed = True
        session.add(course)
        await session.commit()
        await session.refresh(course)
        return course


course_crud = CRUDCourse(Course)
