# -*- coding: utf-8 -*-
from django.contrib import admin

from django_kikrit.merchandise.models import Merchandise, MerchandiseTag


class MerchandiseAdmin(admin.ModelAdmin):
	#select_related = True
	list_display = ('name', 'ordinary_price', 'internal_price', 'ean', 'get_tags')
	search_fields = ('name', 'ordinary_price', 'internal_price', 'ean')
	list_filter = ('tags',)
	oredring = ('name',)

	def get_tags(self, obj):
		return u",".join((tag.__unicode__() for tag in obj.tags.all()))
	get_tags.short_description = 'tags'




admin.site.register(Merchandise, MerchandiseAdmin)
admin.site.register(MerchandiseTag)
