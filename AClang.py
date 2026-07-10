from lark import Lark, Transformer

# AClang.lark から文法を読み込む
with open("AClang.lark", "r", encoding="utf-8") as f:
    grammar = f.read

# 変換器
class AClangTransformer(Transformer):
    def start(self, items):
        return "\n".join(items)
    
    def out_cmd(self, items):
        # items[0] には後ろの式が入っている
        expr = items[0]
        return f"std::cout << {expr} << endl;"
    
    def string(self, items):
        return items[0]
    
    def number(self, items):
        return items[0]

# パーサーを作成
perser = Lark(grammar, perser="lalr", transformer=AClangTransformer())