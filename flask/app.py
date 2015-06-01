from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello'

@app.route('/kittens')
def kittens():
    name = "you"
    return render_template('kittens.html', name=name)

@app.route('/kittens/<name>')
def kittens_name(name):
    return render_template('kittens.html', name=name )


@app.route('/hello')
def hello():
    return 'Hello, you.'


@app.route('/hello/<name>')
def hello_name(name):
    return 'Hello, {}.'.format(name)

@app.route('/count')
def count():
    numbers = range(1,101)   # the range(n) function generates a list:
                         # [1, 2, .. n]
    return render_template('counter.html', numbers=numbers)

if __name__=='__main__':
    app.run(debug=True)
