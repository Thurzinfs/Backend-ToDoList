from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class TarefaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    concluida: Optional[bool] = None
    prazo: Optional[date] = None
    prioridade: Optional[str] = None
    data_conclusao: Optional[datetime] = None