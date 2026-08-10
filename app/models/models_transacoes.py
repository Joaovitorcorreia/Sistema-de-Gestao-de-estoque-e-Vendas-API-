from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database.session import Base
from datetime import datetime

class Transacoes(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comprador_id = Column(Integer, ForeignKey("users.id"))
    valor = Column(Float, nullable=False)
    
    metodo_pagamento = Column(String, nullable=False)
    status_pagamento = Column(String, nullable=False)

    data_transacao = Column(DateTime, nullable=False, default=datetime.utcnow)

    user = relationship("Users", back_populates="transacoes")


class Historico(Base):
    __tablename__ = "historico"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    antigo_dono_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    novo_dono_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    data_transacao = Column(DateTime, nullable=False, default=datetime.utcnow)

    user = relationship("Users", back_populates="historico")