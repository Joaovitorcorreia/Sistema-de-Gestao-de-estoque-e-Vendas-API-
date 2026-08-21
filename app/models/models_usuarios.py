from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database.session import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)

    products = relationship("Products", back_populates="owner", cascade="all, delete-orphan")
    transacoes = relationship("Transacoes", foreign_keys="[Transacoes.owner_id]", back_populates="user", cascade="all, delete-orphan")
    excluir_compras = relationship("Transacoes", foreign_keys="[Transacoes.comprador_id]", back_populates="excluir_compras", cascade="all, delete-orphan")
    historico = relationship("Historico", foreign_keys="[Historico.novo_dono_id]", back_populates="user", cascade="all, delete-orphan")

    
    