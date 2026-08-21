from fastapi import FastAPI, APIRouter, Depends, HTTPException
from app.database.session import get_db
from app.models.models_produtos import Products
from app.schemas.schemas_produtos import (CriarProdutoSchema, RespostaProdutoSchema, ListarProdutosSchema, ListarProdutosResponseSchema, AtualizarProdutoSchema, RespostaAtualizarProdutoSchema, DeletarProdutoSchema, RespostaDeletarProdutoSchema,
DonoResumoSchema, ProdutoComDonoSchema)
from app.core.security import verificar_senha
from app.core.auth_token import verificar_token
from app.models.models_usuarios import Users
from typing import List
from sqlalchemy.orm import Session


produtos = APIRouter(tags=["Cadastro de Produtos"])

@produtos.post("/criar-produtos/")
async def cadastrar_produto(produto: CriarProdutoSchema, db=Depends(get_db)):
    usuario = db.query(Users).filter(Users.nome == produto.nome_do_usuario, Users.email == produto.email_do_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado, é necessário criar um usuário antes de cadastrar um produto.")

    if not verificar_senha(produto.senha_do_usuario, usuario.senha):
        raise HTTPException(status_code=401, detail="Senha incorreta.")

    if usuario.email != produto.email_do_usuario:
        raise HTTPException(status_code=401, detail="Email incorreto.")

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
async def listar_produtos(usuario_email: str, db=Depends(get_db)):
    usuario = db.query(Users).filter(Users.email == usuario_email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    produtos = db.query(Products).filter(Products.owner_id == usuario.id).all()
    produtos_schema = [ListarProdutosSchema.model_validate(p) for p in produtos]
    return ListarProdutosResponseSchema(produtos=produtos_schema, message="Produtos listados com sucesso.")


@produtos.put("/atualizar-produtos", response_model=RespostaAtualizarProdutoSchema)
async def atualizar_produto(produto_atualizado: AtualizarProdutoSchema, token_payload: dict = Depends(verificar_token), db=Depends(get_db)):

    """Observação: Voçê deve estar autenticado antes de atualizar o produto"""

    usuario_email = token_payload.get("sub")

    usuario = db.query(Users).filter(Users.email == usuario_email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado ou token inválido.")

    produto = db.query(Products).filter(Products.nome == produto_atualizado.nome_do_antigo_produto, Products.owner_id == usuario.id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado ou não pertence ao usuário.")

    if produto_atualizado.nome is not None:
        produto.nome = produto_atualizado.nome
    if produto_atualizado.descricao is not None:
        produto.descricao = produto_atualizado.descricao
    if produto_atualizado.preco is not None:
        produto.preco = produto_atualizado.preco

    db.commit()
    db.refresh(produto)

    return RespostaAtualizarProdutoSchema(nome=produto.nome, descricao=produto.descricao, preco=produto.preco, message="Produto atualizado com sucesso.")

@produtos.delete("/deletar-produtos")
async def deletar_produto(produto_deletar: DeletarProdutoSchema, token_payload: dict = Depends(verificar_token), db=Depends(get_db)):
    usuario_email = token_payload.get("sub")
    usuario = db.query(Users).filter(Users.email == usuario_email).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado ou token inválido.")
    
    produto = db.query(Products).filter(Products.nome == produto_deletar.nome, Products.descricao == produto_deletar.descricao, Products.preco == produto_deletar.preco ).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    db.delete(produto)
    db.commit()

    return RespostaDeletarProdutoSchema(nome=produto.nome, descricao=produto.descricao, preco=produto.preco, message="Produto deletado com sucesso.")

# lista todos os produtos cadastrados
produtos_disponiveis = APIRouter(tags=["Produtos Disponíveis para Comercialização"])

@produtos_disponiveis.get("/Todos-os-produtos-existentes-para-comercialização", response_model=List[ProdutoComDonoSchema])
async def obter_produto_com_dono(db: Session = Depends(get_db)):
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