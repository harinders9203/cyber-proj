import requests

site=input("Enter the site url to check if its live or not: ").lower()
res=requests.get(site)

if res.status_code==200:
    print(res.json)
else:
    print("fail")