# -*- coding: utf-8 -*-
from django.db import models

from django_kikrit.accounts.models import Account


class MerchandiseTag(models.Model):
	name = models.CharField(max_length=20)
	description = models.TextField(null=True, blank=True)

	def __unicode__(self):
		return self.name



class Merchandise(models.Model):
	name = models.CharField(max_length=50)
	ordinary_price = models.PositiveIntegerField()
	internal_price = models.PositiveIntegerField()
	ean = models.CharField(max_length=20, unique=True)
	tags = models.ManyToManyField(MerchandiseTag, null=True, blank=True)

	def __unicode__(self):
		return self.name



class Transaction(models.Model):
	"""Class for logging transactions.

	"""
	timestamp = models.DateTimeField(auto_now_add=True, editable=False)
	account = models.ForeignKey(Account)
	merchandise = models.ManyToManyField(Merchandise, null=True, blank=True)
	amount = models.IntegerField()

	def __unicode__(self):
		return self.timestamp



def buy_merchandise(account, merchandise_list):
	"""Try ro buy merchandice_list with credit from account. Return True upon
	sucsess, or False upon failure.

	"""
	# WARNING: No input check written, as I am rather lazy..

	if account.has_internal_price():
		price = sum((m.internal_price for m in merchandise_list))
	else:
		price = sum((m.ordinary_price for m in merchandise_list))

	if account.withdraw(price):
		transaction = Transaction(account=account, amount=-price)
		transaction.save()

		# ManyToManyFields must be set after save:
		transaction.merchandise = merchandise_list
		return True
	return False



