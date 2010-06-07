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

from accounts.models import Account, LimitGroup
from merchandise.models import MerchandiseTag, Merchandise, PurchasedItem,\
                               buy_merchandise


class MerchandiseTest(TestCase):
	def test_merchandise_tags(self):
		"""Test that tags are not deleted together with merchandise.

		"""
		tag1 = MerchandiseTag(name="tag1")
		tag1.save()
		tag1_id = tag1.id
		m1 = Merchandise(name="m1", internal_price=3, ordinary_price=4)
		m1.save()
		m1.tags = [tag1]
		m1.save()

		# Test that the tag has been added:
		m1 = Merchandise.objects.get(id=m1.id)
		self.failUnlessEqual(m1.tags.all()[0], tag1)

		# Test that the tag is not deleted together with it's merchandise:
		m1.delete()
		tag_count = MerchandiseTag.objects.filter(id=tag1_id).count()
		self.failUnlessEqual(tag_count, 1)


	def test_ordinary_purchase(self):
		"""Test basic purchases (ordinary price)

		"""
		account = Account(name="tset")
		account.deposit(500) # Depost issues the save routine
		operator = None

		m1 = Merchandise(name="m1", internal_price=3, ordinary_price=4)
		m1.save()
		m2 = Merchandise(name="m2", internal_price=2, ordinary_price=4)
		m2.save()

		merchandise_list = [m1, m1, m1, m2]

		# Test a basic purchase:
		total_price = sum(m.ordinary_price for m in merchandise_list)
		trans = buy_merchandise(account, merchandise_list, operator)
		account = Account.objects.get(id=account.id) # Force update
		self.failUnlessEqual(trans.amount, -total_price)
		self.failUnlessEqual(account.balance, 500 - total_price)

		# Test if the number of purchased items related to the transaction is
		# correct:
		pm_count = PurchasedItem.objects.filter(transaction=trans).count()
		item_count = len(merchandise_list)
		self.failUnlessEqual(pm_count, item_count)


	def test_internal_purchase(self):
		"""Test basic purchases (internal price)

		"""
		limit_group = LimitGroup(internal_price=True)
		limit_group.save()
		account = Account(name="tset", limit_group=limit_group)
		account.deposit(500) # Depost issues the save routine
		operator = None

		m1 = Merchandise(name="m1", internal_price=3, ordinary_price=4)
		m1.save()
		m2 = Merchandise(name="m2", internal_price=2, ordinary_price=4)
		m2.save()

		merchandise_list = [m1, m1, m1, m2]

		# Test internal purchase:
		total_price = sum(m.internal_price for m in merchandise_list)
		trans = buy_merchandise(account, merchandise_list, operator)
		account = Account.objects.get(id=account.id) # Force update
		self.failUnlessEqual(trans.amount, -total_price)
		self.failUnlessEqual(account.balance, 500 - total_price)


	def test_illegal_purchase(self):
		"""Test if purchases are canceled if they should not be allowed

		"""
		account = Account(name="tset")
		account.deposit(3) # Deposit issues the save routine
		operator = None

		m1 = Merchandise(name="m1", internal_price=3, ordinary_price=4)
		m1.save()

		# Test illegal purchase:
		trans = buy_merchandise(account, [m1], operator)
		account = Account.objects.get(id=account.id) # Force update
		self.failUnlessEqual(trans, None)
		self.failUnlessEqual(account.balance, 3)


	def test_against_cascade_deletion_of_purchaseditem(self):
		"""Test that purchased items are not removed when related merchandise
		is

		"""
		account = Account(name="tset")
		account.deposit(500) # Depost issues the save routine
		operator = None

		m1 = Merchandise(name="m1", internal_price=3, ordinary_price=4)
		m1.save()
		m2 = Merchandise(name="m2", internal_price=2, ordinary_price=4)
		m2.save()

		# Test a basic purchase:
		trans = buy_merchandise(account, [m1], operator)

		# Test that transactions are not deleted when related merchandise is,
		# and that backup information is stored to merchandise_tags and
		# merchandise_name:
		pm1_id = PurchasedItem.objects.get(transaction=trans).id
		merchandise_name = m1.name[:30]
		merchandise_tags = "|".join((unicode(t) for t in m1.tags.all()))[:30]
		m1.delete()
		pm1 = PurchasedItem.objects.get(id=pm1_id)
		self.failUnlessEqual(pm1.merchandise_name, merchandise_name)
		self.failUnlessEqual(pm1.merchandise_tags, merchandise_tags)



__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}
