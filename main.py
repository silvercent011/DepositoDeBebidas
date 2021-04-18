from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
# from env import DB_INFO

from utils.db import *
import json

with open('./env.json','r') as env:
    DB_INFO = json.loads(env.read())


app = Flask(__name__)
db = SQLAlchemy(app)

@app.route('/produtos', methods=['GET', 'POST'])
def produtos():
    db = Database(DB_INFO)
    info = db.select_rows('SELECT * FROM produtos')
    return render_template('produtos.html', produtos=info)

@app.route('/produtos/alcoolicos', methods=['GET', 'POST'])
def produtos_alcoolicos():
    db = Database(DB_INFO)
    info = db.select_rows('SELECT * FROM bebida_alcoolica')
    return render_template('produtos.html', produtos=info)

@app.route('/produtos/nao-alcoolicos', methods=['GET', 'POST'])
def produtos_nao_alcoolicos():
    db = Database(DB_INFO)
    info = db.select_rows('SELECT * FROM bebida_nao_alcoolica')
    return render_template('produtos.html', produtos=info)

@app.route('/fornecedores', methods=['GET', 'POST'])
def fornecedores():
    db = Database(DB_INFO)
    info = db.select_rows('SELECT * FROM fornecedores')
    return render_template('fornecedores.html', fornecedores=info)

@app.route('/funcionarios', methods=['GET', 'POST'])
def funcionarios():
    db = Database(DB_INFO)
    info = db.select_rows('SELECT * FROM funcionarios')
    return render_template('funcionarios.html', funcionarios=info)

@app.route('/pedidos/fornecedores', methods=['GET', 'POST'])
def pedido_fornecedores():
    db = Database(DB_INFO)
    info = db.select_rows('SELECT * FROM pedido_fornecedor')
    return render_template('fornecedores.html', funcionarios=info)

@app.route('/pedidos/clientes', methods=['GET', 'POST'])
def pedido_cliente():
    db = Database(DB_INFO)
    info = db.select_rows('SELECT * FROM pedido_cliente')
    return render_template('fornecedores.html', funcionarios=info)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)
