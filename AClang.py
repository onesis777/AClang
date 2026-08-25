from lark import Lark, Transformer

# AClang.lark から文法を読み込む
with open("AClang.lark", "r", encoding="utf-8") as f:
    grammar = f.read()

# 変換器
class AClangTransformer(Transformer):
    def start(self, items):
        return "\n".join(items)
    
    def block(self, items):
        return "\n".join(items)
    
    def if_stmt(self, items):
        # if
        if_cond = items[0]
        if_block = items[1]
        cpp_code = [f"if {if_cond} {{\n    {if_block}\n}} "]
        
        # else
        i = 2
        while i < len(items):
            # 最後の要素なら else
            # 最後の餃子か
            if i == len(items) - 1:
                else_block = items[i]
                cpp_code.append(f"else {{\n    {else_block}\n}}")
                break
            # elif
            else:
                elif_cond = items[i]
                elif_block = items[i + 1]
                cpp_code.append(f"else if {elif_cond} {{\n    {elif_block} \n}} ")
                i += 2
                
        return "".join(cpp_code)

    def out_cmd(self, items):
        expr = items[0]
        return f'std::cout << std::boolalpha << {expr} << "\\n";'
    
    def var_cmd(self, items):
        name = items[0]
        expr = items[1]
        return f"auto {name} = {expr};"
    
    def read_expr(self, items):
        return "[](){ string s; std::cin >> s; return s; }()"
    
    def iread_expr(self, items):
        return "[](){ int n; std::cin >> n; return n; }()"
    
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
        return f"(static_cast<long long>({number1}) % static_cast<long long>({number2}))"
    
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
    
    def eq(self, items):
        expr1 = items[0]
        expr2 = items[1]
        return f"({expr1} == {expr2})"

    def neq(self, items):
        expr1 = items[0]
        expr2 = items[1]
        return f"({expr1} != {expr2})"

    def lte(self, items):
        expr1 = items[0]
        expr2 = items[1]
        return f"({expr1} <= {expr2})"

    def gte(self, items):
        expr1 = items[0]
        expr2 = items[1]
        return f"({expr1} >= {expr2})"

    def lt(self, items):
        expr1 = items[0]
        expr2 = items[1]
        return f"({expr1} < {expr2})"

    def gt(self, items):
        expr1 = items[0]
        expr2 = items[1]
        return f"({expr1} > {expr2})"
        
    def log_or(self, items):
        expr1 = items[0]
        expr2 = items[1]
        return f"({expr1} || {expr2})"
    
    def log_and(self, items):
        expr1 = items[0]
        expr2 = items[1]
        return f"({expr1} && {expr2})"
    
    def log_not(self, items):
        expr = items[0]
        return f"!({expr})"
    
    def string(self, items):
        return items[0]
    
    def number(self, items):
        return items[0]
    
    def cname(self, items):
        return items[0]
    
    def true_lit(self, items):
        return items[0]
    
    def false_lit(self, items):
        return items[0]

# パーサーを作成
parser = Lark(grammar, parser="lalr", transformer=AClangTransformer())

# AClang.ac からAClangのコードを読み込む
with open("AClang.ac", "r", encoding="utf-8") as f:
    aclang_code = f.read()

# パーサーでC++に変換
cpp_code = parser.parse(aclang_code)
cpp_template = """\
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cmath>
#include <numeric>
#include <map>
#include <set>
#include <queue>
#include <stack>
#include <tuple>

// 入出力の高速化
struct Init { Init() { std::ios::sync_with_stdio(0); std::cin.tie(0); } }init;

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

int main(void) {
"""

# AClang.cpp にC++に変換したコードを書き込む
with open("AClang.cpp", "w", encoding="utf-8") as f:
    f.write(cpp_template)
    f.write(str(cpp_code))
    f.write("\nreturn 0;\n}")