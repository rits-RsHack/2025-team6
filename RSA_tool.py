from Crypto.Util.number import long_to_bytes
import requests
from gmpy2 import iroot
import math
from math import gcd
import owiener


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



def solve(p, q, e, ct):    #通常攻撃プログラム

    try:
        phi = (p-1) * (q-1)
        d = pow(e, -1, phi)
        plain_hex = pow(ct, d, p*q)
        plain_text = long_to_bytes(plain_hex)
        return plain_text.decode()
    except Exception as e:
        print(f"Error has occurred: {e}")
        return "Decryption failed"
        #復号失敗



def low_index(e, ct): #低指数攻撃プログラム

    try:    
        plain_hex,exact = iroot(e, ct)

        if exact:
            plain_text = long_to_bytes(plain_hex)
            return plain_text.decode()
    except Exception as e:
        print(f"Error has occurred: {e}")
        return "Decryption failed" #復号失敗



def super_low_index(N, e, ct):

    if e == 1:
        plain_hex = pow(ct, e, N)
        plain_text = long_to_bytes(plain_hex)
        return plain_text.decode()
    else:
        return "Decryption failed" #復号失敗


def squared_index(N, e, ct):

    try:    
        f = math.isqrt(n)
        phi = (f-1)*f
        d = pow(e, -1, phi)
        plain_hex = pow(ct, d, N)
        plain_text = long_to_bytes(plain_hex)
        return plain_text.decode()
    except Exception as e:
        print(f"Error has occurred: {e}")
        return "Decryption failed" #復号失敗


def N_prime(N, e, ct):

    try:    
        f = math.isqrt(n)
        phi = N-1
        d = pow(e, -1, phi)
        plain_hex = pow(ct, d, N)
        plain_text = long_to_bytes(plain_hex)
        return plain_text.decode()
    except Exception as e:
        print(f"Error has occurred: {e}")
        return "Decryption failed" #復号失敗


def Wiener(N, e, ct):

    d = owiener.attack(e, N)
    if d is None:
        return "Decryption failed" #復号失敗
    else:
        try:
            plain_hex = pow(ct, d, N)
            plain_text = long_to_bytes(plain_hex)
            return plain_text.decode()
        except Exception as e:
            print(f"Error has occurred: {e}")
            return "Decryption failed" #復号失敗