from flask import current_app
from firebase_admin import firestore
from datetime import datetime, timedelta
import jwt
import bcrypt

SECRET_KEY = "sua_chave_secreta_super_secreta"

def add_user(nome_fantasia, email, cnpj, telefone, password):
    try:
        db = firestore.client()
        
        
        salt = bcrypt.gensalt()
        en_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        
    
        user_data = {
            'nome_fantasia': nome_fantasia,
            'email': email,
            'cnpj': cnpj,
            'telefone': telefone,
            'password': en_password.decode('utf8')
        }


        db.collection('academias').document(nome_fantasia).set(user_data)
        return {"message": "A academia, agora, está apta a utilizar nosso serviço!"}
    except Exception as e:
        return {"error": str(e)}
    
def get_user(user_id):
    try:
        db = current_app.config['FIRESTORE_DB']
        user_ref = db.collection('users').document(user_id)
        user = user_ref.get()
        if user.exists:
            return user.to_dict()
        else:
            return {"error": "Usuário não encontrado."}
    except Exception as e:
        return {"error": str(e)}


def update_user(user_id, user_data):
    try:
        db = current_app.config['FIRESTORE_DB']
        db.collection('users').document(user_id).update(user_data)
        return {"message": "Usuário atualizado com sucesso!"}
    except Exception as e:
        return {"error": str(e)}


def delete_user(user_id):
    try:
        db = current_app.config['FIRESTORE_DB']
        db.collection('users').document(user_id).delete()
        return {"message": "Usuário excluído com sucesso!"}
    except Exception as e:
        return {"error": str(e)}
    
    
def verify_user(cnpj, password):
    try:
        db = firestore.client()

        
        user_ref = db.collection('academias').where('cnpj', '==', cnpj).limit(1).stream()
        user_doc = next(user_ref, None)


        if not user_doc:
            return {"error": "Usuário não encontrado"}, 404


        user_data = user_doc.to_dict()
        stored_pass = user_data['password']


        if bcrypt.checkpw(password.encode('utf-8'), stored_pass.encode('utf-8')):
            
            token = jwt.encode(
                {
                "cnpj": cnpj,
                "expiration": (datetime.now() + timedelta(hours=1)).timestamp()
                },
                SECRET_KEY,
                algorithm="HS256"
            )
            
            return {"message": "Login bem-sucedido!", "token": token}, 200 
        else:    
            return {"error": "Senha incorreta"}, 401

    except Exception as e:
        return {"error": str(e)}, 500   