from gensim.models import KeyedVectors

model = KeyedVectors.load_word2vec_format('model.vec', binary=False)
model.save("model.kv")
word = input()
ans = model.most_similar(word)
print(ans)

wv = KeyedVectors.load('model.kv', mmap='readonly')
ans = wv.most_similar(positive=["フランス", "東京"], negative=["パリ"])
print(ans)