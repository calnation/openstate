import VoteEvent
from Tables import Tables


class LegislatorVote(Tables):

    def __init__(self):
        Tables.__init__(self)
        self.template_name = 'Relation:LegislatorVote'


def type_if_sponsor(leg_id, sponsors_dic_list):
    # sponsor_leg_ids = map(lambda dic: leg_id, sponsors_dics)
    # matching_sponsorships = filter(lambda dic: dic['leg_id'] == leg_id, sponsors_dics)
    matching_sponsorship = next((dic for dic in sponsors_dic_list if dic["leg_id"] == leg_id), None)
    if matching_sponsorship:
        return matching_sponsorship['type']
    else:
        return None


def vote(vote_type, leg_id, sponsors_dic_list):
    sponsorship_type_ = type_if_sponsor(leg_id, sponsors_dic_list)
    vote_type_dic = {'yes_votes': 'Yes',
                     'no_votes': 'No',
                     'other_votes': 'Abs(ent/tained)'}
    vote_p1 = vote_type_dic[vote_type]
    if sponsorship_type_:
        vote_p2 = ' (' + sponsorship_type_ + ')'
    else:
        vote_p2 = ''
    return vote_p1 + vote_p2


def table_row(vote_type, leg_id, sponsors_dic_list):
    legis_vote_dic = {
        'os_leg_id': leg_id,
        'vote': vote(vote_type, leg_id, sponsors_dic_list),
    }
    return legis_vote_dic


def table_rows(vote_event_dic, sponsorships):
    vote_event_legis_votes = []
    legis_vote_dic = VoteEvent.vote_event_base(vote_event_dic)

    # TODO add cosponsor as an alternative value
    for leg_vote in vote_event_dic['no_votes']:
        if leg_vote:
            legis_vote_dic.update(table_row('no_votes', leg_vote['leg_id'], sponsorships))
            vote_event_legis_votes.append(legis_vote_dic)
    for leg_vote in vote_event_dic['yes_votes']:
        if leg_vote:
            legis_vote_dic.update(
                table_row('yes_votes', leg_vote['leg_id'], sponsorships))
            vote_event_legis_votes.append(legis_vote_dic)
    for leg_vote in vote_event_dic['other_votes']:
        if leg_vote:
            legis_vote_dic.update(
                table_row('other_votes', leg_vote['leg_id'], sponsorships))
            vote_event_legis_votes.append(legis_vote_dic)

    return vote_event_legis_votes
