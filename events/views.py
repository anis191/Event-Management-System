from django.shortcuts import render, redirect
from django.http import HttpResponse
from events.models import *
from events.forms import *
from django.contrib import messages
from django.db.models import Q, Avg, Count, Min, Max, Sum
from datetime import date

def home(request):
    return render(request, "home.html")

def organizerDashboard(request):
    type = request.GET.get('type')
    title = request.GET.get('title', "Today's")

    '''1.Total, 2.Upcoming, 3.Past 4.Participants'''
    counts = Event.objects.aggregate(
        total_event = Count('id'),
        upcoming = Count('id', filter=(Q(date__gt=date.today()))),
        past = Count('id', filter=(Q(date__lt=date.today())))
    )
    total_Participants = Participant.objects.aggregate(total = Count('id'))
    all_category = Category.objects.all()

    base_query = Event.objects.prefetch_related('category')
    if request.method == 'POST':
        category_id = request.POST.get('category')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')


    if type == 'all':
        events = base_query.all()
    elif type == 'upcoming':
        events = base_query.filter(date__gt=date.today())
    elif type == 'past':
        events = base_query.filter(date__lt=date.today())
    else:
        events = base_query.filter(date=date.today())

    context = {
        "counts" : counts,
        "total_Participants" : total_Participants,
        "events" : events,
        "title" : title,
        "all_category" : all_category
    }
    return render(request, "organizerDashboard.html", context)

def event_form(request):
    event_form = EventModelForm()

    if request.method == 'POST':
        event_form = EventModelForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Create Successfully!")
            return redirect('event-form')
    context = {
        "event_form" : event_form
    }
    return render(request, "event_form.html", context)
