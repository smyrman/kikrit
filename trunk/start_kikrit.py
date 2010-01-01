#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PS! This is a shortcut for starting the webserver and the client in one
# click/command. It requires screen, and are therefore not Windows compatible.

import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT)
from settings import RUNSERVER_PORT

# Start webserver:
os.system("screen -d -m django_kikrit/manage.py runserver localhost:%s"%
		RUNSERVER_PORT)

# Start client:
from qt_client import client
client.main()

# Resume webserver screen:
os.system("screen -r")
