import state_utils
import utils
from Tables import Tables


class VoteEvent(Tables):

    def __init__(self):
        Tables.__init__(self)
        self.template_name = 'VoteEvent'


def total_vote_count(vote_dic):
    return vote_dic['yes_count'] + vote_dic['no_count'] + vote_dic['other_count']


def vote_scope(vote_event_dic):
    # if vote_dic.get('bill_chamber'):
    chamber_name_ = state_utils.chamber_name(vote_event_dic['chamber'])
    if total_vote_count(vote_event_dic) < 30:
        # TODO add committee name when api settles down
        return chamber_name_ + ' Committee'
    else:
        return chamber_name_


def vote_outcome(vote_event_dic):
    if vote_event_dic['passed'] == 'true':
        outcome_p1 = 'Passed '
    else:
        outcome_p1 = 'Failed '

    scope = vote_scope(vote_event_dic)
    outcome_p2 = scope + ' '

    if vote_event_dic['+threshold'] != '1/2':
        outcome_p3 = 'supermajority vote '
    else:
        outcome_p3 = ''

    return outcome_p1 + \
           outcome_p2 + \
           outcome_p3 + \
           'with ' + \
           str(vote_event_dic['yes_count']) + ' voting for, ' + \
           str(vote_event_dic['no_count']) + ' voting against & ' + \
           str(vote_event_dic['other_count']) + ' not voting'


def vote_events(bill_dic):
    return bill_dic['votes']


def vote_event_base(vote_event_dic):
    return {
        'os_bill_id': vote_event_dic['bill_id'],
        'os_vote_id': vote_event_dic['vote_id'],
    }


def table_row(vote_event_dic):
    new_vote_event_dic = vote_event_base(vote_event_dic)
    new_vote_event_dic.update({
        'scope': vote_scope(vote_event_dic),
        'date': utils.datetime_to_date(vote_event_dic['date']),
        'outcome': vote_outcome(vote_event_dic),
        'motion': vote_event_dic['motion'],
        'website': vote_event_dic['sources'][-1]['url'],
    })

    return new_vote_event_dic
