from fastapi import APIRouter

from app.api.endpoints import (
    user_router, group_router, tariff_router,
    examination_router, course_router, task_router,
    achievement_router, profile_router,
)

main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(
    group_router, prefix='/group', tags=['Group']
)
main_router.include_router(
    tariff_router, prefix='/tariff', tags=['Tariff']
)
main_router.include_router(
    examination_router, prefix='/examination', tags=['Examination']
)
main_router.include_router(
    course_router, prefix='/course', tags=['Course']
)
main_router.include_router(
    task_router, prefix='/task', tags=['Task']
)
main_router.include_router(
    achievement_router, prefix='/achievement', tags=['Achievement']
)
main_router.include_router(
    profile_router, prefix='/profile', tags=['Profile']
)
