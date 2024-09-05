from flask import current_app
from firebase_admin import firestore
import bcrypt


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
# Função para obter um documento
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

# Função para atualizar um documento
def update_user(user_id, user_data):
    try:
        db = current_app.config['FIRESTORE_DB']
        db.collection('users').document(user_id).update(user_data)
        return {"message": "Usuário atualizado com sucesso!"}
    except Exception as e:
        return {"error": str(e)}

# Função para excluir um documento
def delete_user(user_id):
    try:
        db = current_app.config['FIRESTORE_DB']
        db.collection('users').document(user_id).delete()
        return {"message": "Usuário excluído com sucesso!"}
    except Exception as e:
        return {"error": str(e)}