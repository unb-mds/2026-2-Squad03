# # backend/app/adapters/api_adapter/locais_routes.py
# from fastapi import APIRouter, HTTPException, Depends
# from pydantic import BaseModel

# from backend.app.adapters.json_adapter import JsonRepositoryAdapter
# from backend.app.domain.entities import RegiaoMonitorada


# # Ela cria o 'router' que o main.py está tentando importar.
# router = APIRouter(prefix="/api/locais", tags=["Locais"])

# class RegiaoSchema(BaseModel):
#     nome: str
#     latitude: float
#     longitude: float

# def get_repo():
#     return JsonRepositoryAdapter()

# @router.post("/")
# def cadastrar(payload: RegiaoSchema, repo: JsonRepositoryAdapter = Depends(get_repo)):
#     nova_regiao = RegiaoMonitorada(
#         id=None, 
#         nome=payload.nome, 
#         latitude=payload.latitude, 
#         longitude=payload.longitude
#     )
    
#     if not nova_regiao.coordenadas_validas():
#         raise HTTPException(status_code=400, detail="Coordenadas inválidas")
        
#     return repo.salvar(nova_regiao)

# @router.get("/")
# def listar(repo: JsonRepositoryAdapter = Depends(get_repo)):
#     return repo.listar_todas()