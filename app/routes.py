from flask import Blueprint, request, jsonify
from firebase_admin import auth

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nome_usuario = data.get('nome_usuario')
    email = data.get('email')
    cpf = data.get('cpf')
    password = data.get('password')
    
    try:
        user = auth.create_user(nome_usuario=nome_usuario, email=email, cpf=cpf, password=password)
        return jsonify({"message": "Usuário criado com sucesso!", "uid": user.uid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400
    
    #falta validacao para login, no momento, o login está sendo feito apenas com o email
    
    try:
        user = auth.get_user_by_email(email)
        return jsonify({"message": "Login bem-sucedido!", "uid": user.uid}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400