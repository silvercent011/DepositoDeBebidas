from flask_wtf import Form
from wtforms import TextField, SubmitField, SelectField
from wtforms.validators import * 

class NovoProduto(Form):
    id = TextField('Cód de Barras', validators=[DataRequired()])
    nome = TextField('Nome', validators=[DataRequired()])
    valor_venda = TextField('Valor de Venda', validators=[DataRequired()])
    valor_compra = TextField('Valor de Compra', validators=[DataRequired()])
    quantidade_estoque = TextField('Estoque', validators=[DataRequired()])
    tipo = SelectField('Tipo do produto', choices=[],coerce=int, validators=[DataRequired()])
    cadastrar = SubmitField("Cadastrar Produto")