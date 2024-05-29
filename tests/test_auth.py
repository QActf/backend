import pytest
from fastapi import status

from tests.fixtures.user import USER_EMAIL, USER_PASSWORD, USER_USERNAME

REGISTRATION_SCHEMA = {
    'email': USER_EMAIL,
    'password': USER_PASSWORD,
    'role': 'user',
    'username': USER_USERNAME,
}

WRONG_EMAIL = 'wrongtestuser@example.com'
WRONG_PASSWORD = 'wrongpassword'


class TestRegister:
    @pytest.mark.skip
    async def test_register_new_user(self, new_client):
        """Тест регистрации пользователя с корректными данными."""
        response = await new_client.post(
            '/auth/register', json=REGISTRATION_SCHEMA
        )
        assert response.status_code == status.HTTP_201_CREATED, (
            'При успешной регистрации пользователя, '
            'должен возвращаться статус-код 201.'
        )

    async def test_repeat_register_user_bad_code(
            self, register_client, new_client
    ):
        """Тест регистрации пользователя с некорректными данными."""
        response = await new_client.post(
            '/auth/register', json=REGISTRATION_SCHEMA
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST, (
            'Некорректные данные при регистрации пользователя, '
            'должен возвращаться статус-код 400.'
        )

    async def test_repeat_register_user(self, register_client, new_client):
        """Тест регистрации пользователя, который уже есть в БД."""
        response = await new_client.post(
            '/auth/register', json=REGISTRATION_SCHEMA
        )
        assert response.json().get('detail') == (
            'REGISTER_USER_ALREADY_EXISTS'), (
            'Пользователь с указанными данными уже есть в БД.'
        )

    async def test_register_invalid_password(self, new_client):
        """Тест регистрации пользователя с паролем менее трёх символов."""
        data_new_client = REGISTRATION_SCHEMA
        data_new_client['password'] = '!'
        response = await new_client.post(
            '/auth/register', json=data_new_client
        )
        data = response.json()
        assert data == {
            'detail': {
                'code': 'REGISTER_INVALID_PASSWORD',
                'reason': 'Password should be at least 3 characters',
            },
        }, (
            'Пароль должен содержать не менее трёх символов.'
        )

    async def test_register_password_contain_email(self, new_client):
        """Тест регистрации пользователя с паролем, содержащим email."""
        data_new_client = REGISTRATION_SCHEMA
        data_new_client['password'] = USER_EMAIL
        response = await new_client.post(
            '/auth/register', json=data_new_client
        )
        data = response.json()
        assert data == {
            'detail': {
                'code': 'REGISTER_INVALID_PASSWORD',
                'reason': 'Password should not contain e-mail',
            },
        }, (
            'Нельзя зарегистрировать пользователя с паролем, '
            'содержащим в себе email.'
        )

    async def test_register_invalid_json(self, new_client):
        """Тест регистрации пользователя с недопустимыми данными."""
        response = await new_client.post('/auth/register', json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, (
            'Недопустимые данные при регистрации пользователя, '
            'должен возвращаться статус-код 422.'
        )


class TestLogin:
    async def test_login_correct_client(self, new_client, register_client):
        """Тест входа в систему с корректными данными."""
        response = await new_client.post(
           '/auth/jwt/login',
           data={'username': USER_EMAIL, 'password': USER_PASSWORD},
        )
        assert response.status_code == status.HTTP_200_OK, (
            'При успешном входе в систему, '
            'должен возвращаться статус-код 200.'
        )

    async def test_login_wrong_client(self, new_client):
        """Тест входа в систему с неверными данными."""
        response = await new_client.post(
           '/auth/jwt/login',
           data={'username': WRONG_EMAIL, 'password': WRONG_PASSWORD},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST, (
            'При попытке входа в систему с данными, отсутствующими в БД, '
            'должен возвращаться статус-код 400.'
        )

    async def test_login_wrong_username(self, new_client, register_client):
        """Тест входа в систему с неверным email."""
        response = await new_client.post(
           '/auth/jwt/login',
           data={'username': WRONG_EMAIL, 'password': USER_PASSWORD},
        )
        assert response.json().get('email') != register_client.email, (
            'Нельзя войти в систему по email, которого нет в БД. '
        )

    async def test_login_invalid_data(self, new_client, register_client):
        """Тест входа в систему с недопустимыми данными."""
        response = await new_client.post(
           '/auth/jwt/login',
           data={},
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, (
            'При попытке входа в систему с недопустимыми данными '
            'должен возвращаться статус-код 422.'
        )


class TestLogout:
    async def test_logout_auth_client(self, auth_client):
        """Тест выхода из системы залогиненного пользователя."""
        response = await auth_client.post('/auth/jwt/logout')

        assert response.status_code == status.HTTP_204_NO_CONTENT, (
            'При попытке выхода из системы залогиненного пользователя, '
            'должен возвращаться статус-код 204.'
        )

    async def test_logout_new_client(self, new_client):
        """Тест выхода из системы незалогиненного пользователя."""
        response = await new_client.post('/auth/jwt/logout')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
            'При попытке выхода из системы незалогиненного пользователя, '
            'должен возвращаться статус-код 401.'
        )
