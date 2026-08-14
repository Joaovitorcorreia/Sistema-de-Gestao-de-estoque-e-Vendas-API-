
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from app.schemas.schemas_usuarios import CriarUsuarioSchema, RespostaUsuarioSchema, VerificarUsuarioSchema, RespostaVerificarUsuarioSchema, AtualizarUsuarioSchema, DeletarUsuarioSchema, AlterarSenha
from app.database.session import get_db, Base, engine
from app.models.models_usuarios import Users
from app.core.security import gerar_hash_senha, verificar_senha
from app.core.auth_token import criar_token, verificar_token, oauth2_scheme


cadastro = APIRouter(tags=["Cadastro de Usuários"])
auth = APIRouter(tags=["Criar Token de autenticação"])
alteração_de_senha = APIRouter(tags=["Alteração de Senha"])

@cadastro.post("/criar-usuários", response_model=RespostaUsuarioSchema)
async def cadastrar_usuario(usuario: CriarUsuarioSchema, db=Depends(get_db)):
    try:
        novo_usuario = Users(nome=usuario.nome, email=usuario.email, senha=gerar_hash_senha(usuario.senha))
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email já cadastrado por outro usuário.")

    return RespostaUsuarioSchema(nome=novo_usuario.nome, email=novo_usuario.email, message="Usuário cadastrado com sucesso.")

@cadastro.get("/verificar-usuários", response_model=RespostaVerificarUsuarioSchema)
async def verificar_usuario(email: str, db=Depends(get_db)):
    usuario = db.query(Users).filter(Users.email == email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    return RespostaVerificarUsuarioSchema(nome=usuario.nome, email=usuario.email, message="Usuário encontrado com sucesso.")

@cadastro.put("/atualizar-usuários/{user_id}", response_model=RespostaUsuarioSchema)
async def atualizar_usuario(usuario_atualizado: AtualizarUsuarioSchema, db=Depends(get_db)):
    usuario = db.query(Users).filter(Users.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    if usuario_atualizado.nome is not None:
        usuario.nome = usuario_atualizado.nome
    if usuario_atualizado.email is not None:
        usuario.email = usuario_atualizado.email

    db.commit()
    db.refresh(usuario)

    return RespostaUsuarioSchema(nome=usuario.nome, email=usuario.email, message="Usuário atualizado com sucesso.")

# para atualizar a senha, você pode criar um endpoint separado que aceite a senha antiga e a nova senha, com o Jwt.
@auth.post("/criar-token-de-acesso")
async def criar_tokens(auth_form: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    """Observação: É necessário somente preencher o campo 'nome' com o email do usuário e a senha, o resto deixar em branco. Somente o email do usuário é aceito como username, não o nome do usuário."""

    usuario = db.query(Users).filter(Users.email == auth_form.nome).first()

    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")

    if not verificar_senha(auth_form.senha, usuario.senha) or auth_form.nome != usuario.email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas.")
    token_data = {"sub": usuario.email}
    token = criar_token(data=token_data)
    return {"access_token": token, "token_type": "bearer"}

@auth.get("/verificar_tokens")
def verificar_tokens(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if "error" in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=payload["error"])
    return {"message": "Token válido.", "user": payload["sub"]}

    
@alteração_de_senha.put("/alterar-senha", response_model=RespostaUsuarioSchema)
async def alterar_senha(usuario: AlterarSenha = Depends(verificar_token), db=Depends(get_db)):

    """Observação: voçê deve antes de alterar a senha, criar e validar o token gerado"""

    usuario_existente = db.query(Users).filter(Users.email == email, Users.nome == nome).first()

    if not usuario_existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")

    try:
        if len(nova_senha) < 6 or len(nova_senha) > 100:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A nova senha deve ter entre 6 e 100 caracteres.")

        usuario_existente.senha = gerar_hash_senha(nova_senha)
        db.commit()
        db.refresh(usuario_existente)
        
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao redefinir senha.")

    return {"email": usuario_existente.email, "message": "Senha redefinida com sucesso!"}



@cadastro.delete("/deletar-usuários/{user_id}", response_model=RespostaUsuarioSchema)
async def deletar_usuario(usuario: DeletarUsuarioSchema, db=Depends(get_db)):
    usuario = db.query(Users).filter(Users.nome == usuario.nome, Users.email == usuario.email, Users.senha == usuario.senha).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    db.delete(usuario)
    db.commit()

    return RespostaUsuarioSchema(nome=usuario.nome, email=usuario.email, message="Usuário deletado com sucesso.")