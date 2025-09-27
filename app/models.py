from datetime import datetime
from typing import Union
from database import Base
from sqlalchemy import Column, Date, Integer,Date, Float, String

"""
    Modelo UserMovies
    ela armazena o id do filme, o id do usuario e o score
    
 """
class UserMovies(Base):
    __tablename__ = 'userMovies'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    movie_id = Column(String)
    score = Column(Integer)
    created_at = Column(Date, default=datetime.now())
    updated_at = Column(Date, default=datetime.now())
    
    def __init__(self, user_id, movie_id, score):
        self.user_id = user_id
        self.movie_id = movie_id
        self.score = score

    
    
    
        

