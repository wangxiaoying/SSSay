from django.http import HttpResponse
from enum import Enum

import simplejson

class MESSAGE(Enum):
	Success = 'Success'
	Fail = 'Fail'
	WrongPassword = 'Wrong Password'
	WrongUsername = 'Wrong Username'
	UserExist = 'User Already Exist'
	NoUser = 'None Existing User'
	NoUserHero = 'None Existing User Hero'
	InvalidToken = 'Invalid Token'
	RelationExist = 'Relation Already Exist'
	NoRelationExist = 'Relation Not Exist'
	InsertDBFail = 'Fail To Insert Into Database'
	NoDoing = 'None Existing Doing'
	NoLifeLog = 'None Existing LifeLog'
	Following = 'Following'
	Followed = 'Followed'
	Friends = 'Friends'
	NoRelation = 'No Relation'
	SamePerson = 'Same Person'
	
def getDateFormat():
	return '%Y-%m-%d %H:%M:%S'

def getShortDateFormat():
	return '%m-%d %H:%M'

def generateHTTPResponse(message, key="result"):
	result = {}
	result[key] = message
	return HttpResponse(simplejson.dumps(result))

def getConfig(key):
	config = {
		'md5_random' : '6xlove7j',
	}
	return config[key]