from sqlalchemy import Column, Integer, Boolean, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from database import Base
from typing import Optional, List


class MushroomModel(Base):
    __tablename__ = "mushrooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    edible = Column(Boolean)
    weight = Column(Integer)
    freshness = Column(String)
    basket_id = Column(Integer, ForeignKey("baskets.id"), nullable=True)

    basket = relationship("BasketModel", back_populates="mushrooms")


class BasketModel(Base):
    __tablename__ = "baskets"

    id = Column(Integer, primary_key=True, index=True)
    owner_name = Column(String)
    capacity = Column(Integer)

    mushrooms = relationship("MushroomModel", back_populates="basket")


class MushroomBase(BaseModel):
    name: str
    edible: bool
    weight: int = Field(gt=0, description="weight in grams")
    freshness: str


class MushroomCreate(MushroomBase):
    pass

class Mushroom(MushroomBase):
    id: int
    basket_id: Optional[int] = None
    
    class Config:
        from_attributes = True

class BasketBase(BaseModel):
    owner_name: str
    capacity: int = Field(gt=0, description="Вместимость в граммах")

class BasketCreate(BasketBase):
    pass

class Basket(BasketBase):
    id: int
    mushrooms: list[Mushroom] = []
    
    class Config:
        from_attributes = True

class AddMushroomToBasket(BaseModel):
    mushroom_id: int






