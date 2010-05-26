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

class SimpleTest(TestCase):
	def test_transaction(self):
		"""Test simple transactions
		"""
		from django_kikrit.accounts.models import Account, LimitGroup,\
				 withdraw_from_account, deposit_to_account
		from datetime import datetime, timedelta
		from django.contrib.auth.models import User

		user1 = User(username="tada", password="tada")
		user1.save()

		account = Account(id=1,name="Test Account", balance=0, limit_group=None)
		account.save()
		trans1 = deposit_to_account(account, 200, user1)
		account = Account.objects.get(pk=1)
		self.failUnlessEqual(account.balance, 200)

		trans2 = withdraw_from_account(account, 200, user1)
		account = Account.objects.get(pk=1)
		self.failUnlessEqual(account.balance, 0)

		transX = withdraw_from_account(account, 200, user1)
		self.failUnlessEqual(transX, None)

		lg = LimitGroup(id=1, name="Tester1", black_limit=-200, max_grey_hours=1)
		lg.save()
		account.limit_group = lg
		account.save()
		trans3 = withdraw_from_account(account, 199, user1)
		account = Account.objects.get(pk=1)
		self.failUnlessEqual(account.balance, -199)

		trans4 = withdraw_from_account(account, 1, user1)
		account = Account.objects.get(pk=1)
		self.failUnlessEqual(account.balance, -200)

		transX= withdraw_from_account(account, 1, user1)
		self.failUnlessEqual(transX, None)

		trans3.undo()
		account = Account.objects.get(pk=1)
		self.failUnlessEqual(account.balance, -1)
		trans3.delete()

		account.timestamp_grey = datetime.now() - timedelta(hours=2, seconds=1)
		account.save()

		transX = withdraw_from_account(account, 1, user1)
		self.failUnlessEqual(transX, None)

		trans1.delete()
		trans2.delete()
		trans4.delete()
		account.delete()
		user1.delete()
		# TODO: Test that transactions is not deleted when a user is.


__test__ = {"doctest": """
Test Group permissions

>>> from django.contrib.auth.models import Group
>>> g_admin = Group.objects.get(pk=1)
>>> p_admin = [unicode(p) for p in g_admin.permissions.all()]
>>> p_admin.sort()
>>> for p in p_admin: print p
accounts | account | Can add account
accounts | account | Can change account
accounts | account | Can delete account
accounts | balance image | Can add balance image
accounts | balance image | Can change balance image
accounts | balance image | Can delete balance image
accounts | limit group | Can add limit group
accounts | limit group | Can change limit group
accounts | limit group | Can delete limit group
accounts | rfid card | Can add rfid card
accounts | rfid card | Can change rfid card
accounts | rfid card | Can delete rfid card
accounts | transaction | Can add purchase
accounts | transaction | Can add transaction
accounts | transaction | Can change purchase
accounts | transaction | Can change transaction
accounts | transaction | Can delete purchase
accounts | transaction | Can delete transaction
auth | group | Can add group
auth | group | Can change group
auth | group | Can delete group
auth | permission | Can add permission
auth | permission | Can change permission
auth | permission | Can delete permission
auth | user | Can add user
auth | user | Can change user
auth | user | Can delete user
merchandise | merchandise tag | Can add merchandise tag
merchandise | merchandise tag | Can change merchandise tag
merchandise | merchandise tag | Can delete merchandise tag
merchandise | merchandise | Can add merchandise
merchandise | merchandise | Can change merchandise
merchandise | merchandise | Can delete merchandise


>>> g_staff = Group.objects.get(pk=2)
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

