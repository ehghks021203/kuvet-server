# Makefile to generate .env file

# Define default values for the environment variables
ENV_FILE=.env
# API keys
DEFAULT_MAFRA_API_KEY=default_api_key
DEFAULT_KAKAO_API_KEY=default_api_key
DEFAULT_VWORLD_API_KEY=default_api_key
DEFAULT_GOOGLE_API_KEY=default_api_key

# Flask config
DEFAULT_SECRET_KEY=default_secret_key
DEFAULT_JSON_AS_ASCII=False
DEFAULT_DB_URI=sqlite:///default.db
DEFAULT_TRACK_MODIFICATIONS=False

# Server
DEFAULT_SERVER_DOMAIN=localhost
DEFAULT_SERVER_PORT=5000

# model
DEFAULT_CHATBOT_MODEL=your_model_name
DEFAULT_CHATBOT_CHROMA_DB_PATH=yout_chroma_db_model

DEFAULT_DB_USER=default_user
DEFAULT_DB_HOST=default_host
DEFAULT_DB_PASSWORD=default_password
DEFAULT_DB_NAME=default_name

DEFAULT_FIREBASE_ADMINSDK_PATH=default_path

# Target to create the .env file
create-env:
		@echo "Creating .env file..."
		@echo "MAFRA_KEY_API_KEY=${DEFAULT_MAFRA_API_KEY}" >> $(ENV_FILE)
		@echo "KAKAO_API_KEY=${DEFAULT_KAKAO_API_KEY}" >> $(ENV_FILE)
		@echo "VWORLD_API_KEY=${DEFAULT_VWORLD_API_KEY}" >> $(ENV_FILE)
		@echo "OPENAI_API_KEY=${DEFAULT_GOOGLE_API_KEY}" >> $(ENV_FILE)

		@echo "SECRET_KEY=${DEFAULT_SECRET_KEY}" >> ${ENV_FILE}
		@echo "SQLALCHEMY_DATABASE_URI=${DEFAULT_DB_URI}" >> $(ENV_FILE)
		@echo "SQLALCHEMY_TRACK_MODIFICATIONS=${DEFAULT_TRACK_MODIFICATIONS}" >> $(ENV_FILE)
		@echo "JSON_AS_ASCII=${DEFAULT_JSON_AS_ASCII}" >> ${ENV_FILE}

		@echo "SERVER_DOMAIN=${DEFAULT_SERVER_DOMAIN}" >> $(ENV_FILE)
		@echo "SERVER_PORT=${DEFAULT_SERVER_PORT}" >> $(ENV_FILE)

		@echo "CHATBOT_MODEL=${DEFAULT_CHATBOT_MODEL}" >> ${ENV_FILE}
		@echo "CHATBOT_CHROMA_DB_PATH=${DEFAULT_CHATBOT_CHROMA_DB_PATH}" >> ${ENV_FILE}

		@echo "DB_USER=${DEFAULT_DB_USER}" >> ${ENV_FILE}
		@echo "DB_HOST=${DEFAULT_DB_HOST}" >> ${ENV_FILE}
		@echo "DB_PASSWORD=${DEFAULT_DB_PASSWORD}" >> ${ENV_FILE}
		@echo "DB_NAME=${DEFAULT_DB_NAME}" >> ${ENV_FILE}

		@echo "FIREBASE_ADMINSDK_PATH=${DEFAULT_FIREBASE_ADMINSDK_PATH}" >> ${ENV_FILE}
		@echo ".env file created successfully!"

# Target to clean the .env file
clean-env:
		@echo "Removing .env file..."
		@rm -f $(ENV_FILE)
		@echo ".env file removed successfully!"

# Default target
all: create-env