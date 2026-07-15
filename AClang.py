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
        return f"{number1} + {number2}"
    
    def string(self, items):
        return items[0]
    
    def number(self, items):
        return items[0]
    
    def cname(self, items):
        return items[0]

# パーサーを作成
perser = Lark(grammar, parser="lalr", transformer=AClangTransformer())

# AClang.ac からAClangのコードを読み込む
with open("AClang.ac", "r", encoding="utf-8") as f:
    aclang_code = f.read()

# パーサーでC++に変換
cpp_code = perser.parse(aclang_code)
cpp_template = """#include <bits/stdc++.h>
using namespace std;

int main() {
"""

# AClang.cpp にC++に変換したコードを書き込む
with open("AClang.cpp", "w", encoding="utf-8") as f:
    f.write(cpp_template)
    f.write(str(cpp_code))
    f.write("\n}")