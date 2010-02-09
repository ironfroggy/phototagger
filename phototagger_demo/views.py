from django.template import RequestContext 
from django.shortcuts import render_to_response

from phototagger_demo.models import DemoForm


def demo(request):

    form = DemoForm()

    return render_to_response("demo.html",
        RequestContext(request, {
            'form': form,
        }))

