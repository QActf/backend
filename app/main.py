
from fastapi import FastAPI
from sqladmin import Admin

from app.admin.authentication import AdminAuth
from app.admin.base import add_admin_models
from app.api.routers import main_router
from app.core.config import settings
from app.core.db import engine
from app.core.init_db import create_first_superuser

app = FastAPI(title=settings.app_title)

app.include_router(main_router)

authentication_backend = AdminAuth(secret_key=settings.secret)

admin = Admin(
    engine=engine,
    app=app,
    authentication_backend=authentication_backend
)


@app.on_event('startup')
async def startup():
    await create_first_superuser()
    await add_admin_models(admin)
