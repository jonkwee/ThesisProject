import datetime
import pandas as pd


def date_to_microseconds(n):
    """returns interval of dates in microseconds based on n"""
    past_date = datetime.datetime.now() + datetime.timedelta(-n)
    past_micro = (past_date - datetime.datetime(1601, 1, 1, 0, 0)).total_seconds() * 1000000
    return past_micro


def convert_dict_to_series_sort(dictionary):
    return pd.Series(dictionary).sort_values(ascending=False)
