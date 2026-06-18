from pydantic import BaseModel

class NewsClassification(BaseModel):
    feminicidio: str
    title: str
    resumo: str
    local: str