import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


# 1. Teste de Sucesso: Criar produto com usuário existente e credenciais corretas
def test_cadastrar_produto_sucesso(client: TestClient):
    sufixo = uuid.uuid4().hex[:8]
    
    # Passo A: Criar um usuário real no banco para vinculação
    payload_user = {
        "nome":  "Usuario",
        "email": "teste__@email.com",
        "senha": "senha123"
    }
    client.post("/criar-usuários", json=payload_user)

    # Passo B: Enviar o payload do produto exatamente como o CriarProdutoSchema espera
    payload_produto = {
        "nome": f"Produto Teste",
        "descricao": "Descrição de teste",
        "preco": 50.0,
        "nome_do_usuario": payload_user["nome"],
        "email_do_usuario": payload_user["email"],
        "senha_do_usuario": payload_user["senha"]
    }

    response = client.post("/criar-produtos/", json=payload_produto)

    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == payload_produto["nome"]

# 2. Teste de Erro: Tentar criar produto com usuário inexistente (Status 404)
def test_cadastrar_produto_usuario_nao_encontrado(client: TestClient):
    payload_produto = {
        "nome": "Produto Teste",
        "descricao": "Descrição de teste",
        "preco": 50.0,
        "nome_do_usuario": "usuario_fantasma_1234",
        "email_do_usuario": "fantasma@email.com",
        "senha_do_usuario": "senha123"
    }

    response = client.post("/criar-produtos/", json=payload_produto)

    assert response.status_code == 404
    assert "Usuário não encontrado" in response.json()["detail"]

# 3. Teste de Erro: Tentar criar produto com senha errada (Status 404)
def test_cadastrar_produto_senha_incorreta(client: TestClient):
    sufixo = uuid.uuid4().hex[:8]
    
    # Criar usuário
    payload_user = {
        "nome": f"Dono_{sufixo}",
        "email": f"dono_{sufixo}@email.com",
        "senha": "senhaCerta123"
    }
    client.post("/criar-usuarios", json=payload_user)

    # Payload com senha errada
    payload_produto = {
        "nome": "Produto Teste",
        "descricao": "Teste de senha",
        "preco": 100.0,
        "nome_do_usuario": payload_user["nome"],
        "email_do_usuario": payload_user["email"],
        "senha_do_usuario": "senhaERRADA"
    }

    response = client.post("/criar-produtos/", json=payload_produto)

    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado, é necessário criar um usuário antes de cadastrar um produto."