main.pyは,入力の受け取りと関数の呼び出し部分を担っている.

RSA_tool.pyは,RSA暗号解読にかかわる関数を置いている.

RSA_tool.pyの関数には,factorDBでpまたはqが巨大素数の積Nから分かった場合に限りsolve関数の実行をする。p,qが不明な場合[Wiener, low_index, Fermat_factor, squared_index, N_prime, yafu_factor]の順番で関数を実行する.

Hastadのブロードキャスト攻撃は,Nとctの入力が複数になるため,場合分けで関数を実行している.(複数の入力にはカンマ「,」を使う)

プログラムのN,e,ctはindex.htmlのname="N",name="e",name="ct"がそれぞれ対応しており,decode結果は{{ output }}のテンプレート変数で表示することができる.