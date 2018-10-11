#!/usr/bn/env python
# -*- coding: utf-8 -*-

"""Frugality in querying module"""

from __future__ import print_function
import copy
import pyopenstates

import config
from Singleton import Singleton


class Metadata:
    __metaclass__ = Singleton

    def __init__(self):
        pyopenstates.set_api_key(config.OPENSTATES_API_KEY)
        self.raw_dictionary = pyopenstates.get_metadata(state=config.STATE)
        self.latest_term_name = self.raw_dictionary['terms'][-1]['name']
        self.latest_session_name = self.raw_dictionary['terms'][-1]['sessions'][-1]

    def session_name(self, session_):
        display = self.raw_dictionary['session_details'][session_]['display_name'].lower()
        return display[0:5] + display[7:]

    def terms_to_sessions_dict(self):
        terms = copy.deepcopy(self.raw_dictionary['terms'])
        for i, term in enumerate(terms):
            new_term = {term['name']: term['sessions']}
            terms[i] = new_term
        return terms
