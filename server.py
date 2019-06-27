from flask import Flask, render_template, request, g, url_for, redirect
from unicodedata import normalize as normal
from control_functions import Controler
import requests
from datetime import datetime
from bs4 import BeautifulSoup as bs

app = Flask(__name__)
control = Controler()
dba = control.create_dba()


@app.route('/teste')
def teste():
    base_url = "https://eusebio.tudotransparente.com.br/api/licitacoes/xml/{}"
    # return redirect(url_for('index'))
    # bd = dba.bd
    # q = "SELECT municipio, edital, objeto, modalidade, " \
    #    "orgao, data_abertura, status FROM licitacoes;"

    for ano in ['2019', '2018']:
        temp_url = base_url.format(ano)
        page = requests.get(temp_url)
        soup = bs(page.content, 'lxml')
        lics = soup.findAll('licitacoes')
        for lic in lics:
            data = lic.data.text
            if('/' in data):
                if(len(data) == 10):
                    data = datetime.strptime(data, '%d/%m/%Y')
                    data = data.strftime('%Y-%m-%d')
                elif(len(data) == 8):
                    data = datetime.strptime(data, '%d/%m/%y')
                    data = data.strftime('%Y-%m-%d')
            elif('-' in data):
                if(len(data) == 10):
                    data = datetime.strptime(data, '%d-%m-%Y')
                    data = data.strftime('%Y-%m-%d')
                elif(len(data) == 8):
                    data = datetime.strptime(data, '%d-%m-%y')
                    data = data.strftime('%Y-%m-%d')
            lic = [144, lic.numero.text, lic.objeto.text, lic.modalidade.text,
                   'Prefeitura', data, None]
            dba.add_licitacoes(lic)

    return redirect('/dados/eusebio/prefeitura')


@app.route('/', methods=['GET', 'POST'])
def index():
    cams = dba.get_entes(ente='Câmara')
    prefs = dba.get_entes(ente='Prefeitura')
    return render_template('index.html', cams=cams, prefs=prefs)


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/consulta-basica', methods=['POST'])
def consulta_basica():
    req = request.form
    cidade = req['municipio'].lower().replace(' ', '-')
    cidade = None
    for municipio in g.municipios:
        if(str(municipio) == req['municipio']):
            cidade = municipio.nome_tratado
            break
    ente = req['entidade'].lower()
    ente = normal('NFKD', ente).encode('ASCII', 'ignore').decode('ASCII')
    return redirect('/dados/{}/{}'.format(cidade, ente))


@app.route('/dados/', defaults={'cidade': None, 'ente': None})
@app.route('/dados/<cidade>/<ente>')
def dados_abertos(cidade, ente):
    temp = None
    for municipio in g.municipios:
        if(municipio.nome_tratado == cidade):
            temp = municipio
            break

    cidade = temp

    if(ente in ['camara', 'prefeitura']):
        temp = {'camara': 'Câmara', 'prefeitura': 'Prefeitura'}
        ente = temp[ente]
    else:
        ente = None

    if(not cidade or not ente):
        return redirect(url_for('index'))

    if(dba):
        lics = dba.get_licitacoes(municipio, ente)
    else:
        lics = control.read_licitacoes()
    return render_template('dados-entidades.html', ente=ente,
                           municipio=municipio, lics=lics)


@app.before_request
def before_request():
    g.brand_name = 'Dados Abertos CE'
    if(dba):
        g.municipios = dba.get_municipios()
    else:
        g.municipios = control.read_municipios()


if(__name__ == '__main__'):
    app.run()
