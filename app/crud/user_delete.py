from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_session
from app.core.security import get_current_user
from app.services.user_services import delete_user_service

delete_router = APIRouter(prefix="/api/users", tags=['users'])

@delete_router.delete(
    path='/{user_id}'
)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    return delete_user_service(
        session = session, 
        user_id =user_id, 
        current_user = current_user
    )