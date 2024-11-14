from flask import Blueprint, request, jsonify

from .firestore_services import add_filial, add_sede, add_acad, get_acad, update_filial, delete_acad, verify_user, \
    verify_acad, add_user, get_all_users, get_user, get_all_acads, update_sede
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


@auth_bp.route('/register_filial', methods=['POST'])
def register_filial_acad():
    data = request.get_json(force=True)
    cnpj_matriz = data.get('cnpj_matriz')
    nome_fantasia = data.get('nome_fantasia')
    endereco = data.get('endereco')
    lotacao = data.get('lotacao')
    if not cnpj_matriz:
        return jsonify({"error": "cnpj e senha são obrigatórios"}), 400
    
    response = add_filial(cnpj_matriz, nome_fantasia, endereco, lotacao)
    return jsonify(response), 200 if 'message' in response else 400


@auth_bp.route('/register_sede', methods=['POST'])
def register_sede_route():
    data = request.get_json(force=True)
    nome_fantasia = data.get('nome_fantasia')
    email = data.get('email')
    cnpj = data.get('cnpj')
    telefone = data.get('telefone')
    password = data.get('password')
    if not cnpj or not password:
        return jsonify({"error": "cnpj e senha são obrigatórios"}), 400
    
    response = add_sede(nome_fantasia, email, cnpj, telefone, password)
    return jsonify(response), 200 if 'message' in response else 400


@auth_bp.route('/get_acad/<string:cnpj>', methods=['GET'])
def get_academia(cnpj):
    try:
        response, status_code = get_acad(cnpj)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@auth_bp.route('/get_all_acads', methods=['GET'])
def get_all_acads_route():
    try:
        response, status_code = get_all_acads()
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/update_sede/<string:cnpj>', methods=['PUT'])
def update_sede_route(cnpj):
    try:
        data = request.get_json()

        if not data or not isinstance(data, dict):
            return jsonify({"error": "Dados atualizados devem ser fornecidos em formato JSON."}), 400

        response, status_code = update_sede(cnpj, data)
        return jsonify(response), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/update_filial/<string:nome_fantasia>', methods=['PUT'])
def update_academia(nome_fantasia):
    try:
        data = request.get_json()

        if not data or not isinstance(data, dict):
            return jsonify({"error": "Dados atualizados devem ser fornecidos em formato JSON."}), 400

        response, status_code = update_filial(nome_fantasia, data)
        return jsonify(response), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
    
@auth_bp.route('/get_user/<string:cpf>', methods=['GET'])
def get_user_route(cpf):
    try:
        response, status_code = get_user(cpf)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@auth_bp.route('/get_all_users', methods=['GET'])
def get_all_users_route():
    try:
        response, status_code = get_all_users()
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500