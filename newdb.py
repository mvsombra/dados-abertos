from sqlalchemy import (create_engine, MetaData, Table, select)
import os


class Database:
    def __init__(self):
        self.engine = create_engine(os.environ['DB_URL'])
        self.conn = self.engine.connect()
        self.metadata = MetaData()

    def select_municipios(self, dados=None):
        # Tabela utilizada
        muns = Table('municipios', self.metadata, autoload=True,
                     autoload_with=self.engine)
        if(dados not in ['Prefeitura', 'Câmara']):
            dados = None
        # query
        if(dados):
            lics = Table('licitacoes', self.metadata, autoload=True,
                         autoload_with=self.engine)
            muns = muns.columns
            q = select([muns.nome, muns.url])
            print(q)
            print(type(q))
            q = q.join(lics, muns.id == lics.columns.municipio)
            print(type(q))
            print(q)
            q = q.filter(lics.orgao == dados)
            print(type(q))
            print(q)
            q = q.group_by(muns.nome, muns.url)
            print(type(q))
            q = q.order_by(muns.nome)
            print(type(q))
        else:
            q = select([muns])
        # executa a query
        return self.conn.execute(q).fetchall()

    def select_lics(self):
        # Tabelas utilizadas
        lics = Table('licitacoes', self.metadata, autoload=True,
                     autoload_with=self.engine).columns
        muns = Table('municipios', self.metadata, autoload=True,
                     autoload_with=self.engine).columns
        # query
        q = select([lics.id, lics.municipio, lics.edital, lics.objeto,
                    lics.modalidade, lics.orgao, lics.data_abertura,
                    muns.id])
        # executa a query
        r = self.conn.execute(q).fetchall()
        for i in r:
            print(i)
