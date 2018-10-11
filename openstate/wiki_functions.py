#!/usr/bn/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import utils


def external_link(text):
    return '[' + text + ']'


def link(text):
    return '[[' + text + ']]'


def titlize(var, type, **kwargs):
    if type == 'bill_id':
        return link(var + ', ' + kwargs['session_name'])  # e.g. '[[SB 323, 2017-18 session]]'
    elif type == '':
        ''
    else:
        return link(var)


def name_for_DataTransfer(field_name, template_name):
    """
    Changes 'field_name' to 'template_name[field_name]'
    Args:
        field_name:
        template_name:
    """
    return template_name + external_link(field_name)


def modify_dict_for_DataTransfer(dic, template_name):
    """
    Modifies all dic keys from 'key_name' to 'template_name[key_name]' to work with DataTransfer:
    https://www.mediawiki.org/wiki/Extension:Data_Transfer#Importing_CSV_files
    Args:
        dic: Dictionary of data with keys matching a wiki template fields
        template_name:
    """
    for key in dic.keys():
        if key == 'Title':
            pass
        else:
            new_key = name_for_DataTransfer(key, template_name)
            dic[new_key] = dic.pop(key)
    return dic


def write_to_csv_file_for_DataTransfer(inst, dics):
    """
    Writes/Overwrites CSV files with data supplied in dictionaries
    Note: Dictionary keys will be changed to work with DataTransfer extension
    Args:
        inst: Instance of the class (Legislator, Committee..) to indicate which file to write to and what's the template name
        dics: Dictionaries which will be written into a CSV file
    """
    modified_dics = [modify_dict_for_DataTransfer(
        dic,
        inst.template_name) for dic in dics]
    utils.dict_to_csv(modified_dics, inst.file_path)
