# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from random import randint

from django.db import models
from django.contrib import admin
#from django.core.exceptions import PermissionDenied

from merchandise.models import Merchandise, MerchandiseTag
from utils.admin import SimpleDeleteModelAdmin

class MerchandiseAdmin(SimpleDeleteModelAdmin):
	list_display = ('name', 'ordinary_price', 'internal_price', 'ean',
			'get_tags')
	search_fields = ('name', 'ordinary_price', 'internal_price', 'ean',
			'tags__name')
	list_filter = ('tags',)
	oredring = ('name',)
	actions = ['generate_eans', 'remove_eans']
	formfield_overrides = {models.ManyToManyField: {'widget':
		admin.widgets.FilteredSelectMultiple('tags', False)}}

	def get_tags(self, obj):
		return u",".join((tag.__unicode__() for tag in obj.tags.all()))
	get_tags.short_description = 'tags'

	def generate_eans(self, request, queryset):
		"""Action to generate an EAN-13 barcode for merchandises useing the
		'in-store' area codeo of 21.

		"""
		queryset = queryset.filter(ean__isnull=True)
		for obj in queryset:
			sys_code = [2, 1]
			manuf_code = [0, 0, 0, 0, 0]

			# Generate a random product code, and buid an ean-13 string:
			count = 1
			while count > 0:
				prod_code = [randint(0,9) for i in range(5)]
				ean = sys_code + manuf_code + prod_code + [0]
				# calculate check digit:
				ean[12] = 10
				ean[12] -= (ean[1]+ean[3]+ean[5]+ean[7]+ean[9]+ean[11])*3
				ean[12] -= (ean[0]+ean[2]+ean[4]+ean[6]+ean[8]+ean[10])
				ean[12] %= 10
				ean_u = u"".join((unicode(digit) for digit in ean))
				count = queryset.model.objects.filter(ean=ean_u).count()

			obj.ean = ean_u
			obj.save()
	generate_eans.short_description = "Generate EANs for selected merchandises"
	def remove_eans(self, request, queryset):
		queryset.update(ean=None)
	remove_eans.short_description = "Remove EANs from selected merchandises"


admin.site.register(Merchandise, MerchandiseAdmin)
admin.site.register(MerchandiseTag)
