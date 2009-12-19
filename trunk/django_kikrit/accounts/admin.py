# -*- coding: utf-8 -*-
from django.contrib import admin

from django_kikrit.accounts.models import Account, RFIDCard, LimitGroup


class RFIDCardInline(admin.TabularInline):
	fk_name = 'account'
	model = RFIDCard


class AccountAdmin(admin.ModelAdmin):
	#select_related = True
	list_display = ('name', 'user', 'limit_group', 'balance', 'color')
	list_filter = ('limit_group','color')
	oredring = ('id',)
	inlines = (RFIDCardInline,)



admin.site.register(Account, AccountAdmin)
admin.site.register(LimitGroup)
