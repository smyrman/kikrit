# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre
#
# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from django.conf.urls.defaults import *
from django.views import static
from django.contrib import admin
admin.autodiscover()

#from django_kikrit.utils.views import logout_view
from django.conf import settings


urlpatterns = patterns('',
	(r'^media/(?P<path>.*)$', static.serve,
		{'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
	#(r'^logout/', logout_view),
	# FIXME: For the auto complete to work in the admin view, the deprecated
	# admin URL conf syntax is needed (^admin/(.*)$, ...). Before Django 1.3,
	# a better solution MUST be found, as admin.ste.root will be erased from
	# the source code then.
	(r'^admin/(.*)$', admin.site.root),
	(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
	urlpatterns += patterns('',
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':
	settings.MEDIA_ROOT, 'show_indexes': True}),
)
