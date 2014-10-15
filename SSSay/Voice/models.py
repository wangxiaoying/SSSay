from django.db import models
from Doing.models import *

class Voice(models.Model):
	while_doing = models.ForeignKey(LifeLog)
	voice_file = models.FileField(upload_to="voice")
	listen_num = models.IntegerField(default=0)
