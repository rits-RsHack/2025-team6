from Crypto.Util.number import long_to_bytes
import requests
from gmpy2 import iroot
import math
from math import gcd
from math import isqrt, ceil
import owiener
import subprocess
import os
import re


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


def yafu_factor(N, e, ct):

    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        yafu_path = os.path.join(script_dir, "tools", "yafu.exe")

        if not os.path.isfile(yafu_path):
            print(f"yafu not found: {yafu_path}")
            return None

        result = subprocess.run(
            [yafu_path], 
            input = f"factor({N})\n",
            text = True,
            shell = True,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            timeout = 600
        )

        

        factors = []
        for line in result.stdout.splitlines():
            line = line.strip()
            m = re.match(r'(?:P\d+|prp\d+|c\d+)\s*=\s*([0-9]+)', line)
            if m:
                factors.append(int(m.group(1)))
    
        if not factors:
            print("Not found")
            return None
        
        p = 1
        phi = 1
        for p in factors:
            phi *= (p-1)

        d = pow(e, -1, phi)
        plain_hex = pow(ct, d, N)
        plain_text = long_to_bytes(plain_hex)

        return plain_text.decode()

    except Exception as e:
        print(f"Decryption error: {e}")
        return "Decryption failed" #復号失敗



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



def low_index(N, e, ct): #低指数攻撃プログラム

    try:    
        plain_hex,exact = iroot(e, ct)

        if exact:
            plain_text = long_to_bytes(plain_hex)
            return plain_text.decode()
    except Exception as e:
        Wiener(N, e, ct)



def squared_index(N, e, ct):

    try:    
        f = math.isqrt(N)
        phi = (f-1)*f
        d = pow(e, -1, phi)
        plain_hex = pow(ct, d, N)
        plain_text = long_to_bytes(plain_hex)
        return plain_text.decode()
    except Exception as e:
        yafu_factor(N, e, ct)


def N_prime(N, e, ct):

    try:    
        f = math.isqrt(N)
        phi = N-1
        d = pow(e, -1, phi)
        plain_hex = pow(ct, d, N)
        plain_text = long_to_bytes(plain_hex)
        return plain_text.decode()
    except Exception as e:
        squared_index(N, e, ct)
         #復号失敗


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
            Fermat_factor(N, e, ct)


def is_square(n):
    s = isqrt(n)
    return s * s == n

def Fermat_factor(N, e, ct):

    max_diff=10**6
    a = isqrt(N)
    if a * a < N:
        a += 1

    limit = max_diff // 2
    
    for _ in range(limit):
        diff = a*a - N
        if is_square(diff):  # b^2 なら即 return
            b = isqrt(diff)
            p = a + b
            q = a - b
        
            try:
                phi = (p-1) * (q-1)
                d = pow(e, -1, phi)
                plain_hex = pow(ct, d, p*q)
                plain_text = long_to_bytes(plain_hex)
                return plain_text.decode()
            except Exception as e:
                N_prime(N, e, ct)
                #復号失敗

        a += 1
    N_prime(N, e, ct)
    