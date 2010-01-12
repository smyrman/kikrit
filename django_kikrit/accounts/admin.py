# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from django.contrib import admin

from django_kikrit.accounts.models import Account, RFIDCard, LimitGroup,\
		BalanceImage


class RFIDCardInline(admin.TabularInline):
	fk_name = 'account'
	model = RFIDCard


class AccountAdmin(admin.ModelAdmin):
	#select_related = True
	list_display = ('name', 'user', 'limit_group', 'balance', 'color', 'email',
			'phone_number')
	search_fields = ('name', 'user', 'limit_group', 'balance')
	list_filter = ('limit_group','color')
	oredring = ('id',)
	inlines = (RFIDCardInline,)


class BalanceImageAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'minimum_balance', 'maximum_balance',
			'black', 'grey', 'white')
	search_fields = list_display
	list_filter = ('black','grey','white')

admin.site.register(Account, AccountAdmin)
admin.site.register(LimitGroup)
admin.site.register(BalanceImage, BalanceImageAdmin)
