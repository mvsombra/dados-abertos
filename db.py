from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()


class Licitacao(Base):
    __tablename__ = 'licitacoes'
    id = Column(Integer, primary_key=True)
    edital = Column(String)
    municipio = Column(Integer, ForeignKey('municipios.id'))
    objeto = Column(String)
    modalidade = Column(String)
    orgao = Column(String)
    data_abertura = Column(Date)
    status = Column(String)


class DB:
    def __init__(self):
        self.engine = create_engine(os.environ['DB_URL'])
        self.Session = sessionmaker(bind=self.engine)

    def get_licitacoes(self):
        session = self.Session()
        lics = session.query(Licitacao).all()
        session.close()
        return lics
