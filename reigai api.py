import requests

number = 13373801376856352919495636794117610920860037770702465464324474778341963699665011787021257

url = f"https://factordb.com/api?query={number}"
try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if data['status'] == "FF":
        factors = data.get('factors',[])
        if len(faactors) >= 2:
            p = data['factors'][0][0]
            q = data['factors'][1][0]
            print(f"p = {p}")
            print(f"q = {q}")
        else:
            print("Two factors could not be found")
            #因数が2つ以上存在しない
    else:
        print("It was not a complete prime factorization")
        #完全な素因数分解が不可
except requests.exceptions.RequestException as e:
    print(f"A communication error has occurred: {e}")
    #通信エラー
except ValueError as e:
    print(f"Analysis of JSON failed: {e}")
    #JSONの解析に失敗
except IndexError as e:
    print(f"Insufficient factor information :{e}")
    #因数の情報が不足
except Exception as e:
    print(f"An unexpected error has occurred :{e}")
    #その他の予期せぬエラー


