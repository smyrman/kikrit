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
		m6 = Merchandise(name=u"m6", ordinary_price=10, internal_price=5)
		m7 = Merchandise(name=u"m7", ordinary_price=10, internal_price=5)
		m8 = Merchandise(name=u"m8", ordinary_price=10, internal_price=5)
		m9 = Merchandise(name=u"m9", ordinary_price=10, internal_price=5)
		m10 = Merchandise(name=u"m10", ordinary_price=10, internal_price=5)
		m11 = Merchandise(name=u"m11", ordinary_price=10, internal_price=5)
		m12 = Merchandise(name=u"m12", ordinary_price=10, internal_price=5)
		m13 = Merchandise(name=u"m13", ordinary_price=10, internal_price=5)
		m14 = Merchandise(name=u"m14", ordinary_price=10, internal_price=5)
		m15 = Merchandise(name=u"m15", ordinary_price=10, internal_price=5)
		m16 = Merchandise(name=u"m16", ordinary_price=10, internal_price=5)
		m17 = Merchandise(name=u"m17", ordinary_price=10, internal_price=5)
		m18 = Merchandise(name=u"m18", ordinary_price=10, internal_price=5)
		m19 = Merchandise(name=u"m19", ordinary_price=10, internal_price=5)
		m20 = Merchandise(name=u"m20", ordinary_price=10, internal_price=5)
		m21 = Merchandise(name=u"m21", ordinary_price=10, internal_price=5)
		m22 = Merchandise(name=u"m22", ordinary_price=10, internal_price=5)
		m23 = Merchandise(name=u"m23", ordinary_price=10, internal_price=5)
		m24 = Merchandise(name=u"m24", ordinary_price=10, internal_price=5)
		m25 = Merchandise(name=u"m25", ordinary_price=10, internal_price=5)
		m26 = Merchandise(name=u"m26", ordinary_price=10, internal_price=5)
		m27 = Merchandise(name=u"m27", ordinary_price=10, internal_price=5)
		m28 = Merchandise(name=u"m28", ordinary_price=10, internal_price=5)
		m29 = Merchandise(name=u"m29", ordinary_price=10, internal_price=5)
		m30 = Merchandise(name=u"m30", ordinary_price=10, internal_price=5)
		m1.save()
		m2.save()
		m3.save()
		m4.save()
		m5.save()
		m6.save()
		m7.save()
		m8.save()
		m9.save()
		m10.save()
		m11.save()
		m12.save()
		m13.save()
		m14.save()
		m15.save()
		m16.save()
		m17.save()
		m18.save()
		m19.save()
		m20.save()
		m21.save()
		m22.save()
		m23.save()
		m24.save()
		m25.save()
		m26.save()
		m27.save()
		m28.save()
		m29.save()
		m30.save()
		print "30 Merchandise created"

		# ManyToManyField data must be assigned after save:
		m1.tags = (t1,)
		m2.tags = (t1,)
		m3.tags = (t1,)
		m4.tags = (t2,)
		m5.tags = (t2,)
		print "5 Merchandise tag associations has been made"
		print "Move along now.."

