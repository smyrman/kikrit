# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from django.contrib import admin

from django_kikrit.merchandise.models import Merchandise, MerchandiseTag,\
		Transaction, Transaction_Merchandise


class MerchandiseAdmin(admin.ModelAdmin):
	#select_related = True
	list_display = ('name', 'ordinary_price', 'internal_price', 'ean',
			'get_tags')
	search_fields = ('name', 'ordinary_price', 'internal_price', 'ean',
			'tags__name')
	list_filter = ('tags',)
	oredring = ('name',)

	def get_tags(self, obj):
		return u",".join((tag.__unicode__() for tag in obj.tags.all()))
	get_tags.short_description = 'tags'

class Transaction_MerchandiseInline(admin.TabularInline):
	model = Transaction_Merchandise
	extra = 2

class TransactionAdmin(admin.ModelAdmin):
	date_hierarchy = 'timestamp'
	list_display = ('timestamp', 'account', 'amount')
	search_fields = ('timestamp', 'account__name', 'amount')
	list_filter = ('type',)
	inlines = (Transaction_MerchandiseInline,)

admin.site.register(Merchandise, MerchandiseAdmin)
admin.site.register(MerchandiseTag)
admin.site.register(Transaction, TransactionAdmin)
