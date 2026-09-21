# AClang
競技プログラミングに適した言語を目指して開発しています

## 文法
AClangの文法は以下のようなものです。実装済みのものも、今後実装予定のものも、まとめて掲載します。
```
// コメント
// 以下コメント
/* コメント */

// 代入
a = "Hello" // str
a = 1 // int
a = 1.0 // double
a = true // bool

// リスト
l = [1, 5, 3] // list
l = int[] // 空のlist (intを格納)
l = int[5](0) // [0, 0, 0, 0, 0]
l = int[H][W](0) // H行W列の２次元配列を0で初期化
l[3] // lの3番目の要素 (0-indexed)

// 演算子
+ 加算
- 減算
* 乗算
/ 除算 (int同士では計算結果もint, どちらかにdoubleが含まれれば計算結果はdouble)
** べき乗
% 係数

< より小さい
> より大きい
<= 次の値以下
>= 次の値以上
== 等式
!= 非等価

&& 論理積 AND
|| 論理和 OR
! 否定 NOT

// 入力
s = read // str型
n = iread // int型
m, n = iread // 空白・改行区切りの要素をint型で受け取り、それぞれm, nに格納
l = iread[n] // n個の空白・改行区切りの要素をint型で受け取り、配列に格納

// 出力
out a // aを出力 末尾に改行が入る
out 1 + 2 // 3
out "Hello" // Hello
out n, m // n m
print a // aを出力 末尾に改行が入らない
ynout 条件式 // true のとき Yes, false のとき No をout
 
// if文
if 式
    処理
elif 式
    処理
else
    処理
end

// 例
if n == 1
    out "nは1"
elif n != 2
    n -= 2 // n = n - 2
else
    n++ // n = n + 1
end

// for文Ⅰ 添字と回数のみ
rep 添字, 回数
    処理
end

 // 例
repp i, 5:
	out i

// for文Ⅱ
for 添字 in (start)..(stop)..(step) //stepは省略可
処理
end

// 例
for i in 1..12..2
out i
end

// for文 Ⅲ
for 変数 in 列
	処理
end

// 例
l = [1, 3, 5, 9, 0]
for x in l
out x
end

/* break を使うとループを途中で抜けることができる
continue を使うと後の処理を飛ばして次のループへ進むことができる */

// while 文
while 条件式
	処理
end

// 例
n = 5
while n < 5
	n–
	out n
end

// 関数
// 定義
def 関数名(パラメータ)
	return 戻り値
end

// 例
A = 3
B = 5
def a_plus_b(int a, int b)
	a++
	b -= 2
	return a + b
out a_plus_b(A, B) // 7

// 組み込み関数など
min() // 与えられた2つ以上の数値の中の最小値 数値をリストとして与えることも可能
max() // 与えられた2つ以上の数値の中の最大値 数値をリストとして与えることも可能
sum() // リストに含まれる値の合計
len(s) // str s の長さ
s[1:4] // sの1番目から4番目をスライス
l.sort(begin, end, rev)
l.sort() // lを全部昇順ソート 
l.sort(rev) // lを全部降順ソート
l.sort(2, 5) // lの2番目から5番目まで昇順ソート (0-indexed)
INF // 1 << 60 (2の60乗)
mod998 // 998244353
mod107 // 1000000007
```