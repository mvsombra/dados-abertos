import os
import psycopg2
from municipio import Municipio
from licitacao import Licitacao
from ente import Ente


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

    def get_licitacoes(self, municipio, ente):
        q = "SELECT * FROM licitacoes INNER JOIN municipios AS m ON " \
            "m.id=municipio WHERE nome='{}' AND orgao='{}';"
        q = q.format(municipio, ente)
        list1 = self.bd.read_query(q)
        new = []
        for l in list1:
            lic = Licitacao(l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7])
            new.append(lic)
        return new

    def get_entes(self, ente=''):
        q = "SELECT m.nome, e.nome, dados_abertos, url FROM municipios AS m " \
            "INNER JOIN entes AS e ON m.id=e.municipio WHERE e.nome='{}' " \
            "AND dados_abertos='t' ORDER BY m.nome;".format(ente)
        list1 = self.bd.read_query(q)
        new = []
        for l in list1:
            new.append(Ente(l[0], l[1], l[2], l[3]))

        return new

    def add_licitacoes(self, dados):
        q = "INSERT INTO licitacoes (municipio, edital, objeto, modalidade, " \
            "orgao, data_abertura, status) VALUES ({}, '{}', '{}', '{}', " \
            "'{}', '{}', '{}');".format(dados[0], dados[1], dados[2], dados[3],
                                        dados[4], dados[5], dados[6])
        self.bd.cud_query(q)

    def delete_licitacoes(self):
        self.cud_query("DELETE * FROM licitacoes;")
