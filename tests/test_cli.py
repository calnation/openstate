"""Tests for our main skele CLI module."""
import json
from subprocess import PIPE, Popen as popen
from unittest import TestCase

from Bill import Bill

__version__ = "0.0.1"


class TestHelp(TestCase):
    def test_returns_usage_information(self):
        output = popen(['skele', '-h'], stdout=PIPE).communicate()[0]
        self.assertTrue('Usage:' in output)

        output = popen(['skele', '--help'], stdout=PIPE).communicate()[0]
        self.assertTrue('Usage:' in output)


class TestVersion(TestCase):
    def test_returns_version_information(self):
        output = popen(['skele', '--version'], stdout=PIPE).communicate()[0]
        self.assertEqual(output.strip(), __version__)


def stuff():
    # relevant_bills = dict()
    # with open('keywords.json', 'r') as keywords_file:
    #     keywords = json.load(keywords_file)
    # for state in get_states():
    #     relevant_bills[state] = dict()
    #     for session in get_sessions_for_state(state).keys():
    #         relevant_bills[state][session] = dict()
    #         print(state, "session", session)
    #         bills = pyopenstates.search_bills(state=state, session=session,
    #                                           subject='Reproductive Issues')
    #         relevant_bills[state][session].update(search_bills_for_keywords(bills, keywords))
    # print(json.dumps(relevant_bills, default=serialize_datetime))
    # my_latest_term_name = os_funcs.latest_term_name(mystate.state)
    bills = Bill()
    bills.query()
    bills.parse()
    my_bills = bills.bill_table
    first_hundred_bills = my_bills[0:10]
    ten_bills = Bill.add_bill_fields(first_hundred_bills, 'votes')
    # voted_bills = filter(has_votes, my_bills)
    voted_bills = filter(Bill.has_votes, ten_bills)
    results = json.dumps(voted_bills, ensure_ascii=False)
    return print(results)
