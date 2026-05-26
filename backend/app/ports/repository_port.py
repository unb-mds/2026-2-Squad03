from abc import ABC, abstractmethod
from backend.app.domain.entities import RegiaoMonitorada

class IRegiaoRepository(ABC):
    @abstractmethod
    def salvar(self, regiao: RegiaoMonitorada) -> RegiaoMonitorada:
        pass

    @abstractmethod
    def listar_todas(self) -> list[RegiaoMonitorada]:
        pass