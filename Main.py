from LanguageProcessingController import LanguageProcessingController
from UserHistoryController import UserHistoryController as UHC
import Utilities
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

import os
from google import google

processed_text = UHC.get_recent_key_terms(5)

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

s = calculate_similarity()
result = google.search(s[0], 1)[0].link
print(result)