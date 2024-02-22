import requests
import json
import datetime

# 보낼 데이터
start = datetime.datetime.now()
start = start.strftime("%Y-%m-%d %H:%M:%S")

data = {
    "time": start,
    "label": 'fire',
    "percentage": 0.5,
    }


# 데이터를 JSON 형식으로 직렬화
json_data = json.dumps(data)
print(json_data)
# POST 요청 보내기
url = 'http://3.37.201.238/object-data-upload'
response = requests.post(url, data=json_data, headers={"Content-Type": "application/json"})

# 응답 결과 확인
if response.status_code == 200:
    print("데이터 전송 성공")
else:
    print(response.status_code)
    print("데이터 전송 실패")