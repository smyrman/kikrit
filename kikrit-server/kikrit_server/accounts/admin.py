# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import User, UserAdmin, Group, GroupAdmin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response

from utils.admin import SimpleDeleteModelAdmin
from jquery_widgets.admin import ExtendedModelAdmin
from merchandise.models import PurchasedItem
from accounts.models import Account, RFIDCard, LimitGroup, BalanceImage,\
                            Transaction, deposit_to_account,\
                            withdraw_from_account, purchase_from_account\


class RFIDCardInline(admin.TabularInline):
	fk_name = 'account'
	model = RFIDCard



class AccountAdmin(ExtendedModelAdmin, SimpleDeleteModelAdmin):
	related_search_fields = {'user': ('username', 'email'),}

	list_display = ('name', 'user', 'limit_group', 'balance', 'color', 'email',
			'phone_number')
	search_fields = ('name', 'user__username', 'limit_group__name', 'balance')
	list_filter = ('limit_group', 'color')
	ordering = ('name',)
	inlines = (RFIDCardInline,)



class BalanceImageAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'minimum_balance', 'maximum_balance',
			'black', 'grey', 'white')
	search_fields = list_display
	list_filter = ('black','grey','white')


User.account.verbose_name = "Account"

class TransactionAdmin(ExtendedModelAdmin):
	related_search_fields = {'account': ('name', 'email'),}
	date_hierarchy = 'timestamp'
	actions = ['undo']
	list_display = ('timestamp', 'account', 'amount', 'type', 'responsible',
			'get_merchandise')
	search_fields = ('timestamp', 'account__name', 'amount',
			'responsible__username', 'responsible__first_name',
			'responsible__last_name')
	list_filter = ('type',)
	formfield_overrides = {models.IntegerField: {'min_value': 1}}

	def save_form(self, request, form, change):
		if change:
			raise PermissionDenied

		obj = form.save(commit=False)
		trans = None

		if obj.type == Transaction.TYPE_DEPOSIT:
			trans = deposit_to_account(obj.account, obj.amount, request.user)
		elif obj.type == Transaction.TYPE_WITHDRAWAL:
			trans = withdraw_from_account(obj.account, obj.amount, request.user)
		elif obj.type == Transaction.TYPE_PURCHASE:
			trans = purchase_from_account(obj.account, obj.amount, request.user)

		if trans == None:
			raise PermissionDenied

		return trans


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

	def get_actions(self, request):
		actions = super(TransactionAdmin, self).get_actions(request)
		if 'delete_selected' in actions:
			 del actions['delete_selected']
		return actions

	def get_merchandise(self, obj):
		objs = PurchasedItem.objects.filter(transaction=obj)
		ret = u" ".join((unicode(o) for o in objs))
		if len(ret) >= 40:
			ret = ret[:37] + u"..."
		return ret
	get_merchandise.short_description = "purchased items"



class UserAdmin2(UserAdmin):
	select_related = True
	actions = UserAdmin.actions + ['create_accounts', 'update_accounts']
	list_display = UserAdmin.list_display + ('get_account',)
	list_filter = UserAdmin.list_filter + ('groups',)
	filter_vertical = ('user_permissions',)
	fieldsets = list(UserAdmin.fieldsets)
	#fieldsets[1][1]["classes"] = ("collapse",)
	fieldsets[2][1]["classes"] = ("collapse",)
	fieldsets[3][1]["classes"] = ("collapse",)
	fieldsets[4][1]["classes"] = ("collapse",)

	def get_account(self, obj):
		from django.core.urlresolvers import reverse
		from django.utils.html import escape
		if not obj.account:
			return None
		a_str = escape(unicode(obj.account))
		a_href = reverse('admin:accounts_account_change', args=(obj.account.id,))
		return u'<a href="%s">%s</a>' % (a_href, a_str)
	get_account.short_desctiption = "Account"
	get_account.allow_tags = True

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
	filter_vertical = ('permissions',)



admin.site.register(Account, AccountAdmin)
admin.site.register(LimitGroup)
admin.site.register(BalanceImage, BalanceImageAdmin)
admin.site.register(Transaction, TransactionAdmin)

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin2)
admin.site.register(Group, GroupAdmin2)
