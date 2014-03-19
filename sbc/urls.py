from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from sitemaps import *
sitemaps = {
	'event': CalendarItemSitemap,
	'static': StaticViewSitemap,
	'members_by_name': MemberListSitemap,
	'members_by_year': MemberSitemap
}

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sbc.views.home', name='home'),
    # url(r'^sbc/', include('sbc.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('home.urls')),
    url(r'^', include('ine.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'home.views.not_found_view'