import requests

number = 13373801376856352919495636794117610920860037770702465464324474778341963699665011787021257

url = f"https://factordb.com/api?query={number}"
response = requests.get(url)
data = response.json()

if data['status'] == "FF":
    p = data['factors'][0][0]
    q = data['factors'][1][0]
    print(f"p = {p}")
    print(f"q = {q}")



