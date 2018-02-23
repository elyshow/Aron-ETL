from django.shortcuts import render

# Create your views here.
import time
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import urllib.request
import urllib.parse


def sendBeginClean(**options):

	workid = options['workid']
	url ='http://' + options['host'] + reverse('dataCleaning:start')
	response = urllib.request.urlopen(url, urllib.parse.urlencode({'id': workid}).encode('utf-8'))
	print(response.status, response.read())

	#except Exception:
	#	print('send start request Error!')
	#	return False
