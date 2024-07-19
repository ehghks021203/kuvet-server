from flask import Blueprint, request, jsonify
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from src.llm import chatbot

chat_routes = Blueprint("chat", __name__)

@chat_routes.route("/chat", methods=["POST"])
def chat():
    # Error: 데이터 형식이 JSON이 아님
    if not request.is_json:
        return jsonify({
            "result": "error", 
            "msg": "missing json in request"
        }), 400
    # 파라미터 받아오기
    user_msg = request.json["msg"] if "msg" in request.json else ""
    history = request.json["history"] if "history" in request.json != None else []

    if len(history) == 0:
        bot_msg, bot_timestamp, history = chatbot.rag(user_msg)
    else:
        bot_msg, bot_timestamp, history = chatbot.rag(user_msg, history)
    
    return jsonify({
        "result": "success", 
        "msg": bot_msg,
        "timestamp": bot_timestamp,
        "history": history
    }), 200
