from psycopg2 import OperationalError
from database import AcessoBD
from municipio import Municipio
from licitacao import Licitacao
import pandas as pd


class Controler:
    def create_dba(self):
        try:
            return AcessoBD()
        except OperationalError:
            return None
        except KeyError:
            return None

    def _read_csv(self, dir):
        return pd.read_csv(dir)

    def read_municipios(self):
        csv = self._read_csv('static/municipios.csv')
        ids = csv['id']
        nomes = csv['municipio']
        mesos = csv['mesorregiao']
        micros = csv['microregiao']
        municipios = []
        for n in range(184):
            m = Municipio(ids[n], nomes[n], mesos[n], micros[n])
            municipios.append(m)

        return municipios

    def read_licitacoes(self):
        csv = self._read_csv('static/licitacoes.csv')
        ids = csv['id']
        editais = csv['edital']
        municipios = csv['municipio']
        objetos = csv['objeto']
        modalidades = csv['modalidade']
        orgaos = csv['orgao']
        datas = csv['data_abertura']
        status = csv['status']
        licitacoes = []
        for n in range(1):
            lic = Licitacao(ids[n], editais[n], municipios[n], objetos[n],
                            modalidades[n], orgaos[n], datas[n], status[n])
            licitacoes.append(lic)

        return licitacoes
