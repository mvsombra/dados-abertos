from flask import Flask, render_template, request, g, url_for, redirect
from control_functions import Controler

app = Flask(__name__)
control = Controler()
dba = control.create_dba()


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
    ente = req['entidade'].lower().replace(' ', '-')
    return redirect('/dados/{}/{}'.format(cidade, ente))


@app.route('/dados/', defaults={'municipio': None, 'ente': None})
@app.route('/dados/<municipio>/<ente>')
def dados_abertos(municipio, ente):
    if(not municipio or not ente):
        return redirect(url_for('index'))

    ente = ente.capitalize().replace('-', ' ')
    temp = ""
    for palavra in municipio.split('-'):
        if(palavra.lower() not in ['do', 'de', 'da']):
            temp += palavra.capitalize() + ' '
        else:
            temp += palavra + ' '
    municipio = temp.strip()
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
