from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

sent = "Hello, I am testing if this works. if this doesn't work, i don't know what to do. my thesis is due tomorrow"
stop_words = set(stopwords.words("english"))

word = word_tokenize(sent)
filtered_sentence = [w for w in word if w not in stop_words]
print(word)
print(filtered_sentence)