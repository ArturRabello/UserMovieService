import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

"""
    criação da conecção com o banco de dados.
"""

# url do banco 
DataBase_Url = os.getenv("DATABASE_URL")

# criação do engine
engine = create_engine(DataBase_Url)
# criação da sessão
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# criação da base
Base = declarative_base()
