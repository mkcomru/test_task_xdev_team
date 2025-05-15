from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models import Mushroom, MushroomCreate, MushroomModel
from database import get_db

router = APIRouter()

@router.post("/", response_model=Mushroom)
def create_mushroom(mushroom: MushroomCreate, db: Session = Depends(get_db)):
    db_mushroom = MushroomModel(**mushroom.model_dump())
    db.add(db_mushroom)
    db.commit()
    db.refresh(db_mushroom)
    return db_mushroom

@router.get("/{mushroom_id}", response_model=Mushroom)
def get_mushroom(mushroom_id: int, db: Session = Depends(get_db)):
    db_mushroom = db.query(MushroomModel).filter(MushroomModel.id == mushroom_id).first()
    if db_mushroom is None:
        raise HTTPException(status_code=404, detail="Гриб не найден")
    return db_mushroom

@router.put("/{mushroom_id}", response_model=Mushroom)
def update_mushroom(mushroom_id: int, mushroom: MushroomCreate, db: Session = Depends(get_db)):
    db_mushroom = db.query(MushroomModel).filter(MushroomModel.id == mushroom_id).first()
    if db_mushroom is None:
        raise HTTPException(status_code=404, detail="Гриб не найден")
    
    for key, value in mushroom.model_dump().items():
        setattr(db_mushroom, key, value)
    
    db.commit()
    db.refresh(db_mushroom)
    return db_mushroom
