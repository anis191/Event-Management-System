from django.shortcuts import render, redirect
from django.http import HttpResponse
from events.models import *
from events.forms import *
from django.contrib import messages
from django.db.models import Q, Avg, Count, Min, Max, Sum
from datetime import date
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.models import Group, Permission
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView,UpdateView,DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin,PermissionRequiredMixin,LoginRequiredMixin
from django.contrib.auth import get_user_model
User = get_user_model()


def is_admin_or_organizer(user):
    return (user.groups.filter(name='Organizer').exists() or 
        user.groups.filter(name='Admin').exists())

class AdminOrOrganizerCheckMixin(UserPassesTestMixin):
    login_url = 'no-permission'
    def test_func(self):
        return is_admin_or_organizer(self.request.user)
    # login_url = 'no-permission'

def is_participant(user):
    return user.groups.filter(name='Participant').exists()

def user_role(user):
    if user.is_authenticated:
        if user.groups.filter(name='Admin').exists():
            return 'Admin'
        elif user.groups.filter(name='Organizer').exists():
            return 'Organizer'
        elif user.groups.filter(name='Participant').exists():
            return 'Participant'
    return None

def home(request):
    user_type = user_role(request.user)

    base_query = Event.objects.select_related('category')
    events = base_query.filter(date__gt = date.today())
    context = {
        "events" : events,
        "title" : "Upcoming",
        "user_type" : user_type
    }
    return render(request, "home.html", context)

@login_required
# @user_passes_test(is_admin_or_organizer, login_url='no-permission')
def organizerDashboard(request):
    type = request.GET.get('type')
    title = request.GET.get('title', "Today's")
    result = request.GET.get('search', '').strip()
    user_type = user_role(request.user)

    '''1.Total, 2.Upcoming, 3.Past 4.Participants'''
    counts = Event.objects.aggregate(
        total_event = Count('id'),
        upcoming = Count('id', filter=(Q(date__gt=date.today()))),
        past = Count('id', filter=(Q(date__lt=date.today())))
    )
    total_Participants = User.objects.count()
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
        "all_category" : all_category,
        "user_type" : user_type
    }
    return render(request, "organizerDashboard.html", context)

#Admin and Organizer both are create a events:
# @login_required
'''
@user_passes_test(is_admin_or_organizer, login_url='no-permission')
@permission_required("events.add_event", login_url='no-permission')
def event_form(request):
    event_form = EventModelForm()

    if request.method == 'POST':
        event_form = EventModelForm(request.POST, request.FILES)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Create Successfully!")
            return redirect('event-form')
    context = {
        "event_form" : event_form
    }
    return render(request, "event_form.html", context)
'''
class EventFormView(AdminOrOrganizerCheckMixin, PermissionRequiredMixin, View):
    template_name = "event_form.html"
    success_url = reverse_lazy('event-form')
    permission_required = "events.add_event"
    login_url = 'no-permission'

    def get(self, request, *args, **kwargs):
        form = EventModelForm()
        return render(request, self.template_name, {"event_form": form})
    
    def post(self, request, *args, **kwargs):
        form = EventModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Created Successfully!")
            return redirect('event-form')
        return render(request, self.template_name, {"event_form": form})

'''
@user_passes_test(is_admin_or_organizer, login_url='no-permission')
@permission_required("events.change_event", login_url='no-permission')
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
'''
class UpdateEventView(AdminOrOrganizerCheckMixin, PermissionRequiredMixin, UpdateView):
    model = Event
    form_class = EventModelForm
    template_name = 'event_form.html'
    permission_required = "events.change_event"
    login_url = 'no-permission'
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_form'] = self.get_form()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        event_form = EventModelForm(request.POST, instance=self.object)
        if event_form.is_valid():
            event_form.save()
            messages.success(self.request, "Event Update Successfully!")
            return redirect("update-event", self.object.id)

'''
@login_required
@permission_required("events.delete_event", login_url='no-permission')
def delete_event(request, id):
    if request.method == 'GET':
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request ,"Event Delete Successfully!")
        return redirect('organizer-dashboard')
'''
class DeleteTaskView(AdminOrOrganizerCheckMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'events.delete_event'
    model = Event
    success_url = reverse_lazy('organizer-dashboard')
    pk_url_kwarg = 'id'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, "Event deleted successfully!")
        return redirect(self.success_url)

'''
@login_required
def rsvp_event(request, event_id):
    event = Event.objects.get(id = event_id)
    user_id = request.user.id
    if event.rsvp.filter(id=user_id).exists():
        messages.success(request, "You've already RSVP to this event.")
    else:
        event.rsvp.add(request.user)
        event.save()
        messages.success(request, "RSVP this event successful!")
    return redirect('organizer-dashboard')
'''
rsvp_decorator = [login_required(login_url='sign-in')]
@method_decorator(rsvp_decorator, name="dispatch")
class RSVPEventView(View):
    def get(self, request, event_id, *args, **kwargs):
        event = Event.objects.get(id=event_id)
        user_id = request.user.id
        if event.rsvp.filter(id=user_id).exists():
            messages.success(request, "You've already RSVP to this event.")
        else:
            event.rsvp.add(request.user)
            messages.success(request, "RSVP to this event successful!")
        return redirect('organizer-dashboard')

@login_required
# @user_passes_test(is_participant, login_url='no-permission')
def participant_dashboard(request):
    rsvped_events = request.user.rsvp_events.all()
    user_type = user_role(request.user)
    context = {
        'events': rsvped_events,
        'title': 'Your All RSVPs Events',
        'user_type': user_type
    }
    return render(request, 'participantDashboard.html', context)

'''
@login_required
# @permission_required("events.view_events", login_url='no-permission')
def event_details(request, event_id):
    user_type = user_role(request.user)
    event = Event.objects.get(id = event_id)
    return render(request, 'event_details.html', {"event" : event, "user_type":user_type})
'''
event_detail_decorators = [login_required(login_url='sign-in')]
@method_decorator(event_detail_decorators, name="dispatch")
class EventDetailsView(DetailView):
    model = Event
    template_name = 'event_details.html'
    context_object_name = 'event'
    pk_url_kwarg = 'event_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = user_role(self.request.user)
        return context

@user_passes_test(is_admin_or_organizer, login_url='no-permission')
def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully!")
            return redirect('create-category')
    else:
        form = CategoryForm()
    
    return render(request, 'category_form.html', {'form': form})