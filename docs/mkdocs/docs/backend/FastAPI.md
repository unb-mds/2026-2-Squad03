# Instalação do FastAPI (bash)


# Criação do ambiente virtual

## Criar um diretório para o código

### bash
```bash
mkdir projeto
# cria um diretório para o projeto
cd projeto
# acessa o diretório criado
```
## Criar o ambiente virtual usando o módulo venv do Python

### bash
```bash
python -m venv .venv
# cria o ambiente virtual no diretório oculto .venv
```
## Ativar o ambiente virtual

### bash
```bash
source .venv/bin/activate
```

# Instalação do pacote FastAPI

## No ambiente virtual ativo:

### bash
```bash
pip install "fastapi[standard]"
```

# Estrutura exemplar em FastAPI

## Criar um arquivo main.py

### python
```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```

## Execute o servidor

### bash
```bash
fastapi dev
```

## Conferir 

* Abra o navegador em http://127.0.0.1:8000/
* A resposta em JSON deverá ser ```{"message": "Hello World"}```

## Implementar endpoints básicos (CRUD)

### routers/locais.py

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.local import LocalCreate
from app.services import locais_service

router = APIRouter(prefix="/locais", tags=["Locais"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def criar(local: LocalCreate, db: Session = Depends(get_db)):
    return locais_service.criar_local(
        db,
        local.nome,
        local.latitude,
        local.longitude
    )

@router.get("/")
def listar(db: Session = Depends(get_db)):
    return locais_service.listar_locais(db)

@router.get("/{id}")
def buscar(id: int, db: Session = Depends(get_db)):
    local = locais_service.buscar_local(db, id)
    if not local:
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return local

@router.put("/{id}")
def atualizar(id: int, local: LocalCreate, db: Session = Depends(get_db)):
    atualizado = locais_service.atualizar_local(
        db,
        id,
        local.nome,
        local.latitude,
        local.longitude
    )
    if not atualizado:
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return atualizado

@router.delete("/{id}")
def deletar(id: int, db: Session = Depends(get_db)):
    removido = locais_service.deletar_local(db, id)
    if not removido:
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return {"message": "Local removido com sucesso"}
```


### services/locais_service.py
```python
from sqlalchemy.orm import Session
from app.models.local import Local
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

def criar_local(db: Session, nome: str, lat: float, lon: float):
    ponto = from_shape(Point(lon, lat), srid=4326)
    local = Local(nome=nome, geom=ponto)
    db.add(local)
    db.commit()
    db.refresh(local)
    return local

def listar_locais(db: Session):
    return db.query(Local).all()

def buscar_local(db: Session, id: int):
    return db.query(Local).filter(Local.id == id).first()

def atualizar_local(db: Session, id: int, nome: str, lat: float, lon: float):
    local = db.query(Local).filter(Local.id == id).first()
    if not local:
        return None

    local.nome = nome
    local.geom = from_shape(Point(lon, lat), srid=4326)

    db.commit()
    db.refresh(local)
    return local

def deletar_local(db: Session, id: int):
    local = db.query(Local).filter(Local.id == id).first()
    if not local:
        return None

    db.delete(local)
    db.commit()
    return True
```
## Integrar com banco de dados PostgreSQL

### Instalar dependências

```bash
pip install sqlalchemy psycopg2-binary geoalchemy2
````

### database.py

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:senha@localhost:5432/gis"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
```

### models/base.py

```python
from sqlalchemy.orm import declarative_base

Base = declarative_base()
```

### models/local.py

```python
from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from app.models.base import Base

class Local(Base):
    __tablename__ = "locais"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    geom = Column(Geometry("POINT", srid=4326))
```

### Criar tabelas no banco

```python
from app.database import engine
from app.models.base import Base
from app.models import local

Base.metadata.create_all(bind=engine)
```

### Usar sessão no FastAPI

```python
from app.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Testar conexão

```python
from app.database import engine

with engine.connect() as conn:
    print("Conectado com sucesso")
```

## Validar dados de entrada com Pydantic

### schemas/local.py

```python
from pydantic import BaseModel, Field

class LocalBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)

class LocalCreate(LocalBase):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class LocalUpdate(BaseModel):
    nome: str | None = Field(None, min_length=2, max_length=100)
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)

class LocalResponse(LocalBase):
    id: int

    class Config:
        orm_mode = True
````

### Uso nos endpoints

```python id="xq4x7s"
from app.schemas.local import LocalCreate, LocalUpdate

@router.post("/")
def criar(local: LocalCreate, db: Session = Depends(get_db)):
    return locais_service.criar_local(
        db,
        local.nome,
        local.latitude,
        local.longitude
    )

@router.put("/{id}")
def atualizar(id: int, local: LocalUpdate, db: Session = Depends(get_db)):
    return locais_service.atualizar_local(
        db,
        id,
        local.nome,
        local.latitude,
        local.longitude
    )
```

### Exemplo de requisição válida

```json id="uk1gqk"
{
  "nome": "Brasília",
  "latitude": -15.7942,
  "longitude": -47.8825
}
```

## Testar endpoints via Swagger UI

### Executar a aplicação

```bash
uvicorn app.main:app --reload
````

### Acessar Swagger UI

Abra no navegador:

```
http://localhost:8000/docs
```

### Acessar documentação alternativa

```
http://localhost:8000/redoc
```

### Testar endpoints

Na interface do Swagger:

* Clique em um endpoint (ex: POST /locais)
* Clique em "Try it out"
* Preencha o corpo da requisição
* Clique em "Execute"

### Exemplo de teste (POST /locais)

```json
{
  "nome": "Brasília",
  "latitude": -15.7942,
  "longitude": -47.8825
}
```

### Ver resposta

* Código HTTP (200, 201, 404, etc.)
* Corpo da resposta
* Tempo de execução

### Testar outros endpoints

* GET /locais → lista todos
* GET /locais/{id} → busca por id
* PUT /locais/{id} → atualiza
* DELETE /locais/{id} → remove

## Documentar uso da API

## Base URL

```text
http://localhost:8000
````

## Endpoints

### Criar local

```http
POST /locais
```

Corpo da requisição:

```json
{
  "nome": "Brasília",
  "latitude": -15.7942,
  "longitude": -47.8825
}
```

Resposta:

```json
{
  "id": 1,
  "nome": "Brasília"
}
```

### Listar locais

```http
GET /locais
```

Resposta:

```json
[
  {
    "id": 1,
    "nome": "Brasília"
  }
]
```

### Buscar local por ID

```http
GET /locais/{id}
```

Exemplo:

```http
GET /locais/1
```

Resposta:

```json
{
  "id": 1,
  "nome": "Brasília"
}
```

### Atualizar local

```http
PUT /locais/{id}
```

Exemplo:

```http
PUT /locais/1
```

Corpo da requisição:

```json
{
  "nome": "Brasília Atualizada",
  "latitude": -15.80,
  "longitude": -47.90
}
```

Resposta:

```json
{
  "id": 1,
  "nome": "Brasília Atualizada"
}
```

### Remover local

```http
DELETE /locais/{id}
```

Exemplo:

```http
DELETE /locais/1
```

Resposta:

```json
{
  "message": "Local removido com sucesso"
}
```

## Códigos de resposta

* 200 OK: requisição bem-sucedida
* 201 Created: recurso criado
* 404 Not Found: recurso não encontrado
* 422 Unprocessable Entity: erro de validação

