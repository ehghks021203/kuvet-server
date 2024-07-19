from flask import Blueprint, request, jsonify
import firebase_admin
from firebase_admin import credentials, auth
import requests
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from src.llm import chatbot

user_routes = Blueprint("user", __name__)


def _get_google_token_info(id_token):
    response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}')
    response.raise_for_status()
    return response.json()

def _get_kakao_user_info(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('https://kapi.kakao.com/v1/oidc/userinfo', headers=headers)
    response.raise_for_status()
    return response.json()

def _get_or_create_user(email):
    try:
        #이메일 기반으로 유저 조회
        user = auth.get_user_by_email(email)
    except auth.UserNotFoundError:
        #유저 존재 안하면 계정 생성
        user = auth.create_user(email=email)
    return user

def _create_custom_token(uid):
    #커스텀 토큰 발급
    custom_token = auth.create_custom_token(uid)
    return custom_token


@user_routes.route("/login", methods=["GET"])
def login():
    platform = request.args.get('platform')
    token = request.args.get('token')

    if not platform or not token:
        return jsonify({
            "result": "error", 
            "msg": "필수 파라미터가 누락되었습니다.", 
            "token": ""
        }), 401
    
    try:
        if platform == "google":
            #구글 아이디 토큰을 기반으로 이메일 추출
            token_info = _get_google_token_info(token)
            email = token_info.get("email")
        elif platform == "kakao":
            #카카오 엑세스 토큰을 기반으로 이메일 추출
            user_info = _get_kakao_user_info(token)
            email = user_info.get("email")
        else:
            return jsonify({
                "result": "error", 
                "msg": "지원하지 않는 플랫폼으로 로그인을 진행하였습니다.", 
                "token": ""
            }), 401
        
        if email:
            #유저를 로그인/회원가입 진행
            user = _get_or_create_user(email)
            
            #계정 기반으로 토큰 발행
            custom_token = _create_custom_token(user.uid)

            return jsonify({
                "result": "error", 
                "msg": "login success", 
                "token": custom_token.decode("utf-8")
            }), 200
        else:
            return jsonify({
                "result": "error", 
                "msg": "토큰 정보에서 이메일을 조회할 수 없습니다.", 
                "token": ""
            }), 401
    except Exception as e:
        return jsonify({
                "result": "error", 
                "msg": str(e), 
                "token": ""
            }), 401

