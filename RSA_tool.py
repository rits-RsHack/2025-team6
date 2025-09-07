from Crypto.Util.number import long_to_bytes
import requests


#factordbとのAPI処理
def factordb(number):
    
    url = f"https://factordb.com/api?query={number}"
    response = requests.get(url)
    data = response.json()

    if data['status'] == "FF":
        p = int(data['factors'][0][0])
        q = int(data['factors'][1][0])
        #print(f"p = {p}")
        #print(f"q = {q}")
        return p,q
    else:
        print("No found")
        return None, None


def solve(p, q, e, ct):    #解読プログラム

    phi = (p-1) * (q-1)
    d = pow(e, -1, phi)
    plain_hex = pow(ct, d, p*q)
    plain_text = long_to_bytes(plain_hex)

    return plain_text.decode(errors = "ignore")