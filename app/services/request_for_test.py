import requests


response = requests.get("http://13.60.99.228/food/get_all_foods?page=1")

response_json = response.json()

for i in response_json.get("foods"):
    print(i)
