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

	timestamp = models.DateTimeField(auto_now_add=True)
	merchandise = modles.ManyToManyField(Merchandise)
	account = models.ForeignKey(Merchandise)
	amount = models.IntegerField()

