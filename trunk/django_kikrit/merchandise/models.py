from django.db import models

from django_kikrit.accounts.models import Account

class Merchandise(model.Model):
	name = model.CharField()
	ordinary_price = models.IntegerField()
	internal_price = models.IntegerField()
	ean = models.CharField()


class Transaction(models.Model):
	"""Class for logging transactions.

	"""

	timestamp = models.DateTimeField(auto_now_add=True, editable=False)
	account = models.ForeignKey(Account)
	merchandise = modles.ManyToManyField(Merchandise, null=True, blank=True)
	amount = models.IntegerField()



def buy_merchandise(account, merchandise_list):
	"""Try ro buy merchandice_list with credit from account. Return True upon
	sucsess, or False upon failure.

	"""
	# WARNING: No input check written, as I am rather lazy..

	if account.has_internal_price()
		price = sum((m.internal_price for m in merchandise_list))
	else:
		price = sum((m.ordinary_price for m in merchandise_list))

	if account.withdraw(price):
		transaction = Transaction(account=account, amount=-price)
		transaction.save()
		# Note: ManyToManyFields must be set after save!
		transaction.merchandise = merchandise_list
		return True
	return False



