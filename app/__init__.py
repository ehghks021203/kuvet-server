from config import settings, api
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import firebase_admin
from firebase_admin import credentials

# create flask app
app = Flask(__name__)
app.config.from_object(settings)

db = SQLAlchemy(app)

from app.routes import get_disease_data_routes, chat_routes, user_routes

app.register_blueprint(get_disease_data_routes)
app.register_blueprint(chat_routes)
app.register_blueprint(user_routes)

# Firebase 초기화
cred_path = api.FIREBASE_ADMINSDK_PATH
cred = credentials.Certificate(cred_path)
firebase_app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'hci-animal-chatbot.appspot.com'
})