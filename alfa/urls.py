from django.conf.urls import url
from alfa import views

urlpatterns = [
	url(r'^dashboard$', views.dashboard_page, name='dashboard_url'),
	url(r'^config$', views.config_page, name='config_url'),
	url(r'^projects/new$', views.new_project_page, name='new_project_url'),
	url(r'^projects/delete/(?P<id>\d+)$', views.delete_project_page, name='delete_project_url'),
	url(r'^projects/edit/(?P<id>\d+)$', views.edit_project_page, name='edit_project_url'),
	url(r'^config/new$', views.new_config_page, name='new_config_url'),
	url(r'^config/delete/(?P<id>\d+)$', views.delete_config_page, name='delete_config_url'),
	url(r'^config/edit/(?P<id>\d+)$', views.edit_config_page, name='edit_config_url'),

]
