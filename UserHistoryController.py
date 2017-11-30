import os
import sqlite3
import numpy as np
import pandas as pd
from collections import defaultdict
import Utilities


# Only works for Google Chrome
class UserHistoryController:
    def __init__(self):
        self.visitString = "VISIT COUNT"
        self.keyWordsString = "KEY WORDS"
        self.urlView = self.get_from_db(self.visitString)
        self.mainUrlView = pd.Series()
        self.get_main_url()

    def get_from_db(self, keyString):
        """Gets data from Chrome History Database"""
        data_path = os.path.expanduser('~') + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        history_db = os.path.join(data_path, 'history')
        c = sqlite3.connect(history_db)
        cursor = c.cursor()
        select_statement = ""
        results = []

        if keyString == self.visitString:
            select_statement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url" \
                               " ORDER BY urls.visit_count DESC;"
        elif keyString == self.keyWordsString:
            select_statement = "SELECT keyword_search_terms.lower_term FROM keyword_search_terms"

        if select_statement != "":
            cursor.execute(select_statement)
            results = cursor.fetchall()
            c.close()

        return np.array(results)

    @staticmethod
    def get_recent_key_terms(n):
        """Gets the first n days of key search terms"""
        data_path = os.path.expanduser('~') + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        history_db = os.path.join(data_path, 'history')

        c = sqlite3.connect(history_db)
        cursor = c.cursor()
        past_micro = Utilities.date_to_microseconds(n)

        select_statement = "SELECT keyword_search_terms.lower_term " \
                           "FROM urls, keyword_search_terms WHERE (urls.id = keyword_search_terms.url_id AND " \
                           "urls.last_visit_time > %s) ORDER BY urls.last_visit_time DESC;" % past_micro

        cursor.execute(select_statement)
        results = cursor.fetchall()
        c.close()
        return np.array(results)

    # get main portion of url from user history
    def get_main_url(self):
        returnable_dictionary = defaultdict(int)
        for item in self.urlView:
            url = item[0]
            double_slash_index = url.index("//") + len("//")
            single_slash_index = url.index("/", double_slash_index)
            returnable_dictionary[url[double_slash_index: single_slash_index]] += 1
        self.mainUrlView = pd.Series(returnable_dictionary).sort_values(ascending=False)

    # get first n visited websites
    def get_most_visited(self, n):
        return self.mainUrlView[:n]


UHC = UserHistoryController()
#print(UHC.get_most_visited(10))
