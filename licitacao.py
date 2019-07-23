
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Integer, ForeignKey, String, Column, Date
import datetime

Base = declarative_base()


class Licitacao(Base):
    __tablename__ = 'licitacoes'
    id = Column(Integer, primary_key=True)
    edital = Column(String)
    municipio = Column(Integer, ForeignKey('municipios.id'))
    objeto = Column(String)
    modalidade = Column(String)
    entidade = Column(String)
    data_abertura = Column(Date)
    status = Column(String)

    def __init__(self, i, mun, ed, obj, mod, org, dt, sts):
        self.id = i
        self.edital = ed
        self.municipio = mun
        self.objeto = obj
        self.modalidade = mod
        self.entidade = org
        self._dt = str(dt)
        self.status = sts

    def __str__(self):
        return '{} - {}'.format(self.edital, self.objeto)

    @property
    def data_abertura(self):
        if(not self._dt):
            return '---'
        y = datetime.datetime.strptime(self._dt, '%Y-%m-%d')
        return y.strftime('%d/%m/%Y')
