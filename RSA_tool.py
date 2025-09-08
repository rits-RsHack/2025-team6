from Crypto.Util.number import long_to_bytes
import requests
from gmpy2 import iroot
import math
from math import gcd
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
            print("No factors found by yafu")
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
        print(f"yafu Decryption error: {e}")
        return "yafu Decryption failed" #復号失敗



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



def super_low_index(e, ct):

    if e == 1:
        plain_text = long_to_bytes(ct)
        return plain_text.decode()
    else:
        return "Decryption failed" #復号失敗


def squared_index(N, e, ct):

    try:    
        f = math.isqrt(N)
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
        f = math.isqrt(N)
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

ct = 320721490534624434149993723527322977960556510750628354856260732098109692581338409999983376131354918370047625150454728718467998870322344980985635149656977787964380651868131740312053755501594999166365821315043312308622388016666802478485476059625888033017198083472976011719998333985531756978678758897472845358167730221506573817798467100023754709109274265835201757369829744113233607359526441007577850111228850004361838028842815813724076511058179239339760639518034583306154826603816927757236549096339501503316601078891287408682099750164720032975016814187899399273719181407940397071512493967454225665490162619270814464
N = 580642391898843192929563856870897799650883152718761762932292482252152591279871421569162037190419036435041797739880389529593674485555792234900969402019055601781662044515999210032698275981631376651117318677368742867687180140048715627160641771118040372573575479330830092989800730105573700557717146251860588802509310534792310748898504394966263819959963273509119791037525504422606634640173277598774814099540555569257179715908642917355365791447508751401889724095964924513196281345665480688029639999472649549163147599540142367575413885729653166517595719991872223011969856259344396899748662101941230745601719730556631637
e = 65537

result = yafu_factor(N, e, ct)
print(result)