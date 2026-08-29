1. Nome do projeto

Sistema de Gestão e Estoque de Vendas
Descrição: Esse projeto é uma API que facilita o sistema de criação, administração e vendas de um produto.

2. Sobre o projeto

O que o sistema faz?
Ele tem a capacidade de cadastrar usuários e produtos com CRUD completo, podendo também fazer transferências de produtos para outros usuários.

Objetivo do projeto
Implementar de maneira simples, um sistema completo e seguro tanto para os usuários, quanto aos produtos criados.

3. Funcionalidades

Cadastro/login
JWT
CRUD de Usuários
CRUD de Produtos
Alteração de senha com autenticação JWT (senha salva com bcrypt no SQL)
Validações
Lista de todos os produtos existentes
Filtragem de produtos existentes para comercialização
etc.


4. Tecnologias utilizadas

Python
FastAPI
SQLAlchemy
PostgreSQL
Alembic
Pydantic
JWT
Docker
Docker Compose
Pytest


5. Arquitetura do projeto

├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── README
│   └── script.py.mako
├── app/
│   ├── api/
│   ├── core/
│   │   ├── auth_token.py
│   │   └── security.py
│   ├── database/
│   │   └── session.py
│   ├── models/
│   │   ├── models_produtos.py
│   │   ├── models_transacoes.py
│   │   └── models_usuarios.py
│   ├── schemas/
│   │   ├── schemas_produtos.py
│   │   ├── schemas_transacoes.py
│   │   └── schemas_usuarios.py
│   ├── main.py
│   └── testes/
│       ├── __init__.py
│       └── teste_test.py
├── .env
├── .dockerignore
├── .gitignore
├── alembic.ini
├── Dockerfile
├── docker-compose.yaml
├── README.md
└── requirements.txt


6. Pré-requisitos

Python
Docker
Docker Compose
Git



7. Como executar Explicar desde o clone:

git clone ...
docker compose up --build


8. Banco de dados

PostgreSQL
SQLAlchemy


9. Autenticação:

Login
Token de Acesso
JWT
Rotas protegidas
Hash de senha



10. Documentação da API, Como acessar?:

/docs
/redoc


11. Testes

pytest (sendo testado algumas operações de rota dos usuários e produtos)


12. Endpoints principais


|   Método   |   Endpoint   |   Descrição   |   Categoria   |
|------------|--------------|---------------|---------------|
| POST       | /criar-usuarios | Cadastrar Usuário | Cadastro de Usuários |
| GET        | /verificar-usuarios | Verificar Usuário | Cadastro de Usuários |
| PUT        | /atualizar-usuarios/{user_id} | Atualizar Usuário | Cadastro de Usuários |
| DELETE     | /deletar-usuarios/{user_id} | Deletar Usuário | Cadastro de Usuários |


| POST       | /criar-produtos/ | Cadastrar Produto | Cadastro de Produtos |
| GET        | /listar-produtos/{user_id} | Listar Produtos | Cadastro de Produtos |
| PUT        | /atualizar-produtos | Atualizar Produto | Cadastro de Produtos |
| DELETE     | /deletar-produtos | Deletar Produto | Cadastro de Produtos |

| POST       | /realizar-transacao | Realizar Transação | Compras e Vendas |

| GET        | /todos-os-produtos-existentes-para-comercializacao | Obter Produto Com Dono | Produtos Disponíveis |
| GET        | /filtrar-produtos | Filtrar Produtos | Produtos Disponíveis |


| POST       | /criar-token-de-acesso | Criar Tokens | Criar Token de Autenticação |
| GET        | /verificar_tokens | Verificar Tokens | Criar Token de Autenticação |


| PUT        | /alterar-senha | Alterar Senha | Alteração de Senha |


13. Decisões técnicas:


Por que PostgreSQL?
Ele é um banco onde é bem grande e rápido e é fácil de sintetizar e de administrá-lo.

Por que SQLAlchemy?
Ele irá facilitar a comunicação do SQL com o usuário dentro da API, sendo fácil de trabalhar com ele.

Por que Alembic?
Ele faz as migrações de versões de uma database automaticamente, alterando tables, colunas, etc.

Por que JWT?
Irá trazer segurança ao usuário, garantindo que realmente é a pessoa que está fazendo operações em sua conta.

Por que Docker?
Ele irá armazenar o SQL e a API em containers, com suas versões compatíves a fim de qualquer pessoa consiga acessar em sua máquina local.

Por que separar schemas, models, services e repositories?

Caso ocorrer erros, ou procurar nomes de variáveis ou uma síntese específica, etc, irá conseguir encontrá-lo facilmente nesses arquivos, e também consegue estruturar a API de forma organizada.

