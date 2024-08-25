from fastapi import APIRouter

from app.api.endpoints import (
    achievement_router, course_router, examination_router, group_router,
    locale_router, notification_router, profile_router, question_router,
    subscription_router, tariff_router, task_router, user_router,
)

main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(group_router, prefix='/groups', tags=['Groups'])
main_router.include_router(tariff_router, prefix='/tariffs', tags=['Tariffs'])
main_router.include_router(
    examination_router, prefix='/examinations', tags=['Examinations']
)
main_router.include_router(course_router, prefix='/courses', tags=['Courses'])
main_router.include_router(task_router, prefix='/tasks', tags=['Tasks'])
main_router.include_router(
    achievement_router, prefix='/achievements', tags=['Achievements']
)
main_router.include_router(
    profile_router, prefix='/profiles', tags=['Profiles']
)
main_router.include_router(
    question_router, prefix='/questions', tags=['Questions']
)
main_router.include_router(
    locale_router, prefix='/locales', tags=['Locales']
)
main_router.include_router(
    notification_router, prefix='/notifications', tags=['Notifications']
)
main_router.include_router(
    subscription_router, prefix='/subscriptions', tags=['Subscriptions']
)
