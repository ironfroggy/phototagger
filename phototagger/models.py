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
        w, h = self.photo.get_display_size()
        return self.render_img()

    def render_img(self, w=None, h=None):
        if h is None and w is None:
            hw = ''
        else:
            hw = "height: %(height)spx; width: %(width)spx;" % {
                'height': self.height,
                'width': self.width,
            }
        return mark_safe('''<img src="%(src)s" style="position: absolute; %(hw)s clip:rect(%(top)dpx, %(right)dpx, %(bottom)dpx, %(left)dpx);" class="clipexpand"/>''' % {
            'src': self.photo.get_display_url(),
            'top': self.y,
            'right': self.width + self.x,
            'bottom': self.height + self.y,
            'left': self.x,
            'pos_top': -self.y,
            'pos_left': -self.x,
            'hw': hw,
        })


