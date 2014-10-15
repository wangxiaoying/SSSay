from django.shortcuts import render
from utils import *
from Doing.models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import simplejson
import hashlib
from django.utils import timezone
from datetime import timedelta, date

@csrf_exempt
def getAllDoing(request):
	try:
		token = request.POST.get('user_token')

		#check token first
		check_result = __check_token(token)
		if check_result is False:
			return generateHTTPResponse(MESSAGE.InvalidToken.value)

		all_categories = DoingCategory.objects.all()

		result = []
		for temp_category in all_categories:
			cate_map = {}
			cate_doings = []
			all_doing_for_cate = Doing.objects.filter(category=temp_category)
			for d in all_doing_for_cate:
				people_count = LifeLog.objects.filter(doing=d)

				cate_doings.append("%d;%s;%d" % (d.id, d.name, len(people_count)))
			cate_map[temp_category.name] = cate_doings
			result.append(cate_map)
		return HttpResponse(simplejson.dumps(result))
	except Exception as e:
		print('Exception:', e)
		return generateHTTPResponse(MESSAGE.Fail.value)

def getDoingInfo(request):
	try:
		token = request.POST.get('user_token')
		doing_id = request.POST.get('doing_id')

		#check token first
		check_result = __check_token(token)
		if check_result is False:
			return generateHTTPResponse(MESSAGE.InvalidToken.name)

		#get doing
		doing = __get_doing(doing_id)

		#continue only when doing exist
		if doing is not None:
			logs = LifeLog.objects.filter(doing=doing, end_time=None)
			logs = logs.exclude()
			result = []
			info = {}
			info['name'] = doing.name
			info['people_num'] = len(logs)
			# info['voice_num'] = 0
			result.append(info)
			return HttpResponse(simplejson.dumps(result))
		return generateHTTPResponse(MESSAGE.NoDoing.name)
	except Exception as e:
		print('Exception:', e)
		return generateHTTPResponse(MESSAGE.Fail.name)

@csrf_exempt
def startDoing(request):
	try:
		token = request.POST.get('user_token')
		doing_id = request.POST.get('doing_id')

		#check token first
		check_result = __check_token(token)
		if check_result is False:
			return generateHTTPResponse(MESSAGE.InvalidToken.value)

		#get doing
		doing = __get_doing(doing_id)

		#get user
		user = __get_user(token.split(':')[0])

		if doing is None:
			return generateHTTPResponse(MESSAGE.NoDoing.value)
		if user is None:
			return generateHTTPResponse(MESSAGE.NoUser.value)

		#stop the doing first
		logs = LifeLog.objects.filter(user=user, is_finish=False)
		# print("doing right now: ", len(logs))
		if len(logs) > 0:
			for log in logs:
				log.end_time = timezone.now()
				log.is_finish = True
				log.save()

		#start new doing
		new_lifelog = LifeLog(user=user, doing=doing)
		new_lifelog.save()

		response = {}
		response['result'] = MESSAGE.Success.value
		response['lifelog_id'] = new_lifelog.id
		return HttpResponse(simplejson.dumps(response))

	except Exception as e:
		print('Exception:', e)
		return generateHTTPResponse(MESSAGE.Fail.value)

@csrf_exempt
def stopDoing(request):
	try:
		token = request.POST.get('user_token')
		doing_id = request.POST.get('doing_id')

		#check token first
		check_result = __check_token(token)
		if check_result is False:
			return generateHTTPResponse(MESSAGE.InvalidToken.name)

		#get doing
		doing = __get_doing(doing_id)

		#get user
		user = __get_user(token.split(':')[0])

		if doing is None:
			return generateHTTPResponse(MESSAGE.NoDoing.name)
		if user is None:
			return generateHTTPResponse(MESSAGE.NoUser.name)

		#stop the doing
		logs = LifeLog.objects.filter(user=user, doing=doing, is_finish=False)
		# print("doing right now: ", len(logs))
		if len(logs) > 0:
			logs[0].end_time = timezone.now()
			logs[0].save()

		return generateHTTPResponse(MESSAGE.Success.name)
	except Exception as e:
		print('Exception:', e)
		return generateHTTPResponse(MESSAGE.Fail.name)

def getPastWeekRecords(request):
	try:
		token = request.POST.get('user_token')

		#check token first
		check_result = __check_token(token)
		if check_result is False:
			return generateHTTPResponse(MESSAGE.InvalidToken.name)

		#get user
		user = __get_user(token.split(':')[0])
		if user is None:
			return generateHTTPResponse(MESSAGE.NoUser.name)

		#get start date
		start_day = date.today() - timedelta(days=7)

		# get logs of past week
		result = []
		logs = LifeLog.objects.filter(user=user, start_time__gte=start_day).exclude(end_time=None)
		for l in logs:
			log = {}
			log['user'] = l.user.name
			log['doing'] = l.doing.name
			log['start_time'] = l.start_time.strftime(getDateFormat())
			log['end_time'] = l.end_time.strftime(getDateFormat())
			result.append(log)
		return HttpResponse(simplejson.dumps(result))
	except Exception as e:
		print('Exception:', e)
		return generateHTTPResponse(MESSAGE.Fail.name)

@csrf_exempt
def getDoingHistory(request):
	try:
		token = request.POST.get('user_token')
		user_id = request.POST.get('user_id')

		#check token first
		check_result = __check_token(token)
		if check_result is False:
			return generateHTTPResponse(MESSAGE.InvalidToken.name)

		#get user
		user = __get_user(user_id)
		if user is None:
			return generateHTTPResponse(MESSAGE.NoUser.name)

		#get doing history
		result = []
		logs = LifeLog.objects.filter(user=user).exclude(end_time=None)
		for l in logs:
			log = {}
			log['doing'] = l.doing.name
			log['start_time'] = l.start_time.strftime(getShortDateFormat())
			log['end_time'] = l.end_time.strftime(getShortDateFormat())
			log['category'] = l.doing.category.name
			result.append(log)
		return HttpResponse(simplejson.dumps(result))
	except Exception as e:
		print('Exception:', e)
		return generateHTTPResponse(MESSAGE.Fail.name)

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

def __get_doing(doing_id):
	'''
	return the matching Doing object, or return None
	'''
	doings = Doing.objects.filter(id = doing_id)
	if len(doings) > 0:
		return doings[0]
	return None

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
