from pydantic import BaseModel, Field


class CommonCreate(BaseModel):
    all_notification: str
    profile: str
    ok: str
    exit: str
    cancel: str
    main: str
    tasks: str
    subscription: str
    account: str
    notifications: str
    help: str
    contacts: str
    email: str
    email_placeholder: str
    login: str
    login_placeholder: str
    password: str
    password_placeholder: str
    message: str
    message_placeholder: str


class CommonRead(CommonCreate):
    all_notification: str = Field(serialization_alias='allNotification')
    email_placeholder: str = Field(serialization_alias='emailPlaceholder')
    login_placeholder: str = Field(serialization_alias='loginPlaceholder')
    password_placeholder: str = Field(
        serialization_alias='passwordPlaceholder'
    )
    message_placeholder: str = Field(serialization_alias='messagePlaceholder')


class HeaderCreate(BaseModel):
    modal_title: str
    modal_question: str


class HeaderRead(HeaderCreate):
    modal_title: str = Field(serialization_alias='modalTitle')
    modal_question: str = Field(serialization_alias='modalQuestion')


class AuthCreate(BaseModel):
    welcome: str
    auth_title1: str
    auth_title2: str
    forgot_password: str
    enter: str
    register_: str


class AuthRead(AuthCreate):
    auth_title1: str = Field(serialization_alias='authTitle1')
    auth_title2: str = Field(serialization_alias='authTitle2')
    forgot_password: str = Field(serialization_alias='forgotPassword')
    register_: str = Field(serialization_alias='register')


class ContactsCreate(BaseModel):
    support: str
    text: str
    our_contacts: str
    phones: str
    phone1: str
    phone2: str
    select_label: str
    select_placeholder: str
    select_option1: str
    select_option2: str
    select_option3: str
    email_placeholder: str


class ContactsRead(ContactsCreate):
    our_contacts: str = Field(serialization_alias='ourContacts')
    select_label: str = Field(serialization_alias='selectLabel')
    select_placeholder: str = Field(serialization_alias='selectPlaceholder')
    select_option1: str = Field(serialization_alias='selectOption1')
    select_option2: str = Field(serialization_alias='selectOption2')
    select_option3: str = Field(serialization_alias='selectOption3')
    email_placeholder: str = Field(serialization_alias='emailPlaceholder')


class HelpCreate(BaseModel):
    title: str
    questions: str
    write_us: str


class HelpRead(HelpCreate):
    write_us: str = Field(serialization_alias='writeUs')


class MainCreate(BaseModel):
    title1: str
    text1: str
    text2: str
    text3: str
    title2: str
    text4: str
    button_text: str
    title3: str


class MainRead(MainCreate):
    button_text: str = Field(serialization_alias='buttonText')


class RestoreCreate(BaseModel):
    restore_password: str
    text: str
    button_text: str
    modal_title: str
    modal_agreements: str
    modal_option1: str
    modal_option2: str
    modal_option3: str
    modal_option4: str
    modal_check1: str
    modal_check2: str
    modal_check3: str
    modal_check4: str


class RestoreRead(RestoreCreate):
    restore_password: str = Field(serialization_alias='restorePassword')
    button_text: str = Field(serialization_alias='buttonText')
    modal_title: str = Field(serialization_alias='modalTitle')
    modal_agreements: str = Field(serialization_alias='modalAgreements')
    modal_option1: str = Field(serialization_alias='modalOption1')
    modal_option2: str = Field(serialization_alias='modalOption2')
    modal_option3: str = Field(serialization_alias='modalOption3')
    modal_option4: str = Field(serialization_alias='modalOption4')
    modal_check1: str = Field(serialization_alias='modalChek1')
    modal_check2: str = Field(serialization_alias='modalChek2')
    modal_check3: str = Field(serialization_alias='modalChek3')
    modal_check4: str = Field(serialization_alias='modalChek4')


class SubscriptionCreate(BaseModel):
    button_text1: str
    button_text2: str
    button_text3: str


class SubscriptionRead(SubscriptionCreate):
    button_text1: str = Field(serialization_alias='buttonText1')
    button_text2: str = Field(serialization_alias='buttonText2')
    button_text3: str = Field(serialization_alias='buttonText3')


class TasksCreate(BaseModel):
    breadcrumb: str
    loading: str
    button_text1: str
    button_text2: str
    button_text3: str


class TasksRead(TasksCreate):
    button_text1: str = Field(serialization_alias='buttonText1')
    button_text2: str = Field(serialization_alias='buttonText2')
    button_text3: str = Field(serialization_alias='buttonText3')


class ErrorsCreate(BaseModel):
    incorect_email: str
    required_email: str
    required_login: str
    required_password: str
    requirement_password: str
    error400: str
    error409: str
    error500: str


class ErrorsRead(ErrorsCreate):
    incorect_email: str = Field(serialization_alias='incorectEmail')
    required_email: str = Field(serialization_alias='requiredEmail')
    required_login: str = Field(serialization_alias='requiredLogin')
    required_password: str = Field(serialization_alias='requiredPassword')
    requirement_password: str = Field(
        serialization_alias='requirementPassword'
    )


class LocaleCreate(BaseModel):
    language: str
    common: CommonCreate
    header: HeaderCreate
    auth: AuthCreate
    contacts: ContactsCreate
    help: HelpCreate
    main: MainCreate
    restore: RestoreCreate
    subscription: SubscriptionCreate
    tasks: TasksCreate
    errors: ErrorsCreate


class LocaleCreated(LocaleCreate):
    id: int

    class Config:
        from_attributes = True


class LocaleRead(BaseModel):
    id: int
    language: str

    class Config:
        from_attributes = True


class LocaleReadByID(BaseModel):
    common: CommonRead
    header: HeaderRead
    auth: AuthRead
    contacts: ContactsRead
    help: HelpRead
    main: MainRead
    restore: RestoreRead
    subscription: SubscriptionRead
    tasks: TasksRead
    errors: ErrorsRead
