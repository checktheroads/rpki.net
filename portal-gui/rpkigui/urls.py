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

    #(r'^dashboard/', include('myrpki.dashboardurls')),
    (r'^myrpki/', include('rpkigui.myrpki.urls')),

    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),

#XXX
(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        #{'document_root': '/Users/fenner/src/portal-gui/media/'}),
        {'document_root': '/home/me/src/rpki/portal-gui/media/'}),

)
