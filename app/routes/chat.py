from config.database import Database
from app.utils.decorators import *
from flask import Blueprint, request, jsonify
import jwt
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from src.llm import chatbot

chat_routes = Blueprint("chat", __name__)

@chat_routes.route("/chat", methods=["POST"])
@validation_token()
def chat(uid):
    # Error: 데이터 형식이 JSON이 아님
    if not request.is_json:
        return jsonify({
            "result": "error", 
            "msg": "missing json in request"
        }), 400
    # 횟수 검증
    db = Database()
    sql = "SELECT * FROM daily_chat_count WHERE user_id=%s"
    daily_chat_count = db.executeOne(sql, (uid))
    if daily_chat_count is None:
        sql = "INSERT INTO daily_chat_count (user_id, chat_count) VALUE (%s, %s)"
        db.execute(sql, (uid, 0))
        db.commit()
        chat_count = 0
    else:
        chat_count = daily_chat_count["chat_count"]
    
    if chat_count >= 5:
        db.close()
        return jsonify({
            "result": "error", 
            "msg": "chatting limit exceeded"
        }), 401

    # 파라미터 받아오기
    user_msg = request.json["msg"] if "msg" in request.json else ""
    history = request.json["history"] if "history" in request.json != None else []

    if len(history) == 0:
        bot_msg, bot_timestamp, history = chatbot.rag(user_msg)
    else:
        bot_msg, bot_timestamp, history = chatbot.rag(user_msg, history)
    
    chat_count = chat_count + 1
    sql = "UPDATE daily_chat_count SET chat_count=%s WHERE user_id=%s"
    db.execute(sql, (chat_count, uid))
    db.commit()
    db.close()

    
    
    return jsonify({
        "result": "success", 
        "msg": bot_msg,
        "timestamp": bot_timestamp,
        "history": history
    }), 200
