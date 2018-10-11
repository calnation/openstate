import state_utils
from Tables import Tables


class LegislatorCommittee(Tables):

    def __init__(self):
        Tables.__init__(self)
        self.template_name = 'Relation:LegislatorCommittee'


def table_row(os_leg_id, role_dic):
    new_committee_dic = {
        'os_leg_id': os_leg_id,
        'committee_id': role_dic['committee_id'],
        'role': role_dic['position'],
        'term': state_utils.term_name(role_dic['term']),
    }

    return new_committee_dic
