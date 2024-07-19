from config.default import *
import os

# API Keys
MAFRA_API_KEY = os.getenv("MAFRA_API_KEY", "default_api_key")
KAKAO_API_KEY = os.getenv("KAKAO_API_KEY", "default_api_key")
VWORLD_API_KEY = os.getenv("VWORLD_API_KEY", "default_api_key")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "default_api_key")
FIREBASE_ADMINSDK_PATH = os.getenv("FIREBASE_ADMINSDK_PATH", "")