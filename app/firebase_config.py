import firebase_admin
import os
from firebase_admin import credentials, auth, firestore
from dotenv import load_dotenv

load_dotenv()

def initialize_firebase():
    cred = credentials.Certificate('./firebase_credentials.json')
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

        
    db = firestore.client()
    return db