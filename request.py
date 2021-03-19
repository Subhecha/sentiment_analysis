import requests

url = 'http://127.0.0.1:5000/classify_api'
r = requests.post(url,json = {'hi': True, 'i': True, 'am': True, 'happy': True})

print(r.json)