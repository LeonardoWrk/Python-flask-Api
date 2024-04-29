from flask import Flask , request, jsonify
from  modules.data_manager  import ENGINE, Users


app = Flask(__name__)

conn = ENGINE.get_connection()
_ = Users(conn)
ENGINE.release_connection(conn)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/database', methods=['GET'])
def getValue():
     # Utilizar jsonify é uma boa prática, pois torna explícito que estou retornando um objeto JSON.
     return jsonify(dataBase)

@app.route('/addvalue', methods=['POST'])
def addValue():
    conn = ENGINE.get_connection()
    UserInterface = Users(conn)
    # Verifica se a solicitação POST contém dados JSON
    if request.is_json:
        # Recebe os dados JSON do corpo da solicitação
        data = request.json
        print(data)
        # Verifica se a chave e o valor estão presentes nos dados recebidos
        index = 1
        for item in data:
            if 'key' in item and 'value' in item:
                # Adiciona a chave e o valor ao dicionário
                minhaChave = item['key'] + str(index)  # Usando uma chave única para cada valor
                meuValor = item['value']
                print(minhaChave)
                print(meuValor)
                dataBase[minhaChave] = meuValor
                index += 1
                print('teste', dataBase)
                print('teste', dataBase)
                print('teste', dataBase) 
                print('teste', dataBase)
            else: 
                ENGINE.release_connection(conn)
                return jsonify({'error': 'Chave e/ou valor ausentes nos dados enviados!'}), 400
        ENGINE.release_connection(conn)
        return jsonify({'message': 'Valores adicionados com sucesso ao dicionário!'}), 200
    else:
        ENGINE.release_connection(conn)
        return jsonify({'error': 'Solicitação deve conter dados JSON!'}), 400

@app.route('/deletevalue/<chave>', methods=['DELETE'])
def deleteValue(chave):
    if chave in dataBase:
        del dataBase[chave]
        return jsonify({'message': f'Valor com chave {chave} deletado com sucesso!'}), 200
    else:
        return jsonify({'error': 'Chave não encontrada no dicionário!'}), 404

@app.route('/updatevalue/<chave>', methods=['PATCH'])
def updateValue(chave):
    if chave in dataBase:
        # Recebe os dados JSON do corpo da solicitação
        data = request.json
        if 'value' in data:
            # Atualiza o valor da chave com o novo valor fornecido
            dataBase[chave] = data['value']
            return jsonify({'message': f'Valor com chave {chave} atualizado com sucesso!'}), 200
        else:
            return jsonify({'error': 'O campo "value" é obrigatório nos dados enviados!'}), 400
    else:
        return jsonify({'error': 'Chave não encontrada no dicionário!'}), 404
