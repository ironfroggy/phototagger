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
        real_w = self.photo.image.width
        real_h = self.photo.image.height
        crop_w = self.width
        crop_h = self.height
        cropfrom_w, cropfrom_h = self.photo.get_display_size()

        # The crop selection was made against the display image, so that on very large images it is still usable
        # The crop selection needs to be scaled to the real image size
        x_scale = real_w / float(cropfrom_w)
        y_scale = real_h / float(cropfrom_h)

        # CSS clip measures are all topleft oriented
        right = (crop_w + self.x) * x_scale
        bottom = (crop_h + self.y) * y_scale
        top = self.y * y_scale
        left = self.x * x_scale

        return mark_safe('''<img src="%(src)s" style="position: absolute; %(hw)s clip:rect(%(top)dpx %(right)dpx %(bottom)dpx %(left)dpx);" class="clipexpand" data-width="%(real_w)d" data-height="%(real_h)d" %(extra)s />''' % {
            'src': self.photo.image.url,
            'top': top,
            'right': right,
            'bottom': bottom,
            'left': left,
            'hw': hw,
            'real_h': real_h,
            'real_w': real_w,
            'extra': extra,
        })


