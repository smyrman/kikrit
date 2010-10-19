# -*- coding: utf-8 -*-
# Create your views here.
import barcode
#from elaphe import barcode

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, Http404

from merchandise.models import Merchandise

def merchandises_as_pdf(request, quryset):
	pass
	# FIXME.

def merchandise_ean(request, merchandise_id):
	try:
		merchandise = Merchandise.objects.get(id=int(merchandise_id),
				ean__isnull=False)
	except merchandise.DoesNotExist:
		raise Http404

	response = HttpResponse(mimetype='application/svg')
	response['Content-Disposition'] = \
			'attachment; filename=merchandise_%d.svg' %merchandise.id

	Ean13_class = barcode.get_barcode_class('ean13')
	ean = Ean13_class(merchandise.ean)
	ean.write(response)
	#pil_img = barcode('ean13', merchandise.ean, {'includetext':True, "width":150,
	#	"height":80})
	#pil_img.show()
	#pil_img.save(response, "png")
	return response


