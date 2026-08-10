from pydantic import BaseModel, EmailStr, Field


# criar produtos
class CriarProdutoSchema(BaseModel):
    nome_do_usuario: str = Field(..., example="Seu nome de usuário")
    email_do_usuario: EmailStr = Field(..., example="seu.email@exemplo.com")
    senha_do_usuario: str = Field(..., min_length=6, example="sua_senha_segura")

    nome: str = Field(..., example="Produto Exemplo")
    descricao: str = Field(..., example="Descrição do produto exemplo")
    preco: float = Field(..., example=99.99)

class RespostaProdutoSchema(BaseModel):
    nome: str
    descricao: str
    preco: float
    message: str = Field(..., example="Produto cadastrado com sucesso.")

# listar produtos
class ListarProdutosSchema(BaseModel):
    nome: str
    descricao: str
    preco: float

class ListarProdutosResponseSchema(BaseModel):
    produtos: list[ListarProdutosSchema]
    message: str = Field(..., example="Produtos listados com sucesso.")

# atualizar produtos
class AtualizarProdutoSchema(BaseModel):
    nome: str | None = Field(None, example="Produto Atualizado")
    descricao: str | None = Field(None, example="Descrição atualizada do produto")
    preco: float | None = Field(None, example=149.99)

class RespostaAtualizarProdutoSchema(BaseModel):
    nome: str | None
    descricao: str | None
    preco: float | None
    message: str = Field(..., example="Produto atualizado com sucesso.")

# deletar produtos
class DeletarProdutoSchema(BaseModel):
    nome: str
    descricao: str
    preco: float
    
class RespostaDeletarProdutoSchema(BaseModel):
    nome: str
    descricao: str
    preco: float
    message: str = Field(..., example="Produto deletado com sucesso.")

   
"""Lista de todos os produtos cadastrados, com o nome do usuário que cadastrou cada produto, e o email do usuário que cadastrou cada produto."""

class DonoResumoSchema(BaseModel):
    id: int
    nome: str
    email: EmailStr


class ProdutoComDonoSchema(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float
    dono: DonoResumoSchema

    class Config:
        from_attributes = True