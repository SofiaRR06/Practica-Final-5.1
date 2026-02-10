from sqlalchemy import Table, ForeignKey, Column, Integer
from database.database import Base

videogame_platforms = Table(
    "videogame_platforms",
    Base.metadata,
    Column("videogame_id", Integer, ForeignKey("Videogame.id"), primary_key=True),
    Column("platform_id", Integer, ForeignKey("platforms.id"), primary_key=True)
)
