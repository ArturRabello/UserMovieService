from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from flask_smorest import Api, Blueprint
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from utils.token import Token
from models import UserMovies
from database import Base, Session, engine
from schemas import *
import jwt
import datetime
import os

#chave utilizada para descodificar o token
SECRET_KEY = "chave_super_secreta"

app = Flask(__name__)

CORS(app, supports_credentials=True, origins=["http://localhost:3000"])
app.config["API_TITLE"] = "Movie Service"
app.config["API_VERSION"] = "1.0"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
api = Api(app)

#definição da blueprint
auth_db = Blueprint('MovieUser', 'MovieUser', url_prefix="/movieUser",description="Movie and User Association Operations")

#criação da tabela
Base.metadata.create_all(bind=engine)


@auth_db.route('/setTokenDev', methods=['POST'])
@auth_db.arguments(IdAddTokenSchema)
@auth_db.response(200, description="Development cookie set successfully")
def register_dev(data):
    """Endpoint para desenvolvimento - cookie menos seguro mas compatível com Swagger"""
    token = Token.gerar_token(data['user_id'])    

    payload = jwt.decode(token, options={"verify_signature": False})
    exp_time = datetime.datetime.fromtimestamp(payload["exp"], tz=datetime.timezone.utc)
    max_age = (exp_time - datetime.datetime.now(datetime.timezone.utc)).total_seconds()
    
    response = make_response(jsonify({"message": "Development cookie set successfully", "token": token}))
    
    # Cookie para desenvolvimento - sem httponly, secure=False
    response.set_cookie(
        "token", 
        token, 
        httponly=False,  # Permite acesso via JavaScript
        samesite='Lax',  # Menos restritivo
        max_age=int(max_age), 
        secure=False     # Para desenvolvimento local
    )
    
    return response

# SOLUÇÃO 3: Função helper para extrair token tanto do cookie quanto do header
def get_token_from_request():
    """Extrai token do cookie ou do header Authorization"""
    # Primeiro tenta pegar do cookie
    token = request.cookies.get('token')
    
    if not token:
        # Se não tem no cookie, tenta pegar do header Authorization
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
    
    return token

# SOLUÇÃO 4: Endpoint para testar autenticação
@auth_db.route('/testAuth', methods=['GET'])
@auth_db.response(200, description="Authentication test successful")
@auth_db.response(401, description="Token not found or invalid")
def test_auth():
    """Endpoint para testar se a autenticação está funcionando"""
    token = get_token_from_request()
    
    if not token:
        return jsonify({"message": "Token not found in cookie or Authorization header"}), 401
    
    payload = Token.decode_token(token)
    if "message" in payload:
        return jsonify(payload), 401
    
    return jsonify({
        "message": "Authentication successful",
        "user_id": payload["user_id"],
        "token_source": "cookie" if request.cookies.get('token') else "header"
    }), 200

# Atualizar os endpoints existentes para usar a função helper
@auth_db.route('/addMovies', methods=['POST'])
@auth_db.arguments(UserMovieSchema)
@auth_db.response(201, responseUserSchema, description="Movie added successfully")
@auth_db.response(400, errorInvalidRequestDataSchema, description="Validation error")
@auth_db.response(409, movieAlredyExists, description="Movie already exists")
@auth_db.response(500, errorDatabaseErrorSchema, description="Database error")
@auth_db.response(401, TokenExpiredSchema,description="Token expired")
def add_movie(data):
    # Usar a função helper para pegar o token
    token = get_token_from_request()
    if not token:
        return jsonify({"message": "Token not found in cookie or Authorization header"}), 401
        
    payload = Token.decode_token(token)
    if("message" in payload):
        return (jsonify(payload), 401)
    
    user_id = payload["user_id"]
        
    userMovie = UserMovies(
        user_id = user_id,
        movie_id = data['movie_id'],
        score = data['score']
    )
    session = Session()

    try:
        if session.query(UserMovies).filter(UserMovies.user_id == userMovie.user_id, UserMovies.movie_id == userMovie.movie_id).first():
            session.close()
            return jsonify({"message": "Movie already exists"}), 409
        
        session.add(userMovie)
        session.commit()        
        return jsonify({"message": "Movie added successfully"}), 201
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400        
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"message": "Database error", "error": str(e)}), 500
    finally:
        if session:
            session.close()

# Aplicar a mesma mudança nos outros endpoints...
@auth_db.route('/removeMovies', methods=['DELETE'])
@auth_db.arguments(MovieIdQuerySchema, location='query')
@auth_db.response(201, responseDelMovieSchema, description="Movie removed successfully")
@auth_db.response(400, errorInvalidRequestDataSchema, description="Validation error")
@auth_db.response(409, errorUserNotFoundSchema, description="User not found")
@auth_db.response(500, errorDatabaseErrorSchema, description="Database error")
@auth_db.response(401, TokenExpiredSchema,description="Token expired")
def remove(args):
    movie_id = args["movie_id"]
    if not movie_id:
        return jsonify({"message": "movie_id is required"}), 400    
    
    # Usar a função helper
    token = get_token_from_request()
    if not token:
        return jsonify({"message": "Token not found in cookie or Authorization header"}), 401
        
    payload = Token.decode_token(token)
    if("message" in payload):
        return (jsonify(payload), 401)
    
    user_id = payload["user_id"]
     
    session = Session()
    try:
        user = session.query(UserMovies).filter(UserMovies.user_id == user_id, UserMovies.movie_id == movie_id).first()
        
        if user == None:
            session.close()
            return jsonify({"message": "User not found"}), 409
        else:
            session.delete(user)
            session.commit()
            session.close()
            return jsonify({"message": "Movie removed successfully"}), 201
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"message": "Database error", "error": str(e)}), 500
    finally:
        if session:
            session.close()

# Aplicar a correção nos endpoints restantes
@auth_db.route('/setScore', methods=['PUT'])
@auth_db.arguments(UserMovieSchema)
@auth_db.response(201, responseUpdateScoreSchema, description="Score updated successfully")
@auth_db.response(400, errorInvalidRequestDataSchema, description="Validation error")
@auth_db.response(409, errorUserNotFoundSchema, description="User not found")
@auth_db.response(500, errorDatabaseErrorSchema, description="Database error")
@auth_db.response(401, TokenExpiredSchema,description="Token expired")
def update(data):
    # Usar a função helper
    token = get_token_from_request()
    if not token:
        return jsonify({"message": "Token not found in cookie or Authorization header"}), 401
        
    payload = Token.decode_token(token)
    if("message" in payload):
        return (jsonify(payload), 401)
    
    user_id = payload["user_id"]
    
    userMovie = UserMovies(
        user_id = user_id,
        movie_id = data['movie_id'],
        score = data['score']
    )
    session = Session()
    try:
        user = session.query(UserMovies).filter(UserMovies.user_id == userMovie.user_id, UserMovies.movie_id == userMovie.movie_id).first()
        
        if user == None:
            session.close()
            return jsonify({"message": "User not found"}), 409
        else:
            user.score = data["score"]
            session.commit()
            session.close()
            return jsonify({"message": "Score updated successfully"}), 201
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"message": "Database error", "error": str(e)}), 500
    finally:
        if session:
            session.close()

@auth_db.route('/getList', methods=['GET'])
@auth_db.response(201, UserMovieSchemaList(many=True), description="User found successfully")
@auth_db.response(409, errorUserNotFoundSchema, description="User not found")
@auth_db.response(500, errorDatabaseErrorSchema, description="Database error")
@auth_db.response(400, errorInvalidRequestDataSchema, description="Validation error")
@auth_db.response(401, TokenExpiredSchema,description="Token expired")
def getList():
    # Usar a função helper
    token = get_token_from_request()
    if not token:
        return jsonify({"message": "Token not found in cookie or Authorization header"}), 401
        
    payload = Token.decode_token(token)
    if("message" in payload):
        return (jsonify(payload), 401)
    
    user_id = payload["user_id"]
    session = Session()
    try:
        user = session.query(UserMovies).filter(UserMovies.user_id == user_id).all()
        
        if not user:
            return jsonify({"message": "User not found"}), 409
        else:
            return jsonify(returnUserMovies(user)), 200
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"message": "Database error", "error": str(e)}), 500
    finally:
        if session:
            session.close()

@auth_db.route('/verifyMovie', methods=['GET'])
@auth_db.arguments(MovieIdQuerySchema, location='query')
@auth_db.response(200, description="The movie is already added")
@auth_db.response(404, description="Movie not found")
@auth_db.response(401, description="Token expired or invalid")
def verifyMovie(args):
    movie_id = args["movie_id"]
    if not movie_id:
        return jsonify({"message": "movie_id is required"}), 400
    
    # Usar a função helper
    token = get_token_from_request()
    if not token:
        return jsonify({"message": "Token not found in cookie or Authorization header"}), 401

    payload = Token.decode_token(token)
    if "message" in payload:
        return jsonify(payload), 401

    user_id = payload["user_id"]

    session = Session()
    try:
        user_movie = session.query(UserMovies).filter(
            UserMovies.user_id == user_id,
            UserMovies.movie_id == movie_id
        ).first()

        if not user_movie:
            return jsonify({"message": "Movie not found"}), 404

        return jsonify({"message": "The movie is already added"}), 200

    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400
    finally:
        session.close()

@auth_db.route('/getScore', methods=['GET'])
@auth_db.arguments(MovieIdQuerySchema, location='query')
@auth_db.response(201, description="Score found successfully")
@auth_db.response(409, errorUserNotFoundSchema, description="User not found")
@auth_db.response(500, errorDatabaseErrorSchema, description="Database error")
@auth_db.response(400, errorInvalidRequestDataSchema, description="Validation error")
@auth_db.response(401, TokenExpiredSchema,description="Token expired")
def getScore(args):
    movie_id = args["movie_id"]
    if not movie_id:
        return jsonify({"message": "movie_id is required"}), 400
    
    # Usar a função helper
    token = get_token_from_request()
    if not token:
        return jsonify({"message": "Token not found in cookie or Authorization header"}), 401
    
    payload = Token.decode_token(token)
    if("message" in payload):
        return (jsonify(payload), 401)
    
    user_id = payload["user_id"]
    session = Session()

    try:
        user_movies = session.query(UserMovies).filter(UserMovies.user_id == user_id, UserMovies.movie_id == movie_id).first()

        if not user_movies:
            return jsonify({"message": "User not found"}), 409
        
        return jsonify({"movie_id": user_movies.movie_id, "score": user_movies.score}), 201
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"message": "Database error", "error": str(e)}), 500
    finally:
        if session:
            session.close()

# Registra as rotas na documentação    
api.register_blueprint(auth_db)

if __name__ == "__main__":
    app.run(debug=True)