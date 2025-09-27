
import datetime
import jwt
""" 
    Função responsavel por gerar o token e decodifica-lo
"""

SECRET_KEY = "chave_super_secreta"
class Token:
  @staticmethod
  def gerar_token(user_id:int):
    now = datetime.datetime.now(datetime.timezone.utc)
    payload = {
       "user_id": user_id,
       "exp": now + datetime.timedelta(hours=3),
       "iat": now
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token
  @staticmethod
  def decode_token(token:str):
    try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
      return payload
    except jwt.ExpiredSignatureError:
      return {"message": "Token expirado"}
    except jwt.InvalidTokenError:
      return {"message": "Token inválido"}
