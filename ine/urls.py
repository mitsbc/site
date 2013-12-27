from django.conf.urls import patterns, url

from ine import views

urlpatterns = patterns('',
	url(r'^ine_admin/', views.ine_admin, name='ine_admin'),
    url(r'^ine/', views.ine, name='ine'),
    url(r'^book/(?P<_type>\d+)/(?P<year>\d+)/$', views.book, name='book'),
)