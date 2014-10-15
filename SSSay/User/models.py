from django.db import models
from django.contrib import admin

class User(models.Model):
	name = models.CharField(max_length=200, unique=True)
	password = models.CharField(max_length=50)
	join_date = models.DateTimeField(auto_now_add=True)
	portrait = models.FileField(upload_to="portrait",null=True)

	def __unicode__(self):
		return self.name

class FollowRelation(models.Model):
	hero = models.ForeignKey(User, related_name='user_hero')
	fan = models.ForeignKey(User, related_name='user_fan')
	follow_date = models.DateTimeField(auto_now_add=True)
	valid = models.BooleanField(default=True)

class UserToken(models.Model):
	user = models.ForeignKey(User)
	token = models.CharField(max_length=254)
	valid = models.BooleanField(default=True)

class UserAdmin(admin.ModelAdmin):
	list_display = ('name', 'password', 'join_date')

class FollowRelationAdmin(admin.ModelAdmin):
	list_display = ('hero', 'fan', 'follow_date')

admin.site.register(User, UserAdmin)
admin.site.register(FollowRelation, FollowRelationAdmin)