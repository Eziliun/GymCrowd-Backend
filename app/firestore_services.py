from flask import current_app
from firebase_admin import firestore
from datetime import datetime, timedelta
import jwt
import bcrypt

SECRET_KEY = "sua_chave_secreta_super_secreta"

def add_acad(nome_fantasia, email, cnpj, telefone, password):
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

def add_sede(nome_fantasia, email, cnpj, telefone, password):
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


        db.collection('sedes').document(cnpj).set(user_data)
        return {"message": "A academia, agora, está apta a utilizar nosso serviço!"}
    except Exception as e:
        return {"error": str(e)}


def add_filial(cnpj_matriz, nome_fantasia, endereco, lotacao):
    try:
        db = firestore.client()
     
    
        user_data = {
            'nome_fantasia': nome_fantasia,
            'endereco': endereco,
            'cnpj_matriz': cnpj_matriz,
            'lotacao': lotacao,
            'latitude': '',
            'longitude':  '',
        }

        db.collection('academias').document(nome_fantasia).set(user_data)
        return {"message": "A filial foi adicionada com sucesso!"}
    except Exception as e:
        return {"error": str(e)}

    
def get_acad(cnpj):
    try:
        db = firestore.client()

        academia_ref = db.collection('academias').where('cnpj', '==', cnpj).limit(1).stream()
        academia_doc = next(academia_ref, None)

        if not academia_doc:
            return {"error": "Academia não encontrada"}, 404

        academia_data = academia_doc.to_dict()
        return academia_data, 200

    except Exception as e:
        return {"error": str(e)}, 500
    
    
def get_all_acads():
    try:
        db = firestore.client()

        acads = []
        acads_ref = db.collection('academias').stream()
        for acad in acads_ref:
            acad_data = acad.to_dict()
            acad_data['id'] = acad.id
            acad_data.pop('password', None)
            acads.append(acad_data)

        return {"Acads": acads}, 200

    except Exception as e:
        return {"error": str(e)}, 500
    
    
def get_all_filiais(cnpj_matriz):
    try:
        db = firestore.client()

        acads = []
        acads_ref = db.collection('academias').where('cnpj_matriz' == cnpj_matriz).stream()
        for acad in acads_ref:
            acad_data = acad.to_dict()
            acad_data['id'] = acad.id
            acad_data.pop('password', None)
            acads.append(acad_data)

        return {"Acads": acads}, 200

    except Exception as e:
        return {"error": str(e)}, 500

      
def update_filial(nome_filial, new_data):
    try:
        db = firestore.client()

        academia_ref = db.collection('academias').where('nome_fantasia', '==', nome_filial).limit(1).stream()
        academia_doc = next(academia_ref, None)

        if not academia_doc:
            return {"error": "Academia não encontrada"}, 404

        academia_data = academia_doc.to_dict()
        db.collection('academias').document(nome_filial).update(new_data)
        return {"message": "Informações da academia atualizadas com sucesso!"}, 200

    except Exception as e:
        return {"error": str(e)}, 500

      
def delete_acad(user_id):
    try:
        db = current_app.config['FIRESTORE_DB']
        db.collection('users').document(user_id).delete()
        return {"message": "Usuário excluído com sucesso!"}
    except Exception as e:

        return {"error": str(e)}
    
    
def verify_acad(cnpj, password):
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
            
            return {"message": "Login bem-sucedido!",
                    "token": token,
                    "cnpj": cnpj, 
                    "email": user_data['email'],
                    "telefone": user_data['telefone']}, 200 
        else:    
            return {"error": "Senha incorreta"}, 401

    except Exception as e:
        return {"error": str(e)}, 500   




                                                                            #MOBILE VERSION
def add_user(nome_usuario, email, cpf, password):
    try:
        db = firestore.client()
        
        salt = bcrypt.gensalt()
        en_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        user_data = {
            'nome_usuario': nome_usuario,
            'email': email,
            'cpf': cpf,
            #'telefone': telefone,
            'password': en_password.decode('utf8')
        }

        db.collection('users').document(email).set(user_data)
        return {"message": "Um usuario novo acaba de se cadastrar: ${nome_usuario}"}
    except Exception as e:
        return {"error": str(e)}


def get_user(cpf):
    try:
        db = firestore.client()

        academia_ref = db.collection('users').where('cpf', '==', cpf).limit(1).stream()
        academia_doc = next(academia_ref, None)

        if not academia_doc:
            return {"error": "Usuário não identificado"}, 404

        academia_data = academia_doc.to_dict()
        return academia_data, 200

    except Exception as e:
        return {"error": str(e)}, 500
    
def get_all_users():
    try:
        db = firestore.client()

        users = []
        users_ref = db.collection('users').stream()
        for user in users_ref:
            user_data = user.to_dict()
            user_data['id'] = user.id
            user_data.pop('password', None)
            users.append(user_data)

        return {"users": users}, 200

    except Exception as e:
        return {"error": str(e)}, 500



def verify_user(email, password):
    try:
        db = firestore.client()
        
        user_ref = db.collection('users').where('email', '==', email).limit(1).stream()
        user_doc = next(user_ref, None)

        if not user_doc:
            return {"error": "Usuário não encontrado"}, 404

        user_data = user_doc.to_dict()
        stored_pass = user_data['password']

        if bcrypt.checkpw(password.encode('utf-8'), stored_pass.encode('utf-8')):
            
            token = jwt.encode(
                {
                "email": email,
                "expiration": (datetime.now() + timedelta(hours=1)).timestamp()
                },
                SECRET_KEY,
                algorithm="HS256"
            )
            
            return {
                "nome_usuario": user_data['nome_usuario'],
                "email": user_data['email'],
                "token": token,
                "message": "Login bem-sucedido!"}, 200 
        else:    
            return {"error": "Senha incorreta"}, 401

    except Exception as e:
        return {"error": str(e)}, 500   
    
    