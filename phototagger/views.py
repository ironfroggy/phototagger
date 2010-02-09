from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from photos.models import Image

def get_boxes(request, id):
    """
    Responds with JSON data detailing the current photo tags.
    """
    photo = get_object_or_404(Image, id=id)
    # @@@: test
    if not photo.is_public and request.user != photo.member:
        raise Http404

    photo_tags = []
    for photo_tag in photo.photo_tags.all():
        photo_tags.append({
            'x1': photo_tag.x,
            'y1': photo_tag.y,
            'width': photo_tag.width,
            'height': photo_tag.height,
        })

    return HttpResponse(simplejson.dumps(photo_tags), mimetype="application/json")

def add_photo_tag(request, id):
    form = PhotoBoxForm(request.user, id, request.POST)
    if form.is_valid():
        form.save()
        return HttpResponse('OK', mimetype='text/plain')

def get_image_url(request, id):
    return HttpResponse(Image.objects.get(id=int(id)).get_display_url())
