from flask import Flask, request, render_template
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
# from env import DB_INFO
import json

with open('./env.json','r') as env:
    DB_INFO = json.loads(env.read())

#Routes
from routes.users import *

app = Flask(__name__)
api = Api(app)

engine = create_engine(f"postgresql+psycopg2://{DB_INFO['username']}:{DB_INFO['password']}@{DB_INFO['host']}:{DB_INFO['port']}/{DB_INFO['database']}")

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
db_session.execute("SELECT * FROM funcionarios")
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class Funcionarios(Resource):
    def get(self):
        funcionarios = [funcionario for funcionario in db_session.execute("SELECT * FROM funcionarios")]
        return {'funcionarios': funcionarios}
@app.route('/funcionarios')
def funcionarios():
    funcionarios = Funcionarios().get()
    return render_template('funcionarios.html', funcionarios=funcionarios['funcionarios'])

# api.add_resource(Auth, '/auth')
# api.add_resource(HelloWorld, '/')
# api.add_resource(Funcionarios, '/funcionarios')

if __name__ == '__main__':
    app.run(debug=True)