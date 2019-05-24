from psycopg2 import OperationalError
from database import AcessoBD


class Controler:
    def create_dba(self):
        try:
            return AcessoBD()
        except OperationalError:
            return None
