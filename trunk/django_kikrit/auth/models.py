from django.db import models
from django.contrib.auth.models import User


class LimitGroup(models.Model):
	"""A user might be a member of ONE LimitGroup. This determin how negative
	saldo he can have without going black.

	"""
	name = models.CharField(max_length=50)
	black_limit = models.IntegerField(default=0,
			help_text="Minimum saldo where transactions are still allowed.")
	grey_limit = 0 # Hard coded limit (for now).
	# XXX: There exist a django snippets for a timedelta fild, but I think this
	# is easier:
	max_gray_hours = models.SmallIntegerField(default=24,
			help_text="The maximum number of hours a person migth have a "
			"'grey' (negative) saldo before he goes black. (-1 implies no "
			"limit)")


class KikritUser(User):
	"""Extend django user with additional information, such as saldo and
	limit_group.

	"""
	saldo = models.IntegerField(default=0)
	limit_group = models.ForeignKey(LimitGroup, null=True, blank=True)


class RFIDCard(models.Model):
	user = models.ForeignKey(KikritUser)
	code = models.CharField(mac_length=100)

