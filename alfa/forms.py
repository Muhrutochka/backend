from django import forms
from alfa.models import *
from django_select2.forms import Select2MultipleWidget


class ProjectForm(forms.Form):
	name = forms.CharField(required=True)
	alias = forms.CharField(required=True)

class ConfigForm(forms.Form):
    name = forms.CharField(required=True)
    datastructure = forms.CharField(required=True)
    projects = forms.ModelMultipleChoiceField(queryset=Project.objects.all(), widget=Select2MultipleWidget)



