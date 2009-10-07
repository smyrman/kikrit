from django.db import models

# Create your models here.

class Merchandise(model.Model):
	name = model.CharField()
	ordinary_price = models.IntegerField()
	internal_price = models.IntegerField()
	ean = models.CharField()
