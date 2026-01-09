from fastapi import APIRouter, Depends
from app.db.database import get_session
from sqlalchemy.orm import Session
from app.schemas.schemas.user_schemas import UserSchema
from app.schemas.public.user_public import UserPublic
from app.services.user_services import create_user_service

post_router = APIRouter(prefix="/api/users", tags=['users'])

@post_router.post(
    path='/',
    response_model=UserPublic
)
def create_user(
    user: UserSchema,
    session: Session = Depends(get_session)
):
    data = user.model_dump()

    return create_user_service(session, data)