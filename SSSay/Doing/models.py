from django.db import models
from User.models import *
from django.contrib import admin

class DoingCategory(models.Model):
	name = models.CharField(max_length=200, unique=True)

	def __unicode__(self):
		return self.name

class Doing(models.Model):
	name = models.CharField(max_length=200, unique=True)
	category = models.ForeignKey(DoingCategory)

	def __unicode__(self):
		return self.name

class LifeLog(models.Model):
	user = models.ForeignKey(User)
	doing = models.ForeignKey(Doing)
	start_time = models.DateTimeField(auto_now_add=True)
	end_time = models.DateTimeField(auto_now_add=True)
	is_finish = models.BooleanField(default=False)


class DoingCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class DoingAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')

class LifeLogAdmin(admin.ModelAdmin):
	list_display = ('user', 'doing', 'start_time', 'end_time')

admin.site.register(DoingCategory, DoingCategoryAdmin)
admin.site.register(Doing, DoingAdmin)
admin.site.register(LifeLog, LifeLogAdmin)
