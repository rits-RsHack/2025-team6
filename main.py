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


def solve(p, q, e, ct):    #解読プログラム

    phi = (p-1) * (q-1)
    d = pow(e, -1, phi)
    plain_hex = pow(ct, d, p*q)
    plain_text = long_to_bytes(plain_hex)

    print(plain_text.decode())


#N = 13373801376856352919495636794117610920860037770702465464324474778341963699665011787021257
#e = 65537
#c = 39119617768257067256541748412833564043113729163757164299687579984124653789492591457335

N = int(input("N:"))
e = int(input("e:"))
ct = int(input("ct:"))

p,q = factordb(N)

solve(p, q, e, ct)



