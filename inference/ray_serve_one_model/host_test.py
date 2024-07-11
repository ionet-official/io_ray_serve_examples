#host_test
import requests

text = "Create a funny joke"
response = requests.post("http://127.0.0.1:8000/", json=text)
print(response.text)