# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


# Signals:
def create_user_account(signal, instance, **kwargs):
	"""Signal for automatically creating an Account upon user creation/save.

	"""
	from django_kikrit.accounts.models import Account
	account, new = Account.objects.get_or_create(user=instance)
	if new:
		account.name = instance.username
		account.save()


models.signals.post_save.connect(create_user_account, sender=User)


