from flask_wtf import Form
from wtforms import TextField, SubmitField, SelectField
from wtforms.validators import * 

class NovaVenda(Form):
    id = TextField('ID venda', validators=[DataRequired()])
    data_pedido = TextField('Pedido', validators=[DataRequired()])
    funcionario_cpf = TextField('CPF Funcionário', validators=[DataRequired()])
    id_produto_pedido = TextField('Produtos', validators=[DataRequired()])