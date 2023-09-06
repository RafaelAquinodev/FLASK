from flask import Flask, jsonify, request #jsonify função que retorna um objeto response./request -> solicitação http


from flask_mysqldb import MySQL


from config import config


app = Flask(__name__)


conexion=MySQL(app)


@app.route('/jogador', methods=['GET'])
def listar_jogadores():
    try:
        cursor = conexion.connection.cursor()
        sql="SELECT id, nome, clube FROM jogadores "
        cursor.execute(sql)
        dados=cursor.fetchall() #busca todas as linhas do resultado de uma consulta.
        jogar = []
        for fila in dados:
            curso={'id':fila[0], 'nome':fila[1],'clube':fila[2]}
            jogar.append(curso)
        return jsonify({'jogadores':jogar, 'mensagem':"Jogadores Listados"})

    except Exception as ex:
        return jsonify({ 'mensagem':"Error"})

@app.route('/jogador/<id>', methods=['GET'])
def ler_jogadores(id):
    try:
     
        cursor = conexion.connection.cursor()
        sql="SELECT id, nome, clube FROM jogadores WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        dados = cursor.fetchone() #retorna um unico registro ou none(caso não tenha linhas disponiveis)
        if dados != None:
             curso={'id':dados[0], 'nome':dados[1],'clube':dados[2]}
             return jsonify({'jogadores':curso, 'mensagem':"Jogadores Encontrados"})
        else:
             return jsonify({'mensagem': "Jogador não encontrado."})

    except Exception as ex:
        return jsonify({ 'mensagem':"Error"})

@app.route('/jogador', methods=['POST'])
def registrar_jogadores():
    try:
        cursor = conexion.connection.cursor()
        sql="""INSERT INTO jogadores(id, nome, clube) VALUES ('{0}','{1}','{2}')""".format(request.json['id'],
        request.json['nome'], request.json['clube'] )
        cursor.execute(sql)
        conexion.connection.commit() #confirma a ação de inserção.
        return jsonify({'mensagem': 'Jogador Registrado'})
    except Exception as ex:
        return jsonify({'mensagem': "Error"})

@app.route('/jogador/<id>', methods=['PUT'])
def atualizar_jogadores(id):
    try:
        cursor = conexion.connection.cursor()
        sql="""UPDATE jogadores SET nome= '{0}', clube='{1}' WHERE id='{2}'""".format(request.json['nome'],request.json['clube'],id)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'messagem': 'jogador atualizado'})
    except Exception as ex:
        return jsonify({'mensagem': "Error"})

@app.route('/jogador/<id>', methods=['DELETE'])
def deletar_jogadores(id):
    try:
        cursor = conexion.connection.cursor()
        sql="DELETE FROM jogadores WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        conexion.connection.commit() #confirma a ação de inserção.
        return jsonify({'mensagem': 'Jogador deletado'})
    except Exception as ex:
        return jsonify({'mensagem': "Error"})

def pagina_nao_encontrada(error):
    return "Pagina não existe!", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_nao_encontrada)
    app.run()
