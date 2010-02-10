from django.db.models import get_model
from django.forms import widgets
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.safestring import mark_safe

import json


class PhotoBoxWidget(widgets.Select):
    class Media:
        js = (
            getattr(settings, 'MEDIA_JQUERY_URL', 'http://ajax.googleapis.com/ajax/libs/jquery/1.2.6/jquery.min.js'),
            getattr(settings, 'MEDIA_JQUERY_UI_URL', 'js/jquery-ui.min.js'),
            getattr(settings, 'MEDIA_IMGAREASELECT_URL', 'js/jquery.imgareaselect-0.4.js'),
            getattr(settings, 'MEDIA_IMGNOTES_URL', 'js/jquery.imgnotes-0.2.js'),
            settings.MEDIA_URL + 'js/jquery.phototagging.js',
        )

        css = {'all': (
            getattr(settings, 'MEDIA_PHOTOTAGGER_CSS_URL', 'css/phototagger.css'),
        )}

    def render(self, name, value, attrs=None):
        box_field = widgets.HiddenInput().render(name, value)
        value = 38
        if value:
            box = get_model('phototagger', 'PhotoBox').objects.get(id=int(value))
            photo_value = box.photo.id
            box_data = {
                'id': box.id,
                'x': box.x,
                'y': box.y,
                'width': box.width,
                'height': box.height,
            }
        else:
            box_data = {}
            photo_value = ''
        photo_choices = ((str(p.id), p.title) for p in get_model('photos', 'Image').objects.all())
        img_select = widgets.Select().render(name + '__img_select', photo_value, attrs, choices=photo_choices)
        return  mark_safe(u'''
        <span class="photoboxfield">
            %(media)s
            %(box_field)s
            %(img_select)s
            <img class="phototagger_image" src="" />
            <script type="text/javascript">
                $(document).ready(function(){
                    $('#id_%(selectid)s').photoSelectAndTag({
                        ajaxGetImageURL: "%(get_image_url)s",
                        ajaxAddPhotoBoxURL: "%(add_photo_box_url)s",
                        box: %(box)s,
                    });
                });
            </script>
        </span>''' % {
                'selectid': name,
                'get_image_url': reverse('phototagger-get_image_url', args=(12345,)).replace('12345/', ''),
                'add_photo_box_url': reverse('phototagger-add_box', args=(12345,)).replace('12345', '${photo_id}'),
                'media': mark_safe(unicode(self.media)),
                'box_field': box_field,
                'img_select': img_select,
                'box': json.dumps(box_data),
            })
