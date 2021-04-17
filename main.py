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

@app.route('/fornecedores', methods=['GET', 'POST'])
def fornecedores():
    db = Database(DB_INFO)
    info = db.select_rows('SELECT * FROM fornecedores')
    return render_template('fornecedores.html', fornecedores=info)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)
