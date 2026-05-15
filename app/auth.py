#logica de autenticação 

#1. Hash e verificação de senhas com bcrypt

#2. Geraçaõ de token jwt

#3. Leitura e validação de token vindo do cookie

from datetime import datetime, timedelta, timezone
from jose import JWSError, jwt 
from passlib.context import CryptContext
from fastapi import Request, HTTPException, status
from dotenv import load_dotenv
import os 

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTE = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTE")

#Configurar o algoritmo do hash - bcrypt
pwd_context = CryptContext(schemes={"bcrypt"}, deprecated = "auto")


#Teste de senha 
# senha = "1234"
# senha_hash = pwd_context.hash(senha)
# # #$2b$12$wdruLcWwB1.gnra1lkgNROD1iiQED5.q9HaVudHkhM7jnOUNhd21S

# # print(senha)
# # print("Senha com hash: ")
# # print(senha_hash)


# senha_atual = "1234"

# print( pwd_context.verify(senha_atual, senha_hash))
#
def hash_senha(senha: str):
    return pwd_context.hash(senha)

def verificar_senha(senha: str, senha_hash: str):
    return pwd_context.verify(senha, senha_hash)

# Funções do token JWT

def criar_token(dados: dict):

    payload = dados.copy()

    #Define quando o token expira
    expira = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    payload.update({"exp": expira}) 

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token 
def decodificar_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms={ALGORITHM})
    return payload

#função para usar nas rotas
def get_usuario_logado(request: Request):

    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )

    try:
        payload = decodificar_token(token)
        email: str = payload.get("sub")

        if email is None:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )
        return payload
    except JWSError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido ou expirado"
        )