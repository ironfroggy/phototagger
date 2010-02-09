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
            getattr(settings, 'MEDIA_JQUERY_UI_URL', 'js/jquery.imgareaselect-0.4.js'),
            getattr(settings, 'MEDIA_JQUERY_UI_URL', 'js/jquery.imgnotes-0.2.js'),
            settings.MEDIA_URL + 'js/jquery.phototagging.js',
        )

    def render(self, name, value, attrs=None):
        photos = get_model('photos', 'Image').objects.all()
        choices = [(p.id, p.title) for p in photos]
        base_render = super(PhotoBoxWidget, self).render(name, value, attrs, choices=choices)
        return mark_safe(unicode(self.media)) + base_render + mark_safe(u'''
            <img class="phototagger_image" src="" />
            <script type="text/javascript">
                $(document).ready(function(){
                    $('#id_%(selectid)s').photoSelectAndTag({ajaxGetImageURL: "%(get_image_url)s"});
                });
            </script>''' % {
                'selectid': name,
                'get_image_url': reverse('phototagger-get_image_url', args=(12345,)).replace('12345/', '')
            })
