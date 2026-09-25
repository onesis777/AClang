from lark import Lark, Transformer

# AClang.lark から文法を読み込む
with open("AClang.lark", "r", encoding="utf-8") as f:
    grammar = f.read()

# 変換器
class AClangTransformer(Transformer):
    def __init__(self):
        super().__init__()
        # 宣言済みの変数を記憶しておくset
        self.declared_vars = set()
    
    def start(self, items):
        return "\n".join(items)
    
    def block(self, items):
        return "\n".join(items)
    
    def var_list(self, items):
        return items

    def expr_list(self, items):
        return items
    
    def if_stmt(self, items):
        # items から None を取り除く
        items = [x for x in items if x is not None]
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
    
    def for_stmt(self, items):
        # items から None を取り除く
        items = [x for x in items if x is not None]
        for_var = items[0] # 添字
        start_expr = items[1]
        stop_expr = items[2]
        block_code = items[-1]
        step_expr = "1" if len(items) == 4 else items[3]
        return f"""for (long long {for_var} = {start_expr}; {for_var} < {stop_expr}; {for_var} += {step_expr}) {{
{block_code}
}}"""

    def while_stmt(self, items):
        while_cond = items[0]
        block_code = items[1]
        return f"""while ({while_cond}) {{
{block_code}
}}"""

    def break_stmt(self, items):
        return "break;"

    def continue_stmt(self, items):
        return "continue;"

    def out_cmd(self, items):
        exprs = items[0]
        if isinstance(exprs, list):
            exprs = ' << " " << '.join(exprs)
        return f'std::cout << std::boolalpha << {exprs} << "\\n";'
    
    def var_cmd(self, items):
        vars_ = items[0]
        exprs = items[1]
        # 未宣言の変数(配列アクセスではないもの)
        new_vars = [v for v in vars_ if v not in self.declared_vars and "[" not in v]
        
        # 複数の入力をカンマ区切りで同時に受け取る
        if len(vars_) > 1 and len(exprs) == 1 and "std::cin" in exprs[0]:
            # 新しい変数だけを long long で宣言する
            decl = f"long long {', '.join(new_vars)};\n" if new_vars else ""
            cin = f"std::cin >> {' >> '.join(vars_)};"
            self.declared_vars.update(new_vars) # 未宣言の変数を declared_vars に追加
            return f"{decl}{cin}"

        # 単一代入
        if len(vars_) == len(exprs) == 1:
            var_name = vars_[0]
            # 再代入や配列アクセスの場合、autoを付けない
            if var_name in self.declared_vars or "[" in var_name:
                return f"{var_name} = {exprs[0]};"
            # 変数宣言時は、autoを付ける
            # 宣言した変数は declared_vars に追加する
            else:
                self.declared_vars.add(var_name)
                return f"auto {var_name} = {exprs[0]};"

        # 複数代入
        var_str = ", ".join(vars_)
        expr_str = ", ".join(exprs)
        # すべて未宣言の変数なら auto をつける
        if len(new_vars) == len(vars_):
            self.declared_vars.update(vars_)
            return f"auto [{var_str}] = std::make_tuple({expr_str});"
            
        # 宣言済みの変数が混ざっている場合は、新しい変数だけ宣言してから std::tie を使う
        else:
            decl = f"long long {', '.join(new_vars)};\n" if new_vars else ""
            self.declared_vars.update(new_vars)
            return f"{decl}std::tie({var_str}) = std::make_tuple({expr_str});"
    
    def sort_asc(self, items):
        target = items[0]
        return f"std::sort({target}.begin(), {target}.end());"
    
    def sort_desc(self, items):
        target = items[0]
        return f"std::sort({target}.rbegin(), {target}.rend());"
    
    def append_cmd(self, items):
        target = items[0]
        value = items[1]
        return f"{target}.push_back({value});"
    
    def vector(self, items):
        elements = [x for x in items if x is not None] # None を取り除いた vector の中身
        # 空配列[]
        if elements == []:
            return "std::vector<long long>()"
        # 二次元空配列[[]]
        elif len(items) == 1 and items[0] == "std::vector<long long>()":
            return "std::vector<std::vector<long long>>()"
        return f"std::vector{{{', '.join(elements)}}}"
    
    def vector_access(self, items):
        var_name = items[0]
        index_expr = items[1]
        return f"{var_name}[{index_expr}]"
    
    def vector_init(self, items):
        value = items[0]
        size = items[1]
        if "std::vector" in value:
            return f"std::vector({size}, {value})"
        return f"std::vector<long long>({size}, {value})"
    
    def read_vector(self, items):
        return f"""[&]{{
    std::vector<string> _v({items[0]});
    for (string& _x : _v) std::cin >> _x;
    return _v;
}}()"""
    
    def iread_vector(self, items):
        return f"""[&]{{
    std::vector<long long> _v({items[0]});
    for (long long& _x : _v) std::cin >> _x;
    return _v;
}}()"""

    def read_expr(self, items):
        return "[]{ string s; std::cin >> s; return s; }()"
    
    def iread_expr(self, items):
        return "[]{ int n; std::cin >> n; return n; }()"
    
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

// オンラインジャッジでなければ配列外参照にエラーを出す
#ifndef ONLINE_JUDGE
#define _GLIBCXX_DEBUG
#endif

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