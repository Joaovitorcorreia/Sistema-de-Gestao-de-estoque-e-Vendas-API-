from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class RealizarTransacaoSchema(BaseModel):
    product_id: str = Field(..., example="ID do produto")

    vendedor_email: EmailStr = Field(..., example="vendedor@example.com")

    valor: float = Field(..., example=99.99)
    metodo_pagamento: str = Field(..., example="Cartão de Crédito")
    

class RespostaTransacaoSchema(BaseModel):
    product_id: str
    valor: float
    metodo_pagamento: str
    status_pagamento: str
    data_transacao: datetime
    message: str = Field(..., example="Transacao realizada com sucesso.")
    
    class Config:
        from_attributes = True