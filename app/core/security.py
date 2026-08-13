import bcrypt

def gerar_hash_senha(senha: str) -> str:
    senha_bytes = senha.encode('utf-8')  # Converte a senha para bytes
    # Gera um salt aleatório
    salt = bcrypt.gensalt(rounds=12)
    # Gera o hash da senha usando o salt
    hash_senha = bcrypt.hashpw(senha_bytes, salt)
    return hash_senha.decode('utf-8')

def verificar_senha(senha_digitada: str, hash_salvo: str) -> bool:
    return bcrypt.checkpw(
        senha_digitada.encode('utf-8'),
        hash_salvo.encode('utf-8')
    )