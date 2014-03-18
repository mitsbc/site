from django.conf.urls import patterns, url

from home import views

urlpatterns = patterns('',
    url(r'^timezone/', views.set_timezone, name='set_timezone'),
    url(r'^about/', views.about, name='about'),
    url(r'^contact/', views.contact, name='contact'),
    url(r'^subscribe/', views.subscribe, name='subscribe'),
    url(r'^events/all/', views.events_all, name='events_all'),
    url(r'^events/json/', views.events_json, name='events_json'),
    url(r'^events/(?P<slug>[-\w]+)/$', views.event, name='event'),
    url(r'^members/(?P<list>[-\w]+)/$', views.members_by_name, name='members_by_name'),
    url(r'^class/(?P<year>\d{4})/$', views.members_by_year, name='members_by_year'),
    url(r'^$', views.index, name='index'),
)