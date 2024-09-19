from functools import wraps
from flask import request, jsonify
import jwt

SECRET_KEY = "sua_chave_secreta_super_secreta"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"error": "Token de autorização é necessário."}), 403

        try:
           
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado. Faça login novamente."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido. Faça login novamente."}), 401

        return f(*args, **kwargs)
    return decorated