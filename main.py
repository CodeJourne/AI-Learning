import requests

API_KEY = "05624eb50fd5405da93c5f8cfd1efd92.hhK4DWG7wyiZ3g5Y"

url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

messages = []

while True:
    user_input = input("你：")

    if user_input == "退出":
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    data = {
        "model": "GLM-4.6",
        "messages": messages
    }

    response = requests.post(url, headers=headers, json=data)

    result = response.json()


    ai_reply = result["choices"][0]["message"]["content"]

    print("AI:", ai_reply)

    messages.append({
        "role": "assistant",
        "content": ai_reply
    })
