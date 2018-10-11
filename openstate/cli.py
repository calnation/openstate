#!/usr/bn/env python
# -*- coding: utf-8 -*-

"""
openstate

Usage:
  openstate schedule
  openstate -h | --help
  openstate --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  openstate hello

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/rdegges/openstate-cli
"""

import logging
from Singleton import Singleton
from sys import version_info
from apscheduler.schedulers.background import BackgroundScheduler

# import pandas as pd
import wiki_functions
from Bill import Bill
from BillSponsor import BillSponsor
from Committee import Committee
from Legislator import Legislator
from LegislatorCommittee import LegislatorCommittee
from LegislatorVote import LegislatorVote
from VoteEvent import VoteEvent

IS_PY3 = version_info[0] >= 3
log_format = '%(asctime)-15s [%(filename)s:%(lineno)d] %(message)s'
logging.basicConfig(format=log_format)
logger = logging.getLogger('openstate.cli')
logger.setLevel(logging.INFO)


class Refresh:

    @staticmethod
    def committees():
        os_committees = Committee()
        os_committees.query()
        os_committees.parse()
        wiki_functions.write_to_csv_file_for_DataTransfer(os_committees,
                                                          os_committees.table)

    @staticmethod
    def legislators():
        os_legislators = Legislator()
        legislator_committees = LegislatorCommittee()

        os_legislators.query()
        os_legislators.parse()

        wiki_functions.write_to_csv_file_for_DataTransfer(os_legislators,
                                                          os_legislators.legislator_table)
        wiki_functions.write_to_csv_file_for_DataTransfer(legislator_committees,
                                                          os_legislators.legislator_committee_table)

    @staticmethod
    def bills():
        os_bills = Bill()
        os_vote_events = VoteEvent()
        os_bill_sponsors = BillSponsor()
        os_legislator_votes = LegislatorVote()

        os_bills.query()
        os_bills.parse()

        wiki_functions.write_to_csv_file_for_DataTransfer(os_bills,
                                                          os_bills.bill_table)
        wiki_functions.write_to_csv_file_for_DataTransfer(os_vote_events,
                                                          os_bills.vote_event_table)
        wiki_functions.write_to_csv_file_for_DataTransfer(os_legislator_votes,
                                                          os_bills.legislator_vote_table)
        wiki_functions.write_to_csv_file_for_DataTransfer(os_bill_sponsors,
                                                          os_bills.bill_sponsor_table)


class Scheduler:
    __metaclass__ = Singleton

    def __init__(self):
        self.background_scheduler = BackgroundScheduler()

    def committees(self):
        print "Scheduling a refresh of committees"
        if not self.background_scheduler.get_job('committees'):
            self.background_scheduler.add_job(Refresh.committees,
                                              'cron',
                                              name='committees',
                                              day='last fri')

    def legislators(self):
        if not self.background_scheduler.get_job('legislators'):
            self.background_scheduler.add_job(Refresh.legislators,
                                              'cron',
                                              name='legislators',
                                              day_of_week='mon',
                                              hour=18,
                                              minute=30)

    def bills(self):
        if not self.background_scheduler.get_job('bills'):
            self.background_scheduler.add_job(Refresh.bills, 'cron',
                                              name='bills',
                                              day_of_week='mon-fri',
                                              hour=19,
                                              minute=30)

    @staticmethod
    def all():
        schedule = Scheduler()
        schedule.committees()
        schedule.legislators()
        schedule.bills()
        schedule.start()

    def start(self):
        self.background_scheduler.start()

    def list(self):
        self.background_scheduler.print_jobs()


def main():
    # Scheduler.all()
    try:
        import fire
        """Main CLI entrypoint."""
        fire.Fire({
            'refresh': Refresh(),
            'schedule': Scheduler(),
        })

    except ImportError as e:
        raise ImportError(e)


if __name__ == '__main__':
    main()
