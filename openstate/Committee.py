import pyopenstates

import config
import state_utils
from Tables import Tables


class Committee(Tables):

    def __init__(self):
        Tables.__init__(self)
        self.template_name = 'Infobox committee'

    def query(self, type='all'):
        Tables.query(self)
        committees = pyopenstates.search_committees(state=config.STATE)
        self.raw_dictionary = map(lambda comm_dic: pyopenstates.get_committee(comm_dic['id'],
                                                                              fields=['id',
                                                                                      'chamber',
                                                                                      'sources',
                                                                                      'subcommittee',
                                                                                      'committee',
                                                                                      'parent_id']),
                                  committees)

    def parse(self):
        committee_table = []
        for committee_dic in self.raw_dictionary:
            new_committee_dic = self.table_row(committee_dic)
            committee_table.append(new_committee_dic)

        self.table = committee_table

    @staticmethod
    def table_row(committee_dic):
        new_committee_dic = {
            'id': committee_dic['id'],
            'chamber': state_utils.chamber_name(committee_dic['chamber']),
            'website': committee_dic['sources'][0]['url'],
        }

        if committee_dic['subcommittee']:
            new_committee_dic.update({
                'name': committee_dic['subcommittee'],
                'parent_id': committee_dic['parent_id'],
            })
        else:
            new_committee_dic.update({
                'name': committee_dic['committee'],
            })

        return new_committee_dic

    # def craps(self, numb=4):
    #     self.no = self.crap(numb) + 'or not'
    #
    # @staticmethod
    # def crap(numb=4):
    #     return 'winner is ' + str(numb)
