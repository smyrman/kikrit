# Create your views here.
from django.contrib.auth import logout
from django.shortcuts import HttpResponseRedirect

def logout_view(request):
	"""A customized logout view"""
	logout(request)
	return HttpResponseRedirect("/")
