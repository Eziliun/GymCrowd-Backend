# firestore_service.py
from flask import current_app

# Função para adicionar um documento
def add_user(user_id, user_data):
    try:
        db = current_app.config['FIRESTORE_DB']
        db.collection('users').document(user_id).set(user_data)
        return {"message": "Usuário adicionado com sucesso!"}
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