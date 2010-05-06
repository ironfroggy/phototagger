from django.db.models import get_model
from django.forms import widgets
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.safestring import mark_safe

import json


class PhotoBoxWidget(widgets.Select):
    class Media:
        js = (
            getattr(settings, 'MEDIA_JQUERY_URL', 'http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js'),
            getattr(settings, 'MEDIA_JQUERY_UI_URL', 'js/jquery-ui.min.js'),
            settings.MEDIA_URL + 'js/jquery.Jcrop.min.js',
            settings.MEDIA_URL + 'js/jquery.phototagging.js',
        )

        css = {'all': (
            getattr(settings, 'MEDIA_PHOTOTAGGER_CSS_URL', 'css/phototagger.css'),
            getattr(settings, 'MEDIA_PHOTOTAGGER_CSS_URL', 'css/jquery.Jcrop.css'),
        )}

    def render(self, name, value, attrs=None):
        box_field = widgets.HiddenInput().render(name, value)

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
        photo_choices = [(str(p.id), p.title) for p in get_model('photos', 'Image').objects.all()]
        photo_choices.insert(0, ('', '(None)'))
        img_select = widgets.Select().render(name + '__img_select', photo_value, attrs, choices=photo_choices)
        return  mark_safe(u'''
        <span class="photoboxfield">
            %(box_field)s
            %(img_select)s
            <input type="button" name="pb_toggle" value="+"></input>
            <img class="phototagger_image" src="" />
            <script type="text/javascript">
                $(document).ready(function(){
                    $('#id_%(selectid)s').photoSelectAndTag({
                        ajaxGetImageURL: "%(get_image_url)s",
                        ajaxAddPhotoBoxURL: "%(add_photo_box_url)s",
                        box: %(box)s,
                        force_aspect: %(force_aspect)s,
                        read_aspect_h: %(read_aspect_h)s,
                        read_aspect_w: %(read_aspect_w)s
                    });
                });
            </script>
        </span>''' % {
                'selectid': name,
                'get_image_url': reverse('phototagger-get_image_url', args=(12345,)).replace('12345/', '${photo_id}'),
                'add_photo_box_url': reverse('phototagger-add_box', args=(12345,)).replace('12345', '${photo_id}'),
                'media': mark_safe(unicode(self.media)),
                'box_field': box_field,
                'img_select': img_select,
                'box': json.dumps(box_data),
                'force_aspect': (float(self.attrs['force_aspect'][1]) / float(self.attrs['force_aspect'][0])) if self.attrs['force_aspect'] else 'null',
                'read_aspect_h': json.dumps(self.attrs['read_aspect_h']),
                'read_aspect_w': json.dumps(self.attrs['read_aspect_w']),
            })
