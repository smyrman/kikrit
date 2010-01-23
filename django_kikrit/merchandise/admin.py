# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from django.db import models
from django.contrib import admin
from django.core.exceptions import PermissionDenied

from django_kikrit.accounts.admin import TransactionAdmin
from django_kikrit.merchandise.models import Merchandise, MerchandiseTag,\
		Purchase, PurchasedItem


class MerchandiseAdmin(admin.ModelAdmin):
	list_display = ('name', 'ordinary_price', 'internal_price', 'ean',
			'get_tags')
	search_fields = ('name', 'ordinary_price', 'internal_price', 'ean',
			'tags__name')
	list_filter = ('tags',)
	oredring = ('name',)
	formfield_overrides = {models.ManyToManyField: {'widget':
		admin.widgets.FilteredSelectMultiple('tags', False)}}

	def get_tags(self, obj):
		return u",".join((tag.__unicode__() for tag in obj.tags.all()))
	get_tags.short_description = 'tags'



class PurchasedItemInline(admin.TabularInline):
	model = PurchasedItem
	fk_name = 'transaction'
	extra = 2



class PurchaseAdmin(TransactionAdmin):
	exclude = ('amount',)
	list_display = ('timestamp', 'account', 'amount')
	search_fields = ('timestamp', 'account__name', 'amount')
	list_filter = ()
	inlines = (PurchasedItemInline,)

	def save_form(self, request, form, change):
		raise PermissionDenied



admin.site.register(Merchandise, MerchandiseAdmin)
admin.site.register(MerchandiseTag)
#admin.site.register(Purchase, PurchaseAdmin)
#admin.site.register(PurchasedItem)
