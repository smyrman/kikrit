# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from django.contrib import admin
from utils.admin_actions import simple_delete_selected

class SimpleDeleteModelAdmin(admin.ModelAdmin):
	delete_confirmation_template = 'admin/simple_delete_confirmation.html'
	delete_selected_confirmation_template = \
			'admin/simple_delete_selected_confirmation.html'

	actions = ['custom_delete_selected']

	def get_actions(self, request):
		actions = super(SimpleDeleteModelAdmin, self).get_actions(request)
		if 'delete_selected' in actions:
			 actions['delete_selected'] = (simple_delete_selected,
					 'delete_selected',
					 simple_delete_selected.short_description)
		return actions
