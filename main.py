from flask import Flask , request, jsonify
from database import dataBase

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/database', methods=['GET'])
def getValue():
     # Utilizar jsonify é uma boa prática, pois torna explícito que estou retornando um objeto JSON.
     return jsonify(dataBase)
    

@app.route('/addvalue', methods=['POST'])
def addValue():
    # Verifica se a solicitação POST contém dados JSON
    if request.is_json:
        # Recebe os dados JSON do corpo da solicitação
        data = request.json
        print(data)
        # Verifica se a chave e o valor estão presentes nos dados recebidos
        if 'key' in data and 'value' in data:
            # Adiciona a chave e o valor ao dicionário
            minhaChave = data['key']
            meuValor = data['value']
            print(minhaChave)
            print(meuValor)
            dataBase[minhaChave] = meuValor
            print('teste',dataBase)
            return jsonify({'message': 'Valor adicionado com sucesso ao dicionário!'})
        else:
            return jsonify({'error': 'Chave e/ou valor ausentes nos dados enviados!'}), 400
    else:
        return jsonify({'error': 'Solicitação deve conter dados JSON!'}), 400