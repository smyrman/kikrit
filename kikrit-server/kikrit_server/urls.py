# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre
#
# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from django.conf.urls.defaults import url, patterns, include
from django.views import static
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

def p_url(regex, *args, **kw):
	"""A tiny wrapper to prefix urls with settings.BASE_URL"""
	regex = regex.replace(r'^', r'^'+settings.BASE_URL.strip('/'))
	return url(regex, *args, **kw)

urlpatterns = patterns('',
	#p_url(r'^logout/', logout_view),
	p_url(r'^admin/', include(admin.site.urls)),
	p_url(r'^jqw/', include('jquery_widgets.urls', namespace='jquery-widgets')),
	p_url(r'^kikrit-xml/', include('kikrit_xml.urls', namespace='kikrit-xml')),
)

# In debug or runserver mode (), serve static media:
if settings.SERVE_STATIC_MEDIA:
	urlpatterns += patterns('',
		(r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'), static.serve,
			{'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
	)
