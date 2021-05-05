import requests

#response = requests.get ('http://ec2-3-16-160-97.us-east-2.compute.amazonaws.com:28888/')
response = requests.get ('http://127.0.0.1:8000/')

resp_dict = response.json()
print (resp_dict)
