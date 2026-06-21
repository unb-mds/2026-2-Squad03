from datetime import datetime
from typing import Optional, List

class UserAuth:  # <-- Mude o nome aqui para bater com o import do seu auth_routes
    def __init__(self, id: Optional[int], nome: str, email: str, senha_hash: str):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash

    def validar_email(self) -> bool:
        return "@" in self.email and "." in self.email
    
    
class Noticia:
    def __init__(
        self, 
        id: Optional[int], 
        titulo: str, 
        conteudo: str, 
        fonte_url: str,
        data_publicacao: Optional[datetime],
        latitude: Optional[float],
        longitude: Optional[float],
        data_coleta: Optional[datetime] = None
    ):
        self.id = id
        self.titulo = titulo
        self.conteudo = conteudo
        self.fonte_url = fonte_url
        self.data_publicacao = data_publicacao
        self.latitude = latitude
        self.longitude = longitude
        self.data_coleta = data_coleta or datetime.utcnow()

    def possui_geolocalizacao(self) -> bool:
        """Verifica se a notícia coletada possui coordenadas válidas para plotagem no mapa."""
        return self.latitude is not None and self.longitude is not None


class RegiaoMonitorada:
    def __init__(
        self, 
        id: Optional[int], 
        nome: str, 
        coordenadas_poligono: List[tuple], 
        usuario_id: int
    ):
        self.id = id
        self.nome = nome
        self.coordenadas_poligono = coordenadas_poligono  # Lista de tuplas [(lat, lng), ...]
        self.usuario_id = usuario_id

    def validar_poligono(self) -> bool:
        """Garante que o polígono faz sentido mínimo (precisa de pelo menos 3 pontos)."""
        return len(self.coordenadas_poligono) >= 3