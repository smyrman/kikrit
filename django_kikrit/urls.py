# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre
#
# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from django.conf.urls.defaults import *
from django.views import static
from django.contrib import admin
from django.conf import settings

#from django_kikrit.utils.views import logout_view
#from jquery_widgets import namespaced_urls as jquery_widgets_urls

admin.autodiscover()

urlpatterns = patterns('',
	#(r'^logout/', logout_view),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^jqw/', include('jquery_widgets.urls', app_name='jquery_widgets')),
)


if settings.DEBUG:
	urlpatterns += patterns('',
	(r'^media/(?P<path>.*)$', static.serve, {'document_root':
	settings.MEDIA_ROOT, 'show_indexes': True}),
)
