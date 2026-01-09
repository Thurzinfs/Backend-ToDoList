from pydantic import BaseModel
from typing import Optional

class UserUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None