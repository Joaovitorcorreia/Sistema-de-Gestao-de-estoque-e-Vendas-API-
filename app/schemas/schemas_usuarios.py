from pydantic import BaseModel, EmailStr, Field

# criar usuários
class CriarUsuarioSchema(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    senha: str = Field(..., min_length=6)

class RespostaUsuarioSchema(BaseModel):
    nome: str
    email: EmailStr
    message: str

# verificar usuários
class VerificarUsuarioSchema(BaseModel):
    email: EmailStr

class RespostaVerificarUsuarioSchema(BaseModel):
    nome: str
    email: EmailStr
    message: str

# atualizar usuários
class AtualizarUsuarioSchema(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., min_length=1, max_length=100)
# vai ser usado como resposta o respostausuarioschema

class AlterarSenha(BaseModel):
    nome: str
    email: EmailStr
    nova_senha: str

class DeletarUsuarioSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str = Field(..., min_length=6)
#a mesma coisa, vai ser usado como resposta o respostausuarioschema
    class Config:
        from_attributes = True
    
