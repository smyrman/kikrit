# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.


"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

class AccountTestCase(TestCase):

	def test_transaction(self):
		"""Test simple transactions """
		from django_kikrit.accounts.models import Account, LimitGroup,\
				 Transaction, withdraw_from_account, deposit_to_account
		from datetime import datetime, timedelta
		from django.contrib.auth.models import User

		# Create an operator:
		operator = User(username="tada", password="tada")
		operator.save()

		# Create a 'bank' account:
		account = Account(id=1,name="Test Account", balance=0, limit_group=None)
		account.save()

		# Test to deposit 200:
		trans_deposit = deposit_to_account(account, 200, operator)
		account = Account.objects.get(pk=1)
		self.failUnlessEqual(account.balance, 200)

		# Test to withdraw 200:
		trans_withdraw = withdraw_from_account(account, 200, operator)
		account = Account.objects.get(pk=1)
		self.failUnlessEqual(account.balance, 0)

		# Test to withdraw 200 from an empty account:
		trans_withdraw2 = withdraw_from_account(account, 200, operator)
		self.failUnlessEqual(trans_withdraw2, None)

		# Modify black_limit to -200 and test to withdraw 199:
		limit_group = LimitGroup(id=1, name="Tester1", black_limit=-200,
				max_grey_hours=1)
		limit_group.save()
		account.limit_group = limit_group
		account.save()
		trans_withdraw3 = withdraw_from_account(account, 199, operator)
		account = Account.objects.get(pk=1)
		self.failUnlessEqual(account.balance, -199)

		# Test to withdraw the last 1:
		trans_withdraw4 = withdraw_from_account(account, 1, operator)
		account = Account.objects.get(pk=1)
		self.failUnlessEqual(account.balance, -200)

		# Test to withdraw another 1:
		trans_withdraw5 = withdraw_from_account(account, 1, operator)
		self.failUnlessEqual(trans_withdraw5, None)

		# Test to undo a transaction:
		trans_withdraw3.undo()
		account = Account.objects.get(pk=1)
		self.failUnlessEqual(account.balance, -1)
		trans_withdraw3.delete()

		# Test if user go black after grey_time hours:
		account.timestamp_grey = datetime.now() - timedelta(hours=2, seconds=1)
		account.save()
		trans_withdraw6 = withdraw_from_account(account, 1, operator)
		self.failUnlessEqual(trans_withdraw6, None)

		# Test that transactions are not deleted when users are, and that bacup
		# information is stored to responsible_name:
		trans_id = trans_withdraw.id
		responsible_name = operator.username
		operator.delete()
		trans_withdraw = Transaction.objects.get(id=trans_id)
		self.failUnlessEqual(trans_withdraw.responsible_name, responsible_name)

		# Test that transactions are not deleted when accounts are, and that
		# backup information is stored to account_name:
		trans_id = trans_withdraw.id
		account_name = account.name
		account.delete()
		trans_withdraw = Transaction.objects.get(id=trans_id)
		self.failUnlessEqual(trans_withdraw.account_name, account_name)


__test__ = {"fixtures":["default_groups.json"], "doctest": """
Test default Group permissions

>>> from django.contrib.auth.models import Group
>>> g_staff = Group.objects.get(pk=1)
>>> p_staff = [unicode(p) for p in g_staff.permissions.all()]
>>> p_staff.sort()
>>> for p in p_staff: print p
accounts | account | Can add account
accounts | account | Can change account
accounts | account | Can delete account
accounts | balance image | Can add balance image
accounts | balance image | Can change balance image
accounts | balance image | Can delete balance image
accounts | rfid card | Can add rfid card
accounts | rfid card | Can change rfid card
accounts | rfid card | Can delete rfid card
accounts | transaction | Can add purchase
accounts | transaction | Can add transaction
accounts | transaction | Can change purchase
accounts | transaction | Can change transaction
merchandise | merchandise tag | Can add merchandise tag
merchandise | merchandise tag | Can change merchandise tag
merchandise | merchandise tag | Can delete merchandise tag
merchandise | merchandise | Can add merchandise
merchandise | merchandise | Can change merchandise
merchandise | merchandise | Can delete merchandise

"""}

