import os
from tzlocal import get_localzone

try:
    # >3.2
    from configparser import ConfigParser
except ImportError:
    # python27
    # Refer to the older SafeConfigParser as ConfigParser
    from ConfigParser import SafeConfigParser as ConfigParser

config = ConfigParser()

# get the path to config.ini
# config_dir = os.path.dirname(os.path.abspath(__file__))
config_dir = '/'
config_path = os.path.join(config_dir, 'openstate.ini')

# check if the path is to a valid file
if not os.path.isfile(config_path):
    raise IOError

config.read(config_path)

STATE = config.get('main', 'STATE')  # value
OPENSTATES_API_KEY = config['main']['OPENSTATES_API_KEY']
OUTPUT_PATH = config['main']['OUTPUT_PATH']
DB_NAME = config['db']['OPENSTATES_API_KEY']
DB_USER = config['db']['DB_USER']
DB_PASSWORD = config['db']['DB_PASSWORD']
DB_PORT = config['db']['DB_PORT']
DB_HOST = config['db']['DB_HOST']
DB_SERVER = config['db']['DB_SERVER']

if config.has_option('main', 'TZ'):
    TZ = config.get('main', 'TZ')
else:
    TZ = os.environ.get('TZ') or get_localzone()
