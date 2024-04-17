from flask import Flask
from database import dataBase

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/datbase', methods=['GET'])
def getValue():

    teste = dataBase['chave1']
    print('vem algo',teste)
    return teste

@app.route('/addvalue', methods=['POST'])
def addValue():
