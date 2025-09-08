from Crypto.Util.number import long_to_bytes
import requests


#factordbとのAPI処理
def factordb(number):
    
    url = f"https://factordb.com/api?query={number}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data['status'] == "FF":
            factors = data.get('factors', [])
            if len(factors) >= 2:
                p = int(data['factors'][0][0])
                q = int(data['factors'][1][0])
                #print(f"p = {p}")
                #print(f"q = {q}")
                return p,q
            else:
                print("Data incomplete")
                return None, None
                #データが不完全
        else:
            print("No found")
            return None, None
    except requests.RequestException as e:
        print(f"Error has occurred: {e}")
        return None, None
        #通信エラー
    except (ValueError, KeyError, IndexError) as e:
        print(f"Error has occurred: {e}")
        return None, None
        #データ解析エラー



def solve(p, q, e, ct):    #解読プログラム
    try:
        phi = (p-1) * (q-1)
        d = pow(e, -1, phi)
        plain_hex = pow(ct, d, p*q)
        plain_text = long_to_bytes(plain_hex)
        return plain_text.decode(errors = "ignore")
    except Exception as e:
        print(f"Error has occurred: {e}")
        return "Decryption failed"
        #復号失敗