import firebase_admin
import os
from firebase_admin import credentials, auth, firestore
from dotenv import load_dotenv

load_dotenv()

firebase_config = {
    'databaseURL': "https://gymcrowd-55b46-default-rtdb.firebaseio.com",
    'apiKey': "AIzaSyC1Owy6ZuHY2cMVHv-QbJ2XyGa2L_0zXPo",
    'authDomain': "gymcrowd-f20e1.firebaseapp.com",
    'projectId': "gymcrowd-f20e1",
    'storageBucket': "gymcrowd-f20e1.appspot.com",
    'messagingSenderId': "1021391817554",
    'appId': "1:1021391817554:web:fbf4388d4129f1728bc88b"
}

def initialize_firebase():
    cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS'))
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred, firebase_config)
        
    db = firestore.client()
    return db