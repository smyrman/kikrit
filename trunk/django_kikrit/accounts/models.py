# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User


class LimitGroup(models.Model):
	"""A user might be a member of ONE LimitGroup. This determin how negative
	balance he can have without going black.

	"""
	grey_limit = 0 # Hard coded limit (for now).

	name = models.CharField(max_length=50)
	black_limit = models.IntegerField(default=0,
			help_text="Minimum balance where transactions are still allowed.")
	max_grey_hours = models.SmallIntegerField(default=24,
			help_text="The maximum number of hours a person migth have a "
			"'grey' (negative) saldo before he goes black. (-1 implies no "
			"limit)")
	internal_price = models.BooleanField(default=False, blank=True,
			help_text="Give members of this group a 'special price'.")

	def __unicode__(self):
		return self.name



class Account(models.Model):
	"""A profile object, adding extra fields to a django User object.

	"""
	COLOR_BLACK = 0
	COLOR_GREY = 1
	COLOR_WHITE = 2

	COLOR_CHOICES = (
			(COLOR_BLACK, "black"),
			(COLOR_GREY, "grey"),
			(COLOR_WHITE, "white"),
			)

	user = models.OneToOneField(User, null=True, blank=True,
			help_text="Needed to enable login and, to send emails to user.")
	name = models.CharField(max_length=50, help_text="Account name", unique=True)
	balance = models.IntegerField(default=0)
	limit_group = models.ForeignKey(LimitGroup, null=True, blank=True)
	color = models.SmallIntegerField(choices=COLOR_CHOICES, editable=False)
	# Timestamp for when the user last whent grey:
	timestamp_grey = models.DateTimeField(editable=False, null=True, blank=True)

	def save(self, *args, **kwargs):
		# Update color:
		self.color = self.get_color()

		super(self.__class__, self).save(*args, **kwargs)


	def has_internal_price(self):
		"""Returns True if the user should get an internal price on
		merchandise, or False if not.

		"""
		# GUARD: No limit group
		if not self.limit_group:
			return False

		return self.limit_group.internal_price


	def get_color(self, amount=0):
		"""Returns the current color, or if an integer for amount is given,
		returns the color you will get if amount is added to the current
		balance. The color will be either self.COLOR_WHITE, self.COLOR_GREY, or
		self.COLOR_BLACK.

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

		# Get new_balance, time_now, and time_black:
		new_balance = self.balance + amount
		time_now = datetime.now()
		if self.timestamp_grey != None:
			time_black = self.timestamp_grey + timedelta(hours=grey_hours)
		else:
			time_black = time_now - timedelta(1)

		# Return color:
		if new_balance >= grey_limit:
			return self.COLOR_WHITE
		elif new_balance >= black_limit \
		and (grey_hours == -1 or time_now <= time_black):
			return self.COLOR_GREY
		else:
			return self.COLOR_BLACK


	def __unicode__(self):
		return self.name


	def withdraw(self, amount):
		"""Try to withdraw an amount. Returns True on sucsess, and False on
		failure. Succsess is only possible if the new color equals
		self.COLOR_WHITE or self.COLOR_GREY.(Also saves the object, and updates
		the color field!)


		"""
		# Input check:
		if amount.__class__ != int or amount < 0:
			raise ValueError("'amount' must be an Integer greater then, or "
			                 "equal to, 0.")

		new_color = self.get_color(-amount)

		if new_color != self.COLOR_BLACK:
			# Set grey timestamp?
			if self.color == self.COLOR_WHITE \
			and new_color != self.COLOR_WHITE:
				self.timestamp_grey = dateime.now()

			# Update color and balance:
			self.balance -= amount
			self.save()

			return True
		else:
			return False


	def deposit(self, amount):
		"""Add amount to a user's balance, and return True. (Also saves the
		object, and updates the color field!)

		"""
		# Input check:
		if amount.__class__ != int or amount <= 0:
			raise ValueError("'amount' must be an Integer greater then 0.")

		# Update color and balance:
		self.balance += amount
		self.save()

		return True


	class Meta:
		pass
	#	unique_together = (("name", "user",),)



class RFIDCard(models.Model):
	account = models.ForeignKey(Account)
	rfid_string = models.CharField(max_length=50, unique=True)



# Signals:
def create_user_account(signal, instance, **kwargs):
	"""Signal for automatically creating an Account upon user creation/save.

	"""
	account, new = Account.objects.get_or_create(user=instance)
	if new:
		account.name = instance.username
		account.save()

models.signals.post_save.connect(create_user_account, sender=User)


