from django.conf.urls import patterns, url

from home import views

urlpatterns = patterns('',
    url(r'about', views.about, name='about'),
    url(r'^members/(?P<list>\w+)/$', views.members, name='members'),
    url(r'^$', views.index, name='index'),
)