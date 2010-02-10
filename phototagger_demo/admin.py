from django.contrib import admin

from phototagger_demo.models import AThingWithACroppedPhoto

class TheAdmin(admin.ModelAdmin):
    pass
admin.site.register(AThingWithACroppedPhoto, TheAdmin)
