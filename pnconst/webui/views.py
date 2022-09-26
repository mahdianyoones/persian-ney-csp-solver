from multiprocessing import context
from re import template
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Reedpiece

def index(request):
    reedpieces = Reedpiece.objects.all().values()
    context = {
        'reedpieces': reedpieces
    }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))