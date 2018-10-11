#!/usr/bn/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import csv
import datetime
from nameparser import HumanName


# import unicodecsv as csv


def dict_to_csv(dict_list, file_path):
    """
    Example:
        ::
        mydict = [{'id':1, 'name':'Sam', 'color':'blue'},
                  {'id':2, 'name':'Silvia', 'color':'green'}]
        dict_to_csv(mydict, 'path/to/csv.csv')
    Returns:
        color,id,name
        blue,1,Sam
        green,2,Silvia
    """
    # return pd.DataFrame(mydict).to_csv(file_path, index=False)
    with open(file_path, 'wb') as file_:
        w = csv.DictWriter(file_,
                           dict_list[0].keys(),
                           quotechar='"',
                           quoting=csv.QUOTE_MINIMAL,
                           skipinitialspace=True)
        w.writeheader()
        w.writerows(dict_list)


def datetime_to_date(dtime):
    """
    :rtype: str
    In mysql proper format YYYY-MM-DD
    """
    try:
        return datetime.datetime.strptime(dtime, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
    except:
        return None


def dicts_list_to_list_of_internal_values_with(key, dicts_list):
    return map(lambda dic: dic[key], dicts_list)


def names_match(a, b):
    name_a = HumanName(a)
    name_b = HumanName(b)

    name_a.capitalize(force=True)
    name_b.capitalize(force=True)

    if name_a.first == name_b.first and name_a.last == name_b.last:
        return True
    else:
        return False


def str_match_with_same_key_value(dic, key, dic_list_2):
    if key != 'name':
        return next((dic_2 for dic_2 in dic_list_2 if dic_2[key].lower() == dic[key].lower()), None)
    else:
        return next((dic_2 for dic_2 in dic_list_2 if names_match(dic_2[key], dic[key])), None)
