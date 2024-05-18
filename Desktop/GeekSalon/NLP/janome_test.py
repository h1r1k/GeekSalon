# janomeからTokenizerをインポート
from janome.tokenizer import Tokenizer

# 変数tで扱えるようにする
t = Tokenizer()

# 形態素解析したものを一つずつ表示
for token in t.tokenize('すもももももももものうち'):
    print(token)

# 分かち書きモードにする
t = Tokenizer(wakati=True)

# 文章を形態素解析する
tokens = t.tokenize("すもももももももものうち")

 # list型に変換して表示してみる
print(list(tokens))