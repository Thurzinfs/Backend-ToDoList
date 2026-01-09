from pydantic import BaseModel
from datetime import datetime

class UserPublic(BaseModel):
    id: int
    nome: str
    email: str 
    password: str
    criado: datetime