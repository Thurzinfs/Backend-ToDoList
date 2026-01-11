from pydantic import BaseModel
from datetime import date, datetime

class TarefaPut(BaseModel):
    nome: str
    descricao: str
    concluida: bool
    prazo: date
    prioridade: str
    data_conclusao: datetime
