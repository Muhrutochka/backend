from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
	name = models.CharField(max_length=100, default='')
	alias = models.CharField(max_length=100, default='')
	user = models.ForeignKey(User ,on_delete=models.CASCADE, related_name='projects', null=True, default=None)
