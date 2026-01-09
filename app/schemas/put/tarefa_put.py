from pydantic import BaseModel
from datetime import date, datetime

class TarefaPut(BaseModel):
    nome: str
    descricao: str
    concluida: bool
    prazo: date
    data_conclusao: datetime
