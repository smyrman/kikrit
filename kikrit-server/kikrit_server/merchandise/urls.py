# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

from merchandise.views import merchandise_ean

urlpatterns = patterns('',
	url(r'^(\d+)/ean$', merchandise_ean, name="barcode"),
)
