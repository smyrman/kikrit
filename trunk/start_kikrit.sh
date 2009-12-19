#!/bin/bash
screen -d -m django_kikrit/manage.py runserver localhost:8081
qt_client/client.py
screen -i -X exit
