from __future__ import annotations

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Locale(Base):
    language: Mapped[str] = mapped_column(unique=True)
    common: Mapped[Common] = relationship(back_populates='locale')
    header: Mapped[Header] = relationship(back_populates='locale')
    auth: Mapped[Auth] = relationship(back_populates='locale')
    contacts: Mapped[Contacts] = relationship(back_populates='locale')
    help: Mapped[Help] = relationship(back_populates='locale')
    main: Mapped[Main] = relationship(back_populates='locale')
    restore: Mapped[Restore] = relationship(back_populates='locale')
    subscription: Mapped[Subscription] = relationship(back_populates='locale')
    profile_user: Mapped[ProfileUser] = relationship(back_populates='locale')
    secure: Mapped[Secure] = relationship(back_populates='locale')
    achievements: Mapped[Achievements] = relationship(back_populates='locale')
    tasks: Mapped[Tasks] = relationship(back_populates='locale')
    question_banner: Mapped[QuestionBanner] = relationship(
        back_populates='locale'
    )
    errors: Mapped[Errors] = relationship(back_populates='locale')
    months: Mapped[Months] = relationship(back_populates='locale')


class Common(Base):
    all_notification: Mapped[str]
    profile: Mapped[str]
    ok: Mapped[str]
    save: Mapped[str]
    edit: Mapped[str]
    exit: Mapped[str]
    cancel: Mapped[str]
    main: Mapped[str]
    tasks: Mapped[str]
    subscription: Mapped[str]
    account: Mapped[str]
    notifications: Mapped[str]
    help: Mapped[str]
    contacts: Mapped[str]
    email: Mapped[str]
    email_placeholder: Mapped[str]
    login: Mapped[str]
    login_placeholder: Mapped[str]
    password: Mapped[str]
    password_placeholder: Mapped[str]
    message: Mapped[str]
    message_placeholder: Mapped[str]
    upload: Mapped[str]
    locale_id = mapped_column(
        Integer, ForeignKey('locale.id')
    )
    locale: Mapped['Locale'] = relationship(back_populates='common')


class Header(Base):
    modal_title: Mapped[str]
    modal_question: Mapped[str]
    locale_id = mapped_column(
        Integer, ForeignKey('locale.id')
    )
    locale: Mapped['Locale'] = relationship(back_populates='header')


class Auth(Base):
    welcome: Mapped[str]
    auth_title1: Mapped[str]
    auth_title2: Mapped[str]
    forgot_password: Mapped[str]
    enter: Mapped[str]
    register: Mapped[str]
    locale_id = mapped_column(
        Integer, ForeignKey('locale.id')
    )
    locale: Mapped['Locale'] = relationship(back_populates='auth')


class Contacts(Base):
    support: Mapped[str]
    text: Mapped[str]
    our_contacts: Mapped[str]
    phones: Mapped[str]
    phone1: Mapped[str]
    phone2: Mapped[str]
    select_label: Mapped[str]
    select_placeholder: Mapped[str]
    select_option1: Mapped[str]
    select_option2: Mapped[str]
    select_option3: Mapped[str]
    email_placeholder: Mapped[str]
    locale_id = mapped_column(
        Integer, ForeignKey('locale.id')
    )
    locale: Mapped['Locale'] = relationship(back_populates='contacts')


class Help(Base):
    title: Mapped[str]
    locale_id = mapped_column(
        Integer, ForeignKey('locale.id')
    )
    locale: Mapped['Locale'] = relationship(back_populates='help')


class Main(Base):
    title1: Mapped[str]
    text1: Mapped[str]
    text2: Mapped[str]
    text3: Mapped[str]
    title2: Mapped[str]
    text4: Mapped[str]
    button_text: Mapped[str]
    title3: Mapped[str]
    locale_id = mapped_column(
        Integer, ForeignKey('locale.id')
    )
    locale: Mapped['Locale'] = relationship(back_populates='main')


class Restore(Base):
    restore_password: Mapped[str]
    text: Mapped[str]
    button_text: Mapped[str]
    modal_title: Mapped[str]
    modal_agreements: Mapped[str]
    modal_option1: Mapped[str]
    modal_option2: Mapped[str]
    modal_option3: Mapped[str]
    modal_option4: Mapped[str]
    modal_check1: Mapped[str]
    modal_check2: Mapped[str]
    modal_check3: Mapped[str]
    modal_check4: Mapped[str]
    locale_id = mapped_column(
        Integer, ForeignKey('locale.id')
    )
    locale: Mapped['Locale'] = relationship(back_populates='restore')


class Subscription(Base):
    button_text1: Mapped[str]
    button_text2: Mapped[str]
    button_text3: Mapped[str]
    locale_id = mapped_column(
        Integer, ForeignKey('locale.id')
    )
    locale: Mapped['Locale'] = relationship(back_populates='subscription')


class ProfileUser(Base):
    study: Mapped[str]
    secure: Mapped[str]
    achievement: Mapped[str]
    date_not_found: Mapped[str]
    breadcrumb: Mapped[str]
    activity: Mapped[str]
    firstname: Mapped[str]
    secondname: Mapped[str]
    lastname: Mapped[str]
    birthday: Mapped[str]
    gender: Mapped[str]
    upload_avatar: Mapped[str]
    locale_id = mapped_column(
        Integer, ForeignKey('locale.id')
    )
    locale: Mapped['Locale'] = relationship(back_populates='profile_user')


class Secure(Base):
    change_password: Mapped[str]
    current_password: Mapped[str]
    new_password: Mapped[str]
    confirm_password: Mapped[str]
    locale_id = mapped_column(
        Integer, ForeignKey('locale.id')
    )
    locale: Mapped['Locale'] = relationship(back_populates='secure')


class Achievements(Base):
    my_achievements: Mapped[str]
    level: Mapped[str]
    tests_completed: Mapped[str]
    tasks_completed: Mapped[str]
    not_passed: Mapped[str]
    achievements_week: Mapped[str]
    achievements_api: Mapped[str]
    achievements_grade: Mapped[str]
    achievements_db: Mapped[str]
    achievements_month: Mapped[str]
    locale_id = mapped_column(
        Integer, ForeignKey('locale.id')
    )
    locale: Mapped['Locale'] = relationship(back_populates='achievements')


class Tasks(Base):
    breadcrumb: Mapped[str]
    loading: Mapped[str]
    button_text1: Mapped[str]
    button_text2: Mapped[str]
    button_text3: Mapped[str]
    locale_id = mapped_column(
        Integer, ForeignKey('locale.id')
    )
    locale: Mapped['Locale'] = relationship(back_populates='tasks')


class QuestionBanner(Base):
    questions: Mapped[str]
    write_us: Mapped[str]
    locale_id = mapped_column(
        Integer, ForeignKey('locale.id')
    )
    locale: Mapped['Locale'] = relationship(back_populates='question_banner')


class Errors(Base):
    required: Mapped[str]
    incorect_email: Mapped[str]
    required_email: Mapped[str]
    required_login: Mapped[str]
    required_password: Mapped[str]
    requirement_password: Mapped[str]
    error400: Mapped[str]
    error409: Mapped[str]
    error500: Mapped[str]
    locale_id = mapped_column(
        Integer, ForeignKey('locale.id')
    )
    locale: Mapped['Locale'] = relationship(back_populates='errors')


class Months(Base):
    january: Mapped[str]
    february: Mapped[str]
    march: Mapped[str]
    april: Mapped[str]
    may: Mapped[str]
    june: Mapped[str]
    july: Mapped[str]
    august: Mapped[str]
    september: Mapped[str]
    october: Mapped[str]
    november: Mapped[str]
    december: Mapped[str]
    locale_id = mapped_column(
        Integer, ForeignKey('locale.id')
    )
    locale: Mapped['Locale'] = relationship(back_populates='months')
