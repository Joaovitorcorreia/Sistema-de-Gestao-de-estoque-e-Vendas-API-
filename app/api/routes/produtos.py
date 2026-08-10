from fastapi import FastAPI, APIRouter, Depends, HTTPException
from database.session import get_db
from models.models_produtos import Products
from schemas.schemas_produtos import (CriarProdutoSchema, RespostaProdutoSchema, ListarProdutosResponseSchema, AtualizarProdutoSchema, RespostaAtualizarProdutoSchema, RespostaDeletarProdutoSchema,
DonoResumoSchema, ProdutoComDonoSchema)
from models.models_usuarios import Users
from typing import List
from sqlalchemy.orm import Session

produtos = APIRouter(tags=["Cadastro de Produtos"])

@produtos.post("/criar-produtos/")
async def cadastrar_produto(produto: CriarProdutoSchema, db=Depends(get_db)):
    usuario = db.query(Users).filter(Users.email == produto.email_do_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado, é necessário criar um usuário antes de cadastrar um produto.")

    if usuario.senha != produto.senha_do_usuario:
        raise HTTPException(status_code=401, detail="Senha incorreta.")

    novo_produto = Products(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
        owner_id=usuario.id
    )
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return RespostaProdutoSchema(nome=novo_produto.nome, descricao=novo_produto.descricao, preco=novo_produto.preco, message="Produto cadastrado com sucesso.")

@produtos.get("/listar-produtos/{user_id}")
async def listar_produtos(user_id: int, db=Depends(get_db)):
    usuario = db.query(Users).filter(Users.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    produtos = db.query(Products).filter(Products.owner_id == user_id).all()
    return ListarProdutosResponseSchema(produtos=produtos, message="Produtos listados com sucesso.")

@produtos.put("/atualizar-produtos/{produto_id}")
async def atualizar_produto(produto_id: int, produto_atualizado: AtualizarProdutoSchema, db=Depends(get_db)):
    produto = db.query(Products).filter(Products.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    if produto_atualizado.nome is not None:
        produto.nome = produto_atualizado.nome
    if produto_atualizado.descricao is not None:
        produto.descricao = produto_atualizado.descricao
    if produto_atualizado.preco is not None:
        produto.preco = produto_atualizado.preco

    db.commit()
    db.refresh(produto)

    return RespostaAtualizarProdutoSchema(nome=produto.nome, descricao=produto.descricao, preco=produto.preco, message="Produto atualizado com sucesso.")

@produtos.delete("/deletar-produtos/{produto_id}")
async def deletar_produto(produto_id: int, db=Depends(get_db)):
    produto = db.query(Products).filter(Products.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    db.delete(produto)
    db.commit()

    return RespostaDeletarProdutoSchema(nome=produto.nome, descricao=produto.descricao, preco=produto.preco, message="Produto deletado com sucesso.")

# lista todos os produtos cadastrados
produtos_disponiveis = APIRouter(tags=["Produtos Disponíveis para Comercialização"])

@produtos_disponiveis.get("/Todos-os-produtos-existentes-para-comercialização/{produto_id}", response_model=List[ProdutoComDonoSchema])
async def obter_produto_com_dono(produto_id: int, db=Depends(get_db)):
    produto = db.query(Products).filter(Products.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    todos_os_produtos = db.query(Products).all()
    return todos_os_produtos

# filtrar produtos
@produtos_disponiveis.get("/Filtrar-produtos", response_model=List[ProdutoComDonoSchema])
async def filtrar_produtos(nome: str | None = None, descricao: str | None = None, preco_min: float | None = None, preco_max: float | None = None, db=Depends(get_db)):
    query = db.query(Products)

    if nome:
        query = query.filter(Products.nome.ilike(f"%{nome}%"))
    if descricao:
        query = query.filter(Products.descricao.ilike(f"%{descricao}%"))
    if preco_min is not None:
        query = query.filter(Products.preco >= preco_min)
    if preco_max is not None:
        query = query.filter(Products.preco <= preco_max)

    produtos_filtrados = query.all()
    return produtos_filtrados