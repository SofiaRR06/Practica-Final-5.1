from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.database import SessionLocal
from models.platforms import Platform
from schemas.platforms import CreatePlatform, PlatformResponse

router = APIRouter(
    prefix="/platforms",
    tags=["platforms"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Buscar todas las plataformas
@router.get("/", response_model=list[PlatformResponse])
def get_platforms(db: Session = Depends(get_db)):
    return db.query(Platform).all()

#Buscar plataformas por ID
@router.get("/{platform_id}", response_model=PlatformResponse)
def get_platform(platform_id: int, db: Session = Depends(get_db)):
    platform = db. query(Platform).filter(Platform.id == platform_id).first()
    if not platform:
        raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail="No existe ninguna plataforma con ese ID"
    ) 
    return platform
        
#Crear plataformas
@router.post("/", response_model=PlatformResponse, status_code=status.HTTP_201_CREATED)
def create_platform(platform: CreatePlatform, db: Session = Depends(get_db)):
    # Revisar si ya existe
    existing_platform = db.query(Platform).filter(Platform.name.ilike(platform.name)).first()
    if existing_platform:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La plataforma ya está creada"
        )

    # Validación precio
    if platform.price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El precio de la plataforma debe ser mayor que 0"
        )

    # Crear plataforma
    new_platform = Platform(
        name = platform.name,
        description = platform.description,
        price=platform.price,
        release_date = platform.release_date,
        factory = platform.factory,
        obtain_console = platform.obtain_console
    )

    db.add(new_platform)
    db.commit()
    db.refresh(new_platform)

    return new_platform

#Actualizar plataforma
@router.put("/{platform_id}", response_model = PlatformResponse)
def update_platform(platform_id : int, platform : CreatePlatform, db: Session = Depends(get_db)):
    stored_platform = db.query(Platform).filter(Platform.id == platform_id).first()

    #Validación videojuego en la base de datos
    if not stored_platform:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La plataforma no existe en la base de datos"
        )
    
    # Validación precio
    if platform.price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El precio de la plataforma debe ser mayor que 0"
        )

    # Actualizar campos
    stored_platform.name = platform.name
    stored_platform.description = platform.description
    stored_platform.price = platform.price
    stored_platform.release_date = platform.release_date
    stored_platform.factory = platform.factory
    stored_platform.obtain_console = platform.obtain_console

    db.commit()
    db.refresh(stored_platform)

    return stored_platform

#Borrar plataforma
@router.delete("/{platform_id}", status_code=204)
def delete_platform(platform_id: int, db: Session = Depends(get_db)):
    platform = db.query(Platform).filter(Platform.id == platform_id).first()

    #Validación videojuego en la base de datos
    if not platform:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La plataforma no existe en la base de datos"
        )

    db.delete(platform)
    db.commit()

    return {"detail": "Plataforma eliminada"}