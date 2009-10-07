from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User



class LimitGroup(models.Model):
	"""A user might be a member of ONE LimitGroup. This determin how negative
	saldo he can have without going black.

	"""
	MSG_TRANSACTIN_SUCCSEED = ""
	MSG_NOT_ENOUGH_MONEY = ""

	grey_limit = 0 # Hard coded limit (for now).
	message = ""

	name = models.CharField(max_length=50)
	black_limit = models.IntegerField(default=0,
			help_text="Minimum saldo where transactions are still allowed.")
	max_grey_hours = models.SmallIntegerField(default=24,
			help_text="The maximum number of hours a person migth have a "
			"'grey' (negative) saldo before he goes black. (-1 implies no "
			"limit)")
	internal_price = models.BooleanField(default=False, blank=True)



class Account(models.Model):
	"""A profile object, adding extra fields to a django User object.

	"""
	COLOR_WHITE = 2
	COLOR_GREY = 1
	COLOR_BLACK = 0

	user = models.OneToOneField(User)
	balance = models.IntegerField(default=0)
	limit_group = models.ForeignKey(LimitGroup, null=True, blank=True)
	last_color_change = models.DateTimeField(null=True, blank=True,
	                    editable=False)

	def internal_price(self):
		"""Returns True if the user should get an internal price on
		merchandise, or False if not.

		"""
		# GUARD: No limit group
		if not self.limit_group:
			return False

		return self.limit_group.internal_price


	def get_user_color(self, amount=0):
		"""Returns an integer representing the current color, or if an integer
		for amount is given, returns the color you will get if amount is
		added to the current balance.

		"""
		# Input check:
		if amount.__class__ != int:
			raise ValueError("'amount' must be an Integer.")

		# Get limits:
		if self.limit_group:
			grey_limit = self.limit_group.grey_limit
			black_limit = self.limit_group.black_limit
			grey_hours = self.limit_group.max_grey_hours
		else:
			grey_limit = 0
			black_limit = 0
			grey_hours = 0

		new_balance = self.balance + amout
		time_now = datetime.now()
		time_black = self.last_color_change + timedelta(hours=grey_hours)

		# Return color:
		if new_balance >= self.grey_limit:
			return self.COLOR_WHITE
		elif new_balance >= self.black_limit and (grey_hours == -1 \
		     or time_now <= time_black):
			return self.COLOR_GREY
		else:
			return self.COLOR_BLACK


	def withdraw(self, amount):
		"""Try to withdraw an amount. Returns True on sucsess, and False on
		failure. Succsess is only possible if the new color equals
		self.COLOR_WHITE or self.COLOR_GREY. In any case self.message will be
		updated.

		"""
		# Input check:
		if amount.__class__ != int or amount < 0:
			raise ValueError("'amount' must be an Integer greater then, or "
			                 "equal to, 0.")

		color = self.get_color(-amount)

		if color != self.COLOR_BLACK:
			self.balance -= amount
			self.save()
			self.message = self.MSG_TRANSACTON_SUCCSEED
			return True
		else:
			self.message = self.MSG_NOT_ENOUGH_MONEY
			return False


	def deposit(self, amount):
		"""Add amount to a user's balance, and return True.

		"""
		# Input check:
		if amount.__class__ != int or amount <= 0:
			raise ValueError("'amount' must be an Integer greater then 0.")

		self.balance += amount
		self.save()
		self.message = self.MSG_TRANSACTON_SUCCSEED
		return True



class RFIDCard(models.Model):
	account = models.ForeignKey(Account)
	code = models.CharField(max_length=100)

