from pydantic import BaseModel

class UserPut(BaseModel):
    nome: str
    email: str 
    password: str