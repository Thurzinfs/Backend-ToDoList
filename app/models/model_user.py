from sqlalchemy import Integer, String, Column, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, index=True, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    criado = Column(DateTime, default=lambda: datetime.now().replace(microsecond=0))

    tarefas = relationship("Tarefa", back_populates="usuario", cascade="all, delete-orphan")
