from django.db import models

from phototagger.models import PhotoBox
from phototagger.widgets import PhotoBoxWidget

class PhotoBoxField(models.ForeignKey):

    def __init__(self):
        super(PhotoBoxField, self).__init__('phototagger.PhotoBox')

    def formfield(self, *args, **kwargs):
        kwargs['widget'] = PhotoBoxWidget
        return super(PhotoBoxField, self).formfield(*args, **kwargs)


