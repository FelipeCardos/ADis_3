import requests

BASE = "http://127.0.0.1:5000/"

r= requests.post(BASE + "musicas", {'track_id': '3sNVsP50132BTNlImLx70i'})
print("----------------------------------------------------")
print (r.status_code)
print (r.text)
print("----------------------------------------------------")

input()

r= requests.delete(BASE + "artistas/1")
print("----------------------------------------------------")
print (r.status_code)
print (r.text)
print("----------------------------------------------------")

