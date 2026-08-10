from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from schemas.schemas_usuarios import CriarUsuarioSchema, RespostaUsuarioSchema, VerificarUsuarioSchema, RespostaVerificarUsuarioSchema, AtualizarUsuarioSchema, DeletarUsuarioSchema
from database.session import get_db
from models.models_usuarios import Users

AtualizarUsuarioSchema.model_rebuild()
RespostaUsuarioSchema.model_rebuild()


cadastro = APIRouter(tags=["Cadastro de Usuários"])

@cadastro.post("/criar-usuários/", response_model=RespostaUsuarioSchema)
async def cadastrar_usuario(usuario: CriarUsuarioSchema, db=Depends(get_db)):
    novo_usuario = Users(nome=usuario.nome, email=usuario.email, senha=usuario.senha)

    try:
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email já cadastrado por outro usuário.")

    return RespostaUsuarioSchema(nome=novo_usuario.nome, email=novo_usuario.email, message="Usuário cadastrado com sucesso.")

@cadastro.get("/verificar-usuários/{user_id}", response_model=RespostaVerificarUsuarioSchema)
async def verificar_usuario(user_id: int, db=Depends(get_db)):
    usuario = db.query(Users).filter(Users.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    return RespostaVerificarUsuarioSchema(nome=usuario.nome, email=usuario.email, produtos=usuario.products)

@cadastro.put("/atualizar-usuários/{user_id}", response_model=RespostaUsuarioSchema)
async def atualizar_usuario(user_id: int, usuario_atualizado: AtualizarUsuarioSchema, db=Depends(get_db)):
    usuario = db.query(Users).filter(Users.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    usuario.nome = usuario_atualizado.nome
    usuario.email = usuario_atualizado.email

    db.commit()
    db.refresh(usuario)

    return RespostaUsuarioSchema(nome=usuario.nome, email=usuario.email, message="Usuário atualizado com sucesso.")

# para atualizar a senha, você pode criar um endpoint separado que aceite a senha antiga e a nova senha, com o Jwt.

@cadastro.delete("/deletar-usuários/{user_id}", response_model=RespostaUsuarioSchema)
async def deletar_usuario(user_id: int, db=Depends(get_db)):
    usuario = db.query(Users).filter(Users.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    db.delete(usuario)
    db.commit()

    return RespostaUsuarioSchema(nome=usuario.nome, email=usuario.email, message="Usuário deletado com sucesso.")