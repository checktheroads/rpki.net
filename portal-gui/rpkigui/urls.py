# $Id$

from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^foo/', include('foo.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^myrpki/', include('rpkigui.myrpki.urls')),

    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        { 'next_page': '/myrpki/' }),

#XXX
(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/home/melkins/src/rpki/portal-gui/media/'})
)
