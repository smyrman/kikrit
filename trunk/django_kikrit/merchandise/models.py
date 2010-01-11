# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from django.db import models

from django_kikrit.accounts.models import Account


class MerchandiseTag(models.Model):
	name = models.CharField(max_length=20)
	description = models.TextField(null=True, blank=True)

	def __unicode__(self):
		return self.name



class Merchandise(models.Model):
	search_fields = ('name', 'ordinary_price', 'internal_price', 'ean')
	name = models.CharField(max_length=50, unique=True)
	ordinary_price = models.PositiveIntegerField()
	internal_price = models.PositiveIntegerField()
	ean = models.CharField(max_length=20, blank=True, null=True)
	tags = models.ManyToManyField(MerchandiseTag, null=True, blank=True)

	def __unicode__(self):
		return u"%s -  %d,- (%d,-)" % (self.name, self.ordinary_price,
				self.internal_price)


	def filter(self, filter_str):
		"""Return True if object matches filter_str, and False if not.

		"""
		filter_str = unicode(filter_str).lower()
		# Search attributes:
		for attr in self.search_fields:
			if filter_str in unicode(getattr(self, attr)).lower():
				return True

		# Search tags:
		for tag in self.tags.all():
			if filter_str in unicode(tag).lower():
				return True

		return False



class Transaction(models.Model):
	"""Class for logging transactions.

	"""
	TYPE_PURCHASE = 0
	TYPE_DEPOSIT = 1
	TYPE_CHOICES = (
			(TYPE_PURCHASE, "purchase"),
			(TYPE_DEPOSIT, "deposit"),
	)
	timestamp = models.DateTimeField(auto_now_add=True, editable=False)
	account = models.ForeignKey(Account)
	merchandise = models.ManyToManyField(Merchandise, null=True, blank=True,
			through="Transaction_Merchandise")
	amount = models.IntegerField()
	type = models.BooleanField(choices=TYPE_CHOICES, blank=True)

	def __unicode__(self):
		return unicode(self.timestamp)



class Transaction_Merchandise(models.Model):
	"""Associtation table to connect Merchandise to a Transaction

	"""
	transaction = models.ForeignKey(Transaction)
	merchandise = models.ForeignKey(Merchandise)
	number = models.PositiveIntegerField()



def buy_merchandise(account, merchandise_list):
	"""Try ro buy merchandice_list with credit from account. Return True upon
	sucsess, or False upon failure.

	"""
	# Input cheks are done in the Account class.

	if account.has_internal_price():
		price = sum((m.internal_price for m in merchandise_list))
	else:
		price = sum((m.ordinary_price for m in merchandise_list))

	ret = False
	if price == 0 or account.withdraw(price):
		transaction = Transaction(account=account, amount=-price,
				type=Transaction.TYPE_PURCHASE)
		transaction.save()

		# ManyToManyFields must be set after save:
		merchandise_list.sort()
		last_m = merchandise_list[0]
		n = 0
		for m in merchandise_list + [Merchandise()]:
			n += 1
			if m.pk != last_m.pk:
				tm = Transaction_Merchandise()
				tm.transaction = transaction
				tm.merchandise = last_m
				tm.number = n
				tm.save()
				n = 0
			last_m = m
		ret = True

	return ret


def deposit_money(account, amount):
	# Input cheks are done in the Account class.

	ret = False
	if account.deposit(amount):
		transaction = Transaction(account=account, amount=amount,
				type=Transaction.TYPE_DEPOSIT)
		transaction.save()
		ret = True
	return ret

