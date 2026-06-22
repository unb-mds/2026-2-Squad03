# from datetime import datetime
# from typing import Optional, List

# from shapely import geometry

# class UserAuth:  # <-- Mude o nome aqui para bater com o import do seu auth_routes
#     def __init__(self, id: Optional[int], nome: str, email: str, senha_hash: str):
#         self.id = id
#         self.nome = nome
#         self.email = email
#         self.senha_hash = senha_hash

#     def validar_email(self) -> bool:
#         return "@" in self.email and "." in self.email
    
    
# class Noticia:
#     def __init__(
#         self, 
#         id: Optional[int], 
#         titulo: str, 
#         conteudo: str, 
#         fonte_url: str,
#         data_publicacao: Optional[datetime],
#         data_coleta: Optional[datetime] = None
#     ):
#         self.id = id
#         self.titulo = titulo
#         self.conteudo = conteudo
#         self.fonte_url = fonte_url
#         self.data_publicacao = data_publicacao
#         self.data_coleta = data_coleta or datetime.utcnow()



# class RegiaoMonitorada:
#     def __init__(
#         self, 
#         id: Optional[int], 
#         nome: str, 
#         geom: geometry, 

#     ):
#         self.id = id
#         self.nome = nome
#         self.geom = geom

