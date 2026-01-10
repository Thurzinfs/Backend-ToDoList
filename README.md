# ToDoList — API Backend

API em Python (FastAPI) para gerenciamento de tarefas (ToDo) com autenticação JWT (access + refresh tokens) e CRUD de usuários e tarefas.

## Índice
- Visão geral
- Tecnologias
- Pré-requisitos
- Variáveis de ambiente
- Instalação (local)
- Uso com Docker
- Estrutura do projeto
- Endpoints principais
- Observações de produção
- Contribuição
- Licença
- Contato

## Visão geral
Backend RESTful que expõe endpoints protegidos por JWT. Usa SQLAlchemy para persistência; as tabelas são criadas automaticamente pelo projeto ao iniciar (veja `app/db/database.py`).

## Tecnologias
- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL (recomendado em produção) / SQLite em desenvolvimento
- Poetry (gerenciamento de dependências) ou `requirements.txt`
- Uvicorn / Gunicorn (execução)

## Pré-requisitos
- Python 3.11 (para execução local)
- Docker e `docker-compose` (para execução via contêiner)
- Arquivo `.env` com as variáveis descritas abaixo

## Variáveis de ambiente
Exemplo de `.env` (não comitar em repositório público):

```
DATABASE_URL=postgresql://user:password@db:5432/todo_db
SECRET_KEY=uma_chave_forte_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=10080
```

Observações:
- Em execuções via `docker-compose` o host do banco deve ser `db` (nome do serviço no compose).
- Para SQLite use `sqlite:///./test.db` em desenvolvimento.

## Instalação (local)
1. Crie e ative um virtualenv:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
2. Instale dependências (escolha um):
```bash
# Com Poetry
poetry install

# Ou com pip (se houver requirements.txt)
pip install -r requirements.txt
```
3. Configure `.env`.
4. Rode em modo desenvolvimento:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Uso com Docker
O projeto contém um `Dockerfile` e um `docker-compose.yaml` para orquestração com Postgres.

Com docker-compose (rebuild):
```bash
docker-compose -f docker-compose.yaml up --build -d
```

Build e execução manual:
```bash
docker build -t todolist-backend .
docker run --env-file .env -p 8000:8000 todolist-backend
```

Notas importantes sobre Docker:
- No `docker-compose.yaml` garanta que o volume do Postgres esteja mapeado para `/var/lib/postgresql/data`.
- Use um arquivo `.dockerignore` para evitar copiar arquivos desnecessários (ex.: `.venv`, `.git`, `__pycache__`, `tests`, `.env`).
- Em produção prefira builds multi-stage, fixar versão do `poetry` (se usado), criar um usuário não-root e usar um servidor de aplicação como `gunicorn` com workers do `uvicorn`.

Exemplo mínimo de `.dockerignore` recomendado:
```
.venv
__pycache__
*.pyc
.git
.env
tests
```

## Estrutura do projeto (resumida)
- `app/main.py` — inicialização e inclusão de routers
- `app/core/` — configurações, segurança e handlers
- `app/db/` — configuração do SQLAlchemy (`database.py`)
- `app/models/` — modelos ORM (`User`, `Tarefa`)
- `app/crud/` — operações de CRUD
- `app/routers/` — routers (autenticação, tarefas, usuários)
- `app/services/` — lógica de negócio
- `app/schemas/` — Pydantic schemas

## Endpoints principais
- Health: `GET /` → `{"msg": "OK"}`
- Auth:
  - `POST /auth/token` — login (form: `username`, `password`)
  - `POST /auth/refresh/token` — renovar tokens com refresh token
  - `GET /auth/me` — dados do usuário autenticado
- Tarefas (protegido, prefixo `/api/tarefa`): CRUD padrão (`POST`, `GET`, `PUT`, `PATCH`, `DELETE`)

Consulte as rotas reais no código (`app/routers/`) e a documentação interativa em `/docs`.

## Observações para produção
- Não exponha `.env` no repositório; use secrets do provedor de nuvem.
- Fixe versões do Poetry e dependências para reprodutibilidade.
- Use multi-stage builds para reduzir imagem final e remover ferramentas de build.
- Execute com Gunicorn + Uvicorn workers ou configure workers do Uvicorn para escalabilidade.
- Crie usuário não-root na imagem Docker.
- Configure healthchecks, logs e monitore recursos no ambiente de hospedagem.

## Contribuição
1. Fork
2. Branch com feature/fix
3. PR descrevendo mudanças

## Licença
Adicione a licença desejada (ex.: MIT) no repositório.

## Contato
Abra uma issue para dúvidas ou suporte.
