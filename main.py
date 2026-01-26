from fastapi import FastAPI

from database.database import Base, engine
from routes import platforms, videogames

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(videogames.router)
app.include_router(platforms.router)

@app.get("/")
def root():
    return {"message": "API de videojuegos con FastAPI y SQLite"}