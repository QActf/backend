from fastapi import APIRouter

router = APIRouter()


@router.get('/', response_model=list[None])
async def get_all_notifications(
) -> list[None]:
    """Возвращает все Notification."""
    pass


@router.post('/', response_model=None)
async def create_notification(
):
    """Создать Notification"""
    pass


@router.delete('/{obj_id}')
async def delete_profile(
):
    """Удалить объект"""
    pass
