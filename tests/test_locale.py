from fastapi import Response, status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Locale

from .utils import get_obj_count

CREATE_SCHEME = {
    'language': 'en',
    'common': {
        'all_notification': 'privet',
        'profile': 'privet',
        'ok': 'privet',
        'exit': 'privet',
        'cancel': 'privet',
        'main': 'privet',
        'tasks': 'privet',
        'subscription': 'privet',
        'account': 'privet',
        'notifications': 'privet',
        'help': 'privet',
        'contacts': 'privet',
        'email': 'privet',
        'email_placeholder': 'privet',
        'login': 'privet',
        'login_placeholder': 'privet',
        'password': 'privet',
        'password_placeholder': 'privet',
        'message': 'privet',
        'message_placeholder': 'privet'
    },
    'header': {
        'modal_title': 'privet',
        'modal_question': 'privet',
    },
    'auth': {
        'welcome': 'privet',
        'auth_title1': 'privet',
        'auth_title2': 'privet',
        'forgot_password': 'privet',
        'enter': 'privet',
        'register_': 'privet',
    },
    'contacts': {
        'support': 'privet',
        'text': 'privet',
        'our_contacts': 'privet',
        'phones': 'privet',
        'phone1': 'privet',
        'phone2': 'privet',
        'select_label': 'privet',
        'select_placeholder': 'privet',
        'select_option1': 'privet',
        'select_option2': 'privet',
        'select_option3': 'privet',
        'email_placeholder': 'privet',
    },
    'help': {
        'title': 'privet',
        'questions': 'privet',
        'write_us': 'privet',
    },
    'main': {
        'title1': 'privet',
        'text1': 'privet',
        'text2': 'privet',
        'text3': 'privet',
        'title2': 'privet',
        'text4': 'privet',
        'button_text': 'privet',
        'title3': 'privet',
    },
    'restore': {
        'restore_password': 'privet',
        'text': 'privet',
        'button_text': 'privet',
        'modal_title': 'privet',
        'modal_agreements': 'privet',
        'modal_option1': 'privet',
        'modal_option2': 'privet',
        'modal_option3': 'privet',
        'modal_option4': 'privet',
        'modal_check1': 'privet',
        'modal_check2': 'privet',
        'modal_check3': 'privet',
        'modal_check4': 'privet',
    },
    'subscription': {
        'button_text1': 'privet',
        'button_text2': 'privet',
        'button_text3': 'privet',
    },
    'tasks': {
        'breadcrumb': 'privet',
        'loading': 'privet',
        'button_text1': 'privet',
        'button_text2': 'privet',
        'button_text3': 'privet',
    },
    'errors': {
        'incorect_email': 'privet',
        'required_email': 'privet',
        'required_login': 'privet',
        'required_password': 'privet',
        'requirement_password': 'privet',
        'error400': 'privet',
        'error409': 'privet',
        'error500': 'privet',
    }
}

WRONG_CREATE_SCHEME = {
    'language': 'en',
}


class TestCreateLocale:
    async def test_create_locale(
            self,
            db_session: AsyncSession,
            auth_superuser: TestClient,
    ):
        """Тест создания локали."""
        locales = await get_obj_count(Locale, db_session)
        assert locales == 0
        response: Response = await auth_superuser.post(
            '/locales/',
            json=CREATE_SCHEME
        )
        assert response.status_code == status.HTTP_201_CREATED
        new_locale = await get_obj_count(Locale, db_session)
        assert new_locale == locales + 1

    async def test_create_locale_wrong_data(
            self,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест попытки создания локали с неправильными данными."""
        locales_count = await get_obj_count(Locale, db_session)
        response = await auth_superuser.post(
            '/locales/',
            json=WRONG_CREATE_SCHEME,
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        new_locales_count = await get_obj_count(Locale, db_session)
        assert locales_count == new_locales_count

    async def test_create_locale_duplicate(
            self,
            db_session: AsyncSession,
            auth_superuser: TestClient,
    ):
        """Тест запрета создания дубликата локали."""
        await auth_superuser.post('/locales/', json=CREATE_SCHEME)
        locales_count = await get_obj_count(Locale, db_session)
        response: Response = await auth_superuser.post(
            '/locales/',
            json=CREATE_SCHEME,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        new_locales_count = await get_obj_count(Locale, db_session)
        assert locales_count == new_locales_count

    async def test_create_locale_unauthorized_nonauth(
            self,
            new_client: TestClient,
    ):
        """Тест запрета создания локали неавторизованным пользователем."""
        response: Response = await new_client.post(
            '/locales/',
            json=CREATE_SCHEME
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_create_locale_forbidden_auth_user(
            self,
            auth_client: TestClient
    ):
        """Тест запрета создания локали пользователем."""
        response: Response = await auth_client.post(
            '/locales/',
            json=CREATE_SCHEME,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestGetLocale:
    async def test_get_locale_by_id(
            self,
            mock_locales,
            db_session: AsyncSession,
            new_client: TestClient
    ):
        """Тест получения локали по id."""
        response = await new_client.get('/locales/3')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['id'] == 3
        response = await new_client.get('/locales/100')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_all_locales(
            self,
            mock_locales,
            db_session: AsyncSession,
            new_client: TestClient
    ):
        """Тест получения всех локалей."""
        locales_count = await get_obj_count(Locale, db_session)
        response = await new_client.get('/locales/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == locales_count
