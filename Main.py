from LanguageProcessingController import LanguageProcessingController
from UserHistoryController import UserHistoryController as UHC
import Utilities
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from google import google
import json, requests

processed_text = UHC.get_recent_key_terms(2)

LPC = LanguageProcessingController(processed_text)

top_used_words = Utilities.convert_dict_to_series_sort(LPC.count_words).head(10)


def get_chunks(l):
    list_of_chunk = []
    for st in l:
        for t in st:
            if not isinstance(t, tuple):
                list_of_chunk.append((re.sub('[\/\(\)A-Z]', '', t.pformat())))
    return list_of_chunk

# print(top_used_words.keys())
# print(get_chunks(LPC.chunked))

def filter_chunk_by_top_used_words():
    filtered = []
    for word in top_used_words.keys():
        if re.match(r'[^\W]', word):
            for chunk in get_chunks(LPC.chunked):
                if word in chunk:
                    filtered.append(chunk)
    return np.unique(filtered)


def calculate_similarity():
    ar = []
    l = filter_chunk_by_top_used_words()
    tfidf = TfidfVectorizer()
    for i in range(len(l) - 1):
        d = (l[i], l[i+1])
        tfidf_matrix = tfidf.fit_transform(d).toarray()
        if np.sum(tfidf_matrix[0]) + np.sum(tfidf_matrix[1]) < 0.5*(len(tfidf_matrix[0])-(len(tfidf_matrix[0]) * 0.3))*2:
            ar.append(l[i+1])
    return ar

# terms based on user search
s = calculate_similarity()
# print("User Search Terms:", s)
# print()
# terms tangent to user search
def get_autosuggest_terms(term):
    URL = "http://suggestqueries.google.com/complete/search?client=firefox&q=" + term
    headers = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(URL, headers=headers)
    result = json.loads(response.content.decode('utf-8'))
    return result[1]

def google_search(term):
    result = google.search(term, 1)
    for entry in result:
        print("URL", entry.link)
        print("Name", entry.name)
        print("Desc", entry.description)
        print()



auto = get_autosuggest_terms(s[0])
google_search(auto[0])
