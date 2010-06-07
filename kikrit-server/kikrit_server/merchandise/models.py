# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from django.db import models
from django.db import transaction

from accounts.models import Account, Transaction


class MerchandiseTag(models.Model):
	name = models.CharField(max_length=20)
	description = models.TextField(null=True, blank=True)

	class Meta:
		ordering = ('name',)


	def __unicode__(self):
		return self.name


class Merchandise(models.Model):
	SEARCH_FIELDS = ('name', 'ordinary_price', 'internal_price', 'ean')

	name = models.CharField(max_length=50, unique=True)
	ordinary_price = models.PositiveIntegerField()
	internal_price = models.PositiveIntegerField()
	ean = models.CharField(max_length=20, blank=True, null=True, unique=True)
	tags = models.ManyToManyField(MerchandiseTag, null=True, blank=True)

	class Meta:
		ordering = ('name',)


	def __unicode__(self):
		return u"%s: %d,- (%d,-)" % (self.name, self.ordinary_price,
				self.internal_price)


	def save(self, *args, **kw):
		# If strings are saved to the database as empty instead of NULL, this
		# will violate the database fields 'unique' parameter the instance onr
		# try to add the second Merchandise without an ean.
		if self.ean == "":
			self.ean = None
		super(Merchandise, self).save(*args, **kw)


	def delete(self, preserve_transactions=True, **kwargs):
		if preserve_transactions:
			# Generate backup information for purchased item, and 'cut it
			# loose':
			PurchasedItem.objects.filter(merchandise=self).update(merchandise=None,
					merchandise_name=self.name[:30], merchandise_tags="|".join(
					(unicode(t) for t in self.tags.all()))[:30])
		super(Merchandise, self).save(**kwargs)


	def filter(self, filter_str):
		"""Return True if object matches filter_str, and False if not.

		"""
		filter_str = unicode(filter_str).lower()
		# Search attributes:
		for attr in self.SEARCH_FIELDS:
			if filter_str in unicode(getattr(self, attr)).lower():
				return True

		# Search tags:
		for tag in self.tags.all():
			if filter_str in unicode(tag).lower():
				return True

		return False



class TransactionTypeManager(models.Manager):
    """Custom manager for showing certain kinds of transactions"""
    type = None

    def __init__(self, type, *args, **kwargs):
        self.type = type
        super(self.__class__,self).__init__(*args, **kwargs)


    def get_query_set(self):
        return super(self.__class__,
                self).get_query_set().filter(type=self.type)



class PurchasedItem(models.Model):
	"""Associtation table to connect Merchandise to a Transaction.

	"""
	transaction = models.ForeignKey(Transaction)
	merchandise = models.ForeignKey(Merchandise)
	price = models.PositiveIntegerField()

	# Backup information if the realted merchandise object is deleted:
	merchandise_name = models.CharField(max_length=30, null=True, blank=True)
	merchandise_tags = models.CharField(max_length=30, null=True, blank=True)

	def __unicode__(self):
		return u"%s: %s,-" % (self.merchandise.name, self.price)



class Purchase(Transaction):
	default_manager = TransactionTypeManager(type=Transaction.TYPE_PURCHASE)

	class Meta:
		proxy = True


	def undo(self):
		"""Call this function before delete to undo the effect this purchase
		has had on the system.
		"""
		self.account.balance -= self.amount
		self.account.save()
		q = PurchasedItems.objects.filter(transaction__id=self.id)
		q.delete()



## Helper Functions:

@transaction.commit_on_success
def buy_merchandise(account, merchandise_list, responsible=None):
	"""Try ro buy merchandice_list with credit from account. Returns
	transaction object upon success, or None on failure.

	"""
	# Make a 100% sure that the account is up to date:
	account = Account.objects.get(pk=account.pk)

	internal = account.has_internal_price()

	# Input cheks are done in the Account class.
	if internal:
		total_price = sum((m.internal_price for m in merchandise_list))
	else:
		total_price = sum((m.ordinary_price for m in merchandise_list))

	transaction = None
	if total_price == 0 or account.withdraw(total_price):
		transaction = Transaction(account=account, amount=-total_price,
				type=Transaction.TYPE_PURCHASE)
		transaction.save()

		# Purchased items must be created after save:
		for m in merchandise_list:
			pm = PurchasedItem()
			pm.transaction = transaction
			pm.merchandise = m
			if internal:
				pm.price = m.internal_price
			else:
				pm.price = m.ordinary_price
			pm.save()

	return transaction
