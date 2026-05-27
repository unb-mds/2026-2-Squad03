from pydantic import BaseModel


class RegiaoMonitorada:
    def __init__(self, id: int | None, nome: str, latitude: float, longitude: float):
        self.id = id
        self.nome = nome
        self.latitude = latitude
        self.longitude = longitude

    def coordenadas_validas(self) -> bool:
        if not (-34.0 <= self.latitude <= 6.0) or not (-74.0 <= self.longitude <= -34.0):
            return False
        return True
    
class UserAuth(BaseModel):
    nome: str = None
    email: str
    senha: str