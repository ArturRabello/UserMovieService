from flask import request
import jwt
""" 
    Função reponsavel por extrair o user_id do token
"""
def get_user_id_from_token(SECRET_KEY):
    auth_header = request.headers.get('Authorization')
    print(auth_header)
    if not auth_header:
        print("Authorization header not found")
        return None
    
    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print(payload)
        return payload["user_id"]
    except Exception as e:
        print("Error decoding token:", e)
        return None