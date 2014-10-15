from django.http import HttpResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from utils import *
from User.models import *
from Doing.models import *
from Voice.models import *

import random
import simplejson

class UploadVoiceForm(forms.Form):
	voicefile = forms.FileField()

@csrf_exempt
def uploadVoice(request):
	try :
		token = request.POST.get('user_token')

		# check token first
		result = __check_token(token)
		if result is False:
			return generateHTTPResponse(MESSAGE.InvalidToken.value)

		# get doing
		life_log_id = request.POST.get('lifelog_id')
		life_logs = LifeLog.objects.filter(id=life_log_id)
		if len(life_logs) != 1:
			return generateHTTPResponse(MESSAGE.NoLifeLog.value)

		if request.method == 'POST':
			form = UploadVoiceForm(request.POST, request.FILES)
			if form.is_valid():
				new_voice = Voice(while_doing = life_logs[0], voice_file = request.FILES['voicefile'])
				new_voice.save()
				print (new_voice.id)

				return generateHTTPResponse(MESSAGE.Success.name)
			return generateHTTPResponse(MESSAGE.Fail.name)
	except Exception as e:
		print ('Exception:', e)
		return generateHTTPResponse(MESSAGE.Fail.name) 

@csrf_exempt
def randomDoingVoice(request):
	try:
		token = request.POST.get('user_token')

		# check token first
		result = __check_token(token)
		if result is False:
			return generateHTTPResponse(MESSAGE.InvalidToken.value)

		# get lifelogs
		doing_id = int(request.POST.get('doing_id'))
		doing = Doing.objects.filter(id=doing_id)[0]
		lifelogs = LifeLog.objects.filter(doing=doing)

		result = __random_voice(lifelogs)
		return HttpResponse(simplejson.dumps(result))

	except Exception as e:
		print ('Exception:', e)
		return generateHTTPResponse(MESSAGE.Fail.value)

@csrf_exempt
def randomAllVoice(request):
	try:
		result = __random_voice()

		return HttpResponse(simplejson.dumps(result))

	except Exception as e:
		print ('Exception:', e)
		return generateHTTPResponse(MESSAGE.Fail.value)

############################################################
# private functions
def __check_token(token):
	'''
	return True for matched token
	'''
	try:
		tokens = UserToken.objects.filter(token = token, valid = True)
		if len(tokens) > 0:
			return True
		else:
			print ('Fail: token not valid anymore')
			return False

		print('Fail: id %s user token not match' % id)

		return False
	except Exception as e:
		print('Exception:', e)
		return False

def __random_voice(lifelogs=None):
	all_voices = Voice.objects.all()
	if lifelogs != None:
		all_voices = [ v for v in all_voices if v.while_doing in lifelogs ]
	
	print("haha")	
	the_voice = all_voices[random.randint(0, len(all_voices)-1)]
	print("hehe")
	result = {}
	result['result'] = MESSAGE.Success.value
	result['username'] = the_voice.while_doing.user.name
	result['user_id'] = the_voice.while_doing.user.id
	result['doingname'] = the_voice.while_doing.doing.name
	result['doing_id'] = the_voice.while_doing.doing.id
	result['lifelog_id'] = the_voice.while_doing.id
	result['voice_url'] = the_voice.voice_file.name

	return result





