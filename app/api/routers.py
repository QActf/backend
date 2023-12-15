from fastapi import APIRouter

from app.api.endpoints import (
    user_router, group_router, profile_router, tariff_router,
    notification_router,
)

main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(group_router, prefix='/groups', tags=['Group'])
main_router.include_router(profile_router, prefix='/profiles',
                           tags=['Profile'])
main_router.include_router(tariff_router, prefix='/tariffs', tags=['Tariff'])
main_router.include_router(notification_router, prefix='/notifications',
                           tags=['Notification'])
