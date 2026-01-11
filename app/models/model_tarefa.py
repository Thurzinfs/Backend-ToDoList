from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Tarefa(Base):
    __tablename__ = "tarefas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    concluida = Column(Boolean, default=False, nullable=False)

    data = Column(DateTime, default=datetime.utcnow, nullable=False)
    prazo = Column(Date, nullable=False)
    prioridade = Column(String, nullable=False)
    data_conclusao = Column(DateTime, nullable=True)
    usuario_id = Column(Integer, ForeignKey('users.id'))

    usuario = relationship('User', back_populates='tarefas')