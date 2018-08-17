from django import forms

class ProjectForm(forms.Form):
	name = forms.CharField(required=True)
	alias = forms.CharField(required=True)

class ConfigForm(forms.Form):
	name = forms.CharField(required=True)
	datastructure = forms.CharField(required=True)

