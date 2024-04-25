import requests
import sys

# 定義 API 端點 URL
url = 'http://localhost:'+sys.argv[1]+'/LLM/'

# 定義要發送的 JSON 格式的訊息
while True:
    
    data = {}

    text = input("You > ")
    data['message'] = text

    if text == "exit":
        break

    # 發送 POST 請求
    response = requests.post(url, json=data)

    # 解析回應
    if response.status_code == 200:
        # 請求成功，印出回覆的 JSON 資料
        print(response.json())
    else:
        # 請求失敗，印出錯誤訊息
        print('請求失敗:', response.text)
