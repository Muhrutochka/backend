from django.db import models
from django.contrib.auth.models import User


class Config(models.Model):
	name = models.CharField(max_length=100, default='')
	datastructure = models.CharField(max_length=150, default='')
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='configs', null=True, default=None)
	def __str__(self):
		return self.name


class Project(models.Model):
	name = models.CharField(max_length=100, default='')
	alias = models.CharField(max_length=100, default='')
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects', null=True, default=None)
	config = models.ForeignKey(Config, on_delete=models.CASCADE, null=True, default=None, related_name='projects')
	def __str__(self):
		return self.name

class DataItem(models.Model):
	data = models.CharField(max_length=10000, default='')
	config = models.ForeignKey(Config, on_delete=models.CASCADE, null=True, default=None, related_name='data_item')
	project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, default=None, related_name='data_item')
