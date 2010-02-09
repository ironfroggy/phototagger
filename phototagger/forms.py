from django import forms

from phototagger.models import PhotoBox

class PhotoBoxForm(forms.ModelForm):
    class Meta:
        model = PhotoBox

    x = forms.IntegerField(widget=forms.HiddenInput())
    y = forms.IntegerField(widget=forms.HiddenInput())
    height = forms.IntegerField(widget=forms.HiddenInput())
    width = forms.IntegerField(widget=forms.HiddenInput())
    photo = forms.ModelChoiceField(Image, required=False, widget=forms.HiddenInput())

    def __init__(self, id, *args, **kwargs):
        super(PhotoTagForm, self).__init__(*args, **kwargs)
        self.id = id

    def clean_photo(self):
        self.cleaned_data['photo'] = Image.objects.get(id=self.id)
        return self.cleaned_data['photo']


