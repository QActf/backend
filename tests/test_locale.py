from fastapi import Response, status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Locale

from .utils import get_obj_by_id, get_obj_count

CREATE_SCHEMA = {
    'language': 'ru',
    'common': {
        'all_notification': 'Все уведомления',
        'profile': 'Профиль',
        'ok': 'Подтвердить',
        'save': 'Сохранить',
        'edit': 'Редактировать',
        'exit': 'Выйти',
        'cancel': 'Отмена',
        'main': 'Главная',
        'tasks': 'Задачи',
        'subscription': 'Подписка',
        'account': 'Мой аккаунт',
        'notifications': 'Уведомления',
        'help': 'Помощь',
        'contacts': 'Контакты',
        'email': 'Почта',
        'email_placeholder': 'Введите почту',
        'login': 'Логин',
        'login_placeholder': 'Введите логин',
        'password': 'Пароль',
        'password_placeholder': 'Введите пароль',
        'message': 'Сообщение',
        'message_placeholder': 'Введите сообщение',
        'upload': 'Загрузить',
    },
    'header': {
        'modal_title': 'Выход из личного кабинета',
        'modal_question': 'Вы уверены, что хотите выйти из личного кабинета?',
    },
    'auth': {
        'welcome': 'Добро пожаловать!',
        'auth_title1': 'Введите логин и пароль',
        'auth_title2': 'Введите свои данные',
        'forgot_password': 'Забыли пароль?',
        'enter': 'Войти в систему',
        'register_': 'Зарегистрироваться',
    },
    'contacts': {
        'support': 'Служба поддержки',
        'text': (
            'Если у Вас возникнут вопросы, можете обращаться службу '
            'поддержки по телефону либо отправить сообщение, мы '
            'обязательно свяжемся с Вами и поможем!'
        ),
        'our_contacts': 'Наши контакты',
        'phones': 'Телефоны',
        'phone1': '87212777777',
        'phone2': '+77776666666',
        'select_label': 'Тема',
        'select_placeholder': 'Выберите из списка',
        'select_option1': 'Тема 1',
        'select_option2': 'Тема 2',
        'select_option3': 'Тема 3',
        'email_placeholder': 'Введите личный email',
    },
    'help': {
        'title': 'База знаний',
    },
    'main': {
        'title1': 'Практика для QA инженеров',
        'text1': 'Наша миссия',
        'text2': (
            '— помочь тем, кто стремится войти в область информационных '
            'технологий, освоить профессию тестировщика и набраться '
            'практических навыков.'
        ),
        'text3': (
            'Абсолютно верно, теоретическое обучение - это только начало. '
            'Существует множество книг и материалов о тестировании, но чтобы '
            'стать квалифицированным специалистом в области QA, нужно '
            'получить практический опыт.'
        ),
        'title2': 'Обучение на этом курсе — как симулятор стажировки',
        'text4': (
            'Мы предоставляем нашим студентам возможность не только учить '
            'теорию, но и применять полученные знания на практических задачах '
            'и проектах, что позволит набраться опыта, приближенного к '
            'реальным условиям работы QA - специалиста.'
        ),
        'button_text': 'Начать обучение',
        'title3': 'Вопросы и ответы',
    },
    'restore': {
        'restore_password': 'Восстановление пароля',
        'text': (
            'На указанный Вами e-mail будет отправлено письмо, с '
            'новым сгенерированным паролем'
        ),
        'button_text': 'Отправить код подтверждения',
        'modal_title': 'Вход в систему «Аналитика»',
        'modal_agreements': 'ТРЕБУЕТСЯ ВАШЕ СОГЛАСИЕ ПО СЛЕДУЮЩИМ ПУНКТАМ:',
        'modal_option1': (
            'Я подтверждаю, что вся представленная '
            'информация является достоверной и точной;'
        ),
        'modal_option2': (
            'Я несу ответственность в соответствии с '
            'действующим законодательством РК за предоставление заведомо '
            'ложных или неполных сведений;'
        ),
        'modal_option3': (
            'Я выражаю свое согласие на необходимое '
            'использование и обработку своих персональных данных, в том числе '
            'в информационных системах;'
        ),
        'modal_option4': (
            'В случае обнаружения представленной '
            'пользователями неполной и/или недостоверной информации, '
            'услугодатель ответственности не несет.'
        ),
        'modal_check1': (
            'Я подтверждаю свое согласие со всеми вышеперечисленными пунктами'
        ),
        'modal_check2': 'С пользовательским соглашением',
        'modal_check3': 'С политикой конфиденциальности',
        'modal_check4': 'ознакомлен(-а) и согласен(-на)',
    },
    'subscription': {
        'button_text1': 'Входит в текущую подписку',
        'button_text2': 'Текущая подписка',
        'button_text3': 'Приобрести',
    },
    'profile_user': {
        'study': 'Обучение',
        'secure': 'Безопасность',
        'achievement': 'Достижения',
        'date_not_found': 'Дата не найдена',
        'breadcrumb': 'Редактирование личных данных',
        'activity': 'Активность в системе',
        'firstname': 'Имя',
        'secondname': 'Отчество (при наличии)',
        'lastname': 'Фамилия',
        'birthday': 'Дата рождения',
        'gender': 'Пол',
        'upload_avatar': 'Загрузите аватарку',
    },
    'secure': {
        'change_password': 'Смена пароля',
        'current_password': 'Текущий пароль',
        'new_password': 'Новый пароль',
        'confirm_password': 'Подтверждение пароля',
    },
    'achievements': {
        'my_achievements': 'Мои достижения',
        'level': 'Уровень',
        'tests_completed': 'Пройденых тестов',
        'tasks_completed': 'Выполненных заданий',
        'not_passed': 'Нет пройденных',
        'achievements_week': 'Успехи за неделю',
        'achievements_api': 'За тестирование API',
        'achievements_grade': 'За тестирование по грейду',
        'achievements_db': 'За тестирование БД',
        'achievements_month': 'Успехи за месяц',
    },
    'tasks': {
        'breadcrumb': 'Практики',
        'loading': 'Загрузка, подождите...',
        'button_text1': 'Добавить тестовый кейс',
        'button_text2': 'Проверить',
        'button_text3': 'Перейти',
    },
    'question_banner': {
        'questions': 'Возникли вопросы?',
        'write_us': 'Написать нам',
    },
    'errors': {
        'required': 'Поле обязательно',
        'incorect_email': 'Введите корректную почту',
        'required_email': 'Почта это обязательное поле',
        'required_login': 'Логин это обязательное поле',
        'required_password': 'Пароль это обязательное поле',
        'requirement_password': (
            'Пароль должен быть не менее 6 символов, включать '
            'заглавные и строчные буквы, цифры и специальные символы'
        ),
        'error400': 'Неверная почта или пароль',
        'error409': 'Пользователь уже существует',
        'error500': 'Что то пошло не так, попробуйте еще раз',
    },
    'months': {
        'january': 'янв.',
        'february': 'фев.',
        'march': 'мар.',
        'april': 'апр.',
        'may': 'мая',
        'june': 'июня',
        'july': 'июля',
        'august': 'авг.',
        'september': 'сен.',
        'october': 'окт.',
        'november': 'ноя.',
        'december': 'дек.',
    },
}

WRONG_SCHEMA = {
    'language': 'en',
    'common': {
        'ok': 'ok',
    }
}

UPDATE_SCHEMA = dict(
    CREATE_SCHEMA, common={**CREATE_SCHEMA['common'], 'ok': 'ok'}
)


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
            json=CREATE_SCHEMA
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
            json=WRONG_SCHEMA,
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
        await auth_superuser.post('/locales/', json=CREATE_SCHEMA)
        locales_count = await get_obj_count(Locale, db_session)
        response: Response = await auth_superuser.post(
            '/locales/',
            json=CREATE_SCHEMA,
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
            json=CREATE_SCHEMA,
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_create_locale_forbidden_auth_user(
            self,
            auth_client: TestClient
    ):
        """Тест запрета создания локали пользователем."""
        response: Response = await auth_client.post(
            '/locales/',
            json=CREATE_SCHEMA,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestPutLocale:
    async def test_update_locale(
            self,
            db_session: AsyncSession,
            auth_superuser: TestClient,
    ):
        """Тест обновления локали."""
        locales_count = await get_obj_count(Locale, db_session)
        assert locales_count == 0
        response = await auth_superuser.put(
            '/locales/',
            json=CREATE_SCHEMA,
        )
        assert response.status_code == status.HTTP_200_OK
        new_locales_count = await get_obj_count(Locale, db_session)
        assert new_locales_count == locales_count + 1

        response = await auth_superuser.put(
            '/locales/',
            json=UPDATE_SCHEMA,
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['common']['ok'] == UPDATE_SCHEMA['common']['ok']
        db_obj = await get_obj_by_id(
            index=1,
            model=Locale,
            related_objects=[Locale.common],
            session=db_session,
        )
        assert db_obj.common.ok == UPDATE_SCHEMA['common']['ok']

    async def test_update_locale_wrong_data(
            self,
            mock_locales,
            db_session: AsyncSession,
            auth_superuser: TestClient,
    ):
        """Тест попытки обновления локали с неправильными данными."""
        locales_count = await get_obj_count(Locale, db_session)
        response = await auth_superuser.put(
            '/locales/',
            json=WRONG_SCHEMA,
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        new_locales_count = await get_obj_count(Locale, db_session)
        assert locales_count == new_locales_count
        db_obj = await get_obj_by_id(
            index=1,
            model=Locale,
            related_objects=[Locale.common],
            session=db_session,
        )
        assert db_obj.common.ok == CREATE_SCHEMA['common']['ok']

    async def test_update_locale_unauthorized_nonauth(
            self,
            mock_locales,
            new_client: TestClient,
    ):
        """Тест запрета обновления локали неавторизованным пользователем."""
        response: Response = await new_client.put(
            '/locales/',
            json=UPDATE_SCHEMA,
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_update_locale_forbidden_auth_user(
            self,
            mock_locales,
            auth_client: TestClient,
    ):
        """Тест запрета обновления локали пользователем."""
        response: Response = await auth_client.put(
            '/locales/',
            json=UPDATE_SCHEMA,
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

    async def test_get_locale_by_language(
            self,
            mock_locales,
            db_session: AsyncSession,
            new_client: TestClient
    ):
        """Тест получения локали по language."""
        response = await new_client.get('/locales/lang/ch')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['language'] == 'ch'
        response = await new_client.get('/locales/lang/xx')
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


class TestDeleteLocale:
    async def test_delete_locale_by_language(
            self,
            mock_locales,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест удаления локали по language."""
        locales_count = await get_obj_count(Locale, db_session)
        response = await auth_superuser.delete('/locales/lang/ch')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        new_locales_count = await get_obj_count(Locale, db_session)
        assert locales_count - 1 == new_locales_count

    async def test_delete_locale_unauthorized_nonauth(
            self,
            mock_locales,
            db_session: AsyncSession,
            new_client: TestClient
    ):
        """Тест запрета удаления локали неавторизованным пользователем."""
        response = await new_client.delete('/locales/lang/ch')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_delete_locale_forbidden_auth_user(
            self,
            mock_locales,
            db_session: AsyncSession,
            auth_client: TestClient
    ):
        """Тест запрета удаления локали пользователем."""
        response = await auth_client.delete('/locales/lang/ch')
        assert response.status_code == status.HTTP_403_FORBIDDEN
