from multiprocessing import context
from re import template
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Reedpiece

def index(request):
    reedpieces = Reedpiece.objects.all().values()
    context = {
        'reedpieces': reedpieces
    }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))

def add(request):
    template = loader.get_template("add.html")
    return HttpResponse(template.render({}, request))

def addreed(request):
    la = request.POST['label']
    le = request.POST['length']
    d = request.POST['diam']
    t = request.POST['thickness']
    r = request.POST['roundness']
    pr =  Reedpiece(label=la, length=le, thickness=t, \
        roundness=r, diam=d)
    pr.save()
    return HttpResponseRedirect(reverse('index'))