from flask import Flask, render_template, request, g, url_for, redirect
from unicodedata import normalize as normal
from control_functions import Controler

app = Flask(__name__)
control = Controler()
dba = control.create_dba()


@app.route('/teste')
def teste():
    bd = dba.bd
    for municipio in g.municipios:
        q = "insert into entes (municipio, nome) values ({}, 'Prefeitura');"
        q = q.format(municipio.id)
        bd.cud_query(q)

    for municipio in g.municipios:
        q = "insert into entes (municipio, nome) values ({}, 'Câmara');"
        q = q.format(municipio.id)
        bd.cud_query(q)
    temp = bd.read_query('select * from entes;')
    return str(temp)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


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
    for municipio in g.municipios:
        if(municipio.nome_tratado == cidade):
            cidade = municipio
            break

    if(ente in ['camara', 'prefeitura']):
        temp = {'camara': 'Câmara', 'prefeitura': 'Prefeitura'}
        ente = temp[ente]
    else:
        ente = None
    if(not cidade or not ente):
        return redirect(url_for('index'))

    if(dba):
        lics = dba.get_licitacoes(municipio)
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
