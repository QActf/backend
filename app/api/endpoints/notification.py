from typing import List

from fastapi import APIRouter

router = APIRouter()


@router.get('/', response_model=List[None])
async def get_all_notifications(
) -> List[None]:
    """Возвращает все Notification."""
    pass


@router.post('/', response_model=None)
async def create_notification(
):
    """Создать Notification"""
    pass
