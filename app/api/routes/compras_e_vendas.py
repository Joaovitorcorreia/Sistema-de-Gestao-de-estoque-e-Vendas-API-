from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.models_produtos import Products
from app.models.models_transacoes import Transacoes
from app.models.models_usuarios import Users
from app.schemas.schemas_transacoes import RealizarTransacaoSchema, RespostaTransacaoSchema
from app.core.auth_token import verificar_token

compras_e_vendas = APIRouter(tags=["Compras e Vendas"])

@compras_e_vendas.post("/realizar-transacao")
async def realizar_transacao(transacao: RealizarTransacaoSchema, token_payload: dict = Depends(verificar_token), db=Depends(get_db)):
    # Verificar se o produto existe
    produto = db.query(Products).filter(Products.id == transacao.product_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    # Verificar se o comprador existe
    comprador_id = str(token_payload.get("sub"))
    comprador = db.query(Users).filter(Users.email == comprador_id).first()
    if not comprador:
        raise HTTPException(status_code=404, detail="Comprador não encontrado.")


    # Criar a transação
    nova_transacao = Transacoes(
        product_id=transacao.product_id,
        owner_id=produto.owner_id,
        comprador_id=comprador.id,
        valor=transacao.valor,
        metodo_pagamento=transacao.metodo_pagamento,
        status_pagamento="PAGO",
    )

    # Atualizar o dono do produto para o comprador
    produto.owner_id = comprador.id

    db.add(nova_transacao)
    db.commit()
    db.refresh(nova_transacao)
    nova_transacao.message = "Transação realizada com sucesso."
    return RespostaTransacaoSchema.model_validate(nova_transacao)