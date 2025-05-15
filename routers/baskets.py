from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models import Basket, BasketCreate, AddMushroomToBasket, BasketModel, MushroomModel
from database import get_db

router = APIRouter()

@router.post("/", response_model=Basket)
def create_basket(basket: BasketCreate, db: Session = Depends(get_db)):
    db_basket = BasketModel(**basket.model_dump())
    db.add(db_basket)
    db.commit()
    db.refresh(db_basket)
    return db_basket

@router.get("/{basket_id}", response_model=Basket)
def get_basket(basket_id: int, db: Session = Depends(get_db)):
    db_basket = db.query(BasketModel).filter(BasketModel.id == basket_id).first()
    if db_basket is None:
        raise HTTPException(status_code=404, detail="Корзинка не найдена")
    
    return db_basket

@router.post("/{basket_id}/add_mushroom", response_model=Basket)
def add_mushroom_to_basket(basket_id: int, item: AddMushroomToBasket, db: Session = Depends(get_db)):
    db_basket = db.query(BasketModel).filter(BasketModel.id == basket_id).first()
    if db_basket is None:
        raise HTTPException(status_code=404, detail="Корзинка не найдена")
    
    db_mushroom = db.query(MushroomModel).filter(MushroomModel.id == item.mushroom_id).first()
    if db_mushroom is None:
        raise HTTPException(status_code=404, detail="Гриб не найден")
    
    if db_mushroom.basket_id is not None:
        raise HTTPException(status_code=400, detail="Гриб уже в корзинке")
    
    current_weight = sum(mushroom.weight for mushroom in db_basket.mushrooms)
    if current_weight + db_mushroom.weight > db_basket.capacity:
        raise HTTPException(status_code=400, detail="Корзинка переполнена")
    
    db_mushroom.basket_id = basket_id
    db.commit()
    db.refresh(db_basket)
    
    return db_basket

@router.delete("/{basket_id}/remove_mushroom/{mushroom_id}", response_model=Basket)
def remove_mushroom_from_basket(basket_id: int, mushroom_id: int, db: Session = Depends(get_db)):
    db_basket = db.query(BasketModel).filter(BasketModel.id == basket_id).first()
    if db_basket is None:
        raise HTTPException(status_code=404, detail="Корзинка не найдена")
    
    db_mushroom = db.query(MushroomModel).filter(
        MushroomModel.id == mushroom_id,
        MushroomModel.basket_id == basket_id
    ).first()
    
    if not db_mushroom:
        raise HTTPException(status_code=404, detail="Гриб не найден в корзинке")
    
    db_mushroom.basket_id = None
    db.commit()
    db.refresh(db_basket)
    
    return db_basket
