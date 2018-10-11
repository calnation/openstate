#!/usr/bn/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import MySQLdb
import MySQLdb.cursors
import utils
import db_models
import config

Senators_DB = 'cargo__state_senators'
AssemblyMembers_DB = 'cargo__state_representative'


def db_cursor():
    db = MySQLdb.connect(host=config.DB_HOST,
                         user=config.DB_USER,
                         passwd=config.DB_PASSWORD,
                         cursorclass=MySQLdb.cursors.DictCursor)
    db.set_character_set('utf8')
    cursor = db.cursor()
    cursor.execute("USE " + config.DB_NAME)
    return cursor


def db(table, dics_list):
    sql = ''
    for dic in dics_list:
        columns = tuple(dic)
        dics_size = len(dic)
        for i in range(dics_size):
            if type(dic[columns[i]]).__name__ == 'str':
                sql += '\'' + str(dic[columns[i]]) + '\''
            else:
                sql += str(dic[columns[i]])

            if (i < dics_size - 1):
                sql += ', '

    query = "insert into " + \
            str(table) + \
            " " + \
            str(columns) + \
            " values (" + sql + ")" + \
            "ON DUPLICATE KEY UPDATE " + \
            "a = a, b = b, c = c, d = d, e = e, f = f, g = g;"

    cursor = db_cursor()
    try:
        cursor.execute(query, dic.values())
        cursor.executemany(query, dic.values())
        cursor.commit()
    except:
        cursor.rollback()


def db_query(table, columns):
    cursor = db_cursor()
    # By default, when no fields are explicitly passed to select(), all fields
    # will be selected.
    cursor.execute("SELECT {} FROM {}".format(','.join(y for y in columns), table))
    # Save the dictionary to a separate variable
    dics_tuple = cursor.fetchall()
    return dics_tuple


def sync_ids(dics, table, mutual_key, id_key='_ID'):
    db_dics = db_query(table, [mutual_key, id_key])
    for dic in dics:
        db_dic = utils.str_match_with_same_key_value(dic, mutual_key, db_dics)
        if db_dic:
            dic[id_key] = db_dic[id_key]

    return dics


def sync():
    db_models.database.connect()
    query = db_models.CargoStateSenator.select()
