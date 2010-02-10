from django.db.models import get_model
from django.forms import widgets
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.safestring import mark_safe


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
        choices = ((str(p.id), p.title) for p in get_model('photos', 'Image').objects.all())
        img_select = widgets.Select().render(name + '__img_select', value, attrs, choices=choices)
        return  mark_safe(u'''
        <span class="photoboxfield">
            %(media)s
            %(img_select)s
            <img class="phototagger_image" src="" />
            <script type="text/javascript">
                $(document).ready(function(){
                    $('#id_%(selectid)s').photoSelectAndTag({
                        ajaxGetImageURL: "%(get_image_url)s",
                        ajaxAddPhotoBoxURL: "%(add_photo_box_url)s"
                    });
                });
            </script>
        </span>''' % {
                'selectid': name,
                'get_image_url': reverse('phototagger-get_image_url', args=(12345,)).replace('12345/', ''),
                'add_photo_box_url': reverse('phototagger-add_box', args=(12345,)).replace('12345', '${photo_id}'),
                'media': mark_safe(unicode(self.media)),
                'img_select': img_select,
            })
