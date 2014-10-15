from django.test import TestCase, Client
from User.models import *
from utils import *

import hashlib

class UserTest(TestCase):
	c = Client()

	def setUp(self):
		# insert new user
		u = User(name='test', password='test')
		u.save()
		u1 = User(name='test1', password='test')
		u1.save()
		u2 = User(name='test2', password='test')
		u2.save()

		self.user_id = str(u.id)
		self.hero_id = str(u1.id)
		self.test_id = str(u2.id)

		hash_str = str(u.id) + u.password + getConfig('md5_random')
		self.token = str(u.id) + ":" + hashlib.md5(hash_str.encode('utf-8')).hexdigest()
		hash_str = str(u1.id) + u1.password + getConfig('md5_random')
		self.token1 = str(u1.id) + ":" + hashlib.md5(hash_str.encode('utf-8')).hexdigest()

		# insert new token
		t = UserToken(user=u, token=self.token)
		t.save()
		t1 = UserToken(user=u1, token=self.token1)
		t1.save()

		# insert new relation
		r = FollowRelation(fan = u, hero = u1)
		r.save()

	def testRegister(self):
		print("\ntest register user")
		response = self.c.post('/user/register', {'username':'test_user', 'password':'test_password'})
		print(response.content)

	def testLogin(self):
		print("\ntest login user")
		response = self.c.post('/user/login', {'username':'test', 'password':'test'})
		print(response.content)

	def testFollow(self):
		print("\ntest follow user")
		response = self.c.post('/user/follow', {'user_fan_token':self.token, 'user_hero_id':self.hero_id})
		print (response.content)
		self.c.post('/user/unfollow', {'user_fan_token':self.token, 'user_hero_id':self.hero_id})
		response = self.c.post('/user/follow', {'user_fan_token':self.token, 'user_hero_id':self.hero_id})
		print (response.content)

	def testUnfollow(self):
		print ('\ntest unfollow user')
		response = self.c.post('/user/unfollow', {'user_fan_token':self.token, 'user_hero_id':self.hero_id})
		print (response.content)
		response = self.c.post('/user/unfollow', {'user_fan_token':self.token1, 'user_hero_id':self.user_id})
		print (response.content)

	def testGetProfile(self):
		print("\ntest get user profile")
		response = self.c.post('/user/getprofile', {'user_id':self.hero_id, 'user_token':self.token})
		print(response.content)

	def testGetAllFans(self):
		print("\ntest get all fans")
		response = self.c.post('/user/getallfans', {'user_token':self.token, 'user_id':self.hero_id})
		print(response.content)
		response = self.c.post('/user/getallfans', {'user_token':self.token1, 'user_id':self.user_id})
		print(response.content)

	def testGetAllHeros(self):
		print("\ntest get all heros")
		response = self.c.post('/user/getallheros', {'user_token':self.token, 'user_id':self.user_id})
		print(response.content)
		response = self.c.post('/user/getallheros', {'user_token':self.token1, 'user_id':self.hero_id})
		print(response.content)

	def testGetFollowRelation(self):
		print('\ntest get follow relation')
		response = self.c.post('/user/getfollowrelation', {'user_token':self.token, 'user_id':self.user_id})
		print(response.content)
		response = self.c.post('/user/getfollowrelation', {'user_token':self.token, 'user_id':self.hero_id})
		print(response.content)
		response = self.c.post('/user/getfollowrelation', {'user_token':self.token1, 'user_id':self.user_id})
		print(response.content)
		response = self.c.post('/user/getfollowrelation', {'user_token':self.token, 'user_id':self.test_id})
		print(response.content)