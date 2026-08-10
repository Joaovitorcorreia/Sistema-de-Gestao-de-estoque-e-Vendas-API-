from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class RealizarTransacaoSchema(BaseModel):
    product_id: str = Field(..., example="ID do produto")
    comprador_id: int = Field(..., example=2)

    vendedor_email: EmailStr = Field(..., example="vendedor@example.com")
    vendedor_senha: str = Field(..., min_length=6, example="senha_do_vendedor")

    valor: float = Field(..., example=99.99)
    metodo_pagamento: str = Field(..., example="Cartão de Crédito")
    
# observação: quando usar o JWT, o email e a senha do vendedor não serão necessários, pois o JWT já vai validar o usuário logado.

class RespostaTransacaoSchema(BaseModel):
    product_id: str
    comprador_id: int
    valor: float
    metodo_pagamento: str
    status_pagamento: str
    data_transacao: datetime
    message: str = Field(..., example="Transação realizada com sucesso.")

    class Config:
        from_attributes = True