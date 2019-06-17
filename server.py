from flask import Flask, render_template, request, g, url_for, redirect
from unicodedata import normalize as normal
from control_functions import Controler

app = Flask(__name__)
control = Controler()
dba = control.create_dba()


@app.route('/teste')
def teste():
    # return redirect(url_for('index'))
    bd = dba.bd
    tops = ['Acarape', 'Caucaia', 'Crateús', 'Eusébio', 'Fortaleza', 'Sobral',
            'Maranguape', 'Nova Olinda', 'Parambu', 'Pedra Branca', 'Tururu'
            'Pentecoste', 'Pereiro', 'Potengi', 'Quiterianópolis', 'Salitre']
    for municipio in g.municipios:
        if str(municipio) in tops:
            q = "UPDATE entes SET dados_abertos='t' WHERE municipio={} AND " \
                "nome='Prefeitura';".format(municipio.id)
            bd.cud_query(q)

    tops = ['Barro', 'Canindé', 'Carnaubal', 'Crateús', 'Eusébio',
            'Frecheirinha', 'Ibicuitinga', 'Itapiúna', 'Lavras da Mangabeira',
            'Maranguape', 'Nova Olinda', 'Palmácia', 'Quixelô', 'Salitre',
            'Sobral', 'Tabuleiro do Norte', 'Tururu']
    for municipio in g.municipios:
        if str(municipio) in tops:
            q = "UPDATE entes SET dados_abertos='t' WHERE municipio={} AND " \
                "nome='Câmara';".format(municipio.id)
            bd.cud_query(q)

    q = "SELECT m.nome, e.nome, dados_abertos, url FROM municipios AS m " \
        "INNER JOIN entes AS e ON m.id=e.municipio WHERE dados_abertos='t';"
    temp = bd.read_query(q)
    return str(temp)


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
