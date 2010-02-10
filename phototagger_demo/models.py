from django.db import models

from photos.models import Image
from phototagger.fields import PhotoBoxField
from phototagger.widgets import PhotoBoxWidget

class AThingWithACroppedPhoto(models.Model):

    cropped_photo = PhotoBoxField(force_width=200, force_height=150)


from django import forms

class DemoForm(forms.ModelForm):

    cropped_photo = forms.ChoiceField(widget=PhotoBoxWidget())

    class Meta:
        model = AThingWithACroppedPhoto
