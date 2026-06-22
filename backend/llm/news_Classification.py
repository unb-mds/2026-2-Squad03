from pydantic import BaseModel

class NewsClassification(BaseModel):
    feminicidio: bool
    Portal: str
    resumo_raw: str
    resumo_blur: str
    local: str
    fonte_url: str