# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand, CommandError


class Command(NoArgsCommand):
	help = "Custom command to load test data to the database"

	def handle_noargs(self, *args, **options):
		#if len(args) != 0:
		#	 raise CommandError("Command doesn't accept any arguments")
		from django_kikrit.accounts.models import Account, LimitGroup, RFIDCard
		from django_kikrit.merchandise.models import Merchandise,MerchandiseTag

		# Create test Accounts and LimitGroups:
		lim1 = LimitGroup(name=u"Omega Verksted", black_limit=-200)
		lim2 = LimitGroup(name=u"Omega Verksted - VIP", black_limit=-1000,
				internal_price=True)
		lim1.save()
		lim2.save()
		print "2 LimitGroups created"

		a1 = Account(name=u"Workshop Dude", limit_group=lim1, balance=20)
		a2 = Account(name=u"Workshop Meister", limit_group=lim2, balance=8)
		a3 = Account(name=u"Humble Washing Lady", balance=15)
		a1.save()
		a2.save()
		a3.save()
		print "3 Accounts created"

		# Two cards are registered for the Workshop Dude, one for the Meister
		# and none for the Humble Washing Lady...
		c1 = RFIDCard(rfid_string=u"1101010001001", account=a1)
		c2 = RFIDCard(rfid_string=u"1101010001010", account=a1)
		c3 = RFIDCard(rfid_string=u"1101010001011", account=a2)
		c1.save()
		c2.save()
		c3.save()
		print "3 RFIDCards created"


		# Create test Merchandise and MerchandiseTags:
		t1 = MerchandiseTag(name="Beer")
		t2 = MerchandiseTag(name="Drink")
		t1.save()
		t2.save()
		print "2 MerchandiseTags created"

		m1 = Merchandise(name=u"Hansa Premium 0,5L", ordinary_price=30,
				internal_price=28, ean="001")
		m2 = Merchandise(name=u"Hansa Fatøl 0,5L", ordinary_price=30,
				internal_price=28,ean="002")
		m3 = Merchandise(name=u"Hansa Pilsner 0,33L", ordinary_price=20,
				internal_price=18,ean="003")
		m4 = Merchandise(name=u"Farvel til slekt og venner", ordinary_price=20,
				internal_price=18,ean="004")
		m5 = Merchandise(name=u"Dø og brenn i helvete", ordinary_price=20,
				internal_price=18, ean="005")
		m1.save()
		m2.save()
		m3.save()
		m4.save()
		m5.save()
		print "5 Merchandise created"

		# ManyToManyField data must be assigned after save:
		m1.tags = (t1,)
		m2.tags = (t1,)
		m3.tags = (t1,)
		m4.tags = (t2,)
		m5.tags = (t2,)
		print "5 Merchandise tag associations has been made"
		print "Move along now.."

