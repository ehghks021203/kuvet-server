# 🐮 가축 질병 관리 챗봇 KUVet (BACKEND)

> 농림축산식품부 주관 공모전 참여 작품입니다.
>
> KUVet frontend: [KUVet](https://github.com/OverTook/LivestockCare_ChatBot)\
> KUVet RAG: [kuvet-rag](https://github.com/ehghks021203/kuvet-RAG)

<br/>

## **Overview:**
가축의 건강 관리를 위한 전문 챗봇 서비스 입니다. 가축의 증상을 입력하면 병명을 추측하고, 이에 맞는 의약품을 추천하며 복용 방법을 제공합니다. 또한, 주변 가축 질병 발생 현황을 지도상에 시각화하여 사용자들이 질병의 확산을 한눈에 파악하고 예방할 수 있도록 합니다. 이 서비스를 통해 가축의 건강을 효과적으로 관리하고, 농가의 생산성을 높이고자 합니다.

<br/>

## **Environment:**
<img src="https://img.shields.io/badge/Ubuntu%2022.04-E95420?logo=Ubuntu&logoColor=fafafa"/> 
<img src="https://img.shields.io/badge/ChatGPT%204-412991?logo=OpenAI&logoColor=fafafa"/> 
<img src="https://img.shields.io/badge/Python%203.10.4-3776AB?logo=Python&logoColor=fafafa"/> 
<img src="https://img.shields.io/badge/Flask%203.0.3-000000?logo=Flask&logoColor=fafafa"/>

<br/>

## **How to Set Up:**
### 1. 필수 라이브러리 설치

```
pip install -r requirements.txt
```


### 2. .env 파일 생성

```
makefile create-env
```

### 3. .env 파일 정보 수정
```
MAFRA_KEY_API_KEY=default_api_key
KAKAO_API_KEY=default_api_key
VWORLD_API_KEY=default_api_key
OPENAI_API_KEY=default_api_key
SECRET_KEY=default_secret_key
SQLALCHEMY_DATABASE_URI=sqlite:///default.db
SQLALCHEMY_TRACK_MODIFICATIONS=False
JSON_AS_ASCII=False
SERVER_DOMAIN=localhost
SERVER_PORT=5000
CHATBOT_MODEL=your_model_name
CHATBOT_CHROMA_DB_PATH=yout_chroma_db_model
DB_USER=default_user
DB_HOST=default_host
DB_PASSWORD=default_password
DB_NAME=default_name
FIREBASE_ADMINSDK_PATH=default_path
```

### 4. run.py 실행
```
python run.py
```



## **Project Organization:**

