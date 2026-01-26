from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.database import SessionLocal
from models.videogames import Videogame
from models.platforms import Platform

from schemas.videogames import CreateVideogame,VideogameResponse

router = APIRouter(
    prefix="/videogames",
    tags=["videogames"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Buscar todos los videojuegos
@router.get("/", response_model=List[VideogameResponse])
def get_videogames(db: Session = Depends(get_db)):
    videogames = db.query(Videogame).all()
    videogameList = []
    for vg in videogames:
        videogameList.append(
            VideogameResponse(
                id=vg.id,
                name=vg.name,
                genre=vg.genre,
                price=vg.price,
                release_date=vg.release_date,
                platform=[p.name for p in vg.platforms]  
            )
        )
    return videogameList

#Buscar videojuegos por ID
@router.get("/{videogame_id}", response_model=VideogameResponse)
def get_videogame(videogame_id: int, db: Session = Depends(get_db)):
    videogame = db. query(Videogame).filter(Videogame.id == videogame_id).first()
    if not videogame:
        raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail="No existe ningún videojuego con ese ID"
    )
    return VideogameResponse(
        id=videogame.id,
        name=videogame.name,
        genre=videogame.genre,
        price=videogame.price,
        release_date=videogame.release_date,
        platform=[p.name for p in videogame.platforms]  
    )
        
#Crear videojuego
@router.post("/", response_model=VideogameResponse, status_code=status.HTTP_201_CREATED)
def create_videogame(videogame: CreateVideogame, db: Session = Depends(get_db)):
    # Revisar si ya existe
    existing_videogame = db.query(Videogame).filter(Videogame.name.ilike(videogame.name)).first()
    if existing_videogame:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El videojuego ya está creado"
        )

    # Validación precio
    if videogame.price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El precio del videojuego debe ser mayor que 0"
        )

    # Obtener plataformas
    platforms_db = db.query(Platform).filter(Platform.name.in_(videogame.platform)).all()
    if len(platforms_db) != len(videogame.platform):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Alguna de las plataformas no existe"
        )
    
    if not platforms_db:
        raise HTTPException(
            status_code=400,
            detail=f"No se encontraron plataformas: {videogame.platform}"
        )


    # Crear videojuego
    new_videogame = Videogame(
        name=videogame.name,
        genre=videogame.genre,
        price=videogame.price,
        release_date=videogame.release_date
    )
    new_videogame.platforms = platforms_db

    db.add(new_videogame)
    db.commit()
    db.refresh(new_videogame)

    return VideogameResponse(
    id=new_videogame.id,
    name=new_videogame.name,
    genre=new_videogame.genre,
    price=new_videogame.price,
    release_date=new_videogame.release_date,
    platform=[p.name for p in new_videogame.platforms]
)

#Actualizar videojuego
@router.put("/{videogame_id}", response_model=VideogameResponse)
def update_videogame(videogame_id: int, videogame: CreateVideogame, db: Session = Depends(get_db)):
    stored_videogame = db.query(Videogame).filter(Videogame.id == videogame_id).first()
    if not stored_videogame:
        raise HTTPException(status_code=404, detail="No existe el videojuego")
    
    # Validación precio
    if videogame.price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El precio del videojuego debe ser mayor que 0"
        )
    
    # Actualizar campos
    stored_videogame.name = videogame.name
    stored_videogame.genre = videogame.genre
    stored_videogame.price = videogame.price
    stored_videogame.release_date = videogame.release_date

    # Actualizar plataformas
    platforms_db = db.query(Platform).filter(Platform.name.in_(videogame.platform)).all()
    stored_videogame.platforms = platforms_db

    db.commit()
    db.refresh(stored_videogame)

    # Platforms se convierte a lista de nombres para que no salte un error
    return VideogameResponse(
        id=stored_videogame.id,
        name=stored_videogame.name,
        genre=stored_videogame.genre,
        price=stored_videogame.price,
        release_date=stored_videogame.release_date,
        platform=[p.name for p in stored_videogame.platforms]
    )

#Borrar videojuego
@router.delete("/{videogame_id}")
def delete_videogame(videogame_id: int, db: Session = Depends(get_db)):
    videogame = db.query(Videogame).filter(Videogame.id == videogame_id).first()

    #Validación videojuego en la base de datos
    if not videogame:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El videojuego no existe en la base de datos"
        )

    db.delete(videogame)
    db.commit()

    return {"detail": "Videojuego eliminado"}