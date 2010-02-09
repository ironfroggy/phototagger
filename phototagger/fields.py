from django.db import models

from phototagger.widgets import PhotoBoxWidget

class PhotoBoxField(models.ForeignKey):

    def formfield(self, *args, **kwargs):
        kwargs['widget'] = PhotoBoxWidget
        super(PhotoBoxField, self).formfield(*args, **kwargs)
