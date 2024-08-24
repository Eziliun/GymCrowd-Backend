from flask import Blueprint, render_template, Flask, request, jsonify;
import firebase_admin
from firebase_admin import credentials, auth


app = Flask(__name__)


#A FAZER: buscar link do storage e firebasekeyconfig


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

