import requests

for _ in range(10000):
    resp = requests.get("https://8277127070t1.crazedencoder.com")
    print(resp.json())