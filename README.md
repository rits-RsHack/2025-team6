# team6 - R'sA_Hack: RSA Decryption

## サービスの概要
CTFでよく出題される RSA 問題を自動で解析・解読する Web ツール\ 
`N`, `e`, `ct` を入力するだけで、代表的な攻撃手法を順に試し、復号結果を表示\

## プレビュー

## 使用技術
Python / Flask\
HTML / CSS / JavaScript\
API: factordb\

## 実装した機能
factordbを参照 → Nから p,q が得られれば `solve(p,q,e,ct)`\
p,q が得られない場合は順に試行: `Wiener`, `low_index`, `Fermat_factor`, `squared_index`, `N_prime`, `yafu_factor`\
入力 N,ct が複数の場合、`Håstad_attak`を実行\


## 改善できなかった点（実装できなかった機能）
仮にデコードが成功していた場合でも、flagに文字化けの部分が残っていたら解読失敗となってしまう点\

## フィードバックが欲しい点

