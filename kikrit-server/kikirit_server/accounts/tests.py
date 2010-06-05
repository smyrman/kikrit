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

from django_kikrit.accounts.models import Account, LimitGroup, Transaction, \
		withdraw_from_account, deposit_to_account
from datetime import datetime, timedelta
from django.contrib.auth.models import User


class AccountTestCase(TestCase):

	def test_basic_transactions(self):
		"""Test basic deposit and withdraw for normal accounts"""
		# Create an operator:
		operator = User(username="tada", password="tada")
		operator.save()

		# Create a bank account:
		account = Account(id=1, name="Test Account")
		account.save()

		# Test to deposit 200:
		trans_deposit = deposit_to_account(account, 200, operator)
		account = Account.objects.get(pk=1)
		self.failUnlessEqual(account.balance, 200)

		# Test to withdraw 200:
		trans_withdraw = withdraw_from_account(account, 200, operator)
		account = Account.objects.get(pk=1)
		self.failUnlessEqual(account.balance, 0)

		# Test that withdrawing 200 from an empty account fails:
		trans_withdraw2 = withdraw_from_account(account, 200, operator)
		self.failUnlessEqual(trans_withdraw2, None)

		# Return objects for reuse in other tests:
		return account, operator, trans_deposit, trans_withdraw


	def test_limitgroup_transactions(self):
		"""Test credit withdraw for accounts with limitgroup memberships"""

		# Create an operator:
		operator = User(username="tada", password="tada")
		operator.save()

		# Create a bank account with black_limit == -200:
		limit_group = LimitGroup(id=1, name="Tester1", black_limit=-200,
				max_grey_hours=1)
		limit_group.save()
		account = Account(id=1, name="Test Account", limit_group=limit_group)
		account.save()

		# Test to withdraw 199:
		trans_withdraw = withdraw_from_account(account, 199, operator)
		account = Account.objects.get(pk=1)
		self.failUnlessEqual(account.balance, -199)

		# Test to withdraw the last 1:
		trans_withdraw2 = withdraw_from_account(account, 1, operator)
		account = Account.objects.get(pk=1)
		self.failUnlessEqual(account.balance, -200)

		# Test that withdrawing another 1 fails:
		trans_withdraw3 = withdraw_from_account(account, 1, operator)
		self.failUnlessEqual(trans_withdraw3, None)

		# Test that the account go black after max_grey_hours == 1:
		trans_deposit = deposit_to_account(account, 50, operator)
		account.timestamp_grey = datetime.now() - timedelta(hours=1, seconds=1)
		account.save()
		trans_withdraw4 = withdraw_from_account(account, 1, operator)
		self.failUnlessEqual(trans_withdraw4, None)


	def test_undo_transaction(self):
		"""Test that the transaction's undo function completly reverse the
		transaction

		"""
		# Cseate account, operator, and deposit/withdraw transactions:
		bits = self.test_basic_transactions()
		account, operator, trans_deposit, trans_withdraw = bits

		# Test to undo the deposit transaction:
		trans_deposit.undo()
		account = Account.objects.get(pk=1)
		self.failUnlessEqual(account.balance, -200)
		trans_deposit.delete()

		# Test to undo the withdraw transaction:
		trans_withdraw.undo()
		account = Account.objects.get(pk=1)
		self.failUnlessEqual(account.balance, 0)
		trans_withdraw.delete()


	def test_against_cascade_deletion_of_tranasactions(self):
		"""Test that transactions are not removed when related users or
		accounts are deleted

		"""
		# Create account, operator, and deposit/withdraw transactions:
		bits = self.test_basic_transactions()
		account, operator, trans_deposit, trans_withdraw = bits

		# Test that transactions are not deleted when users are, and that bacup
		# information is stored to responsible_name:
		trans_id = trans_deposit.id
		responsible_name = operator.username
		operator.delete()
		trans_deposit = Transaction.objects.get(id=trans_id)
		self.failUnlessEqual(trans_deposit.responsible_name, responsible_name)

		# Test that transactions are not deleted when accounts are, and that
		# backup information is stored to account_name:
		trans_id = trans_deposit.id
		account_name = account.name
		account.delete()
		trans_deposit = Transaction.objects.get(id=trans_id)
		self.failUnlessEqual(trans_deposit.account_name, account_name)


	def test_inactive_accounts(self):
		"""Test that withdraw and deposit are not possible for inactive
		accounts

		"""
		# Create account and operator:
		operator = User(username="tada", password="tada")
		operator.save()
		account = Account(id=1, name="Test Account", is_active=False)
		account.save()

		account_balance = account.balance

		# Test that withdraw fails:
		trans_withdraw = withdraw_from_account(account, 200, operator)
		self.failUnlessEqual(trans_withdraw, None)
		account = Account.objects.get(pk=1)
		self.failUnlessEqual(account.balance, account_balance)

		# Test that deposits are still allowed:
		trans_deposit = deposit_to_account(account, 200, operator)
		account = Account.objects.get(pk=1)
		self.failUnlessEqual(account.balance, account_balance+200)



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

