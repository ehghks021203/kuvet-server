from config.default import *
import os

# General Flask Configurations
JSON_AS_ASCII = os.getenv("JSON_AS_ASCII", False)
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///default.db")
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", False)
