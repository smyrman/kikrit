# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

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
		account.email = instance.email
		account.save()


models.signals.post_save.connect(create_user_account, sender=User)


