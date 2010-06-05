# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from django.db import models
from django import forms
from django.template.defaultfilters import capfirst
from south.modelsinspector import add_introspection_rules


class NegativeIntegerField(models.PositiveIntegerField):
	__metaclass__ = models.SubfieldBase

	def formfield(self, **kwargs):
		defaults = {'max_value': 0}
		defaults.update(kwargs)
		return models.IntegerField.formfield(self, **defaults)


	def to_python(self, value):
		# GUARD: value is None?
		if value == None:
			return value

		value = models.PositiveIntegerField.to_python(self, value)
		if value > 0:
			value *= -1
		return value


	def get_db_prep_value(self, value):
		# GUARD: value is None?
		if value == None:
			return value
		if value < 0:
			value *= -1
		return models.PositiveIntegerField.get_db_prep_value(self, value)


# Tell the Soth migrations system how this custom fields are different from the
# standard django fields:
add_introspection_rules([
	(
		[NegativeIntegerField], # Class(es) these apply to
		[],			# Positional arguments (not used)
		{},			# Keyword argument
	),
], ["^(django_kikrit\.)?accounts\.fields\.Negative.*"])
