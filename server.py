from flask import Flask, render_template, request, g, url_for, redirect
from control_functions import Controler

app = Flask(__name__)
control = Controler()
dba = control.create_dba()


@app.route('/', methods=['GET', 'POST'])
def index():
    if(request.method == 'POST'):
        if(request.form['tipo'] == 'dados'):
            if(dba):
                periodo = {'inicio': request.form['inicio'],
                           'fim': request.form['fim']}
                lics = dba.get_licitacoes(request.form['municipio'], periodo)
            else:
                lics = control.read_licitacoes()
            return render_template('index.html', active=1, results=1,
                                   q=request.form, lics=lics)
        elif(request.form['tipo'] == 'avancado'):
            return render_template('index.html', active=2, results=1,
                                   q=request.form)
        else:
            return redirect(url_for('index'))
    else:
        return render_template('index.html', active=1, results=0)


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/consulta-basica', methods=['POST'])
def consulta_basica():
    req = request.form
    return redirect('/dados/{}/{}'.format(req['municipio'], req['entidade']))


@app.route('/dados/', defaults={'municipio': None, 'ente': None})
@app.route('/dados/<municipio>/<ente>')
def dados_abertos(municipio, ente):
    if(not municipio or not ente):
        return redirect(url_for('index'))

    return 'Dados abertos da {} de {}'.format(ente, municipio)


@app.before_request
def before_request():
    g.brand_name = 'Dados Abertos CE'
    if(dba):
        g.municipios = dba.get_municipios()
    else:
        g.municipios = control.read_municipios()


if(__name__ == '__main__'):
    app.run()
