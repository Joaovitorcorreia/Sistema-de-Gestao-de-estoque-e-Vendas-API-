from fastapi import FastAPI, APIRouter
from api.routes.usuários import cadastro
from api.routes.produtos import produtos
from api.routes.compras_e_vendas import compras_e_vendas
from api.routes.produtos import produtos_disponiveis

app = FastAPI(title="Sistema de Gestão de Estoque e Vendas",description="API para gestão de estoque e vendas", version="1.0.0")
app.include_router(cadastro)
app.include_router(produtos)
app.include_router(compras_e_vendas)
app.include_router(produtos_disponiveis)

