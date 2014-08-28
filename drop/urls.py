from django.conf.urls import patterns, url

from drop import views

urlpatterns = patterns('',
	url(r'^drop/(?P<name>[-\w]+)/resumes/all/', views.drop_resumes, name='drop_resumes'),
	url(r'^drop/(?P<name>[-\w]+)/resumes/(?P<year>\d{4})/', views.drop_resumes_by_year, name='drop_resumes_by_year'),
	url(r'^drop/(?P<name>[-\w]+)/resumes/(?P<industry>\d{1})/', views.drop_resumes_by_industry, name='drop_resumes_by_industry'),
	url(r'^drop/(?P<name>[-\w]+)/admin/', views.drop_admin, name='drop_admin'),
  url(r'^drop/(?P<name>[-\w]+)/book/(?P<industry>\d{1})/(?P<year>\d{4})/$', views.book, name='book'),
  url(r'^drop/(?P<name>[-\w]+)/resume/(?P<year>\d{4})/(?P<unique_hash>\w+)/$', views.resume, name='resume'),
  url(r'^drop/(?P<name>[-\w]+)/', views.drop_drop, name='drop_drop'),
)
