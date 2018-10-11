import pyopenstates

import config
from Singleton import Singleton


class Tables:
    __metaclass__ = Singleton

    def __init__(self, folder_path='/'):
        """
        Sets the main folder path
        Sets the convention by which all created files will be named after the table_name
        Args:
            folder_path: Path where all files generated will be saved.
        """
        self.table_name = self.__class__.__name__
        self.file_name = self.table_name + '.csv'
        self.file_path = folder_path + self.file_name

    def query(self):
        pyopenstates.set_api_key(config.OPENSTATES_API_KEY)

    def __str__(self):
        return "%s is a %s" % (self.table_name, self.file_name)
