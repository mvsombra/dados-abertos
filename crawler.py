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
            return '---'
        if('/' in data):
            if(len(data) == 10):
                data = dt.strptime(data, '%d/%m/%Y').strftime('%Y-%m-%d')
            elif(len(data) == 8):
                data = dt.strptime(data, '%d/%m/%y').strftime('%Y-%m-%d')
            else:
                data = '---'
        elif('-' in data):
            if(len(data) == 10):
                data = dt.strptime(data, '%d-%m-%Y').strftime('%Y-%m-%d')
            elif(len(data) == 8):
                data = dt.strptime(data, '%d-%m-%y').strftime('%Y-%m-%d')
            else:
                data = '---'
        else:
            data = '---'

        return data

    def _tratar_licitacao(self, lic, ente="Prefeitura"):
        i = self.ids[ente]
        num = lic.numero.text
        if(not num):
            num = '---'
        data = self._tratar_data(lic.data.content)
        obj = lic.objeto.text
        if(not obj):
            obj = '---'
        mod = lic.modalidade.text
        if(not mod):
            mod = '---'
        tipo = lic.tipo.text
        if(not tipo):
            tipo = '---'

        return [i, num, obj, mod, ente, data, '---']

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

                    lic = self._tratar_licitacao(lic)
                    self.dba.add_licitacoes(lic)

            for ente in self.camaras:
                temp_url = base_url.format(ente, ano)
                page = requests.get(temp_url)
                soup = bs(page.content, 'lxml')
                lics = soup.findAll('licitacoes')
                for lic in lics:
                    if(not lic):
                        break

                    lic = self._tratar_licitacao(lic, ente="Câmara")
                    self.dba.add_licitacoes(lic)

        return base_url
