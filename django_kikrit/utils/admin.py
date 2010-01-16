# -*- coding: utf-8 -*-

# Based on code from: Jannis Leidal, 2008 (http://jannisleidel.com/),
# Copyright (C) 2010: Sindre Røkenes Myren,

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

import operator
from django.db import models
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import admin
from django.utils.encoding import smart_str

from django_kikrit.utils.widgets import ForeignKeySearchInput


class ExtendedModelAdmin(admin.ModelAdmin):
	"""Extends the normal ModalAdmin with an alternative widget for FoeignKey,
	if you provide it with an aditional attribute related_search_fields.

	Example:

	related_search_fields = {
		'user': ('username', 'email'),
	}

	"""
	def __call__(self, request, url):
		if url is None:
			pass
		elif url == 'search':
			return self.search(request)
		return super(ExtendedModelAdmin, self).__call__(request, url)


	def search(self, request):
		"""Searches in the fields of the given related model and returns the
		result as a simple string to be used by the jQuery Autocomplete plugin

		"""
		query = request.GET.get('q', None)
		app_label = request.GET.get('app_label', None)
		model_name = request.GET.get('model_name', None)
		search_fields = request.GET.get('search_fields', None)

		if search_fields and app_label and model_name and query:
			def construct_search(field_name):
				# use different lookup methods depending on the notation
				if field_name.startswith('^'):
					return "%s__istartswith" % field_name[1:]
				elif field_name.startswith('='):
					return "%s__iexact" % field_name[1:]
				elif field_name.startswith('@'):
					return "%s__search" % field_name[1:]
				else:
					return "%s__icontains" % field_name

			model = models.get_model(app_label, model_name)
			qs = model._default_manager.all()
			for bit in query.split():
				or_queries = [models.Q(**{construct_search(
					smart_str(field_name)): smart_str(bit)})
						for field_name in search_fields.split(',')]
				other_qs = models.query.QuerySet(model)
				other_qs.dup_select_related(qs)
				other_qs = other_qs.filter(reduce(operator.or_, or_queries))
				qs = qs & other_qs
			data = ''.join([u'%s|%s\n' % (f.__unicode__(), f.pk) for f in qs])
			return HttpResponse(data)
		return HttpResponseNotFound()


	def formfield_for_dbfield(self, db_field, **kwargs):
		""" Overrides the default widget for Foreignkey fields if they are
		specified in the related_search_fields class attribute.

		"""
		if isinstance(db_field, models.ForeignKey) and \
				db_field.name in self.related_search_fields:
			kwargs['widget'] = ForeignKeySearchInput(db_field.rel,
									self.related_search_fields[db_field.name])
		return super(ExtendedModelAdmin, self).formfield_for_dbfield(db_field,
				**kwargs)

