import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS

JOGOS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'valorant',
        'author': 'riot',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'lol',
        'author': 'riot',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'GTA V',
        'author': 'rockstar',
        'read': True
    }
]

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

def remove_jogo(jogo_id):
    for jogo in JOGOS:
        if jogo['id'] == jogo_id:
            JOGOS.remove(jogo)
            return True
    return False

@app.route('/jogos', methods=['GET', 'POST'])
def todos_os_jogos():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        JOGOS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Jogo adicionado!'
    else:
        response_object['jogos'] = JOGOS
    return jsonify(response_object)

@app.route('/jogos/<jogo_id>', methods=['PUT', 'DELETE'])
def single_jogo(jogo_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_jogo(jogo_id)
        JOGOS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'jogo updated!'
    if request.method == 'DELETE':
        remove_jogo(jogo_id)
        response_object['message'] = 'jogo removed!'
    return jsonify(response_object)

if __name__ == '__main__':
    app.run()