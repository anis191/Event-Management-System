from django.urls import path
from events.views import *

urlpatterns = [
    path('home/', home, name="home-page"),
    path('organizer-dashboard/', organizerDashboard, name="organizer-dashboard"),
]