import requests

response = requests.get ('http://127.0.0.1:8000/')

resp_dict = response.json()
print (resp_dict)
