import datetime

import pyopenstates

import BillSponsor
import LegislatorVote
import VoteEvent
import config
from Metadata import Metadata
import utils, state_utils
from Tables import Tables


class Bill(Tables):

    def __init__(self):
        Tables.__init__(self)
        self.template_name = 'Infobox bill'

    def query(self, session='session'):  # default 'session' returns only current session
        Tables.query(self)
        bills = pyopenstates.search_bills(state=config.STATE,
                                          search_window=session,
                                          type="bill",
                                          # chamber="upper", # lower
                                          # updated_since="YYYY-MM-DD",
                                          # subject="",
                                          # sponsor_id="000000",
                                          sort="created_at",
                                          fields='id')
        self.raw_dictionary = map(lambda dic: pyopenstates.get_bill(dic['id'],
                                                                    fields=['id',
                                                                            'bill_id',
                                                                            'chamber',
                                                                            '+short_title',
                                                                            'actions',
                                                                            'action_dates',
                                                                            'session',
                                                                            'sources',
                                                                            'sponsors',
                                                                            'subjects',
                                                                            'title',
                                                                            'votes']),
                                  bills)

    def parse(self):
        """

        :rtype: dictionary containing 2 tables:
            bill_vote_events_relational_table: Relational table
        """
        bills_table = []
        vote_events_table = []
        leg_votes_table = []
        bill_sponsors_table = []

        for bill in self.raw_dictionary:

            bill_row = self.table_row(bill)
            bills_table.append(bill_row)

            bill_sponsors_rows = BillSponsor.table_rows(bill)
            bill_sponsors_table.extend(bill_sponsors_rows)

            if bill['votes']:
                for vote_event_dic in bill['votes']:
                    vote_event_row = VoteEvent.table_row(vote_event_dic)
                    vote_events_table.append(vote_event_row)

                    legislators_votes_rows = LegislatorVote.table_rows(vote_event_dic,
                                                                       bill_sponsors_rows)
                    leg_votes_table.extend(legislators_votes_rows)

        self.bill_table = bills_table
        self.bill_sponsor_table = bill_sponsors_table
        self.vote_event_table = vote_events_table
        self.legislator_vote_table = leg_votes_table

    @staticmethod
    def table_row(bill_dic):
        metadata = Metadata()
        session_name = metadata.session_name(bill_dic['session'])
        return {
            'Title': bill_dic['bill_id'] + ', ' + session_name,
            'os_bill_id': bill_dic['id'],
            'bill': bill_dic['bill_id'],
            'bill_title': bill_title(bill_dic),
            'chamber': state_utils.chamber_name(bill_dic['chamber']),
            'website': bill_dic['sources'][-1]['url'],
            'session': session_name,
            'status': bill_status(bill_dic),
            'latest_status': latest_status(bill_dic),
            'bill_date': utils.datetime_to_date(bill_dic['action_dates']['first']),
            'date_passed_senate': utils.datetime_to_date(bill_dic['action_dates']['passed_upper']),
            'date_passed_assembly': utils.datetime_to_date(
                bill_dic['action_dates']['passed_lower']),
            'date_signed': utils.datetime_to_date(bill_dic['action_dates']['signed']),
            'summary': bill_summary(bill_dic),
            'keywords': suggested_topics(bill_dic)
        }


def has_votes(bill_dic):
    bill_votes = bill_dic['votes']
    if not bill_votes:
        return False
    else:
        return True


def add_bill_fields(bills, *fields):
    for i, bill in enumerate(bills):
        bill_details = pyopenstates.get_bill(uid=bill['id'],
                                             fields=fields)
        for field in fields:
            # add each field to the bill
            bill[field] = bill_details[field]

            # updating the specific bill within the bills array
            # bills[i] = bill

    return bills


def is_current(year):
    return datetime.date(year - 1, 12, 1) <= \
           datetime.datetime.now().date() <= \
           datetime.date(year + 1, 11, 30)


def bill_title(bill_dic):
    if bill_dic.get('+short_title'):
        return bill_dic['+short_title']
    else:
        return bill_dic['title']


def bill_summary(bill_dic):
    if bill_dic.get('summary'):
        return bill_dic['summary']
    else:
        return bill_dic['title']


def suggested_topics(bill_dic):
    if bill_dic.get['subjects']:
        return ', '.join(bill_dic['subjects'])
    else:
        return None


def bill_status(bill_dic):
    action_dates = bill_dic['action_dates']
    term_first_year = int(bill_dic['session'][0:4])
    if action_dates['signed']:
        return 'Signed'
    elif not is_current(term_first_year):
        return 'Failed'
    elif action_dates['passed_upper'] and action_dates['passed_lower']:
        return 'Passed'
    elif action_dates['passed_lower']:
        return 'Passed Assembly'
    elif action_dates['passed_upper']:
        return 'Passed Senate'
    elif bill_dic['votes']:
        return 'Not Passed'
    else:
        return 'No Vote'


def latest_status(bill_dic):
    action_dates = bill_dic['action_dates']
    last_date = action_dates['last']
    if last_date in [action_dates['passed_lower'], action_dates['passed_upper'],
                     action_dates['signed']]:
        return bill_status(bill_dic)
    else:
        last_action = next((dic for dic in bill_dic['actions'] if dic["date"] == last_date), None)
        if last_action:
            return last_action.get('action')


def bill_type():
    # SB bill
    # AB bill
    # ACR concurrent resolution
    # ACA constitutional amendment
    # AJR joint resolution
    # HR resolution
    return 0

# def bill_subjects(bill_dic):
#     subjects = set()
#     title = bill_dic['title'].lower()
#     for subj in bill_dic.get('subjects', []):
#         categories = self.categorizer[subj]
#         subjects.update(categories)
#     bill_dic['subjects'] = list(subjects)
#
#     if not bill_dic['subjects'] or bill_dic['subjects'] == ["Other"]:
#         return bill_dic['scraped_subjects']
#     else:
#         return bill_dic['subjects']
