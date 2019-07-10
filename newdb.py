import sqlalchemy as sql
import os


class Database:
    def __init__(self):
        self.engine = sql.create_engine(os.environ['DB_URL'])
        self.conn = self.engine.connect()
        self.metadata = sql.MetaData()

    def select_municipios(self):
        q = sql.select([self.municipios])
        pre_result = self.conn.execute(q)
        return pre_result.fetchall()

    def select_lics(self):
        lics = sql.Table('licitacoes', self.metadata, autoload=True,
                         autoload_with=self.engine).columns
        muns = sql.Table('municipios', self.metadata, autoload=True,
                         autoload_with=self.engine).columns
        q = sql.select([lics.id, lics.municipio, lics.edital, lics.objeto,
                        lics.modalidade, lics.orgao, lics.data_abertura,
                        muns.id])
        pre_result = self.conn.execute(q)
        return pre_result.fetchall()[:3]
