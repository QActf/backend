from sqlalchemy import and_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models import Course, User
from app.models.course import (
    course_tariff_association, course_user_association,
)


class CRUDCourse(CRUDBase):

    async def get_users_obj(
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
        """Получение курса по id, который запрашивает пользователь."""
        course_query = (
            select(Course)
            .where(Course.id == course_id)
            .options(
                selectinload(Course.users),
                selectinload(Course.tasks),
            )
        )
        course = await session.execute(course_query)
        return course.scalars().first()

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

    async def get_multi_courses_with_users(
            self,
            session: AsyncSession,
    ):
        """Вернет курсы с пользователями."""
        stmt = select(self.model).options(
            selectinload(self.model.users)
        )
        objs = await session.execute(stmt)
        return objs.scalars().all()

    async def create_course_tariff_association(
            self,
            obj_in,
            session: AsyncSession,
    ):
        """Создаст ассоциацию курса и тарифа."""
        stmt = course_tariff_association.insert().values(
            course_id=obj_in.course_id,
            tariff_id=obj_in.tariff_id,
        )
        await session.execute(stmt)
        await session.commit()

    async def get_course_tariff_association(
            self,
            course_id: int,
            tariff_id: int,
            session: AsyncSession,
    ):
        """Вернет ассоциацию курса и тарифа."""
        stmt = select(course_tariff_association).where(
            and_(
                course_tariff_association.c.course_id == course_id,
                course_tariff_association.c.tariff_id == tariff_id
            )
        )
        obj = await session.execute(stmt)
        return obj.scalars().first()

    async def delete_course_tariff_association(
            self,
            course_id: int,
            tariff_id: int,
            session: AsyncSession,
    ):
        """Удалит ассоциацию курса и тарифа."""
        stmt = course_tariff_association.delete().where(
            and_(
                course_tariff_association.c.course_id == course_id,
                course_tariff_association.c.tariff_id == tariff_id
            )
        )
        await session.execute(stmt)
        await session.commit()

    async def create_course_user_association(
            self,
            course_id: int,
            user_id: int,
            session: AsyncSession,
    ):
        """Создаст ассоциацию курса и пользователя."""
        stmt = insert(course_user_association).values(
            course_id=course_id,
            user_id=user_id,
        ).on_conflict_do_nothing(index_elements=['course_id', 'user_id'])
        await session.execute(stmt)
        await session.commit()

    async def update_icon(
            self,
            course_id: int,
            image_url: str,
            session: AsyncSession
    ):
        course = await session.execute(
            select(Course).where(Course.id == course_id)
        )
        course = course.scalars().first()
        course.icon = image_url
        session.add(course)
        await session.commit()
        await session.refresh(course)
        return course


course_crud = CRUDCourse(Course)
