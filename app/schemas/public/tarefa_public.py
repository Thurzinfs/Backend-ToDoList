from pydantic import BaseModel
from app.schemas.public.user_public import UserPublic
from datetime import datetime, date
from typing import Optional

class TarefaPublic(BaseModel):
    id: int
    nome: str
    descricao: str
    concluida: bool
    data: datetime
    prazo: date
    data_conclusao: Optional[datetime] = None
    usuario_id: int