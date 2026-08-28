
import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid


@pytest.fixture
def client():
    return TestClient(app)


# 1. Teste de Sucesso: Criar usuário novo
def test_cadastrar_usuario_sucesso(client: TestClient(app)):
    # Gerando e-mail único para não dar conflito no banco
    sulfixo = uuid.uuid4().hex[:8]
    payload = {
        "nome": "Usuario",
        "email": "test@email.com",
        "senha": "senha123"
    }

    response = client.post("/criar-usuários", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == payload["email"]
    assert "nome" in data

# 2. Teste de Erro: Tentar cadastrar o mesmo e-mail duas vezes (IntegrityError)
def test_cadastrar_usuario_email_duplicado(client: TestClient(app)):
    sulfixo = uuid.uuid4().hex[:8]
    payload = {
        "nome": "Usuario",
        "email": "teste@email.com",
        "senha": "senhaSegura123"
    }

    # Primeira requisição: Cadastra com sucesso
    client.post("/criar-usuários", json=payload)

    # Segunda requisição: Deve cair no 'except IntegrityError' (retornando 400)
    response_duplicada = client.post("/criar-usuários", json=payload)

    assert response_duplicada.status_code == 400
    assert response_duplicada.json()["detail"] == "Email já cadastrado por outro usuário."