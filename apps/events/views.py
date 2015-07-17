from datetime import datetime
from django.views.generic import ListView, DetailView
from .models import Event


class EventList(ListView):
    model = Event
    queryset = Event.objects.filter(start_time__gte=datetime.now())


class EventDetail(DetailView):
    model = Event
