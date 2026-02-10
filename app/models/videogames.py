from sqlalchemy import Column, Date, Float, Integer, String
from database.database import Base
from sqlalchemy.orm import relationship
from models.assosiations import videogame_platforms

class Videogame(Base):
    __tablename__ = "Videogame"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    release_date = Column(Date, nullable=False)

    platforms = relationship(
        "Platform",
        secondary=videogame_platforms, 
        back_populates="videogames"
    )


