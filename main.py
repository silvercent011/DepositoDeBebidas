from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

from Forms.NovoProdutoForm import NovoProduto

from utils.db import *
import json

with open('./env.json','r') as env:
    DB_INFO = json.loads(env.read())


app = Flask(__name__)
app.secret_key = 'XABLAU'
db = SQLAlchemy(app)

@app.route('/produtos', methods=['GET', 'POST'])
def produtos():
    db = Database(DB_INFO)
    info = db.select_rows('SELECT * FROM produtos')
    return render_template('produtos.html', produtos=info)

@app.route('/produtos/cadastrar', methods=['GET', 'POST'])
def cadastro_produtos():
    tipos = [(0,'ALCOOLICA'),(1,'NAO ALCOOLICA')]
    form = NovoProduto(request.form)
    form.tipo.choices = tipos
    db = Database(DB_INFO)
    if request.method == 'POST':
        data = request.form
    return render_template('cadastro_produtos.html', form=form)

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
    fornecedores_dict = {}

    for i in range(len(info)):
        fornecedores_dict[info[i][0]] = {'cnpj': info[i][0], 'nome': info[i][1], 'adicionado_em': info[i][2]}
    return render_template('fornecedores.html', fornecedores=fornecedores_dict)

@app.route('/funcionarios', methods=['GET', 'POST'])
def funcionarios():
    db = Database(DB_INFO)
    info = db.select_rows('SELECT * FROM funcionarios')
    funcionarios_dict = {}

    for i in range(len(info)):
        funcionarios_dict[info[i][0]] = {'cpf': info[i][0], 'nome': info[i][1], 'adicionado_em': info[i][2]}
        if info[i][4]:
            gerente_nome = db.select_rows(f'SELECT nome FROM funcionarios WHERE cpf=\'{info[i][4]}\'')[0][0]
            funcionarios_dict[info[i][0]]['gerente'] = f'{info[i][4]} - {gerente_nome}'

    return render_template('funcionarios.html', funcionarios=funcionarios_dict)

@app.route('/pedidos/fornecedores', methods=['GET', 'POST'])
def pedido_fornecedores():
    db = Database(DB_INFO)
    info = db.select_rows('SELECT * FROM pedido_fornecedor')
    return render_template('pedido.html', pedidos=info)

@app.route('/pedidos/clientes', methods=['GET', 'POST'])
def pedido_cliente():
    db = Database(DB_INFO)
    info = db.select_rows('SELECT * FROM pedido_cliente')
    return render_template('pedido.html', pedidos=info)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)
