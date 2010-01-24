# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre
#
# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from django.conf.urls.defaults import *
from django.views import static
from django.contrib import admin
admin.autodiscover()

from django_kikrit.utils.views import logout_view
import settings


urlpatterns = patterns('',
	(r'^media/(?P<path>.*)$', static.serve,
		{'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
	#(r'^logout/', logout_view),
	(r'^(.*)', admin.site.root),
)

