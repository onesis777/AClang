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
    
    def typed_var(self, items):
        var_name = items[0]
        type_str = items[1]
        
        types = {
            "int": "long long",
            "float": "double",
            "string": "std::string",
            "str": "std::string"
        }
        
        cpp_type = types.get(type_str, type_str)
        return (var_name, cpp_type)

    def if_stmt(self, items):
        # items から None を取り除く
        items = [x for x in items if x is not None]
        # if
        if_cond = items[0]
        if_block = items[1]
        cpp_code = [f"if ({if_cond}) {{\n    {if_block}\n}} "]
        
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

    def foreach_stmt(self, items):
        # items から None を取り除く
        items = [x for x in items if x is not None]
        for_var = items[0]
        iterable = items[1]
        block_code = items[2]
        return f"""for (auto&& {for_var} : {iterable}) {{
{block_code}
}}"""
    
    def while_stmt(self, items):
        while_cond = items[0]
        block_code = items[1]
        return f"""while ({while_cond}) {{
{block_code}
}}"""

    def rep_stmt(self, items):
        rep_var = "_i" if items[0] is None else items[0]
        stop_var = items[1]
        block_code = items[-1]
        return f"""for (long long {rep_var} = 0; {rep_var} < {stop_var}; {rep_var}++) {{
{block_code}
}}
"""

    def def_stmt(self, items):
        items = [x for x in items if x is not None]
        func_name = items[0]
        block_code = items[-1]
        
        # itemsの0番目が関数名、-1番目がblockなので、それ以外が引数
        args = items[1:-1]
        cpp_args = []
        
        for arg in args:
            # 型注釈がついているか (=タプルか)
            if isinstance(arg, tuple):
                cpp_args.append(f"{arg[1]} {arg[0]}")
            # 型注釈がついていなければlong long 型とする
            else:
                cpp_args.append(f"long long {arg}")
                
        cpp_args = ", ".join(cpp_args)
        
        # 引数以外の外の変数をすべてキャプチャするラムダ式
        return f"""auto {func_name} = [&]( {cpp_args} ) {{
{block_code}
}};"""
    
    def return_stmt(self, items):
        return f"return {items[0]};"
    
    def func_call(self, items):
        # None を取り除く
        items = [x for x in items if x is not None]
        func_name = items[0]
        args = items[1:]
        args = ', '.join(args)
        return f"{func_name}({args})"

    def func_call_cmd(self, items):
        # 返り値のない関数呼び出しの場合は、末尾にセミコロンをつける
        return f"{items[0]};"
    
    def break_stmt(self, items):
        return "break;"

    def continue_stmt(self, items):
        return "continue;"

    def out_cmd(self, items):
        exprs = items[0]
        if isinstance(exprs, list):
            exprs = ' << " " << '.join(exprs)
        return f'std::cout << std::boolalpha << {exprs} << "\\n";'
    
    def print_cmd(self, items):
        exprs = items[0]
        if isinstance(exprs, list):
            exprs = ' << " " << '.join(exprs)
        return f"std::cout << std::boolalpha << {exprs};"
    
    def yn_lower(self, items):
        cond = items[0]
        return f'std::cout << ({cond} ? "Yes" : "No") << "\\n";'
    
    def yn_upper(self, items):
            cond = items[0]
            return f'std::cout << ({cond} ? "YES" : "NO") << "\\n";'

    def var_cmd(self, items):
        raw_vars = items[0]
        exprs = items[1]
        
        vars_ = []
        typed_vars = {}
        for v in raw_vars:
            if isinstance(v, tuple):
                vars_.append(v[0])
                typed_vars[v[0]] = v[1]
            else:
                vars_.append(v)

        # 未宣言の変数(配列アクセスではないもの)
        new_vars = [v for v in vars_ if v not in self.declared_vars and "[" not in v]
        
        # 複数の入力をカンマ区切りで同時に受け取る
        if len(vars_) > 1 and len(exprs) == 1 and "std::cin" in exprs[0]:
            # ラムダ式の文字列の中に "string" が入っていれば read (文字列入力) と判定
            if "std::string" in exprs[0]:
                default_type = "std::string"
            else:
                default_type = "long long" # iread (数値入力)

            # 新しい変数だけ宣言する（型注釈があればそれを優先、なければ default_type）
            if new_vars:
                decl_lines = [f"{typed_vars[v]} {v};" if v in typed_vars else f"{default_type} {v};" for v in new_vars]
                decl = "\n".join(decl_lines) + "\n"
            else:
                decl = ""
            
            cin = f"std::cin >> {' >> '.join(vars_)};"
            self.declared_vars.update(new_vars) # 未宣言の変数を declared_vars に追加
            return f"{decl}{cin}"

        # 単一代入
        if len(vars_) == len(exprs) == 1:
            var_name = vars_[0]
            
            # 型注釈がある場合は指定された型で宣言する
            if var_name in typed_vars:
                cpp_type = typed_vars[var_name]
                self.declared_vars.add(var_name)
                return f"{cpp_type} {var_name} = {exprs[0]};"

            # 再代入や配列アクセスの場合、autoを付けない
            if var_name in self.declared_vars or "[" in var_name:
                return f"{var_name} = {exprs[0]};"
            # 変数宣言時は、autoを付ける
            else:
                self.declared_vars.add(var_name)
                return f"auto {var_name} = {exprs[0]};"

        # 複数代入
        var_str = ", ".join(vars_)
        expr_str = ", ".join(exprs)
        
        # 複数代入の中に型注釈が含まれる場合は tie を使う
        if typed_vars:
            if new_vars:
                decl_lines = [f"{typed_vars[v]} {v};" if v in typed_vars else f"long long {v};" for v in new_vars]
                decl = "\n".join(decl_lines) + "\n"
            else:
                decl = ""
            self.declared_vars.update(new_vars)
            return f"{decl}std::tie({var_str}) = std::make_tuple({expr_str});"

        # すべて未宣言の変数なら auto をつける
        if len(new_vars) == len(vars_):
            self.declared_vars.update(vars_)
            return f"auto [{var_str}] = std::make_tuple({expr_str});"
            
        # 宣言済みの変数が混ざっている場合は、新しい変数だけ宣言してから std::tie を使う
        else:
            decl = f"long long {', '.join(new_vars)};\n" if new_vars else ""
            self.declared_vars.update(new_vars)
            return f"{decl}std::tie({var_str}) = std::make_tuple({expr_str});"

    def add_assign_cmd(self, items):
        target = items[0]
        value = items[1]
        return f"{target} += {value};"

    def sub_assign_cmd(self, items):
        target = items[0]
        value = items[1]
        return f"{target} -= {value};"

    def mul_assign_cmd(self, items):
        target = items[0]
        value = items[1]
        return f"{target} *= {value};"

    def div_assign_cmd(self, items):
        target = items[0]
        value = items[1]
        return f"{target} /= {value};"
    
    def rounddiv_assign_cmd(self, items):
        target = items[0]
        value = items[1]
        return f"{target} = static_cast<long long>({target}) / static_cast<long long>({value});"

    def mod_assign_cmd(self, items):
        target = items[0]
        value = items[1]
        return f"{target} %= {value};"
    
    def intpow_assign_cmd(self, items):
        target = items[0]
        value = items[1]
        return f"{target} = intpow({target}, {value});"

    def doublepow_assign_cmd(self, items):
        target = items[0]
        value = items[1]
        return f"{target} = pow({target}, {value});"

    def inc_cmd(self, items):
        target = items[0]
        return f"{target}++;"

    def dec_cmd(self, items):
        target = items[0]
        return f"{target}--;"

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
        elements = [str(x) for x in items if x is not None]
        # 空配列[]
        if elements == []:
            return "std::vector<long long>()"
        # 要素が vector なら二次元以上として auto に型推論させる。
        if any("std::vector" in x for x in elements):
            return f"std::vector{{{', '.join(elements)}}}"
        # 数値配列は long long に固定する。
        return f"std::vector<long long>{{{', '.join(elements)}}}"
    
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
    std::vector<std::string> _v({items[0]});
    for (std::string& _x : _v) std::cin >> _x;
    return _v;
}}()"""
    
    def iread_vector(self, items):
        return f"""[&]{{
    std::vector<long long> _v({items[0]});
    for (long long& _x : _v) std::cin >> _x;
    return _v;
}}()"""

    def read_expr(self, items):
        return "[]{ std::string s; std::cin >> s; return s; }()"
    
    def iread_expr(self, items):
        return "[]{ long long n; std::cin >> n; return n; }()"
    
    def min(self, items):
        args = [str(x) for x in items if x is not None]
        if len(args) == 1:
            return f"min({args[0]})"
        return f"min({{{', '.join(args)}}})"
    
    def max(self, items):
        args = [str(x) for x in items if x is not None]
        if len(args) == 1:
            return f"max({args[0]})"
        return f"max({{{', '.join(args)}}})"
        
    def sum(self, items):
        args = [str(x) for x in items if x is not None]
        if len(args) == 1:
            return f"sum({args[0]})"
        return f"sum({{{', '.join(args)}}})"
    
    def chmin(self, items):
        num1 = items[0]
        num2 = items[1]
        return f"chmin({num1}, {num2})"
    
    def chmax(self, items):
        num1 = items[0]
        num2 = items[1]
        return f"chmax({num1}, {num2})"

    def count(self, items):
        iterable = items[0]
        value = items[1]
        return f"std::count({iterable}.begin(), {iterable}.end(), {value})"

    def ternary(self, items):
        cond = items[0]
        expr1 = items[1]
        expr2 = items[2]
        return f"({cond} ? {expr1} : {expr2})"

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

    def char(self, items):
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

template <typename T>
T min(const std::vector<T>& a) {
    if (a.empty()) return 0;

    T ret = a[0];
    for (auto x : a) {
        ret = std::min(ret, x);
    }
    return ret;
}

template <typename T>
T max(const std::vector<T>& a) {
    if (a.empty()) return 0;

    T ret = a[0];
    for (auto x : a) {
        ret = std::max(ret, x);
    }
    return ret;
}

template <typename T>
T sum(const std::vector<T>& a) {
    T total = 0;
    for (T x : a) {
        total += x;
    }
    return total;
}

template <typename T>
bool chmax(T &a, const T& b) {
    if (a < b) {
        a = b;
        return true;
    }
    return false;
}

template <typename T>
bool chmin(T &a, const T& b) {
    if (a > b) {
        a = b;
        return true;
    }
    return false;
}

int main(void) {
"""

# AClang.cpp にC++に変換したコードを書き込む
with open("AClang.cpp", "w", encoding="utf-8") as f:
    f.write(cpp_template)
    f.write(str(cpp_code))
    f.write("\nreturn 0;\n}")