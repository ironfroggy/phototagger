from django.db import models

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


