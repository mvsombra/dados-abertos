from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if(request.method == 'POST'):
        r = True
    else:
        r = False
    return render_template('index.html', active=1, results=r)


if(__name__ == '__main__'):
    app.run()
