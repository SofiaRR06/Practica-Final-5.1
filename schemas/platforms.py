from datetime import date
from pydantic import BaseModel

class PlatformBase (BaseModel):
    name: str
    description: str
    price: float
    release_date: date
    factory: str
    obtain_console: bool

class PlatformResponse(PlatformBase):
    id: int

    class Config:
        orm_mode = True


class CreatePlatform(PlatformBase):
    pass