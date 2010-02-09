from django.conf.urls.defaults import *

urlpatterns = patterns('phototagger.views',
    url(r'get_image_url/(?P<id>\d+)/', 'get_image_url', name='phototagger-get_image_url'),
    url(r'get_boxes/(?P<id>\d+)/', 'get_boxes', name='phototagger-get_boxes'),
    url(r'add_photo_tag/(?P<id>\d+)/', 'add_photo_tag', name='phototagger-add_box'),
)
