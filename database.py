import os
import psycopg2
from municipio import Municipio
from licitacao import Licitacao


class BancoDados:
    def __init__(self):
        comando = os.environ['DATABASE_URL']
        self.conn = psycopg2.connect(comando, sslmode='require')
        self.cur = self.conn.cursor()

    def run_query(self, q):
        self.cur.execute(q)

    def commit(self):
        self.conn.commit()

    def fetch(self):
        return self.cur.fetchall()

    def cud_query(self, q):
        self.run_query(q)
        self.commit()

    def read_query(self, q):
        self.run_query(q)
        return self.fetch()


class AcessoBD:
    def __init__(self):
        self.bd = BancoDados()

    def get_municipios(self):
        q = "SELECT * FROM municipios ORDER BY nome;"
        list1 = self.bd.read_query(q)
        new = []
        for mun in list1:
            m = Municipio(mun[0], mun[1], mun[2], mun[3])
            new.append(m)
        return new

    def get_licitacoes(self):
        q = "SELECT * FROM licitacoes;"
        list1 = self.bd.read_query(q)
        new = []
        for l in list1:
            lic = Licitacao(l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7])
            new.append(lic)
        return new
