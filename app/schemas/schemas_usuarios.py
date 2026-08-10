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

    model_config = {"from_attributes": True}
# verificar usuários
class VerificarUsuarioSchema(BaseModel):
    email: EmailStr

class RespostaVerificarUsuarioSchema(BaseModel):
    nome: str
    email: EmailStr

# atualizar usuários
class AtualizarUsuarioSchema(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., min_length=1, max_length=100)
# vai ser usado como resposta o respostausuarioschema

class DeletarUsuarioSchema(BaseModel):
    nome: str
    email: EmailStr
#a mesma coisa, vai ser usado como resposta o respostausuarioschema

    
