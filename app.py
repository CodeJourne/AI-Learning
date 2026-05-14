# app.py
from flask import Flask, render_template, request, jsonify
import json
import os
import requests
app = Flask(__name__)

api_key = "6fee2daa3c1b4a38882ce04fe8cb9795.kCbqn5wMM7Djw1uW"  # 替换为你的 API Key

# 加载聊天历史（如果存在）
if os.path.exists("chat_history.json"):
    with open("chat_history.json", "r", encoding="utf-8") as f:
        chat_history = json.load(f)
else:
    chat_history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"reply": "请输入消息！"})

    # 添加用户消息到历史
    chat_history.append({"role": "user", "content": user_message})

    # 调用 智谱 AI API（用requests直接调用）
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "glm-4",  # 智谱的模型
        "messages": chat_history
    }

    response = requests.post(url, json=data, headers=headers)
    response_data = response.json()
    ai_reply = response_data["choices"][0]["message"]["content"].strip()

    # 添加 AI 回复到历史
    chat_history.append({"role": "assistant", "content": ai_reply})

    # 保存聊天历史
    with open("chat_history.json", "w", encoding="utf-8") as f:
        json.dump(chat_history, f, ensure_ascii=False, indent=2)

    return jsonify({"reply": ai_reply})

if __name__ == "__main__":
    app.run(debug=True)