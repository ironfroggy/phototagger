from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^phototagger_demo/', include('phototagger_demo.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    
    url(r'^$', 'phototagger_demo.views.demo'),
    url(r'^pt/', include('phototagger.urls')),
)

if settings.DEBUG:
    from django.views.static import serve
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', serve, {'show_indexes': True, 'document_root': './media/'})
    )
