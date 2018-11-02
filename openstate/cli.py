#!/usr/bn/env python
# -*- coding: utf-8 -*-


"""
openstate

Usage:
  openstate schedule  # Uryyb jbeyq!
  openstate refresh  # Uryyb jbeyq!
  openstate -h | --help  # Uryyb jbeyq!
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

# import pandas as pd
from __future__ import print_function
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import STATE_STOPPED, STATE_PAUSED
from Bill import Bill
from BillSponsor import BillSponsor
from Committee import Committee
from Legislator import Legislator
from LegislatorCommittee import LegislatorCommittee
from LegislatorVote import LegislatorVote
from Singleton import Singleton
from sys import version_info
from VoteEvent import VoteEvent

import config
import logging
import wiki_functions

IS_PY3 = version_info[0] >= 3
log_format = '%(asctime)-15s [%(filename)s:%(lineno)d] %(message)s'
logging.basicConfig(format=log_format)
logger = logging.getLogger('openstate.cli')
logger.setLevel(logging.INFO)


class Refresh:

    @staticmethod
    def committees():
        """
        Fetches latest committees data from pyopenstates API.
        """
        os_committees = Committee()
        os_committees.query()
        os_committees.parse()
        wiki_functions.write_to_csv_file_for_DataTransfer(os_committees,
                                                          os_committees.table)

    @staticmethod
    def legislators():
        """
        Fetches latest legislators data from pyopenstates API.
        """
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
        """
        Fetches latest bills data from pyopenstates API.
        """
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

    @staticmethod
    def all():
        """
        Fetches latest committees, legislators and bills data from pyopenstates API.
        """
        Refresh.committees()
        Refresh.legislators()
        Refresh.bills()


class Scheduler:
    __metaclass__ = Singleton

    def __init__(self):
        self.background_scheduler = BackgroundScheduler(timezone=config.TZ)

    def pause(self):
        """
        Pause job processing in the scheduler.

        This will prevent the scheduler from waking up to do job processing until :meth:`resume`
        is called. It will not however stop any already running job processing.

        """
        self.background_scheduler.pause()

    def resume(self):
        """Resume job processing in the scheduler."""
        self.background_scheduler.resume()

    def list(self):
        """
        Prints out a textual listing of all jobs currently scheduled on either all job stores or
        just a specific one.
        """
        self.background_scheduler.print_jobs()

    def clear(self):
        """Removes all scheduled jobs."""
        self.background_scheduler.remove_all_jobs()

    def remove(self, job_id):
        """
        Removes a job, preventing it from being run any more.

        :param str|unicode job_id: the identifier of the job, e.g. 'bills'
        :raises JobLookupError: if the job was not found
        """
        self.background_scheduler.remove_job(job_id)

    def _start(self):
        if self.background_scheduler is None:
            logger.info('Scheduler died! Re-initiating now..')
            self.__init__()

        if self.background_scheduler.state is STATE_STOPPED:
            logger.info('Scheduler was stopped. Restarting now..')
            self.background_scheduler.start()
        elif self.background_scheduler.state is STATE_PAUSED:
            logger.info('Scheduler was paused. Resuming now..')
            self.background_scheduler.resume()
        else:
            pass

    def committees(self):
        """
        Schedules fetching committees data from pyopenstates API on the last Friday of each month.
        """
        print("Scheduling a refresh of committees")
        if not self.background_scheduler.get_job('committees'):
            self.background_scheduler.add_job(Refresh.committees,
                                              'cron',
                                              id='committees',
                                              name='committees',
                                              day='last fri')
            self._start()

    def legislators(self):
        """
        Schedules fetching legislators data from pyopenstates API every Monday at 18:30.
        """
        if not self.background_scheduler.get_job('legislators'):
            self.background_scheduler.add_job(Refresh.legislators,
                                              'cron',
                                              id='legislators',
                                              name='legislators',
                                              day_of_week='mon',
                                              hour=18,
                                              minute=30)
            self._start()

    def bills(self):
        """
        Schedules fetching bills data from pyopenstates API every weekday at 19:30.
        """
        if not self.background_scheduler.get_job('bills'):
            self.background_scheduler.add_job(Refresh.bills, 'cron',
                                              id='bills',
                                              name='bills',
                                              day_of_week='mon-fri',
                                              hour=19,
                                              minute=30)
            self._start()

    @staticmethod
    def all():
        """
        Schedules fetching committees, legislators and bills data from pyopenstates API regularly.
        """
        schedule = Scheduler()
        schedule.committees()
        schedule.legislators()
        schedule.bills()


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
