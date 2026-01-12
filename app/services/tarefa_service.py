from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.model_tarefa import Tarefa
from app.schemas.schemas.tarefa_schemas import TarefaSchemas
from app.schemas.put.tarefa_put import TarefaPut
from app.schemas.update.tarefa_update import TarefaUpdate
from http import HTTPStatus

def service_criar_tarefa(tarefa_data : TarefaSchemas, session: Session, current_user):
    tarefa = Tarefa(
        nome = tarefa_data.nome,
        descricao = tarefa_data.descricao,
        prazo = tarefa_data.prazo,
        prioridade = tarefa_data.prioridade,
        concluida = tarefa_data.concluida,
        usuario_id = current_user.id
    )

    try:
        session.add(tarefa)
        session.commit()
        session.refresh(tarefa)
        return tarefa
    except:
        session.rollback()
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Internal server error")

def service_listar_tarefas(session: Session, current_user):
    tarefas = session.query(Tarefa).filter(Tarefa.usuario_id == current_user.id).order_by(Tarefa.data.desc()).all()
    
    return tarefas

def service_pegar_tarefa(tarefa_id: int, session: Session):
    tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Task not found")
    
    return tarefa

def service_atualizar_tarefa(tarefa_id: int, data: TarefaPut, session: Session):
    tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Task not found")
    
    try:
        tarefa.nome = data.nome
        tarefa.descricao = data.descricao
        tarefa.prazo = data.prazo
        tarefa.prioridade = data.prioridade
        tarefa.concluida = data.concluida

        session.commit()
        session.refresh(tarefa)
        return tarefa
    except:
        session.rollback()
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Internal server error")

def service_atualizar_tarefa_parcialmente(tarefa_id: int, data: TarefaUpdate, session: Session):
    tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Task not found")
    
    try:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(tarefa, field, value)

        session.commit()
        session.refresh(tarefa)
        return tarefa
    except:
        session.rollback()
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Internal server error")

def service_deletar_tarefa(tarefa_id: int, session: Session):
    tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Task not found")

    try:
        session.delete(tarefa)
        session.commit()
        return {
            'status' : 'OK'
        }
    except:
        session.rollback()
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Internal server error")
    