import requests

BASE = "http://127.0.0.1:5000/"

r= requests.get(BASE + "utilizadores", {})
print (r.status_code)
print (r.headers)
print (r.text)
