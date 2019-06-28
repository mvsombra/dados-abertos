import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
from control_functions import Controler


class Lics_Tudo_Transparente:
    def __init__(self):
        control = Controler()
        self.dba = control.create_dba()
        self.anos = [2019, 2018, 2017]
        self.prefeituras = ['eusebio', 'maranguape', 'novaolinda', 'parambu',
                            'pedrabranca', 'salitre']
        self.camaras = ['cmeusebio', 'cmnovaolinda']
        self.ids = {'eusebio': 144, 'maranguape': 193, 'novaolinda': 210,
                    'parambu': 223, 'pedrabranca': 225, 'salitre': 245,
                    'cmeusebio': 144, 'cmnovaolinda': 210}

    def _tratar_data(self, data):
        if(not data):
            return '1970-01-01'
        if('/' in data):
            if(len(data) == 10):
                data = dt.strptime(data, '%d/%m/%Y').strftime('%Y-%m-%d')
            elif(len(data) == 8):
                data = dt.strptime(data, '%d/%m/%y').strftime('%Y-%m-%d')
            else:
                data = '1970-01-01'
        elif('-' in data):
            if(len(data) == 10):
                data = dt.strptime(data, '%d-%m-%Y').strftime('%Y-%m-%d')
            elif(len(data) == 8):
                data = dt.strptime(data, '%d-%m-%y').strftime('%Y-%m-%d')
            else:
                data = '1970-01-01'
        else:
            data = '1970-01-01'

        return data

    def _tratar_texto(self, txt):
        while("'" in txt):
            indice = txt.index("'")
            txt = txt[:indice] + "\\" + txt[indice:]

        while('"' in txt):
            indice = txt.index('"')
            txt = txt[:indice] + "\\" + txt[indice:]

        return txt

    def _tratar_licitacao(self, lic, ente, tipo_ente="Prefeitura"):
        i = self.ids[ente]
        try:
            num = lic.numero.text
        except AttributeError:
            num = None
        if(not num):
            num = '---'
        try:
            data = self._tratar_data(lic.data.text)
        except AttributeError:
            data = None
        if(not data):
            data = '1970-01-01'
        try:
            obj = lic.objeto.text
        except AttributeError:
            obj = None
        if(not obj):
            obj = '---'
        try:
            mod = lic.modalidade.text
        except AttributeError:
            mod = None
        if(not mod):
            mod = '---'
        try:
            tipo = lic.tipo.text
        except AttributeError:
            tipo = None
        if(not tipo):
            tipo = '---'

        return [i, self._tratar_texto(num), self._tratar_texto(obj),
                self._tratar_texto(mod), self._tratar_texto(tipo_ente),
                self._tratar_texto(data), '---']

    def crawl(self):
        base_url = "https://{}.tudotransparente.com.br/api/licitacoes/xml/{}"
        for ano in self.anos:
            for ente in self.prefeituras:
                temp_url = base_url.format(ente, ano)
                page = requests.get(temp_url)
                soup = bs(page.content, 'lxml')
                lics = soup.findAll('licitacoes')
                for lic in lics:
                    if(not lic):
                        break

                    lic = self._tratar_licitacao(lic, ente)
                    self.dba.add_licitacoes(lic)

            for ente in self.camaras:
                temp_url = base_url.format(ente, ano)
                page = requests.get(temp_url)
                soup = bs(page.content, 'lxml')
                lics = soup.findAll('licitacoes')
                for lic in lics:
                    if(not lic):
                        break

                    lic = self._tratar_licitacao(lic, ente, tipo_ente="Câmara")
                    self.dba.add_licitacoes(lic)

        return base_url
