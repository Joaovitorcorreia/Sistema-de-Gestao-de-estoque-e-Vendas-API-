from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.session import get_db
from models.models_produtos import Products
from models.models_transacoes import Transacoes
from models.models_usuarios import Users
from schemas.schemas_transacoes import RealizarTransacaoSchema, RespostaTransacaoSchema


compras_e_vendas = APIRouter(tags=["Compras e Vendas"])

@compras_e_vendas.post("/realizar-transacao/")
async def realizar_transacao(transacao: RealizarTransacaoSchema, db=Depends(get_db)):
    # Verificar se o produto existe
    produto = db.query(Products).filter(Products.id == transacao.product_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    # Verificar se o comprador existe
    comprador = db.query(Users).filter(Users.id == transacao.comprador_id).first()
    if not comprador:
        raise HTTPException(status_code=404, detail="Comprador não encontrado.")

    # Verificar se o vendedor existe e se a senha está correta
    vendedor = db.query(Users).filter(Users.email == transacao.vendedor_email).first()
    if not vendedor or vendedor.senha != transacao.vendedor_senha:
        raise HTTPException(status_code=401, detail="Credenciais do vendedor inválidas.")

    # validar se o produto pertence ao vendedor
    if produto.owner_id != vendedor.id:
        raise HTTPException(status_code=403, detail="O produto não pertence ao vendedor.")

    # Criar a transação
    nova_transacao = Transacoes(
        product_id=transacao.product_id,
        owner_id=vendedor.id,
        buyer_id=transacao.comprador_id,
        value=transacao.valor,
        payment_method=transacao.metodo_pagamento,
        status_pagamento="PAGO",
    )

    # Atualizar o dono do produto para o comprador
    produto.owner_id = comprador.id

    db.add(nova_transacao)
    db.commit()
    db.refresh(nova_transacao)
    return RespostaTransacaoSchema.from_orm(nova_transacao, message="Transação realizada com sucesso.")