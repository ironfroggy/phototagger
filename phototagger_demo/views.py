from django.template import RequestContext 
from django.shortcuts import render_to_response

from phototagger_demo.models import AThingWithACroppedPhoto


def demo(request): 

    return render_to_response("demo.html",
        RequestContext(request, {
            'thing': AThingWithACroppedPhoto.objects.get(id=1),
        }))

