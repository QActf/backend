from fastapi import APIRouter

from app.api.endpoints import (
    user_router, group_router, profile_router, tariff_router,
    notification_router, examination_router, achievement_router,
    course_router, task_router
)

main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(group_router, prefix='/groups', tags=['Group'])
main_router.include_router(profile_router, prefix='/profiles',
                           tags=['Profile'])
main_router.include_router(tariff_router, prefix='/tariffs', tags=['Tariff'])
main_router.include_router(notification_router, prefix='/notifications',
                           tags=['Notification'])
main_router.include_router(examination_router, prefix='/examinations',
                           tags=['Examination'])
main_router.include_router(achievement_router, prefix='/achievements',
                           tags=['Achievement'])
main_router.include_router(course_router, prefix='/courses',
                           tags=['Course'])
main_router.include_router(task_router, prefix='/tasks', tags=['Task'])
