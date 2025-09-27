import datetime
from typing import List
from marshmallow import Schema, fields

"""
   Esquemas de validação e retorno de dados
"""
class UserMovieSchema(Schema):
    movie_id = fields.String(load_default="2")
    score = fields.Integer(load_default=3)

class verifyMovieSchema(Schema):
    movie_id = fields.String(load_default="2")

class IdAddTokenSchema(Schema):
    user_id = fields.Integer(load_default=1)
    
class UserMovieHeaderTokenSchema(Schema):
    authorization = fields.Str(
        required=True,
        metadata={
            "description": "Authorization",
            "example": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJpYXQiOjE3NTY4MjgxODAsImV4cCI6MTc1NjgzODk4MH0.iuwBienipoUDcMhEStsJBfcVJ49iHjUvscYlHqpooPg",
        }
    )

class RemovieMovieSchema(Schema):
    movie_id = fields.String(load_default=2)

class UserMovieSchemaResponse(Schema):
    id = fields.Integer(load_default=1)
    user_id = fields.Integer(load_default=1)
    movie_id = fields.String(load_default=2)
    score = fields.Integer(load_default=3)
    created_at = fields.Date(load_default=datetime.datetime.now())
    updated_at = fields.Date(load_default=datetime.datetime.now())    
    
class UserMovieSchemaList(Schema):
    users = fields.List(fields.Nested(UserMovieSchemaResponse))

class MovieIdQuerySchema(Schema):
    movie_id = fields.String(
        required=True,
        metadata={
            "description": "movie_id",
            "example": "2",
        }
    )
    
def returnUserMovie(UserMovie):
    return {
        "id": UserMovie.id, 
        "user_id": UserMovie.user_id,
        "movie_id": UserMovie.movie_id,
        "score": UserMovie.score,
        "created_at": UserMovie.created_at,
        "updated_at": UserMovie.updated_at    
    }

def returnUserMovies(UserMovies):
    return {
        "users": list(map(returnUserMovie, UserMovies))
    }



class responseUserSchema(Schema):
    errors = fields.Dict(load_default={"message": "movie registered successfully"})
    
class responseUpdateScoreSchema(Schema):
    errors = fields.Dict(load_default={"message": "score updated successfully"})
    
class errorInvalidRequestDataSchema(Schema):
    errors = fields.Dict(load_default={"message": "Invalid request data"})
    
class errorDatabaseErrorSchema(Schema):
    errors = fields.Dict(load_default={"message": "Database error"})
    
class errorMovieAlreadyExistsSchema(Schema):
      errors = fields.Dict(load_default={"message": "movie already exists"})
    
class errorUserNotFoundSchema(Schema):
    errors = fields.Dict(load_default={"message": "User not found"})

class erroInvalidPasswordSchema(Schema):
    errors = fields.Dict(load_default={"message": "Invalid token"})
    
    
class responseUserUpdatePasswordSchema(Schema):
    errors = fields.Dict(load_default={"message": "Password updated successfully"})

    
class responseDelMovieSchema(Schema):
    errors = fields.Dict(load_default={"message": "Movie deleted successfully"})
    
class TokenExpiredSchema(Schema):
    errors = fields.Dict(load_default={"message": "Token expired"})

class movieAlredyExists(Schema):
    errors = fields.Dict(load_default={"message": "Movie already exists"})

    

    


