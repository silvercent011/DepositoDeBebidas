from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

from Forms.NovoProdutoForm import NovoProduto
from Forms.NovaVenda import NovaVenda
from Forms.NovoFuncionario import NovoFuncionario
from Forms.NovoFornecedor import NovoFornecedor

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

@app.route('/vender', methods=['GET', 'POST'])
def nova_venda():
    form = NovaVenda(request.form)
    db = Database(DB_INFO)
    if request.method == 'POST':
        data = request.form
    return render_template('nova_venda.html', form=form)

@app.route('/produtos/cadastrar', methods=['GET', 'POST'])
def cadastro_produtos():
    tipos = [(0,'ALCOOLICA'),(1,'NAO ALCOOLICA'), (2, 'DIET')]
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

@app.route('/fornecedores/<cnpj>', methods=['GET', 'POST'])
def fornecedor(cnpj):
    db = Database(DB_INFO)
    info = db.select_rows(f'SELECT * FROM fornecedores WHERE cnpj=\'{cnpj}\'')

    telefones = db.select_rows(f'SELECT numero FROM telefones WHERE cnpj=\'{cnpj}\'')
    enderecos = db.select_rows(f'SELECT * FROM enderecos WHERE cnpj=\'{cnpj}\'')

    pedidos_fornecedores = db.select_rows(f'SELECT pedido_id, total_pedido_fornecedor(pedido_id) FROM pedido_fornecedor WHERE fornecedor_cnpj=\'{cnpj}\'')

    return render_template('fornecedor.html', fornecedor=info, telefones=telefones,
    enderecos=enderecos, pedidos_fornecedores=pedidos_fornecedores)

@app.route('/fornecedores/cadastrar', methods=['GET', 'POST'])
def novo_fornecedor():
    form = NovoFornecedor(request.form)
    db = Database(DB_INFO)
    if request.method == 'POST':
        data = request.form
    return render_template('cadastro_fornecedor.html', form=form)

@app.route('/funcionarios/cadastrar', methods=['GET', 'POST'])
def novo_funcionario():
    form = NovoFuncionario(request.form)
    db = Database(DB_INFO)
    if request.method == 'POST':
        data = request.form
    return render_template('cadastro_funcionario.html', form=form)

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

@app.route('/funcionarios/<cpf>', methods=['GET', 'POST'])
def funcionario(cpf):
    db = Database(DB_INFO)
    funcionario_info = db.select_rows(f'SELECT * FROM funcionarios WHERE cpf=\'{cpf}\'')
    endereco = db.select_rows(f'SELECT * FROM enderecos WHERE cpf=\'{cpf}\'')
    telefones = db.select_rows(f'SELECT numero FROM telefones WHERE cpf=\'{cpf}\'')
    if funcionario_info[0][4]:
        gerente = db.select_rows(f'SELECT cpf, nome FROM funcionarios WHERE cpf=\'{funcionario_info[0][4]}\'')
        gerenciados = None
    else:
        gerente = None
        gerenciados = db.select_rows(f'SELECT cpf, nome FROM funcionarios WHERE gerente_cpf=\'{cpf}\'')

    pedidos_clientes = db.select_rows(f'SELECT pedido_id, total_pedido_cliente(pedido_id) FROM pedido_cliente WHERE funcionario_cpf=\'{cpf}\'')
    pedidos_fornecedores = db.select_rows(f'SELECT pedido_id, total_pedido_fornecedor(pedido_id) FROM pedido_fornecedor WHERE funcionario_cpf=\'{cpf}\'')

    return render_template('funcionario.html', dados=funcionario_info, cpf=cpf,
    endereco=endereco, telefones=telefones, gerente=gerente, gerenciados=gerenciados,
    pedidos_clientes=pedidos_clientes, pedidos_fornecedores=pedidos_fornecedores)


@app.route('/pedidos/fornecedores', methods=['GET', 'POST'])
def pedido_fornecedores():
    db = Database(DB_INFO)
    info = db.select_rows('SELECT * FROM pedido_fornecedor')
    return render_template('pedidos_fornecedores.html', pedidos=info)

@app.route('/pedidos/fornecedores/<id>', methods=['GET', 'POST'])
def pedido_fornecedor(id):
    db = Database(DB_INFO)
    info = db.select_rows(f'SELECT * FROM pedido_fornecedor WHERE pedido_id={id}')
    pedido_produto = db.select_rows(
        f'SELECT pr.nome, pp.quantidade, pr.valor_compra, pp.quantidade*(pr.valor_compra) AS TOTAL '
        'FROM produto_pedidos pp '
        'JOIN produtos pr ' 
        f'ON pr.id=pp.produto_id WHERE pp.pedido_fornecedor_id={id};'
    )
    funcionario = db.select_rows(f'SELECT nome FROM funcionarios WHERE cpf=\'{info[0][2]}\'')[0][0]
    total = db.select_rows(f'SELECT total_pedido_fornecedor({id});')[0][0]
    return render_template('pedido_fornecedor.html', info=info, pedido_produto=pedido_produto, total=total, funcionario=funcionario)

@app.route('/pedidos/clientes', methods=['GET', 'POST'])
def pedido_cliente():
    db = Database(DB_INFO)
    info = db.select_rows('SELECT * FROM pedido_cliente')
    return render_template('pedido.html', pedidos=info)

@app.route('/pedidos/clientes/<id>', methods=['GET', 'POST'])
def pedido_cliente_id(id):
    db = Database(DB_INFO)
    info = db.select_rows(f'SELECT * FROM pedido_cliente WHERE pedido_id={id}')
    pedido_produto = db.select_rows(
        f'SELECT pr.nome, pp.quantidade, pr.valor_venda, pp.quantidade*(pr.valor_venda) AS TOTAL '
        'FROM produto_pedidos pp '
        'JOIN produtos pr ' 
        f'ON pr.id=pp.produto_id WHERE pp.pedido_cliente_id={id};'
    )
    funcionario = db.select_rows(f'SELECT nome FROM funcionarios WHERE cpf=\'{info[0][2]}\'')[0][0]
    total = db.select_rows(f'SELECT total_pedido_cliente({id})')[0][0]
    return render_template('pedido_cliente.html', info=info, total=total,
    pedido_produto=pedido_produto, funcionario=funcionario)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
