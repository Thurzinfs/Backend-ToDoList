# ToDoList — API Backend

API backend em Python (FastAPI) para gerenciamento de tarefas (ToDo). Projeto com foco em autenticação JWT (access + refresh tokens), CRUD de usuários e gerenciamento de tarefas por usuário.

## Índice
- Visão geral
- Tecnologias
- Estrutura do projeto
- Variáveis de ambiente
- Instalação
- Execução
- Endpoints principais
- Modelos (resumo)
- Contribuição
- Contato

## Visão geral

Este repositório contém a API de backend do ToDoList. A aplicação expõe endpoints protegidos por JWT para operação sobre usuários e tarefas. O banco de dados é gerenciado com SQLAlchemy e as tabelas são criadas automaticamente via `Base.metadata.create_all(bind=engine)`.

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- SQLite/Postgres (via `DATABASE_URL`)
- JWT (PyJWT)

Dependências principais estão em `requeriments.txt`.

## Estrutura do projeto (resumida)

- `app/main.py` — inicialização da aplicação e inclusão de routers
- `app/core/` — configurações, segurança e handlers
- `app/db/` — configuração do SQLAlchemy (`database.py`)
- `app/models/` — modelos ORM (`User`, `Tarefa`)
- `app/crud/` — routers para CRUD de usuários
- `app/routers/` — routers adicionais (autenticação, listagem, tarefas)
- `app/services/` — lógica de negócio para usuários e tarefas
- `app/schemas/` — Pydantic schemas para requests/responses

## Variáveis de ambiente

Crie um arquivo `.env` com as variáveis abaixo (exemplo):

```
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=uma_chave_forte_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=7
```

> Observação: ajuste `DATABASE_URL` para Postgres ou outro banco conforme necessário.

## Instalação

1. Crie e ative um ambiente virtual (recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instale dependências:

```bash
pip install -r requeriments.txt
```

3. Configure o arquivo `.env` com as variáveis acima.

## Execução

Execute a API com Uvicorn (modo desenvolvimento):

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A documentação interativa estará disponível em `/docs` (Swagger) e `/redoc`.

## Endpoints principais

- Health check: `GET /` — retorna `{"msg": "OK"}`
- Autenticação:
  - `POST /auth/token` — login com `username` (email) e `password` (OAuth2PasswordRequestForm). Retorna `access_token` e `refresh_token`.
  - `POST /auth/refresh/token` — receber novo par de tokens usando `refresh_token` (schema `RefreshTokenIn`).
  - `GET /auth/me` — retorna dados do usuário atual (token de acesso necessário).
- Tarefas (protegido): prefixo ` /api/tarefa`
  - `POST /api/tarefa/` — criar tarefa
  - `GET /api/tarefa/listar` — listar tarefas do usuário autenticado
  - `GET /api/tarefa/{tarefa_id}` — obter tarefa por id
  - `PUT /api/tarefa/{tarefa_id}` — atualizar tarefa completa
  - `PATCH /api/tarefa/{tarefa_id}` — atualização parcial
  - `DELETE /api/tarefa/{tarefa_id}` — deletar tarefa

- Usuários: routers de CRUD incluídos (ver `app.crud`)

Exemplo de autenticação (curl):

```bash
curl -X POST "http://localhost:8000/auth/token" -F "username=seu@email.com" -F "password=sua_senha"
```

## Modelos (resumo)

- `User` (`app/models/model_user.py`): `id`, `nome`, `email`, `password`, `criado`.
- `Tarefa` (`app/models/model_tarefa.py`): `id`, `nome`, `descricao`, `concluida`, `data`, `prazo`, `data_conclusao`, `usuario_id`.

## Observações de segurança

- Senhas são armazenadas hasheadas (ver `app.core.security`).
- Tokens de refresh são armazenados em banco com hash e podem ser revogados.

## Contribuição

Fique à vontade para abrir issues e pull requests. Para contribuições:

1. Fork do repositório
2. Branch com feature/fix
3. Abra PR descrevendo mudanças

## Licença

Coloque aqui o tipo de licença (ex.: MIT) se desejar.

## Contato

Para dúvidas ou suporte, abra uma issue no repositório.
