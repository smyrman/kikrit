# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import User, UserAdmin, Group, GroupAdmin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response

from django_kikrit.utils.admin import ExtendedModelAdmin
from django_kikrit.accounts.models import Account, RFIDCard, LimitGroup,\
		BalanceImage, Transaction, deposit_to_account, withdraw_from_account


class RFIDCardInline(admin.TabularInline):
	fk_name = 'account'
	model = RFIDCard



class AccountAdmin(ExtendedModelAdmin):
	#form = make_ajax_form(Account, dict(user='user'))
	related_search_fields = {'user': ('username', 'email'),}

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



class TransactionAdmin(ExtendedModelAdmin):
	related_search_fields = {'account': ('name', 'email'),}
	date_hierarchy = 'timestamp'
	actions = ['undo']
	list_display = ('timestamp', 'account', 'amount', 'type', 'responsible')
	search_fields = ('timestamp', 'account__name', 'amount',
			'responsible__username', 'responsible__first_name',
			'responsible__last_name')
	list_filter = ('type',)

	def save_form(self, request, form, change):
		if change:
			raise PermissionDenied

		obj = form.save(commit=False)
		ret = None

		if obj.amount > 0:
			ret = deposit_to_account(obj.account, obj.amount, request.user)
		elif obj.amount < 0:
			ret = withdraw_from_account(obj.account, -obj.amount, request.user)

		if ret == None:
			raise PermissionDenied

		return ret


	def undo(self, request, queryset):
		n = queryset.count()

		# GUARD: Nothing to do?
		if n == 0:
			return None

		for obj in queryset:
			obj.undo()
			self.log_deletion(request, obj, u"REVERTED:"+unicode(obj))
		queryset.delete()

		# message for user:
		if n == 1: msg_bit = "1 transaction"
		else: msg_bit = "%s trasnactions" % n
		self.message_user(request, "Successfully reverted %s." % msg_bit)

		return None
	undo.short_description = "Revert selected transactions"



class UserAdmin2(UserAdmin):
	select_related = True
	actions = UserAdmin.actions + ['create_accounts', 'update_accounts']
	list_display = tuple(UserAdmin.list_display) + ('has_account',)

	def has_account(self, obj):
		queryset = Account.objects.filter(user=obj)
		if queryset.count() == 0:
			return False
		return True
	has_account.short_description = "Has account"


	def create_accounts(self, request, queryset):
		quryset = queryset.filter(account__isnull=True)
		n = queryset.count()

		# GUARD: Nothing to do?
		if n == 0:
			return

		# Create accounts:
		for obj in queryset:
			name = obj.get_full_name()
			if name in (" ", ""):
				name = obj.username
			a = Account(name=name, email=obj.email, user=obj)
			a.save()
			self.log_addition(request, a)

		# message for user:
		if n == 1: msg_bit = "1 account"
		else: msg_bit = "%s accounts" % n
		self.message_user(request, "Successfully created %s." % msg_bit)


	def update_accounts(self, request, queryset):
		queryset = Account.objects.filter(user__in=queryset)
		n = queryset.count()

		# GUARD: Nothing to do?
		if n == 0:
			return

		# Update accounts:
		for obj in queryset:
			obj.name = obj.user.get_full_name()
			if obj.name in (" ", ""):
				obj.name = obj.user.username
			if obj.user.email not in ("", None):
				obj.email = obj.user.email
			obj.save()
			self.log_change(request, obj, unicode(obj))

		# message for user:
		if n == 1: msg_bit = "1 account"
		else: msg_bit = "%s accounts" % n
		self.message_user(request, "Successfully uppdated %s." % msg_bit)



class GroupAdmin2(GroupAdmin):
	save_as = True



admin.site.register(Account, AccountAdmin)
admin.site.register(LimitGroup)
admin.site.register(BalanceImage, BalanceImageAdmin)
admin.site.register(Transaction, TransactionAdmin)

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin2)
admin.site.register(Group, GroupAdmin2)
