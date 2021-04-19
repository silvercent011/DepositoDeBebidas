from flask_wtf import Form
from wtforms import TextField, SubmitField, SelectField
from wtforms.validators import * 

class NovoFornecedor(Form):
    cnpj = TextField('CNPJ', validators=[DataRequired()])
    nome = TextField('Nome', validators=[DataRequired()])
    cadastrar = SubmitField("Cadastrar Produto")