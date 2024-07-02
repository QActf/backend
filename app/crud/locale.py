from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models import (
    Auth, Common, Contacts, Errors, Header, Help, Locale, Main, Restore,
    Subscription, Tasks,
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
        tasks_data = locale.tasks.model_dump()
        tasks = Tasks(**tasks_data, locale_id=language.id)
        errors_data = locale.errors.model_dump()
        errors = Errors(**errors_data, locale_id=language.id)
        session.add_all(
            (
                common, header, auth, contacts, help_, main,
                restore, subscription, tasks, errors
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
                selectinload(Locale.tasks),
                selectinload(Locale.errors)
            )
        )
        locale = await session.execute(stmt)
        return locale.scalars().first()


locale_crud = LocaleCRUD(Locale)
