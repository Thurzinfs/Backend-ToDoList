from fastapi import APIRouter, Depends
from http import HTTPStatus
from app.db.database import get_session
from app.schemas.public.tarefa_public import TarefaPublic
from app.schemas.schemas.tarefa_schemas import TarefaSchemas
from app.schemas.update.tarefa_update import TarefaUpdate
from app.schemas.put.tarefa_put import TarefaPut
from sqlalchemy.orm import Session
from app.services.tarefa_service import service_criar_tarefa, service_listar_tarefas, service_pegar_tarefa, service_atualizar_tarefa, service_atualizar_tarefa_parcialmente, service_deletar_tarefa
from typing import List
from app.core.security import get_current_user

router = APIRouter(prefix='/api/tarefa', tags=['api', 'tarefa'])

@router.post(
    path='/',
    response_model=TarefaPublic,
    status_code=HTTPStatus.CREATED
)
def criar_tarefa(
    data : TarefaSchemas,
    session: Session = Depends(get_session), 
    current_user = Depends(get_current_user)
):
    return service_criar_tarefa(
        tarefa_data = data,
        session = session,
        current_user=current_user
    )

@router.get(
    path='/listar',
    response_model=List[TarefaPublic],
    status_code=HTTPStatus.OK
)
def listar_tarefas(
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    return service_listar_tarefas(
        session=session,
        current_user = current_user
    )

@router.get(
    path='/{tarefa_id}',
    response_model=TarefaPublic,
    status_code=HTTPStatus.OK
)
def pegar_tarefa(
    tarefa_id: int,
    session: Session = Depends(get_session)
):
    return service_pegar_tarefa(
        tarefa_id=tarefa_id,
        session=session
    )

@router.put(
    path='/{tarefa_id}',
    response_model=TarefaPublic,
)
def atualizar_tarefa(
    tarefa_id: int,
    data: TarefaPut,
    session: Session = Depends(get_session)
):
    return service_atualizar_tarefa(
        tarefa_id=tarefa_id,
        data=data,
        session=session
    )

@router.patch(
    path='/{tarefa_id}',
    response_model=TarefaPublic
)
def atualizar_tarefa_parcialmente(
    tarefa_id: int,
    data: TarefaUpdate,
    session: Session = Depends(get_session)
):
    return service_atualizar_tarefa_parcialmente(
        tarefa_id=tarefa_id,
        data=data,
        session=session
    )

@router.delete(
    path='/{tarefa_id}',
)
def deletar_tarefa(
    tarefa_id: int,
    session: Session = Depends(get_session)
):
    return service_deletar_tarefa(
        tarefa_id=tarefa_id,
        session=session
    )