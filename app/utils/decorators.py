from functools import wraps
from flask import request, jsonify
from firebase_admin import auth

def validation_token() -> object:
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            id_token = request.headers.get("Authorization")
            user_id = request.headers.get("User-ID")
            print("user_id : ", user_id)

            # 여기 부분이 토큰이 "Bearer "로 시작하는지 확인하는 부분인데 없으면 오류 발생.
            if not id_token or not id_token.startswith("Bearer "):
                return jsonify({
                    "result": "error", 
                    "msg": "token does not exist"
                }), 401

            # id_token = id_token.split(' ')[1]으로 토큰을 추출하기 전에 위에서 id_token.startswith('Bearer ')을 먼저 확인해야 함.
            # 토큰이 "Bearer "로 시작하지 않는 경우, split(' ') 메서드는 오류가 발생할 수 있음.
            
            id_token = id_token.split(" ")[1]

            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token["uid"]
            print("uid : ", uid)

            if uid != user_id:
                # 401 = 미승인 및 비인증
                return jsonify({
                    "result": "error", 
                    "msg": "token not authenticated"
                }), 401
            # uid를 kwargs에 추가
            kwargs["uid"] = uid
            return f(*args, **kwargs)
        return wrapped
    return decorator
