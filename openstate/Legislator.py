import pyopenstates

import LegislatorCommittee
import config
import state_utils
from Metadata import Metadata
from Tables import Tables


class Legislator(Tables):

    def __init__(self):
        Tables.__init__(self)
        self.template_name = 'Infobox legislator'

    def query(self, type='active', term_name=None):
        """
        Obtains raw data of legislators, defaults to active legislators from the latest term
        Args:
            term_name: term name as it comes from OpenStates API
            type: Either 'all' or 'active'

        Returns:
            String transformed
        """
        Tables.query(self)

        if type == 'all':
            if term_name is None:
                metadata = Metadata()
                term_name = metadata.latest_term_name
            legislators = pyopenstates.search_legislators(state=config.STATE,
                                                          term=term_name,
                                                          fields='id')
        else:  # 'active'
            legislators = pyopenstates.search_legislators(state=config.STATE,
                                                          active='true',  # default
                                                          fields='id')

        self.raw_dictionary = map(lambda dic: pyopenstates.get_legislator(dic['id'],
                                                                          fields=['id',
                                                                                  'full_name',
                                                                                  'url',
                                                                                  'roles',
                                                                                  # 'old_roles',
                                                                                  'party',
                                                                                  'district',
                                                                                  'chamber',
                                                                                  'offices',
                                                                                  'email']),
                                  legislators)

    def parse(self):
        legislator_table = []
        legislator_committee_table = []

        for legislator_dic in self.raw_dictionary:
            new_legislator_dic = self.table_row(legislator_dic)
            legislator_table.append(new_legislator_dic)

            for role_dic in legislator_dic['roles']:
                if role_dic['party']:
                    pass
                else:
                    legislator_committee_dic = LegislatorCommittee.table_row(legislator_dic['id'],
                                                                             role_dic)
                    legislator_committee_table.append(legislator_committee_dic)

        self.legislator_table = legislator_table
        self.legislator_committee_table = legislator_committee_table

    @staticmethod
    def table_row(legis_dic):
        return {
            'Title': legis_dic['full_name'],
            'os_leg_id': legis_dic['id'],
            'name': legis_dic['full_name'],
            'chamber': state_utils.chamber_name(legis_dic['chamber']),
            'website': legis_dic['url'],
            'active': legis_dic['active'],
            'district': legis_dic['district'],
            'email': legis_dic.get('email'),
            'phone': ', '.join(y.get('phone') for y in legis_dic['offices']),
        }


def leg_id_by_last_name(last_name_, term_name_):
    legislators = Legislator()
    legislators.query('all', term_name_)
    matches = filter(lambda legis: legis['last_name'] == last_name_,
                     legislators.raw_dictionary)
    ids = map(lambda legis_dict: legis_dict['id'], matches)  # e.g. ['CAL000366', 'CAL000461']
    if len(ids) > 1:
        return '|'.join(ids)  # returns string of list divided by |
    else:
        return ids[-1]
