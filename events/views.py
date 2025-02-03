from django.shortcuts import render, redirect
from django.http import HttpResponse
from events.models import *
from events.forms import *
from django.contrib import messages
from django.db.models import Q, Avg, Count, Min, Max, Sum
from datetime import date

def home(request):
    base_query = Event.objects.select_related('category')
    events = base_query.filter(date__gt = date.today())
    context = {
        "events" : events,
        "title" : "Upcoming"
    }
    return render(request, "home.html", context)

def organizerDashboard(request):
    type = request.GET.get('type')
    title = request.GET.get('title', "Today's")
    result = request.GET.get('search', '').strip()

    '''1.Total, 2.Upcoming, 3.Past 4.Participants'''
    counts = Event.objects.aggregate(
        total_event = Count('id'),
        upcoming = Count('id', filter=(Q(date__gt=date.today()))),
        past = Count('id', filter=(Q(date__lt=date.today())))
    )
    total_Participants = Participant.objects.count()
    all_category = Category.objects.all()

    base_query = Event.objects.select_related('category')
    events = base_query.all()

    if type == 'upcoming':
        events = base_query.filter(date__gt=date.today())
    elif type == 'past':
        events = base_query.filter(date__lt=date.today())
    elif type != 'all':
        events = base_query.filter(date=date.today())
    
    if result:
        events = base_query.filter(
            Q(name__icontains=result) | Q(description__icontains=result)
        )
        title = "Found"

    
    if request.method == 'POST':
        category_id = request.POST.get('category')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        if from_date and to_date:
            events = base_query.filter(
                category = category_id,
                date__gt = from_date,
                date__lt = to_date,
        )
        title = "Found"

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

def update_event(request, id):
    event = Event.objects.get(id = id)
    event_form = EventModelForm(instance=event)

    if request.method == 'POST':
        event_form = EventModelForm(request.POST,instance=event)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Update Successfully!")
            return redirect("update-event", id)
    context = {
        "event_form" : event_form
    }
    return render(request, "event_form.html", context)

def delete_event(request, id):
    if request.method == 'GET':
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request ,"Event Delete Successfully!")
        return redirect('organizer-dashboard')
