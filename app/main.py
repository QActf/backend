import logging.config
import sys

from fastapi import FastAPI, applications
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from sqladmin import Admin

from app.admin.authentication import AdminAuth
from app.admin.base import add_admin_models
from app.api.routers import main_router
from app.core.config import settings
from app.core.db import engine
from app.core.init_db import create_first_superuser
from app.core.logger_config import LOGGING_CONFIG
from app.core.middleware import LoggerMiddleware
from app.services.mail import MockEmailServer

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args,
        **kwargs,
        swagger_js_url=(
            'https://cdn.staticfile.net/swagger-ui/5.1.0/'
            'swagger-ui-bundle.min.js'
        ),
        swagger_css_url=(
            'https://cdn.staticfile.net/swagger-ui/5.1.0/swagger-ui.min.css'
        ),
    )


applications.get_swagger_ui_html = swagger_monkey_patch

app = FastAPI(
    title=settings.app_title,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

origins = [f'http://{settings.host}']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
if "pytest" not in sys.modules:
    app.add_middleware(LoggerMiddleware)

app.include_router(main_router)

authentication_backend = AdminAuth(secret_key=settings.secret)

admin = Admin(
    engine=engine, app=app, authentication_backend=authentication_backend
)


@app.on_event('startup')
async def startup():
    await create_first_superuser()
    await add_admin_models(admin)

    logger.info("Application started.")


@app.on_event('shutdown')
async def shutdown():
    logger.info("Application stopped.")


if settings.EMAIL_MOCK_SERVER:
    email_server = MockEmailServer()
    email_server.start()
