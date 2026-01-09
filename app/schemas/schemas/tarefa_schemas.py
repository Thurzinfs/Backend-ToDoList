from pydantic import BaseModel
from datetime import date

class TarefaSchemas(BaseModel):
    nome: str
    descricao: str
    prazo: date
    concluida: bool