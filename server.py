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
                lics = dba.get_licitacoes()
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


@app.before_request
def before_request():
    if(dba):
        g.municipios = dba.get_municipios()
    else:
        g.municipios = control.read_municipios()


if(__name__ == '__main__'):
    app.run()
