from psycopg2 import OperationalError
from database import AcessoBD
from municipio import Municipio
import pandas as pd


class Controler:
    def create_dba(self):
        try:
            return AcessoBD()
        except OperationalError:
            return None
        except KeyError:
            return None

    def read_municipios(self):
        municipios = []
        ids = pd.read_csv('static/municipios.csv')['id']
        nomes = pd.read_csv('static/municipios.csv')['municipio']
        mesos = pd.read_csv('static/municipios.csv')['mesorregiao']
        micros = pd.read_csv('static/municipios.csv')['microregiao']
        for n in range(184):
            m = Municipio(ids[n], nomes[n], mesos[n], micros[n])
            municipios.append(m)

        return municipios
