from django.conf.urls import patterns, url

from ine import views

urlpatterns = patterns('',
	url(r'^ine/resumes/all/', views.ine_resumes, name='ine_resumes'),
	url(r'^ine/resumes/(?P<year>\d{4})/', views.ine_resumes_by_year, name='ine_resumes_by_year'),
	url(r'^ine/resumes/(?P<industry>\d{1})/', views.ine_resumes_by_industry, name='ine_resumes_by_industry'),
	url(r'^ine/admin/', views.ine_admin, name='ine_admin'),
    url(r'^ine/drop/', views.ine_drop, name='ine_drop'),
    url(r'^book/(?P<_type>\d{1})/(?P<year>\d{4})/$', views.book, name='book'),
    url(r'^resume/(?P<year>\d{4})/(?P<unique_hash>\w+)/$', views.resume, name='resume'),
)