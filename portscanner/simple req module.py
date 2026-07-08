import requests


req=requests.get("https://gndec.ac.in")
print(req.status_code)
w=[]
w.append(req.content)
print(w)