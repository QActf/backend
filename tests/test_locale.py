from fastapi import status, Response
from fastapi.testclient import TestClient

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


class TestCreateLocale:
    async def test_create_locale(
            self,
            db_session,
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
