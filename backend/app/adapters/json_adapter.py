# backend/app/adapters/json_adapter.py
import json
import os
from backend.app.ports.repository_port import IRegiaoRepository
from backend.app.domain.entities import RegiaoMonitorada

ARQUIVO_JSON = "banco_prototipo.json"

class JsonRepositoryAdapter(IRegiaoRepository):
    def __init__(self):
        if not os.path.exists(ARQUIVO_JSON):
            with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _ler_banco(self):
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
            return json.load(f)

    def _escrever_banco(self, dados):
        with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def salvar(self, regiao: RegiaoMonitorada) -> RegiaoMonitorada:
        dados = self._ler_banco()
        novo_id = len(dados) + 1
        regiao.id = novo_id
        dados.append({"id": regiao.id, "nome": regiao.nome, "latitude": regiao.latitude, "longitude": regiao.longitude})
        self._escrever_banco(dados)
        return regiao

    def listar_todas(self) -> list[RegiaoMonitorada]:
        dados = self._ler_banco()
        return [RegiaoMonitorada(id=i["id"], nome=i["nome"], latitude=i["latitude"], longitude=i["longitude"]) for i in dados]