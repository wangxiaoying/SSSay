from django.shortcuts import render
from utils import *
from User.models import *
from Voice.models import *
from Doing.models import *
from django.http import HttpResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt

import hashlib
import datetime
import time
import simplejson

@csrf_exempt
def register(request):
	try:
		username = request.POST.get('username')
		password = request.POST.get('password')

		users = User.objects.filter(name = username)
		if len(users) > 0:
			return generateHTTPResponse(MESSAGE.UserExist.value)

		new_user = User(name = username, password = password)
		new_user.save()

		if new_user.id is not None:
			return __perform_login(new_user)
		else:
			return generateHTTPResponse(MESSAGE.InsertDBFail.value)
	except Exception as e:
		print('Exception:', e)
		return generateHTTPResponse(MESSAGE.Fail.value)

@csrf_exempt
def login(request):
	try:
		username = request.POST.get('username')
		password = request.POST.get('password')
		# print(username, password)
		
		users = User.objects.filter(name = username)
		if len(users) > 0:
			user = users[0]
			if user.password == password:
				return __perform_login(user)
			else:
				return generateHTTPResponse(MESSAGE.WrongPassword.value)
		else:
			return generateHTTPResponse(MESSAGE.WrongUsername.value)
	except Exception as e:
		print('Exception:', e)
		return generateHTTPResponse(MESSAGE.Fail.value)

@csrf_exempt
def logout(request):
	try:
		user_id = request.POST.get('user_id')
		
		#get user
		user = __get_user(user_id)

		if user is not None:
			tokens = UserToken.objects.filter(user=user, valid=True)
			for t in tokens:
				t.valid = False
			return generateHTTPResponse(MESSAGE.Success.value)
		else:
			return generateHTTPResponse(MESSAGE.NoUser.value)
	except Exception as e:
		print('Exception:', e)
		return generateHTTPResponse(MESSAGE.Fail.value)

@csrf_exempt
def changePassword(request):
	try:
		token = request.POST.get('user_token')
		old_password = request.POST.get('old_password')
		new_password = request.POST.get('new_password')

		#check token
		check_result = __check_token(token)
		if check_result is False:
			return generateHTTPResponse(MESSAGE.InvalidToken.value)

		#get user
		user = __get_user(token.split(':')[0])

		print(user.password, old_password, new_password)

		if user is not None:
			if user.password == old_password:
				user.password = new_password
				user.save()
				return generateHTTPResponse(MESSAGE.Success.value)
			else:
				return generateHTTPResponse(MESSAGE.WrongPassword.value)
			
		return generateHTTPResponse(MESSAGE.NoUser.value)

	except Exception as e:
		print(e)
		return generateHTTPResponse(MESSAGE.Fail.value)

@csrf_exempt
def getProfile(request):
	try:
		user_id = request.POST.get('user_id')
		token = request.POST.get('user_token')

		#check token first
		check_result = __check_token(token)
		if check_result is False:
			return generateHTTPResponse(MESSAGE.InvalidToken.value)

		#get the user
		user = __get_user(user_id)

		#continue only when the user exist
		if user is not None:
			result = []
			profile = {}
			profile['name'] = user.name
			profile['joing_date'] = user.join_date.strftime(getDateFormat())
			fans = FollowRelation.objects.filter(hero=user, valid=True)
			profile['fans_num'] = len(fans)
			heros = FollowRelation.objects.filter(fan=user, valid=True)
			profile['hero_num'] = len(heros)
			# profile['portrait'] = user.portrait.url
			# voices = 
			# profile['voice_num'] = 
			doings = LifeLog.objects.filter(user=user)
			profile['doing_num'] = len(doings)
			result.append(profile)
			return HttpResponse(simplejson.dumps(result))
		return generateHTTPResponse(MESSAGE.NoUser.name)	

	except Exception as e:
		print('Exception:',e)
		return generateHTTPResponse(MESSAGE.Fail.name)

@csrf_exempt
def follow(request):
	try:
		token = request.POST.get('user_fan_token')
		hero_id = request.POST.get('user_hero_id')

		# check token first
		check_result = __check_token(token)
		if check_result is False:
			return generateHTTPResponse(MESSAGE.InvalidToken.name)

		# get the two user
		user_fan = __get_user(token.split(':')[0])
		user_hero = __get_user(hero_id)

		print('hero_id'+ str(hero_id))

		# continue only when they exist
		if user_fan is not None and user_hero is not None:
			relations = FollowRelation.objects.filter(hero = user_hero, fan = user_fan, valid = True)
			if len(relations) > 0:
				relation = relations[0]
				if relation.valid:
					return generateHTTPResponse(MESSAGE.RelationExist.value)

			new_relation = FollowRelation(hero = user_hero, fan = user_fan, valid = True)
			new_relation.save()

			if new_relation.id is not None:
				return generateHTTPResponse(MESSAGE.Success.value)
			else:
				return generateHTTPResponse(MESSAGE.InsertDBFail.value)
		return generateHTTPResponse(MESSAGE.NoUserHero.value)
	except Exception as e:
		print('Exception:', e)
		return generateHTTPResponse(MESSAGE.Fail.value)

@csrf_exempt
def unfollow(request):
	try:
		token = request.POST.get('user_fan_token')
		hero_id = request.POST.get('user_hero_id')

		# check token first
		check_result = __check_token(token)
		if check_result is False:
			print("hahahaha")
			return generateHTTPResponse(MESSAGE.InvalidToken.name)

		# get the two user
		user_fan = __get_user(token.split(':')[0])
		user_hero = __get_user(hero_id)

		# continue only when they exist
		if user_fan is not None and user_hero is not None:
			relations = FollowRelation.objects.filter(hero = user_hero, fan = user_fan, valid = True)
			if len(relations) > 0:
				relation = relations[0]
				if relation.valid:
					relation.valid = False
					relation.save()
					return generateHTTPResponse(MESSAGE.Success.name)

			return generateHTTPResponse(MESSAGE.NoRelationExist.name)

		return generateHTTPResponse(MESSAGE.NoUserHero.name)
	except Exception as e:
		print('Exception:', e)
		return generateHTTPResponse(MESSAGE.Fail.name)

@csrf_exempt
def getAllFans(request):
	try:
		token = request.POST.get('user_token')
		user_id = request.POST.get('user_id')

		#check token first
		check_result = __check_token(token)
		if check_result is False:
			return generateHTTPResponse(MESSAGE.InvalidToken.name)

		#get the user
		user = __get_user(user_id)

		#continue only when user exists
		if user is not None:
			fans = FollowRelation.objects.filter(hero=user, valid=True)
			result = []
			for f in fans:
				tmp = {}
				tmp['id'] = f.fan.id
				tmp['name'] = f.fan.name
				if f.fan.portrait.name != '':
					tmp['portrait'] = f.fan.portrait.url
				else:
					tmp['portrait'] = 'no'
				result.append(tmp)
			return HttpResponse(simplejson.dumps(result))
	except Exception as e:
		print('Exception:', e)
		return generateHTTPResponse(MESSAGE.Fail.name)

@csrf_exempt
def getAllHeros(request):
	try:
		token = request.POST.get('user_token')
		user_id = request.POST.get('user_id')

		#check token first
		check_result = __check_token(token)
		if check_result is False:
			return generateHTTPResponse(MESSAGE.InvalidToken.name)

		#get the user
		user = __get_user(user_id)

		#continue only when user exists
		if user is not None:
			heros = FollowRelation.objects.filter(fan=user, valid=True)
			print(len(heros))
			result = []
			for h in heros:
				tmp = {}
				tmp['id'] = h.hero.id
				tmp['name'] = h.hero.name
				if h.hero.portrait.name != '':
					tmp['portrait'] = h.hero.portrait.url
				else:
					tmp['portrait'] = 'no'
				result.append(tmp)
			return HttpResponse(simplejson.dumps(result))
	except Exception as e:
		print('Exception:', e)
		return generateHTTPResponse(MESSAGE.Fail.name)

class UploadPortraitForm(forms.Form):
	portraitfile = forms.FileField()

@csrf_exempt
def uploadPortrait(request):
	try:
		token = request.POST.get('user_token')

		#check token first
		check_result = __check_token(token)
		if check_result is False:
			return generateHTTPResponse(MESSAGE.InvalidToken.name)

		#get the user and check
		user = __get_user(token.split(':')[0])
		if user is None:
			return generateHTTPResponse(MESSAGE.NoUser.name)

		#upload portrait
		if request.method == 'POST':
			form = UploadPortraitForm(request.POST, request.FILES)
			if form.is_valid():
				user.portrait = request.FILES['portraitfile']
				user.save()
				return generateHTTPResponse(MESSAGE.Success.name)
	except Exception as e:
		print(e)
		return generateHTTPResponse(MESSAGE.Fail.name)

@csrf_exempt
def getPortraitUrl(request):
	try:
		user_id = request.POST.get('user_id')

		#get the user and check
		user = __get_user(user_id)
		if user is None:
			return generateHTTPResponse(MESSAGE.NoUser.value)

		#return portrait url
		url = {}
		if user.portrait.name != '':
			url['portrait_url'] = user.portrait.url
		else:
			url['portrait_url'] = 'no'
		url['result'] = MESSAGE.Success.value
		return HttpResponse(simplejson.dumps(url))

	except Exception as e:
		print(e)
		return generateHTTPResponse(MESSAGE.Fail.value)


@csrf_exempt
def getFollowRelation(request):
	try:
		token = request.POST.get('user_token')
		user_id = request.POST.get('user_id')

		#check if they are same person
		print(user_id + 'hahaha' + token.split(':')[0])
		if user_id == token.split(':')[0]:
			return generateHTTPResponse(MESSAGE.SamePerson.value)

		#check token first
		check_result = __check_token(token)
		if check_result is False:
			return generateHTTPResponse(MESSAGE.InvalidToken.value)
		#get myself
		me = __get_user(token.split(':')[0])

		#get user
		user = __get_user(user_id)

		#continue only when user exists
		if user is not None:
			relation_1 = FollowRelation.objects.filter(fan = user, hero = me, valid = True)
			relation_2 = FollowRelation.objects.filter(fan = me, hero = user, valid = True)
			len1 = len(relation_1)
			len2 = len(relation_2)
			if len1 > 0 and len2 > 0:
				return generateHTTPResponse(MESSAGE.Friends.value)
			if len1 > 0:
				return generateHTTPResponse(MESSAGE.Followed.value)
			if len2 > 0:
				return generateHTTPResponse(MESSAGE.Following.value)
			return generateHTTPResponse(MESSAGE.NoRelation.value)
		else:
			return generateHTTPResponse(MESSAGE.NoUser.value)

	except Exception as e:
		print(e)
		return generateHTTPResponse(MESSAGE.Fail.value)

######################################################
## private functions start here

def __get_user(user_id):
	'''
	return the matching User object, or return None
	'''
	users = User.objects.filter(id = user_id)
	if len(users) > 0:
		return users[0]
	return None

def __insert_token(user, token):
	'''
	return True if store successfully
	'''
	try :
		# if there is a token existing
		# mark it as invalid
		tokens = UserToken.objects.filter(user = user)
		if len(tokens) > 0:
			for t in tokens:
				if t.valid:
					t.valid = False
					t.save()

		# insert the new user token
		new_token = UserToken(user = user, token = token)
		new_token.save()
		if new_token.id is not None:
			return True
		print ('Error: token insert fail!')
		return False
	except Exception as e:
		print ('Exception', e)
		return False

def __make_token(user_id, password):
	'''
	generate token for user with `id
	'''
	hash_str = str(user_id) + password + getConfig('md5_random')
	return str(user_id) + ":" + hashlib.md5(hash_str.encode('utf-8')).hexdigest()

def __check_token(token):
	'''
	return True for matched token
	'''
	try:
		print('__checktoken', token)
		tokens = UserToken.objects.filter(token = token, valid = True)
		if len(tokens) > 0:
			return True
		else:
			print ('Fail: token not valid anymore')
			return False

		print('Fail: id user token not match')

		return False
	except Exception as e:
		print('Exception:', e)
		return False

def __perform_login(user):
	'''
	generate and store token
	'''
	token = __make_token(user.id, user.password)
	save_result = __insert_token(user, token)

	result = {}
	result['token'] = token
	result['name'] = user.name
	result_data = {}
	result_data['result'] = result
	if save_result:
		return HttpResponse(simplejson.dumps(result_data))
	else:
		print ('Error: save token fail!')
		return generateHTTPResponse(MESSAGE.Fail.name)
