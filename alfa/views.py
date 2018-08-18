from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from alfa.models import *
from alfa.forms import *
import re
import json
from django.views.decorators.csrf import csrf_exempt


def has_premission():
	def has(f):
		def func(request, *args, **kwargs):
			if request.user.is_authenticated:
				return f(request, *args, **kwargs)
			else:
				return HttpResponseRedirect('/accounts/login/')

		return func

	return has

@csrf_exempt
def rest(request, project, config):
	if 'HTTP_NAME' in request.META:
		username = request.META['HTTP_NAME']
	else:
		return HttpResponse(json.dumps({'success': 'false', 'error_message': 'Request does not have NAME header.'}), content_type='application/json')
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		return HttpResponse(json.dumps({'success': 'false', 'error_message': 'Bad NAME header.'}), content_type='application/json')
	try:
		project = Project.objects.get(alias=project, user=user)
	except Project.DoesNotExist:
		return HttpResponse(json.dumps({'success': 'false', 'error_message': 'Bad project name.'}), content_type='application/json')
	try:
		config = Config.objects.get(name=config, user=user)
	except Config.DoesNotExist:
		return HttpResponse(json.dumps({'success': 'false', 'error_message': 'Bad config name.'}), content_type='application/json')
	if project.config != config:
		return HttpResponse(json.dumps({'success': 'false', 'error_message': 'This project has another config'}), content_type='application/json')
	if request.method == 'POST':
		data = DataItem()
		for item in re.split(";", config.datastructure):
			if not item in json.loads(request.body):
				HttpResponse(json.dumps({'success': 'false', 'error_message': 'Request has not ' + item + ' field.'}), content_type='application/json')
		data.data = json.dumps(json.loads(request.body))
		data.project = project
		data.config = config
		data.save()
		return HttpResponse(json.dumps({'success': 'true'}), content_type='application/json')
	elif request.method == 'GET':
		all_data = DataItem.objects.filter(project=project, config=config).all()
		if all_data.count() == 0:
			return HttpResponse(json.dumps({'success': 'true', 'number_of_items': '0', 'items': []}), content_type='application/json')
		else:
			all_items = []
			for item in DataItem.objects.filter(project=project, config=config):
				all_items.append(json.loads(item.data))
			return HttpResponse(json.dumps({'success': 'true', 'number_of_items': str(len(all_items)), 'items': all_items}), content_type='application/json')
	elif request.method == 'DELETE':
		try:
			print(request.body)
			object = DataItem.objects.get(data=json.dumps(json.loads(request.body)), project=project, config=config)
		except DataItem.DoesNotExist:
			return HttpResponse(json.dumps({'success': 'false', 'error_message': 'Object does not exist.'}), content_type='application/json')
		print(object)
		object.delete()
		return HttpResponse(json.dumps({'success': 'true'}), content_type='application/json')
	elif request.method == 'PUT':
		request_data = json.loads(request.body)
		if 'old' in request_data and 'new' in request_data:
			try:
				object = DataItem.objects.get(data=json.dumps(request_data['old']))
			except DataItem.DoesNotExist:
				return HttpResponse(json.dumps({'success': 'false', 'error_message': 'Object does not exist.'}), content_type='application/json')
			for item in re.split(";", config.datastructure):
				if not item in request_data['new']:
					HttpResponse(json.dumps({'success': 'false', 'error_message': 'New object has not ' + item + ' field.'}), content_type='application/json')
			object.data = json.dumps(request_data['new'])
			object.save()
			return HttpResponse(json.dumps({'success': 'true'}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({'success': 'false', 'error_message': 'Bad request method.'}), content_type='application/json')

@has_premission()
def dashboard_page(request):
	context = {}
	a = Project(name='alfa ' + str(Project.objects.count() + 1), user=request.user)
	# a.save()
	context['projects'] = Project.objects.filter(user=request.user)
	return render(request, 'dashboard_page.html', context)


@has_premission()
def new_project_page(request):
	context = {}
	context['header'] = 'New project'
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		if form.is_valid():
			project = Project()
			project.user = request.user
			project.name = form.cleaned_data['name']
			project.alias = form.cleaned_data['alias']
			project.alias = re.sub('[^a-zA-Z0-9]', '', project.alias)
			if project.alias == form.cleaned_data['alias']:
				project.save()
				return HttpResponseRedirect(reverse('dashboard_url'))
			else:
				context['name'] = form.cleaned_data['name']
				context['alias'] = form.cleaned_data['alias']
				context['error'] = True
				context['error_message'] = 'Bad alias (only digits and characters available).'
				return render(request, 'new_project_page.html', context)
		else:
			context['error'] = True
			context['error_message'] = 'Bad form.'
			return render(request, 'new_project_page.html', context)
	else:
		context['form'] = ProjectForm()
		return render(request, 'new_project_page.html', context)


@has_premission()
def delete_project_page(request, id):
	try:
		project = Project.objects.get(id=id)
	except Project.DoesNotExist:
		return HttpResponseRedirect(reverse('dashboard_url'))
	if project.user == request.user:
		project.delete()
	return HttpResponseRedirect(reverse('dashboard_url'))


@has_premission()
def edit_project_page(request, id):
	context = {}
	context['header'] = 'Edit project'
	try:
		project = Project.objects.get(id=id, user=request.user)
	except Project.DoesNotExist:
		return HttpResponseRedirect(reverse('dashboard_url'))
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		if form.is_valid():
			project.name = form.cleaned_data['name']
			project.alias = form.cleaned_data['alias']
			project.alias = re.sub('[^a-zA-Z0-9]', '', project.alias)
			if project.alias == form.cleaned_data['alias']:
				project.save()
				return HttpResponseRedirect(reverse('dashboard_url'))
			else:
				context['name'] = form.cleaned_data['name']
				context['alias'] = form.cleaned_data['alias']
				context['error'] = True
				context['error_message'] = 'Bad alias (only digits and characters available).'
				return render(request, 'new_project_page.html', context)
		else:
			context['error'] = True
			context['error_message'] = 'Bad form.'
			return render(request, 'new_project_page.html', context)
	else:
		context['form'] = ProjectForm()
		context['name'] = project.name
		context['alias'] = project.alias
		return render(request, 'new_project_page.html', context)
	return render(request, 'new_project_page.html', context)


@has_premission()
def config_page(request):
	context = {}
	context['configs'] = Config.objects.filter(user=request.user)
	print(context['configs'])
	return render(request, 'config_page.html', context)


@has_premission()
def new_config_page(request):
	context = {}
	context['header'] = 'New configuration'
	if request.method == 'POST':
		form = ConfigForm(request.POST)
		if form.is_valid():
			config = Config()
			config.user = request.user
			config.name = form.cleaned_data['name']
			config.name = re.sub('[^a-zA-Z0-9]', '', config.name)
			if config.name != form.cleaned_data['name']:
				context['name'] = form.cleaned_data['name']
				context['datastructure'] = form.cleaned_data['datastructure']
				context['error'] = True
				context['form'] = ConfigForm()
				context['error_message'] = 'Bad name (only digits and characters available).'
				return render(request, 'new_config_page.html', context)
			config.datastructure = form.cleaned_data['datastructure']
			config.datastructure = re.sub('[^a-zA-Z;]', '', config.datastructure)
			if config.datastructure == form.cleaned_data['datastructure']:
				config.save()
				for project in form.cleaned_data['projects']:
					project.config = config
					project.save()
				return HttpResponseRedirect(reverse('config_url'))
			else:
				context['name'] = form.cleaned_data['name']
				context['datastructure'] = form.cleaned_data['datastructure']
				context['error'] = True
				context['error_message'] = 'Bad datastructure (only characters available).'
				return render(request, 'new_config_page.html', context)
		else:
			context['error'] = True
			context['error_message'] = 'Bad form.'
			return render(request, 'new_config_page.html', context)
	else:
		context['form'] = ConfigForm()
		return render(request, 'new_config_page.html', context)


@has_premission()
def delete_config_page(request, id):
	try:
		config = Config.objects.get(id=id)
	except Config.DoesNotExist:
		return HttpResponseRedirect(reverse('config_url'))
	if config.user == request.user:
		config.delete()
	return HttpResponseRedirect(reverse('config_url'))


@has_premission()
def edit_config_page(request, id):
	context = {}
	context['header'] = 'Edit config'
	try:
		config = Config.objects.get(id=id, user=request.user)
	except Config.DoesNotExist:
		return HttpResponseRedirect(reverse('config_url'))
	if request.method == 'POST':
		form = ConfigForm(request.POST)
		if form.is_valid():
			config.name = form.cleaned_data['name']
			config.datastructure = form.cleaned_data['datastructure']
			config.datastructure = re.sub('[^a-zA-Z;]', '', config.datastructure)
			if config.datastructure == form.cleaned_data['datastructure']:
				config.save()
				for project in form.cleaned_data['projects']:
					project.config = config
					project.save()
				return HttpResponseRedirect(reverse('config_url'))
			else:
				context['name'] = form.cleaned_data['name']
				context['datastructure'] = form.cleaned_data['datastructure']
				context['error'] = True
				context['error_message'] = 'Bad datastructure (only digits and characters available).'
				return render(request, 'new_config_page.html', context)
		else:
			context['error'] = True
			context['error_message'] = 'Bad form.'
			return render(request, 'new_config_page.html', context)
	else:
		context['form'] = ConfigForm()
		context['name'] = config.name
		context['datastructure'] = config.datastructure
		return render(request, 'new_config_page.html', context)
	return render(request, 'new_config_page.html', context)
