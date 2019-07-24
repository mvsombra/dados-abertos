from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()


class Licitacao(Base):
    __tablename__ = 'licitacoes'
    id = Column('id', Integer, primary_key=True)


class DB:
    def __init__(self):
        self.engine = create_engine(os.environ['DB_URL'])
