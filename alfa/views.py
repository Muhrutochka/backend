from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from alfa.models import *
from alfa.forms import *
import re


def has_premission():
    def has(f):
        def func(request, *args, **kwargs):
            if request.user.is_authenticated:
                return f(request, *args, **kwargs)
            else:
                return HttpResponseRedirect('/accounts/login/')

        return func

    return has


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
            config.datastructure = form.cleaned_data['datastructure']
            config.datastructure = re.sub('[^a-zA-Z;]', '', config.datastructure)
            if config.datastructure == form.cleaned_data['datastructure']:
                config.save()
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
                return HttpResponseRedirect(reverse('config_page.html'))
            else:
                context['name'] = form.cleaned_data['name']
                context['datastructure'] = form.cleaned_data['datastructure']
                context['error'] = True
                context['error_message'] = 'Bad alias (only digits and characters available).'
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
