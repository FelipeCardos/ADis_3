import requests

BASE = "http://127.0.0.1:5000/"

r= requests.post(BASE + "artistas", {'artist_id' : '5K4W6rqBFWDnAN6FQUkS6x'})
print (r.status_code)
print (r.headers)
print (r.text)
