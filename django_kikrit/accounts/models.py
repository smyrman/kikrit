# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from datetime import datetime, timedelta
from random import random
from os.path import sep as path_sep

from django.db import models
from django.contrib.auth.models import User

from settings import UPLOAD_PATH
from django_kikrit.accounts.fields import NegativeIntegerField
import django_kikrit.accounts.signals

class LimitGroup(models.Model):
	"""A user might be a member of ONE LimitGroup. This determin how negative
	balance he can have (and for how long) without going black.

	"""
	grey_limit = 0 # Hard coded limit (for now).

	name = models.CharField(max_length=50, unique=True)
	black_limit = NegativeIntegerField(default=0,
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
			help_text="Needed to enable login.")
	name = models.CharField(max_length=50, help_text="Account name: Users's"
			" full name is recomended", unique=True)
	balance = models.IntegerField(default=0, editable=False)
	limit_group = models.ForeignKey(LimitGroup, null=True, blank=True)
	color = models.SmallIntegerField(choices=COLOR_CHOICES, editable=False)
	email = models.EmailField(blank=True, null=True)
	phone_number = models.IntegerField(blank=True, null=True)
	# Timestamp for when the user last whent grey:
	timestamp_grey = models.DateTimeField(editable=False, null=True, blank=True)

	def save(self, *args, **kwargs):
		"""Customized save function that updates color and grey_time_stamp.

		"""
		new_color = self.get_color()

		# Update grey time stamp:
		if self.color == self.COLOR_WHITE and new_color != self.COLOR_WHITE:
				self.timestamp_grey = datetime.now()
		elif new_color == self.COLOR_WHITE:
			self.timestamp_grey = None

		# Update color and save:
		self.color = new_color
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
		if self.limit_group != None:
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
		if self.timestamp_grey == None:
			time_black = time_now + timedelta(hours=1)
		else:
			time_black = self.timestamp_grey + timedelta(hours=grey_hours)

		# Return color:
		color = self.COLOR_BLACK

		if new_balance >= grey_limit:
			color = self.COLOR_WHITE
		elif new_balance >= black_limit:
			if grey_hours == -1 or time_now < time_black:
				color = self.COLOR_GREY
		return color


	def __unicode__(self):
		return unicode(self.name)


	def withdraw(self, amount):
		"""Try to withdraw an amount. Returns True on sucsess, and False on
		failure. Succsess is only possible if the new color equals
		self.COLOR_WHITE or self.COLOR_GREY.(Also saves the object, and updates
		the color field!)

		"""
		# Input check:
		if amount.__class__ != int or amount <= 0:
			raise ValueError("'amount' must be an Integer greater then zero")

		ret = False
		new_color = self.get_color(-amount)

		if new_color != self.COLOR_BLACK:
			# Update balance and color:
			self.balance -= amount
			self.save()
			ret = True
		elif self.get_color() != self.color:
			self.save()

		return ret


	def deposit(self, amount):
		"""Add amount to a user's balance, and return True. (Also saves the
		object, and updates the color field!)

		"""
		# Input check:
		if amount.__class__ != int or amount <= 0:
			raise ValueError("'amount' must be an Integer greater then zero.")

		# Update balance snd color:
		self.balance += amount
		self.save()

		return True


	def get_image(self):
		"""Query for images matching current balance and color. Then return a
		random image from those that does. If no matching images is found, a
		BalanceImage.DoesNotExist exception is thrown.

		"""
		# Update color before we look for an image:
		if self.get_color() != self.color:
			self.save()

		# Filter based on balance:
		q1 = BalanceImage.objects.filter(minimum_balance__lte=self.balance,
				maximum_balance__gte=self.balance)
		q2 = BalanceImage.objects.filter(minimum_balance=None,
				maximum_balance__gte=self.balance)
		q3 = BalanceImage.objects.filter(minimum_balance__lte=self.balance,
				maximum_balance=None)
		q4 = BalanceImage.objects.filter(minimum_balance=None,
				maximum_balance=None)

		# Filter based on color:
		if self.color == self.COLOR_BLACK:
			q_color = BalanceImage.objects.filter(black=True)
		elif self.color == self.COLOR_GREY:
			q_color = BalanceImage.objects.filter(grey=True)
		elif self.color == self.COLOR_WHITE:
			q_color = BalanceImage.objects.filter(white=True)

		# Combine and pickle (execute) queries:
		imgs = list((q1 | q2 | q3 | q4) & q_color)

		# GUARD: image does not exist?
		if len(imgs) == 0:
			raise BalanceImage.DoesNotExist()

		# Return a random image:
		return imgs[int(random()*len(imgs))]



class BalanceImage(models.Model):
	image = models.ImageField(upload_to=UPLOAD_PATH)
	minimum_balance = models.IntegerField(null=True, blank=True,
			help_text="Minimum balance for when the image can be shown. Can be"
			" left empty.")
	maximum_balance = models.IntegerField(null=True, blank=True,
			help_text="Maximum balance for when the image can be shown. Can be"
			" left empty.")
	white = models.BooleanField(blank=True)
	grey = models.BooleanField(blank=True)
	black = models.BooleanField(blank=True)

	def __unicode__(self):
		return unicode(self.image).split(path_sep)[-1]



class RFIDCard(models.Model):
	account = models.ForeignKey(Account)
	rfid_string = models.CharField(max_length=50, unique=True)

	def __unicode__(self):
		return unicode(self.rfid_string)



class Transaction(models.Model):
	"""Class for logging transactions.

	"""
	TYPE_DEPOSIT = 0
	TYPE_WITHDRAWAL = 1
	TYPE_PURCHASE = 2

	TYPE_CHOICES = (
			(TYPE_DEPOSIT, "deposit"),
			(TYPE_WITHDRAWAL, "withdrawal"),
			(TYPE_PURCHASE, "purchase"),
	)

	timestamp = models.DateTimeField(auto_now_add=True, editable=False)
	responsible = models.ForeignKey(User, blank=True, null=True, editable=False)
	account = models.ForeignKey(Account)
	amount = models.IntegerField()
	type = models.IntegerField(choices=TYPE_CHOICES, editable=False)

	def __unicode__(self):
		print self.type
		type = self.TYPE_CHOICES[self.type][1]
		tf = 'from'
		if self.type == self.TYPE_DEPOSIT:
			tf = 'to'
		return u"%s of %s %s %s" % (type, self.amount, tf, self.account)


	def undo(self):
		"""Call this method before delete, to udo the effect of a transaction
		on an account.

		"""
		self.account.balance -= self.amount
		self.account.save()



## Helper Functions:

def deposit_to_account(account, amount, responsible):
	"""Returns transaction object upon success, or None on failure

	"""
	# Input cheks are done in the Account class.
	ret = None
	if account.deposit(amount):
		transaction = Transaction(account=account, amount=amount,
				responsible=responsible, type=Transaction.TYPE_DEPOSIT)
		transaction.save()
		ret = transaction
	return ret

def withdraw_from_account(account, amount, responsible):
	"""Returns transaction object upon success, or None on failure

	"""
	# Input cheks are done in the Account class.
	ret = None
	if account.withdraw(amount):
		transaction = Transaction(account=account, amount=-amount,
				responsible=responsible, type=Transaction.TYPE_WITHDRAWAL)
		transaction.save()
		ret = transaction
	return ret
