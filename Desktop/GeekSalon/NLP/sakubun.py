import markovify
from janome.tokenizer import Tokenizer

# origin.txtファイルを開いて、読み込んだものを「text」変数に代入
with open("origin.txt", encoding="utf-8") as file:
    text = file.read()

# 出力
# print(text)

table = {
    '\n': '', #改行を削除
    '\r': '', #改行を削除
    '(': '（', #全角に変更
    ')': '）', #全角に変更
    '[': '［', #全角に変更
    ']': '］', #全角に変更
    '"': '”', #全角に変更
    "'": "’" #全角に変更
}

text = text.translate(str.maketrans(table))

# print(text)

t = Tokenizer(wakati=True)
tokens = t.tokenize(text)
tokens = list(tokens)
# print(tokens)

text_wakati = ""
# 分かち書きされた分だけループ
for i in range(len(tokens)):
    text_wakati += tokens[i]
# 改行するべきタイミングで改行をして読みやすくする
    if tokens[i] == '。' or tokens[i] == '！' or tokens[i] == '？':
        text_wakati += '\n'
# 単語間で空白を入れる
    else:
        text_wakati += ' '
# 出力
# print(text_wakati)

text_model = markovify.NewlineText(text_wakati, well_formed=False)

for _ in range(10):
    print(text_model.make_short_sentence(100).replace(" ", ""))