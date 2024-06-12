from flask import Flask , request, jsonify
from  modules.data_manager  import ENGINE, Users



app = Flask(__name__)

conn = ENGINE.get_connection()
_ = Users(conn)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/database', methods=['GET'])
def getValue():

     # Utilizar jsonify é uma boa prática, pois torna explícito que estou retornando um objeto JSON.
     return _.addData()

@app.route('/addvalue', methods=['POST'])
def addValue():
        # Verifica se a solicitação POST contém dados JSON
        if  request.is_json == False:
            ENGINE.release_connection(conn)
            return jsonify({'error': 'Solicitação deve conter dados JSON!'}), 400
        # Recebe os dados JSON do corpo da solicitação
        data = request.json
        print(data)
        # Verifica se a chave e o valor estão presentes nos dados recebidos
        index = 1
        for item in data:
            print('porraaa',item)
            minhaChave = item['key'] + str(index)  # Usando uma chave única para cada valor
            meuValor = item['value']
            password = 'batata'
            if 'key' not in item and 'value' not in item:
                ENGINE.release_connection(conn)
                return jsonify({'error': 'Chave e/ou valor ausentes nos dados enviados!'}), 400    
        # Adiciona a chave e o valor ao dicionário
    
        print(minhaChave)
        print(meuValor)
        _.addData(minhaChave, meuValor, password)
                            
        index += 1

                                
                   
                                
                        


@app.route('/deletevalue/<chave>', methods=['DELETE'])
def deleteValue(chave):
    if chave in dataBase:
        del dataBase[chave]
        return jsonify({'message': f'Valor com chave {chave} deletado com sucesso!'}), 200
    else:
        return jsonify({'error': 'Chave não encontrada no dicionário!'}), 404

@app.route('/updatevalue/<chave>', methods=['PATCH'])
def updateValue(chave):
    """
    Update the value associated with the given key in the database.

    Parameters:
        chave (str): The key whose value needs to be updated.   

    Returns:
        JSON: A JSON response indicating the status of the operation.
            If successful, returns a success message with HTTP status code 200.
            If the key is not found, returns an error message with HTTP status code 404.
            If the request body does not contain the 'value' field, returns an error message with HTTP status code 400.
    """
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
