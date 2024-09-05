from flask import Blueprint, request, jsonify
from .firestore_services import add_user, get_user, update_user, delete_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registerAcad', methods=['POST'])
def register_route():
    data = request.get_json(force=True)
    nome_fantasia = data.get('nome_fantasia')
    email = data.get('email')
    cnpj = data.get('cnpj')
    telefone = data.get('telefone')
    password = data.get('password')
    if not cnpj or not password:
        return jsonify({"error": "cnpj e senha são obrigatórios"}), 400
    
    response = add_user(nome_fantasia, email, cnpj, telefone, password)
    return jsonify(response), 200 if 'message' in response else 400


@auth_bp.route('/get-user/<user_id>', methods=['GET'])
def get_user_route(user_id):
    response = get_user(user_id)
    return jsonify(response), 200 if 'error' not in response else 404

@auth_bp.route('/update-user/<user_id>', methods=['PUT'])
def update_user_route(user_id):
    user_data = request.get_json()
    response = update_user(user_id, user_data)
    return jsonify(response), 200 if 'message' in response else 400

@auth_bp.route('/delete-user/<user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    response = delete_user(user_id)
    return jsonify(response), 200 if 'message' in response else 400