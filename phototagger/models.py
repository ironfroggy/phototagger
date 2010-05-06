from django.db import models
from django.utils.safestring import mark_safe

from photos.models import Image

class PhotoBox(models.Model):
    """
    Define a box in a photo for use in tagging or cropping or anything else box-in-photo related.
    """

    photo = models.ForeignKey('photos.Image', related_name="photo_tags", blank=False, null=False)
    x = models.IntegerField()
    y = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()


    def __unicode__(self):
        return self.render_img('auto')

    def render_img(self, width=None, height=None, extra=''):
        if height is None and width is None:
            height = self.height
            width = self.width
        if width == 'auto':
            hw = ''
        else:
            hw = "height: %(height)spx; width: %(width)spx;" % {
                'height': height,
                'width': width,
            }
        real_w, real_h = self.photo.get_display_size()
        return mark_safe('''<img src="%(src)s" style="position: absolute; %(hw)s clip:rect(%(top)dpx %(right)dpx %(bottom)dpx %(left)dpx);" class="clipexpand" data-real-width="%(real_w)d" data-real-height="%(real_h)d" %(extra)s />''' % {
            'src': self.photo.get_display_url(),
            'top': self.y,
            'right': self.width + self.x,
            'bottom': self.height + self.y,
            'left': self.x,
            'pos_top': -self.y,
            'pos_left': -self.x,
            'hw': hw,
            'real_w': real_w,
            'real_h': real_h,
            'extra': extra,
        })


