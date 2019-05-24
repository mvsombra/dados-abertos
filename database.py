import os
import psycopg2


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
        q = "SELECT nome from municipios ORDER BY nome;"
        return self.bd.read_query(q)
