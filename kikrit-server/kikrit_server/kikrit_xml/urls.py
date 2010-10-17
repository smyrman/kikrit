# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

from kikrit_xml.views import account, merchandises, transaction

urlpatterns = patterns('',
	url(r'^account/$', account, name="kikrit-xml-account"),
	url(r'^merchandises/$', merchandises, name="kikrit-xml-merchandises"),
	url(r'^transaction/$', transaction, name="kikrit-xml-transaction"),
)
