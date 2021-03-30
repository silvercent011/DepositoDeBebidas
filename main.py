from flask import Flask, request
from flask_restful import Resource, Api
import json

#Routes
from routes.users import *

app = Flask(__name__)
api = Api(app)

api.add_resource(Auth, '/auth')

if __name__ == '__main__':
    app.run(debug=True)