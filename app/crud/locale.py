from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models import (
    Achievements, Auth, Common, Contacts, Errors, Header, Help, Locale, Main,
    Months, ProfileUser, QuestionBanner, Restore, Secure, Subscription, Tasks,
)
from app.schemas.locale import LocaleCreate


class LocaleCRUD(CRUDBase):
    async def create(self, locale: LocaleCreate, session: AsyncSession):
        language = Locale(language=locale.language)
        session.add(language)
        await session.commit()
        await session.refresh(language)
        common_data = locale.common.model_dump()
        common = Common(**common_data, locale_id=language.id)
        header_data = locale.header.model_dump()
        header = Header(**header_data, locale_id=language.id)
        auth_data = locale.auth.model_dump()
        auth = Auth(**auth_data, locale_id=language.id)
        contacts_data = locale.contacts.model_dump()
        contacts = Contacts(**contacts_data, locale_id=language.id)
        help_data = locale.help.model_dump()
        help_ = Help(**help_data, locale_id=language.id)
        main_data = locale.main.model_dump()
        main = Main(**main_data, locale_id=language.id)
        restore_data = locale.restore.model_dump()
        restore = Restore(**restore_data, locale_id=language.id)
        subscription_data = locale.subscription.model_dump()
        subscription = Subscription(**subscription_data, locale_id=language.id)
        profile_user_data = locale.profile_user.model_dump()
        profile_user = ProfileUser(
            **profile_user_data, locale_id=language.id
        )
        secure_data = locale.secure.model_dump()
        secure = Secure(**secure_data, locale_id=language.id)
        achievements_data = locale.achievements.model_dump()
        achievements = Achievements(**achievements_data, locale_id=language.id)
        tasks_data = locale.tasks.model_dump()
        tasks = Tasks(**tasks_data, locale_id=language.id)
        question_banner_data = locale.question_banner.model_dump()
        question_banner = QuestionBanner(
            **question_banner_data, locale_id=language.id
        )
        errors_data = locale.errors.model_dump()
        errors = Errors(**errors_data, locale_id=language.id)
        months_data = locale.months.model_dump()
        months = Months(**months_data, locale_id=language.id)
        session.add_all(
            (
                common, header, auth, contacts, help_, main,
                restore, subscription, profile_user, secure, achievements,
                tasks, question_banner, errors, months,
            )
        )
        await session.commit()
        await session.refresh(language)
        return await self.get_by_id(language.id, session)

    async def get_by_id(self, id, session: AsyncSession):
        stmt = (
            select(Locale)
            .where(Locale.id == id)
            .options(
                selectinload(Locale.common),
                selectinload(Locale.header),
                selectinload(Locale.auth),
                selectinload(Locale.contacts),
                selectinload(Locale.help),
                selectinload(Locale.main),
                selectinload(Locale.restore),
                selectinload(Locale.subscription),
                selectinload(Locale.profile_user),
                selectinload(Locale.secure),
                selectinload(Locale.achievements),
                selectinload(Locale.tasks),
                selectinload(Locale.question_banner),
                selectinload(Locale.errors),
                selectinload(Locale.months),
            )
        )
        locale = await session.execute(stmt)
        return locale.scalars().first()


locale_crud = LocaleCRUD(Locale)
