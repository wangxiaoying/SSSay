from django.test import TestCase, Client
from Doing.models import *
from utils import *

import hashlib
from django.utils import timezone

class DoingTest(TestCase):
	c = Client()

	def setUp(self):
		# insert new user
		u = User(name='test', password='test')
		u.save()

		self.user_id = str(u.id)
		hash_str = str(u.id) + u.password + getConfig('md5_random')
		self.token = str(u.id) + ":" + hashlib.md5(hash_str.encode('utf-8')).hexdigest()

		# insert new token
		t = UserToken(user=u, token=self.token)
		t.save()

		#insert new category
		c = DoingCategory(name='relax')
		c.save()
		c1 = DoingCategory(name='work')
		c1.save()

		#insert new doing
		d = Doing(name='run', category=c)
		d.save()
		d1 = Doing(name='listen music', category=c)
		d1.save()
		d2 = Doing(name='meeting', category=c1)
		d2.save()

		self.doing_id = str(d.id)

		#insert new lifelog
		ll = LifeLog(user = u, doing = d)
		ll.save()
		ll1 = LifeLog(user = u, doing = d1, end_time=timezone.now())
		ll1.save()

	def testGetAllDoing(self):
		print('\ntest get all doing')
		response = self.c.post('/doing/getalldoing', {'user_token':self.token})
		print(response.content)

	def testGetDoingInfo(self):
		print('\ntest get doing info')
		response = self.c.post('/doing/getdoinginfo', {'user_token':self.token, 'doing_id':self.doing_id})
		print(response.content)

	def testStartDoing(self):
		print("\ntest start doing")
		response = self.c.post('/doing/startdoing', {'user_token':self.token, 'doing_id':self.doing_id})
		print(response.content)

	def testStopDoing(self):
		print("\ntest stop doing")
		response = self.c.post('/doing/stopdoing', {'user_token':self.token, 'doing_id':self.doing_id})
		print(response.content)

	def testGetPastWeekRecords(self):
		print("\ntest get past week records")
		response = self.c.post('/doing/getpastweekrecords', {'user_token':self.token})
		print(response.content)

	def testGetDoingHistory(self):
		print('\ntest get doing history')
		response = self.c.post('/doing/getdoinghistory', {'user_token':self.token, 'user_id':self.user_id})
		print(response.content)
