from fastapi import FastAPI, APIRouter
from app.api.routes.usuários import cadastro, auth, alteração_de_senha
from app.api.routes.produtos import produtos
from app.api.routes.compras_e_vendas import compras_e_vendas
from app.api.routes.produtos import produtos_disponiveis
from app.database.session import Base, engine
from app.database.session import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Gestão de Estoque e Vendas",description="API para gestão de estoque e vendas", version="1.0.0")
app.include_router(cadastro)
app.include_router(produtos)
app.include_router(compras_e_vendas)
app.include_router(produtos_disponiveis)
app.include_router(auth)
app.include_router(alteração_de_senha)


@app.on_event("startup")
def on_startup():
	# Create database tables at application startup
	Base.metadata.create_all(bind=engine)

