from django.conf.urls import patterns, url

from home import views

urlpatterns = patterns('',
    url(r'^about/', views.about, name='about'),
    url(r'^members/(?P<list>\w+)/$', views.members_by_name, name='members_by_name'),
    url(r'^class/(?P<year>\d+)/$', views.members_by_year, name='members_by_year'),
    url(r'^$', views.index, name='index'),
)