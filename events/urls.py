from django.urls import path
from events.views import *

urlpatterns = [
    path('home/', home, name="home-page"),
    path('organizer-dashboard/', organizerDashboard, name="organizer-dashboard"),
    path('participant-dashboard/', participant_dashboard, name="participant-dashboard"),
    path('event-form/', event_form, name="event-form"),
    path('update-event/<int:id>/', update_event, name="update-event"),
    path('delete-event/<int:id>/', delete_event, name="delete-event"),
    path('rsvp/<int:event_id>/', rsvp_event, name='rsvp-event'),
    path('event/<int:event_id>/details/', event_details, name="event-details"),
    path('create-category/', create_category, name='create-category'),
]