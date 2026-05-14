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