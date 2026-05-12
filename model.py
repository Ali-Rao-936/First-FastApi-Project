from pydantic import BaseModel
from sqlalchemy import Column, Integer, Numeric, String

from app.database import Base


class ProductCreate(BaseModel):
    name: str
    price: float
    description: str
    quantity: int


class ProductRead(ProductCreate):
    id: int

    class Config:
        from_attributes = True


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    description = Column(String(1024), nullable=True)
    quantity = Column(Integer, nullable=False)