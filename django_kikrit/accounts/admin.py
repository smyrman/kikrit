# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from django.contrib import admin
from django.contrib.auth.admin import User, UserAdmin

from django_kikrit.accounts.models import Account, RFIDCard, LimitGroup,\
		BalanceImage


class RFIDCardInline(admin.TabularInline):
	fk_name = 'account'
	model = RFIDCard


class AccountAdmin(admin.ModelAdmin):
	#select_related = True
	list_display = ('name', 'user', 'limit_group', 'balance', 'color', 'email',
			'phone_number')
	search_fields = ('name', 'user__username', 'limit_group__name', 'balance')
	list_filter = ('limit_group','color')
	ordering = ('name',)
	inlines = (RFIDCardInline,)


class BalanceImageAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'minimum_balance', 'maximum_balance',
			'black', 'grey', 'white')
	search_fields = list_display
	list_filter = ('black','grey','white')


class UserAdmin2(UserAdmin):
	select_related = True
	actions = UserAdmin.actions + ['create_accounts', 'update_accounts']
	list_display = tuple(UserAdmin.list_display) + ('has_account',)

	def has_account(self, obj):
		a_list = Account.objects.filter(user=obj)
		if len(a_list) == 0:
			return False
		return True
	has_account.short_description = "has profile"


	def create_accounts(self, request, queryset):
		n = 0
		for obj in queryset:
			a_list = Account.objects.filter(user=obj)
			if len(a_list) == 0:
				n += 1
				name = obj.get_full_name()
				if name in (" ", ""):
					name = obj.username
				a = Account(name=name, email=obj.email, user=obj)
				a.save()

	def update_accounts(self, request, queryset):
		a_list = Account.objects.filter(user__in=queryset)
		n = len(a_list)
		for a in a_list:
			a.name = a.user.get_full_name()
			if a.name in (" ", ""):
				a.name = a.user.username
			if a.user.email not in ("", None):
				a.email = a.user.email
			a.save()



admin.site.unregister(User)
admin.site.register(User, UserAdmin2)
admin.site.register(Account, AccountAdmin)
admin.site.register(LimitGroup)
admin.site.register(BalanceImage, BalanceImageAdmin)
