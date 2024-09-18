from flask import Blueprint, request, jsonify

from .firestore_services import add_acad, get_acad, update_acad, delete_acad, verify_user, verify_acad, add_user
from .decorators import token_required

auth_bp = Blueprint('auth', __name__)

                                                                        #WEB VERSION#
@auth_bp.route('/register_acad', methods=['POST'])
def register_acad_route():
    data = request.get_json(force=True)
    nome_fantasia = data.get('nome_fantasia')
    email = data.get('email')
    cnpj = data.get('cnpj')
    telefone = data.get('telefone')
    password = data.get('password')
    if not cnpj or not password:
        return jsonify({"error": "cnpj e senha são obrigatórios"}), 400
    
    response = add_acad(nome_fantasia, email, cnpj, telefone, password)
    return jsonify(response), 200 if 'message' in response else 400


@auth_bp.route('/get-user/<user_id>', methods=['GET'])
def get_user_route(user_id):
    response = get_acad(user_id)
    return jsonify(response), 200 if 'error' not in response else 404

@auth_bp.route('/update-user/<user_id>', methods=['PUT'])
def update_user_route(user_id):
    user_data = request.get_json()
    response = update_acad(user_id, user_data)
    return jsonify(response), 200 if 'message' in response else 400

@auth_bp.route('/delete-user/<user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    response = delete_acad(user_id)
    return jsonify(response), 200 if 'message' in response else 400

@auth_bp.route('/login_acad', methods=['POST'])
def login_acad_route():
    try:
        data = request.get_json()

        if not data or 'cnpj' not in data or 'password' not in data:
            return jsonify({"error": "CNPJ e senha são obrigatórios."}), 400

        cnpj = data['cnpj']
        password = data['password']

        response, status_code = verify_acad(cnpj, password)

        return jsonify(response), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500



                                                                                    #MOBILE#    
@auth_bp.route('/register_user', methods=['POST'])
def register_user_route():
    data = request.get_json(force=True)
    nome_usuario = data.get('nome_usuario')
    email = data.get('email')
    cpf = data.get('cpf')
    #telefone = data.get('telefone')
    password = data.get('password')
    if not cpf or not password:
        return jsonify({"error": "cnpj e senha são obrigatórios"}), 400
    
    response = add_user(nome_usuario, email, cpf, password)
    return jsonify(response), 200 if 'message' in response else 400    

@auth_bp.route('/login_user', methods=['POST'])
def login_user_route():
    try:
        data = request.get_json()

        if not data or 'email' not in data or 'password' not in data:
            return jsonify({"error": "CNPJ e senha são obrigatórios."}), 400

        email = data['email']
        password = data['password']

        response, status_code = verify_user(email, password)

        return jsonify(response), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500