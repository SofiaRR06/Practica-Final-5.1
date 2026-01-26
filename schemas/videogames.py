from datetime import date
from typing import List
from pydantic import BaseModel

class VideogameBase(BaseModel):
    name: str
    genre: str
    price: float
    platform: List[str]
    release_date: date

class VideogameResponse(VideogameBase):
    id:int

    class Config:
        orm_mode = True

class CreateVideogame(VideogameBase):
    pass