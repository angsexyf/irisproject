# client.py (파일 이름)
import requests

url = "http://211.253.8.46:8080/home/submitRequest"
data = {
    "type": "example_type",
    "id": "example_id",
    "pw": "example_pw"
}
response = requests.post(url, json=data)
print(response.json())
