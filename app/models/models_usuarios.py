from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from database.session import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)

    products = relationship("Products", back_populates="owner")
    transacoes = relationship("Transacoes", back_populates="user")
