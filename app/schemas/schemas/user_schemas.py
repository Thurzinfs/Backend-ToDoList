from pydantic import BaseModel

class UserSchema(BaseModel):
    nome: str
    email: str 
    password: str