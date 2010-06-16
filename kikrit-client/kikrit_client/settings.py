"""
Settings modulde for kikrit_client.

"""

import os
import sys

from utils.paths import path4os


PROJECT_ROOT = os.path.abspath(__file__).rsplit(os.path.sep, 1)[0]

# Search for client_settings.py file and add configdir to path:
for path in (PROJECT_ROOT, '~user/config/kikrit', '/etc/kikrit'):
	cfg_file = path4os(path+'/client_settings.cfg')
	if os.path.exists(cfg_file):
		CONFIG_DIR = path4os(path)
		CONFIG_FILE = cfg_file
		# FIXME: import settings
		break
del cfg_file

# FIXME: Actually get stuff from cfg file.

# URLS for the admin
RUNSERVER_PORT = '8081'
ADMIN_TAB_URL = "http://localhost:%s/admin/" % RUNSERVER_PORT
SPLASH_SCREEN = PROJECT_ROOT + "/"

# QT_CLINET SETTINGS:
RFID_DEVICE = "/dev/ttyS0"
BALANCE_PAGE_TIME_SEC = 5
MESSAGE_TIME_SEC = 5

STYLE_SHEET = path4os(PROJECT_ROOT + "/qt_client/styles/base/style.qss")
ICONS = path4os(PROJECT_ROOT + "/qt_client/styles/base/icons.cfg")
