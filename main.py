from flask import Flask , request, jsonify
from  modules.data_manager  import ENGINE, Users

app = Flask(__name__)

conn = ENGINE.get_connection()
_ = Users(conn)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/database', methods=['GET'])
def get_Value():
     # Utilizar jsonify é uma boa prática, pois torna explícito que estou retornando um objeto JSON.
     data = _.getd_data()

     return data

@app.route('/addvalue', methods=['POST'])
def add_value():
    conn = ENGINE.get_connection()
    # Verifica se a solicitação POST contém dados JSON
    if not request.is_json:
        ENGINE.release_connection(conn)
        return jsonify({'error': 'Solicitação deve conter dados JSON!'}), 400

    # Recebe os dados JSON do corpo da solicitação
    data = request.json

    # Verifica se a chave e o valor estão presentes nos dados recebidos
    for item in data:
        if 'key' not in item or 'value' not in item or 'password' not in item:
            ENGINE.release_connection(conn)
            return jsonify({'error': 'Chave e/ou valor ausentes nos dados enviados!'}), 400
    # ultimo item salvo no for anterior pode ser usado novamente: by letal
    # [0: - 1] slice de lista descontando o ultimo item
    for item in data:
        if _.verify_if_exist(item['value']):
            ENGINE.release_connection(conn)
            return jsonify({'error': 'Valor ja existe!'}), 400
        
        minhaChave = item['key']  # Usando uma chave única para cada valor
        meuValor = item['value']
        password = item['password']

        # Adiciona a chave e o valor ao dicionário
        _.add_data(minhaChave, meuValor, password)

    ENGINE.release_connection(conn)
    return jsonify({'message': 'Valores adicionados com sucesso ao dicionário!'}), 200

@app.route('/deletevalue/<chave>', methods=['DELETE'])
def delete_Value(chave):
    if _.verify_if_exist(chave) is False:
        return jsonify({'error': 'Chave não encontrada no dicionário!'}), 404
        
    _.delete_data(chave)
    ENGINE.release_connection(conn)
    return jsonify({'message': f'Valor com chave {chave} deletado com sucesso!'}), 200   

@app.route('/updatevalue', methods=['PATCH'])
def update_Value():
    data = request.json
     
    for item in data:
        if 'current_email' not in item:
            ENGINE.release_connection(conn)
            return jsonify({'error': 'Chave e/ou valor ausentes nos dados enviados!'}), 400
        
    for item in data:
        if _.verify_if_exist(item['current_email']):
            emailatual = item['current_email']  # Define emailatual within the if block
            name = item['nome']
            email = item['email']
            password = item['password']   
            
            _.update_data(emailatual, name, email, password)

    ENGINE.release_connection(conn)
    return jsonify({'message': 'atualizado!'}), 200

