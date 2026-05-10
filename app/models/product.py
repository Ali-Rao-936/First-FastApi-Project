from sqlalchemy import Column, ForeignKey, Integer, Numeric, String

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id      = Column(Integer, primary_key=True, index=True)
    name    = Column(String(256), nullable=False, index=True)
    price   = Column(Numeric(10, 2), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
