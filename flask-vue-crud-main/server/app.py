from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

"""
Aplicativo Flask para gerenciar uma lista de jogos. 
Utiliza SQLAlchemy para interagir com um banco de dados SQLite e CORS para lidar com solicitações de diferentes origens.

Classe:
    Jogo: Um modelo SQLAlchemy que representa um jogo.

Métodos:
    ping_pong(): Retorna uma resposta JSON 'pong!' para qualquer solicitação GET. Apenas para ver se estava funcionando
    
    remove_jogo(jogo_id): Remove um jogo do banco de dados pelo seu ID.
    
    todos_os_jogos(): Lida com solicitações GET e POST para a rota '/jogos'. 
        Retorna todos os jogos em caso de GET e adiciona um novo jogo em caso de POST.
    
    single_jogo(jogo_id): Lida com solicitações PUT e DELETE para a rota '/jogos/<jogo_id>'. 
        Atualiza um jogo existente em caso de PUT e remove um jogo em caso de DELETE.
"""

app = Flask(__name__)
app.config.from_object(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'jogo.db')
db = SQLAlchemy(app)
CORS(app, resources={r'/*': {'origins': '*'}})

class Jogo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.Text)
    empresa = db.Column(db.Text)
    jogou = db.Column(db.Boolean)
    
    def __init__(self, nome, empresa, jogou):
        self.nome = nome
        self.empresa = empresa
        self.jogou = jogou  
        
    def __repr__(self):
        return f'{self.nome}: {self.empresa} - {self.jogou}'

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

def remove_jogo(jogo_id):
    jogo = db.session.get(Jogo, jogo_id)
    if jogo:
        db.session.delete(jogo)
        db.session.commit()
        return True
    return False

@app.route('/jogos', methods=['GET', 'POST'])
def todos_os_jogos():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        data = request.get_json()
        nome = data.get('nome')
        empresa = data.get('empresa')
        jogou = data.get('jogou')
        jogo = Jogo(nome, empresa, jogou)
        db.session.add(jogo)
        db.session.commit()
        response_object['message'] = 'Jogo adicionado!'
    else:
        jogos = Jogo.query.all()
        response_object['jogos'] = [{'id': jogo.id, 'nome': jogo.nome, 'empresa': jogo.empresa, 'jogou': jogo.jogou} for jogo in jogos]
    return jsonify(response_object)

@app.route('/jogos/<jogo_id>', methods=['PUT', 'DELETE'])
def single_jogo(jogo_id):
    response_object = {'status': 'success'}
    jogo = db.session.get(Jogo, jogo_id)
    if not jogo:
        return jsonify({'message': 'Jogo não encontrado!'}), 404

    if request.method == 'PUT':
        post_data = request.get_json()
        jogo.nome = post_data.get('nome')
        jogo.empresa = post_data.get('empresa')
        jogo.jogou = post_data.get('jogou')
        db.session.commit()
        response_object['message'] = 'Jogo atualizado!'
    elif request.method == 'DELETE':
        db.session.delete(jogo)
        db.session.commit()
        response_object['message'] = 'Jogo removido!'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()