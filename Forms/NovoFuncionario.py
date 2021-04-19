from flask_wtf import Form
from wtforms import TextField, SubmitField, SelectField
from wtforms.validators import * 

class NovoFuncionario(Form):
    cpf = TextField('CPF', validators=[DataRequired()])
    nome = TextField('Nome', validators=[DataRequired()])
    senha = TextField('Senha', validators=[DataRequired()])
    gerente_cpf = TextField('Gerente CPF', validators=[DataRequired()])
    cadastrar = SubmitField("Cadastrar Produto")