from django import template


register = template.Library()

@register.inclusion_tag('phototagger/cropped_img.html', takes_context=True)
def cropped_img(context, photobox, height=None, width=None, extra=''):
    top, left = 0, 0
    if height is None and width is None:
        height = photobox.height
        width = photobox.width
    elif height is not None and width is None:
        width = height * (float(photobox.width) / float(photobox.height))
        left = -int(width/2)

    if extra:
        extra = template.Template(extra).render(context)

    img = photobox.render_img(height=height, width=width, extra=extra, offset=(top, left))
    return locals()
