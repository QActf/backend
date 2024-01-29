from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Group, User

GROUP_SCHEME = {
    'name': 'Test Group',
    'description': 'Test Group Description'
}
UPDATE_SCHEME = {
    'name': 'Updated name',
    'description': 'Updated description',
}


class TestCreateGroup:
    async def test_create_group(
            self,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Создание группы суперюзером"""
        stmt = func.count(Group.id)
        groups = await db_session.execute(stmt)
        groups = groups.scalar()
        response = auth_superuser.post(
            '/groups',
            json=GROUP_SCHEME
        )
        assert response.status_code == status.HTTP_201_CREATED
        new_groups = await db_session.execute(stmt)
        new_groups = new_groups.scalar()
        assert new_groups == groups + 1

    async def test_forbidden_create_group_by_user(
            self,
            auth_client: TestClient
    ):
        """Тест запрета создания группы юзером"""
        response = auth_client.post(
            '/groups',
            json=GROUP_SCHEME
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_forbidden_create_group_nonauth(
            self,
            new_client: TestClient
    ):
        """Тест запрета создания группы неавторизованным."""
        response = new_client.post(
            '/groups',
            json=GROUP_SCHEME
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestGetGroup:
    async def test_get_all_groups_superuser(
            self,
            moc_groups,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Получение всех групп суперюзером."""
        stmt = func.count(Group.id)
        groups = await db_session.execute(stmt)
        groups = groups.scalar()
        response = auth_superuser.get(
            '/groups'
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == groups

    async def test_forbidden_get_all_groups_user(
            self,
            moc_groups,
            db_session: AsyncSession,
            auth_client: TestClient
    ):
        """Тест запрета получения всех групп юзером."""
        response = auth_client.get('/groups')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_forbidden_get_all_groups_nonauth(
            self,
            moc_groups,
            new_client: TestClient
    ):
        """Тест запрета получения групп неавторизованным."""
        response = new_client.get('/groups')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_get_group_by_id_superuser(
            self,
            moc_groups,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Получение суперюзером группы по id."""
        response = auth_superuser.get(
            '/groups/1'
        )
        assert response.json()['id'] == 1

    async def test_forbidden_get_group_by_id_nonauth(
            self,
            moc_groups,
            new_client: TestClient
    ):
        """Тест запрета получения группы по id неавторизованным."""
        response = new_client.get('/groups/1')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_forbidden_get_group_by_id_user(
            self,
            auth_client: TestClient
    ):
        """Тест запрета получения группы по id юзером."""
        response = auth_client.get('/groups/1')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_get_self_groups_user(
            self,
            moc_groups,
            db_session: AsyncSession,
            auth_client: TestClient
    ):
        """Тест получения юзером своих групп."""
        stmt_1 = select(User).options(selectinload(User.groups))
        user = await db_session.execute(stmt_1)
        user = user.scalars().first()
        stmt = (select(Group).filter(Group.id == 1)
                .options(selectinload(Group.users)))
        group = await db_session.execute(stmt)
        group = group.scalars().first()
        group.users.append(user)
        stmt = (select(Group).filter(Group.id == 2)
                .options(selectinload(Group.users)))
        group_2 = await db_session.execute(stmt)
        group_2 = group_2.scalars().first()
        group_2.users.append(user)
        await db_session.commit()
        response = auth_client.get(
            '/groups/me',
        )
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert len(result) == 2
        assert result[0]['id'] in (1, 2)
        assert result[1]['id'] in (1, 2)
        assert result[0]['id'] != result[1]['id']

    async def test_get_group_by_id_user(
            self,
            register_client,
            moc_groups,
            moc_users,
            db_session: AsyncSession,
            auth_client: TestClient
    ):
        """Тест получения юзером группы по id."""
        stmt_1 = select(User).options(selectinload(User.groups))
        user = await db_session.execute(stmt_1)
        user = user.scalars().first()
        stmt = (select(Group).filter(Group.id == 1)
                .options(selectinload(Group.users)))
        group = await db_session.execute(stmt)
        group = group.scalars().first()
        group.users.append(user)
        stmt = (select(Group).filter(Group.id == 2)
                .options(selectinload(Group.users)))
        group_2 = await db_session.execute(stmt)
        group_2 = group_2.scalars().first()
        group_2.users.append(user)
        await db_session.commit()
        response = auth_client.get('groups/me/1')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['id'] == 1
        response = auth_client.get('/groups/me/3')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        response = auth_client.get('/groups/me/22')
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteGroup:
    async def test_delete_group_superuser(
            self,
            moc_groups,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест удаления группы суперюзером."""
        stmt = func.count(Group.id)
        groups = await db_session.execute(stmt)
        groups = groups.scalar()
        response = auth_superuser.delete(
            '/groups/1'
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        groups_after_remove = await db_session.execute(stmt)
        groups_after_remove = groups_after_remove.scalar()
        assert groups_after_remove == groups - 1
        stmt = select(Group).filter(Group.id == 1)
        removed_group = await db_session.execute(stmt)
        removed_group = removed_group.scalars().first()
        assert removed_group is None

    async def test_forbidden_delete_group_user(
            self,
            moc_groups,
            auth_client: TestClient
    ):
        """Тест запрета удаления группы юзером."""
        response = auth_client.delete(
            '/groups/1'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_formidden_delete_group_nonauth(
            self,
            new_client: TestClient
    ):
        """Тест запрета удаления группы неавторизованным пользователем."""
        response = new_client.delete(
            '/groups/1'
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestUpdateGroup:
    async def test_update_group_superuser(
            self,
            moc_groups,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест апдейта группы суперюзером."""
        stmt = select(Group).filter(Group.id == 1)
        group = await db_session.execute(stmt)
        group = group.scalars().first()
        assert group.id == 1
        assert group.name != UPDATE_SCHEME['name']
        assert group.description != UPDATE_SCHEME['description']
        response = auth_superuser.patch(
            '/groups/1',
            json=UPDATE_SCHEME
        )
        assert response.status_code == status.HTTP_200_OK
        upated_group = await db_session.execute(stmt)
        upated_group = upated_group.scalars().first()
        assert group.id == upated_group.id
        assert upated_group.name == UPDATE_SCHEME['name']
        assert upated_group.description == UPDATE_SCHEME['description']

    async def test_forbidden_update_group_user(
            self,
            auth_client: TestClient
    ):
        """Тест запрета апдейта группы юзером."""
        response = auth_client.patch(
            '/groups/1',
            json=UPDATE_SCHEME
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_forbidden_update_group_nonauth(
            self,
            new_client: TestClient
    ):
        """Тест запрета апдейта неавторизованным пользователем."""
        response = new_client.patch(
            '/groups/1',
            json=UPDATE_SCHEME
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
