from lark import Lark, Transformer

# AClang.lark から文法を読み込む
with open("AClang.lark", "r", encoding="utf-8") as f:
    grammar = f.read()

# 変換器
class AClangTransformer(Transformer):
    def start(self, items):
        return "\n".join(items)
    
    def out_cmd(self, items):
        # items[0] には後ろの式が入っている
        expr = items[0]
        return f"cout << {expr} << endl;"
    
    def var_cmd(self, items):
        name = items[0]
        expr = items[1]
        return f"auto {name} = {expr};"
    
    def read_expr(self, items):
        return "[](){ string s; cin >> s; return s; }()"
    
    def iread_expr(self, items):
        return "[](){ int n; cin >> n; return n; }()"
    
    def add(self, items):
        number1 = items[0]
        number2 = items[1]
        return f"({number1} + {number2})"
    
    def sub(self, items):
        number1 = items[0]
        number2 = items[1]
        return f"({number1} - {number2})"
    
    def mul(self, items):
        number1 = items[0]
        number2 = items[1]
        return f"({number1} * {number2})"
    
    def div(self, items):
        number1 = items[0]
        number2 = items[1]
        return f"(static_cast<double>({number1}) / {number2})"
    
    def rounddiv(self, items):
        number1 = items[0]
        number2 = items[1]
        return f"(static_cast<long long>({number1}) / static_cast<long long>({number2}))"
    
    def mod(self, items):
        number1 = items[0]
        number2 = items[1]
        return f"static_cast<long long>({number1}) % static_cast<long long>({number2})"
    
    def intpow(self, items):
        number1 = items[0]
        number2 = items[1]
        return f"intpow({number1}, {number2})"
    
    def modpow(self, items):
        number1 = items[0]
        number2 = items[1]
        number3 = items[2]
        return f"modpow({number1}, {number2}, {number3})"
    
    def doublepow(self, items):
        number1 = items[0]
        number2 = items[1]
        return f"pow({number1}, {number2})"
    
    def string(self, items):
        return items[0]
    
    def number(self, items):
        return items[0]
    
    def cname(self, items):
        return items[0]

# パーサーを作成
parser = Lark(grammar, parser="lalr", transformer=AClangTransformer())

# AClang.ac からAClangのコードを読み込む
with open("AClang.ac", "r", encoding="utf-8") as f:
    aclang_code = f.read()

# パーサーでC++に変換
cpp_code = parser.parse(aclang_code)
cpp_template = """\
#include <bits/stdc++.h>
using namespace std;

// x ^^ n のための繰り返し2乗法
long long intpow(long long x, long long n) {
    long long ret = 1;
    while (n > 0) {
        if (n & 1) ret *= x;
        x *= x;
        n >>= 1;
    }
    return ret;
}

// modpow のための繰り返し2乗法
long long modpow(long long x, long long n, long long MOD) {
    long long ret = 1;
    while (n > 0) {
        if (n & 1) ret = ret * x % MOD;
        x = x * x % MOD;
        n >>= 1;
    }
    return ret;
}

int main() {
"""

# AClang.cpp にC++に変換したコードを書き込む
with open("AClang.cpp", "w", encoding="utf-8") as f:
    f.write(cpp_template)
    f.write(str(cpp_code))
    f.write("\n}")