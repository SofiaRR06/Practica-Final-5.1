from sqlalchemy import Boolean, Column, Date, Float, Integer, String
from sqlalchemy.orm import relationship
from database.database import Base
from models.assosiations import videogame_platforms

class Platform(Base):
    __tablename__ = "platforms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    release_date = Column(Date, nullable=False)
    factory = Column(String, nullable=False)
    obtain_console = Column(Boolean, nullable=False)

    
    videogames = relationship(
        "Videogame",
        secondary=videogame_platforms,
        back_populates="platforms"
    )
