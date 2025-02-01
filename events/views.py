from django.shortcuts import render
from django.http import HttpResponse
from events.models import *
from events.forms import *

def home(request):
    return render(request, "home.html")

def organizerDashboard(request):
    return render(request, "organizerDashboard.html")

def event_form(request):
    event_form = EventModelForm()

    context = {
        "event_form" : event_form
    }
    return render(request, "event_form.html", context)
