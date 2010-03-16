from django import template


register = template.Library()

@register.simple_tag
def cropped_img(photobox, height=None, width=None):
    if height is None and width is None:
        height = photobox.height
        width = photobox.width
    return photobox.render_img(height, width)
