from django import template


register = template.Library()

@register.inclusion_tag('phototagger/cropped_img.html', takes_context=True)
def cropped_img(context, photobox, height=None, width=None, extra=''):
    if height is None and width is None:
        height = photobox.height
        width = photobox.width

    if extra:
        extra = template.Template(extra).render(context)

    img = photobox.render_img(height=height, width=width, extra=extra)
    return locals()
