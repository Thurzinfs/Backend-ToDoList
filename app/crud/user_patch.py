from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.public.user_public import UserPublic
from app.schemas.update.user_update import UserUpdate
from app.db.database import get_session
from app.core.security import get_current_user
from app.services.user_services import patch_user_service

patch_router = APIRouter(prefix='/api/users', tags=['users'])

@patch_router.patch(
    path='/{user_id}',
    response_model=UserPublic
)
def update_user(
    user_id: int,
    user: UserUpdate,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    data = user.model_dump(exclude_unset=True)

    return patch_user_service(
        session=session,
        user_data=data,
        user_id=user_id,
        current_user=current_user
    )