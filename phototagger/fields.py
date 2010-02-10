from django.db import models

from phototagger.models import PhotoBox
from phototagger.widgets import PhotoBoxWidget

class PhotoBoxField(models.ForeignKey):

    def __init__(self, force_width=None, force_height=None, force_aspect=None):
        super(PhotoBoxField, self).__init__('phototagger.PhotoBox')
        self.force_width = force_width
        self.force_height = force_height
        self.force_aspect = force_aspect

    def formfield(self, *args, **kwargs):
        kwargs['widget'] = PhotoBoxWidget(attrs={'force_width': self.force_width, 'force_height': self.force_height, 'force_aspect': self.force_aspect})
        return super(PhotoBoxField, self).formfield(*args, **kwargs)


