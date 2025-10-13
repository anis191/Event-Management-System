from django.urls import path
from events.views import *

urlpatterns = [
    path('home/', home, name="home-page"),
    path('program_detail/', program_detail, name="program-detail"),
    path('organizer-dashboard/', organizerDashboard, name="organizer-dashboard"),
    path('participant-dashboard/', participant_dashboard, name="participant-dashboard"),
    path('event-form/', EventFormView.as_view(), name="event-form"),
    path('update-event/<int:id>/', UpdateEventView.as_view(), name="update-event"),
    path('delete-event/<int:id>/', DeleteTaskView.as_view(), name="delete-event"),
    path('rsvp/<int:event_id>/', RSVPEventView.as_view(), name='rsvp-event'),
    path('event/<int:event_id>/details/', EventDetailsView.as_view(), name="event-details"),
    path('create-category/', create_category, name='create-category'),
]